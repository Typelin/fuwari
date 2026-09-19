// 檢查執行期設定與關鍵 CSS 是否真的生效。
// 用法：node scripts/check-runtime.mjs [path]
import puppeteer from 'file:///D:/Antigravity_proj/important/typlin-arena/node_modules/puppeteer-core/lib/puppeteer/puppeteer-core.js';

const BASE = process.env.BLOG_URL || 'http://localhost:4321';
const path = process.argv[2] || '/';

const browser = await puppeteer.launch({
	executablePath: 'C:/Program Files/Google/Chrome/Application/chrome.exe',
	headless: true,
	args: ['--no-sandbox', '--disable-dev-shm-usage'],
});
const page = await browser.newPage();
await page.setViewport({ width: 1440, height: 900 });
await page.goto(`${BASE}${path}`, { waitUntil: 'networkidle2', timeout: 60000 });
await page.waitForFunction(() => window.swup, { timeout: 30000 });
await new Promise((r) => setTimeout(r, 1500));

const r = await page.evaluate(() => {
	const rules = [];
	for (const s of document.styleSheets) {
		try {
			for (const x of s.cssRules) rules.push(x.cssText);
		} catch (_) {}
	}
	return {
		native: window.swup.options.native,
		containers: window.swup.options.containers,
		updateHead: window.swup.options.updateHead,
		cache: window.swup.options.cache,
		hasStartViewTransition: typeof document.startViewTransition === 'function',
		vtOldAnimation: getComputedStyle(document.documentElement, '::view-transition-old(root)')
			.animationName,
		vtNewAnimation: getComputedStyle(document.documentElement, '::view-transition-new(root)')
			.animationName,
		motionNavRulePresent: rules.some((t) => t.includes('motion-nav')),
		gridHasLongTransition: rules.some(
			(t) => t.includes('#main-grid') && t.includes('transition'),
		),
		leftPanel: !!document.getElementById('left-panel-wrapper'),
		rightPanel: !!document.getElementById('right-panel-wrapper'),
	};
});
console.log(JSON.stringify(r, null, 2));
await browser.close();