// 抓換頁那一下的主執行緒 trace，找出到底是什麼在卡。
// 用法：node scripts/trace-transition.mjs
import puppeteer from 'file:///D:/Antigravity_proj/important/typlin-arena/node_modules/puppeteer-core/lib/puppeteer/puppeteer-core.js';

const BASE = process.env.BLOG_URL || 'http://localhost:4321';

const browser = await puppeteer.launch({
	executablePath: 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
	headless: true,
	args: ['--no-sandbox', '--disable-dev-shm-usage'],
});
const page = await browser.newPage();
await page.setViewport({ width: 1440, height: 900 });
await page.goto(`${BASE}/`, { waitUntil: 'networkidle2', timeout: 60000 });
await page.waitForFunction(
	() => window.swup && document.documentElement.classList.contains('swup-enabled'),
	{ timeout: 30000 },
);
await new Promise((r) => setTimeout(r, 1500));

const client = await page.createCDPSession();
const chunks = [];
client.on('Tracing.dataCollected', ({ value }) => chunks.push(...value));

await client.send('Tracing.start', {
	categories: 'devtools.timeline,v8,blink.user_timing',
	transferMode: 'ReportEvents',
});
await page.click('main a[href^="/posts/"]');
await new Promise((r) => setTimeout(r, 1500));
await client.send('Tracing.end');
await new Promise((r) => client.once('Tracing.tracingComplete', r));

await browser.close();

// 以第一個 Frame 事件的時間戳當基準，列出耗時最長的幾件事。
const withDur = chunks
	.filter((e) => typeof e.dur === 'number' && e.dur > 1000)
	.sort((a, b) => b.dur - a.dur);

console.log(`事件總數 ${chunks.length}，dur > 1ms 的 ${withDur.length} 筆\n`);
console.log('耗時最長的前 25 筆：');
for (const e of withDur.slice(0, 25)) {
	const detail = e.args?.data
		? Object.entries(e.args.data)
				.filter(([k]) => ['functionName', 'url', 'lineNumber', 'type', 'nodeName', 'frame'].includes(k))
				.map(([k, v]) => `${k}=${String(v).slice(0, 70)}`)
				.join(' ')
		: '';
	console.log(`  ${(e.dur / 1000).toFixed(1).padStart(7)}ms  ${e.name.padEnd(26)} ${detail}`);
}

// 依名稱彙總
const byName = new Map();
for (const e of withDur) byName.set(e.name, (byName.get(e.name) || 0) + e.dur);
console.log('\n依事件名彙總（ms）：');
for (const [n, d] of [...byName].sort((a, b) => b[1] - a[1]).slice(0, 12)) {
	console.log(`  ${(d / 1000).toFixed(1).padStart(8)}ms  ${n}`);
}

// JS 依來源檔彙總，找出是誰在吃主執行緒
const byUrl = new Map();
for (const e of withDur) {
	if (e.name !== 'FunctionCall' && e.name !== 'EvaluateScript') continue;
	const u = e.args?.data?.url || '(inline)';
	const fn = e.args?.data?.functionName || '';
	const key = `${u.split('/').slice(-2).join('/')} :: ${fn}`;
	byUrl.set(key, (byUrl.get(key) || 0) + e.dur);
}
console.log('\nJS 依來源彙總（ms）：');
for (const [k, d] of [...byUrl].sort((a, b) => b[1] - a[1]).slice(0, 15)) {
	console.log(`  ${(d / 1000).toFixed(1).padStart(8)}ms  ${k}`);
}