// 燈箱行為驗收：文章配圖點擊跳窗（含 AA 大表）。
// 用法：blog preview 跑在 4322，node scripts/verify-fancybox.mjs（需 arena 的 puppeteer-core）
import puppeteer from 'file:///D:/Antigravity_proj/important/typlin-arena/node_modules/puppeteer-core/lib/puppeteer/puppeteer-core.js';

const BASE = 'http://localhost:4322';
let failures = 0;
const ok = (name, cond) => {
  console.log(`${cond ? 'PASS' : 'FAIL'}  ${name}`);
  if (!cond) failures += 1;
};

const browser = await puppeteer.launch({
  executablePath: 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
  args: ['--no-sandbox', '--disable-dev-shm-usage'],
});
const page = await browser.newPage();
await page.setViewport({ width: 1440, height: 900 });
await page.goto(`${BASE}/posts/typelin-arena-2026-09/`, { waitUntil: 'networkidle2', timeout: 45000 });
await new Promise((r) => setTimeout(r, 1500));

// 一般配圖：點擊後不應出現燈箱
await page.evaluate(() => {
  const img = document.querySelector('.custom-md img:not([src*="aa-index"])');
  img?.scrollIntoView({ block: 'center' });
});
await new Promise((r) => setTimeout(r, 600));
await page.evaluate(() => {
  document.querySelector('.custom-md img:not([src*="aa-index"])')?.click();
});
await new Promise((r) => setTimeout(r, 1200));
ok('一般配圖點擊跳出燈箱', !!(await page.$('.fancybox__container')));
await page.keyboard.press('Escape');
await new Promise((r) => setTimeout(r, 800));

// AA 大表：點擊後應出現燈箱
await page.evaluate(() => {
  document.querySelector('.custom-md img[src*="aa-index"]')?.scrollIntoView({ block: 'center' });
});
await new Promise((r) => setTimeout(r, 600));
await page.evaluate(() => {
  document.querySelector('.custom-md img[src*="aa-index"]')?.click();
});
await new Promise((r) => setTimeout(r, 1500));
ok('AA 大表點擊跳出燈箱', !!(await page.$('.fancybox__container')));
await page.keyboard.press('Escape');

await browser.close();
console.log(failures === 0 ? 'ALL GREEN' : `${failures} FAILURES`);
process.exit(failures === 0 ? 0 : 1);
