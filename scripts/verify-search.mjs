// 搜尋列驗收：⌘K 提示存在，按下聚焦輸入框。
// 用法：blog preview 跑在 4322，node scripts/verify-search.mjs（需 arena 的 puppeteer-core）
import puppeteer from 'file:///D:/Antigravity_proj/important/typlin-arena/node_modules/puppeteer-core/lib/puppeteer/puppeteer-core.js';

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
await page.goto('http://localhost:4322/', { waitUntil: 'networkidle2', timeout: 45000 });
await new Promise((r) => setTimeout(r, 2000));
ok('桌面搜尋列含 ⌘K 提示', (await page.$('#search-bar kbd')) !== null);
await page.keyboard.down('Control');
await page.keyboard.press('KeyK');
await page.keyboard.up('Control');
await new Promise((r) => setTimeout(r, 600));
ok(
  'Ctrl+K 聚焦搜尋輸入框',
  await page.evaluate(() => document.activeElement?.closest('#search-bar') !== null)
);
await browser.close();
console.log(failures === 0 ? 'ALL GREEN' : `${failures} FAILURES`);
process.exit(failures === 0 ? 0 : 1);
