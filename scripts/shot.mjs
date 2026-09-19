// 對指定路徑截圖，用來肉眼驗證版面。
// 用法：node scripts/shot.mjs /schedule/ out.png [width] [height] [waitMs]
import puppeteer from 'file:///D:/Antigravity_proj/important/typlin-arena/node_modules/puppeteer-core/lib/puppeteer/puppeteer-core.js';

const BASE = process.env.BLOG_URL || 'http://localhost:4321';
const [path = '/', out = 'shot.png', w = '1440', h = '1200', wait = '5000'] = process.argv.slice(2);

const browser = await puppeteer.launch({
	executablePath: 'C:/Program Files/Google/Chrome/Application/chrome.exe',
	headless: true,
	args: ['--no-sandbox', '--disable-dev-shm-usage'],
});
const page = await browser.newPage();
await page.setViewport({ width: Number(w), height: Number(h) });
await page.goto(`${BASE}${path}`, { waitUntil: 'networkidle2', timeout: 60000 });
await new Promise((r) => setTimeout(r, Number(wait)));
await page.screenshot({ path: out, fullPage: true });
console.log(`wrote ${out}`);
await browser.close();