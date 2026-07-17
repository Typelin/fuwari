import { access, readdir, readFile } from "node:fs/promises";
import path from "node:path";
import { parse } from "node-html-parser";

const distDir = path.resolve("dist");
const selectors = [
	["a[href]", "href"],
	["link[href]", "href"],
	["script[src]", "src"],
	["img[src]", "src"],
	["source[src]", "src"],
	["video[src]", "src"],
	["audio[src]", "src"],
];

async function walk(directory) {
	const entries = await readdir(directory, { withFileTypes: true });
	const files = await Promise.all(
		entries.map((entry) => {
			const fullPath = path.join(directory, entry.name);
			return entry.isDirectory() ? walk(fullPath) : fullPath;
		}),
	);
	return files.flat();
}

async function exists(filePath) {
	try {
		await access(filePath);
		return true;
	} catch {
		return false;
	}
}

function localPathFromUrl(rawUrl, htmlFile) {
	if (!rawUrl || rawUrl.startsWith("#") || rawUrl.startsWith("//")) return null;
	if (/^(?:[a-z]+:|data:|blob:)/i.test(rawUrl)) return null;

	const withoutQuery = rawUrl.split(/[?#]/, 1)[0];
	if (!withoutQuery) return null;

	let decoded = withoutQuery;
	try {
		decoded = decodeURIComponent(withoutQuery);
	} catch {
		// Keep malformed but literal URLs visible to the checker.
	}

	const target = decoded.startsWith("/")
		? path.resolve(distDir, `.${decoded}`)
		: path.resolve(path.dirname(htmlFile), decoded);

	return target.startsWith(distDir) ? target : null;
}

async function resolvesToBuiltFile(target) {
	const candidates = [target];
	if (!path.extname(target)) {
		candidates.push(path.join(target, "index.html"), `${target}.html`);
	} else if (target.endsWith(path.sep)) {
		candidates.push(path.join(target, "index.html"));
	}
	return (await Promise.all(candidates.map(exists))).some(Boolean);
}

const htmlFiles = (await walk(distDir)).filter((file) => file.endsWith(".html"));
const broken = [];
let checked = 0;

for (const htmlFile of htmlFiles) {
	const root = parse(await readFile(htmlFile, "utf8"));
	for (const [selector, attribute] of selectors) {
		for (const element of root.querySelectorAll(selector)) {
			const rawUrl = element.getAttribute(attribute);
			const target = localPathFromUrl(rawUrl, htmlFile);
			if (!target) continue;
			checked += 1;
			if (!(await resolvesToBuiltFile(target))) {
				broken.push({
					page: path.relative(distDir, htmlFile),
					url: rawUrl,
				});
			}
		}
	}
}

if (broken.length > 0) {
	console.error(`Found ${broken.length} broken local references:`);
	for (const item of broken) console.error(`- ${item.page}: ${item.url}`);
	process.exitCode = 1;
} else {
	console.log(`Checked ${checked} local references across ${htmlFiles.length} HTML files: all valid.`);
}
