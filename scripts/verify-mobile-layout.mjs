// 手機／平板版面的回歸檢查。
// 重點是這次改動動到 grid 結構（左欄包進 #left-panel-wrapper），
// 要確認手機上的「先後順序」與斷點沒有被弄壞。
// 用法：node scripts/verify-mobile-layout.mjs
import puppeteer from 'file:///D:/Antigravity_proj/important/typlin-arena/node_modules/puppeteer-core/lib/puppeteer/puppeteer-core.js';

const BASE = process.env.BLOG_URL || 'http://localhost:4321';
const POST = '/posts/typelin-arena-2026-09/';

let failures = 0;
const ok = (name, cond, extra = '') => {
	console.log(`${cond ? 'PASS' : 'FAIL'}  ${name}${cond || !extra ? '' : `  → ${extra}`}`);
	if (!cond) failures += 1;
};

const browser = await puppeteer.launch({
	executablePath: 'C:/Program Files/Google/Chrome/Application/chrome.exe',
	headless: true,
	args: ['--no-sandbox', '--disable-dev-shm-usage'],
});
const page = await browser.newPage();

const vis = (sel) =>
	page.evaluate((s) => {
		const el = document.querySelector(s);
		if (!el) return false;
		const r = el.getBoundingClientRect();
		return getComputedStyle(el).display !== 'none' && r.width > 0 && r.height > 0;
	}, sel);

const topOf = (sel) =>
	page.evaluate((s) => {
		const el = document.querySelector(s);
		return el ? Math.round(el.getBoundingClientRect().top + window.scrollY) : null;
	}, sel);

const overflow = () =>
	page.evaluate(() => ({
		scrollW: document.documentElement.scrollWidth,
		clientW: document.documentElement.clientWidth,
	}));

async function at(width, height, path, label) {
	await page.setViewport({ width, height });
	await page.goto(`${BASE}${path}`, { waitUntil: 'networkidle2', timeout: 60000 });
	await new Promise((r) => setTimeout(r, 2000));
	console.log(`\n── ${label}（${width}×${height}）${path} ──`);
}

// ============ 手機：首頁 ============
await at(390, 844, '/', '手機 首頁');
{
	const o = await overflow();
	ok('沒有橫向溢出', o.scrollW <= o.clientW + 1, `scrollW=${o.scrollW} clientW=${o.clientW}`);
	ok('右側工具欄隱藏', !(await vis('#right-panel-wrapper')));
	ok('側欄（個人卡）可見', await vis('#sidebar'));
	const mainTop = await topOf('main');
	const leftTop = await topOf('#left-panel-wrapper');
	ok('順序：文章列表在側欄之前', mainTop !== null && leftTop !== null && mainTop < leftTop, `main@${mainTop} left@${leftTop}`);
	ok('卡片為滿寬單欄', await page.evaluate(() => {
		const card = document.querySelector('main .post-card');
		const main = document.querySelector('main');
		if (!card || !main) return false;
		return card.getBoundingClientRect().width >= main.getBoundingClientRect().width - 2;
	}));
}

// ============ 手機：文章頁 ============
await at(390, 844, POST, '手機 文章頁');
{
	const o = await overflow();
	ok('沒有橫向溢出', o.scrollW <= o.clientW + 1, `scrollW=${o.scrollW} clientW=${o.clientW}`);
	ok('桌機版文章導覽 aside 隱藏', !(await vis('#article-navigation')));
	ok('手機版可展開目錄可見', await vis('.article-mobile-nav'));
	const navTop = await topOf('.article-mobile-nav');
	const mainTop = await topOf('main');
	ok('順序：目錄在文章內容之前', navTop !== null && mainTop !== null && navTop < mainTop, `nav@${navTop} main@${mainTop}`);

	// 展開手機目錄，確認裡面真的有目錄連結
	const before = await page.evaluate(() => document.querySelector('.article-mobile-nav')?.hasAttribute('open'));
	await page.click('.article-mobile-nav > summary');
	await new Promise((r) => setTimeout(r, 500));
	const after = await page.evaluate(() => ({
		open: document.querySelector('.article-mobile-nav')?.hasAttribute('open'),
		links: document.querySelectorAll('.article-mobile-nav nav a[href^="#"]').length,
	}));
	ok('點 summary 可以展開', before === false && after.open === true);
	ok('展開後有目錄連結', after.links > 0, `${after.links} 條`);
}

// ============ 平板：首頁（768px 斷點）============
await at(768, 1024, '/', '平板 首頁');
{
	const o = await overflow();
	ok('沒有橫向溢出', o.scrollW <= o.clientW + 1, `scrollW=${o.scrollW} clientW=${o.clientW}`);
	ok('右側工具欄隱藏', !(await vis('#right-panel-wrapper')));
	ok('漢堡選單按鈕可見（lg 以下）', await vis('#nav-menu-switch'));
	ok('桌機導覽連結列隱藏', !(await vis('#navbar .hidden.lg\\:flex')));
}

// ============ 桌機：確認 1536 以上右欄出現 ============
await at(1600, 1000, '/', '桌機 首頁');
{
	ok('右側工具欄出現', await vis('#right-panel-wrapper'));
	ok('時間與天氣卡可見', await vis('#rp-weather'));
	ok('側欄與文章列表並排（同一列）', await page.evaluate(() => {
		const l = document.querySelector('#left-panel-wrapper')?.getBoundingClientRect();
		const m = document.querySelector('main')?.getBoundingClientRect();
		if (!l || !m) return false;
		// 並排 = 垂直位置重疊且左右分開
		return Math.abs(l.top - m.top) < 40 && l.right <= m.left + 1;
	}));
}

// ============ 手機：換頁後手機版目錄要跟著換 ============
// 這是 #left-panel-wrapper 這個容器帶來的效果：手機版的可展開目錄與桌機版
// aside 是兄弟節點，以前只有 aside 內的 #toc 是 swup 容器，所以用手機
// 從首頁點進文章時，整張「文章導覽」卡片根本不會被換進來。
await at(390, 844, '/', '手機 首頁 → 文章（換頁，非重載）');
{
	const before = await vis('.article-mobile-nav');
	const clicked = await page.evaluate(() => {
		const a = document.querySelector('main a[href^="/posts/"]');
		if (!a) return false;
		a.click();
		return true;
	});
	await new Promise((r) => setTimeout(r, 3000));
	const after = await page.evaluate(() => ({
		url: location.href,
		nav: !!document.querySelector('.article-mobile-nav'),
		summary: document.querySelector('.article-mobile-nav summary')?.textContent?.replace(/\s+/g, ' ').trim() || null,
	}));
	ok('首頁上本來沒有手機目錄', clicked && before === false);
	ok('換頁後 URL 正確', after.url.includes('/posts/'), after.url);
	ok('換頁後手機目錄有被換進來', after.nav === true);
	ok('手機目錄內容非空', (after.summary || '').length > 0, after.summary || '');
}

await browser.close();
console.log(failures === 0 ? '\nALL GREEN' : `\n${failures} FAILURES`);
process.exit(failures === 0 ? 0 : 1);