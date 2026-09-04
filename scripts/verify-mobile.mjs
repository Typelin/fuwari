// 手機橫滑列驗收：400px 下 chips 可見、四張大卡隱藏；1440 下反之。
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

// mobile 400
await page.setViewport({ width: 400, height: 900 });
await page.goto('http://localhost:4322/', { waitUntil: 'networkidle2', timeout: 45000 });
await new Promise((r) => setTimeout(r, 1500));
ok('手機：橫滑列可見', await page.evaluate(() => {
  const el = document.querySelector('.tchips');
  return el && getComputedStyle(el).display !== 'none' && el.getBoundingClientRect().width > 0;
}));
ok('手機：四張大卡隱藏', await page.evaluate(() => {
  const els = [...document.querySelectorAll('#sidebar .tlink')];
  return els.length === 4 && els.every((el) => getComputedStyle(el).display === 'none' || el.getBoundingClientRect().width === 0);
}));
ok('手機：橫滑四顆都有', (await page.$$('.tchips .tchip')).length === 4);

// desktop 1440
await page.setViewport({ width: 1440, height: 900 });
await page.reload({ waitUntil: 'networkidle2' });
await new Promise((r) => setTimeout(r, 1500));
ok('桌面：橫滑列隱藏', await page.evaluate(() => {
  const el = document.querySelector('.tchips');
  return el && getComputedStyle(el.closest('.lg\\:hidden') || el).display === 'none';
}));
ok('桌面：四張大卡可見', await page.evaluate(() => {
  const els = [...document.querySelectorAll('#sidebar .tlink')];
  return els.length === 4 && els.every((el) => el.getBoundingClientRect().width > 0);
}));

await browser.close();
console.log(failures === 0 ? 'ALL GREEN' : `${failures} FAILURES`);
process.exit(failures === 0 ? 0 : 1);
