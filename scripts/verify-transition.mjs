// 換頁品質量測：整頁重載、View Transition、畫面亮度曲線、掉幀。
// 用法：node scripts/verify-transition.mjs [--slow] [--no-vt]
//   --slow  把 View Transition 拉長到 2.4s，方便抓「閃一下」的亮度凹陷。
//   --no-vt 在點擊前把 document.startViewTransition 拿掉，做 A/B 對照。
import puppeteer from 'file:///D:/Antigravity_proj/important/typlin-arena/node_modules/puppeteer-core/lib/puppeteer/puppeteer-core.js';

const BASE = process.env.BLOG_URL || 'http://localhost:4321';
const SLOW = process.argv.includes('--slow');
const NO_VT = process.argv.includes('--no-vt');
const SHOTS = process.argv.includes('--shots');
const LITE = process.argv.includes('--lite');
const JS_CLICK = process.argv.includes('--js-click');
const VT_MS = SLOW ? 2400 : 700;

// --lite：關掉可疑的高成本視覺效果，用來驗證卡頓是不是光柵成本造成的。
// 掛在 body 而不是 head，因為 swup 的 head 外掛換頁時會換掉 head 內容。
const LITE_CSS = `
  #bg-box { display: none !important; }
  * { box-shadow: none !important; backdrop-filter: none !important; filter: none !important; }
`;

const browser = await puppeteer.launch({
	executablePath: 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
	headless: true,
	args: ['--no-sandbox', '--disable-dev-shm-usage'],
});
const page = await browser.newPage();
await page.setViewport({ width: 1440, height: 900 });

// 用畫面平均值當亮度指標。截圖丟回頁面用 canvas 解碼，省一個影像套件。
async function brightness(buf) {
	return page.evaluate(async (b64) => {
		const img = new Image();
		img.src = 'data:image/png;base64,' + b64;
		await img.decode();
		const c = document.createElement('canvas');
		c.width = 80;
		c.height = 50;
		const ctx = c.getContext('2d');
		ctx.drawImage(img, 0, 0, 80, 50);
		const d = ctx.getImageData(0, 0, 80, 50).data;
		let sum = 0;
		for (let i = 0; i < d.length; i += 4) sum += (d[i] + d[i + 1] + d[i + 2]) / 3;
		return Math.round(sum / (d.length / 4));
	}, buf.toString('base64'));
}

async function instrument() {
	await page.evaluate((noVt) => {
		window.__marker = 'alive';
		window.__vt = 0;
		if (noVt) {
			// swup 在每次 visit 時讀 document.startViewTransition 決定走不走 VT
			delete document.startViewTransition;
		} else {
			const orig = document.startViewTransition?.bind(document);
			if (orig) {
				document.startViewTransition = (cb) => {
					window.__vt += 1;
					return orig(cb);
				};
			}
		}
		window.__frames = [];
		window.__t0 = performance.now();
		window.__longtasks = [];
		try {
			new PerformanceObserver((list) => {
				for (const e of list.getEntries()) {
					window.__longtasks.push({
						t: Math.round(e.startTime - window.__t0),
						dur: Math.round(e.duration),
					});
				}
			}).observe({ entryTypes: ['longtask'] });
		} catch (_) {}

		// 掛上 swup 各階段計時，把同步渲染工作拆開
		window.__phases = [];
		if (window.swup?.hooks) {
			for (const h of [
				'visit:start',
				'page:load',
				'content:replace',
				'content:scroll',
				'page:view',
				'animation:in:await',
				'visit:end',
			]) {
				window.swup.hooks.on(h, () => {
					window.__phases.push({ h, t: Math.round(performance.now() - window.__t0) });
				});
			}
		}
		let last = performance.now();
		// 記錄換頁期間卡片上出現過哪些動畫。純 CSS transition 會是 CSSAnimation，
		// motion 驅動的會是 WAAPI（沒有 animationName）。用來確認沒有多餘的落定動畫。
		window.__cardAnims = [];
		setInterval(() => {
			for (const a of document.getAnimations()) {
				const el = a.effect?.target;
				if (!el?.classList?.contains?.('post-card')) continue;
				const key = a.animationName
					? `css:${a.animationName}`
					: `waapi:${Math.round(a.effect.getTiming().duration || 0)}ms`;
				if (!window.__cardAnims.includes(key)) window.__cardAnims.push(key);
			}
		}, 40);
		const loop = (t) => {
			window.__frames.push({ t: Math.round(t - window.__t0), dt: Math.round(t - last) });
			last = t;
			requestAnimationFrame(loop);
		};
		requestAnimationFrame(loop);
	}, NO_VT);
}

async function sample(ms) {
	// 截圖本身會佔用主執行緒，會污染掉幀量測，所以預設不截圖。
	if (!SHOTS) {
		await new Promise((r) => setTimeout(r, ms));
		return [];
	}
	const out = [];
	const t0 = Date.now();
	while (Date.now() - t0 < ms) {
		const buf = await page.screenshot({ type: 'png' });
		out.push({ t: Date.now() - t0, b: await brightness(buf) });
	}
	return out;
}

function report(label, samples, state) {
	const b = samples.map((s) => s.b);
	const hasShots = b.length > 0;
	const min = hasShots ? Math.min(...b) : null;
	const max = hasShots ? Math.max(...b) : null;
	const base = hasShots ? b[0] : null;
	const dip = hasShots ? base - min : 0;
	const frames = state.frames || [];
	const dts = frames.map((f) => f.dt);
	const worst = dts.length ? Math.max(...dts) : 0;
	const sorted = [...dts].sort((x, y) => x - y);
	const p95 = sorted.length ? sorted[Math.floor(sorted.length * 0.95)] : 0;
	const stallIdx = dts.indexOf(worst);
	const around = frames
		.slice(Math.max(0, stallIdx - 3), stallIdx + 3)
		.map((f) => `${f.t}ms:+${f.dt}`)
		.join('  ');

	console.log(`\n── ${label} ──`);
	console.log(`  整頁重載      : ${state.marker === 'alive' ? '沒有' : '有（marker 消失）'}`);
	console.log(`  ViewTransition: ${state.vt} 次`);
	console.log(`  URL           : ${state.url}`);
	console.log(`  body class    : ${state.bodyClass || '(空)'}`);
	if (hasShots) {
		console.log(`  亮度 起始/最低/最高 : ${base} / ${min} / ${max}  → 凹陷 ${dip}`);
		console.log(`  亮度曲線      : ${b.join(' ')}`);
	}
	console.log(`  最長幀 / p95  : ${worst}ms / ${p95}ms（共 ${frames.length} 幀）`);
	console.log(`  卡點前後      : ${around}`);
	const lt = state.longtasks || [];
	console.log(
		`  主執行緒 longtask: ${lt.length === 0 ? '無 → 卡的是合成/光柵，不是 JS' : lt.map((t) => `t=${t.t}ms:+${t.dur}ms`).join('  ')}`,
	);
	const ph = state.phases || [];
	if (ph.length) {
		const first = ph[0].t;
		const lastP = ph[ph.length - 1].t;
		console.log(
			`  swup 階段     : ${ph.map((p, i) => `${p.h}@${p.t - first}ms${i > 0 ? `(+${p.t - ph[i - 1].t})` : ''}`).join('  ')}`,
		);
		console.log(`  階段總跨距    : ${lastP - first}ms`);
	}
	const rq = state.reqs || [];
	if (rq.length) {
		const heads = rq.filter((r) => r.startsWith('HEAD'));
		const doc = rq.filter((r) => r.includes('localhost:4321') && !r.startsWith('HEAD'));
		console.log(`  換頁期間請求  : 共 ${rq.length}（HEAD ${heads.length}、站內文件 ${doc.length}）`);
		if (heads.length) console.log(`    HEAD: ${heads.slice(0, 5).join(' | ')}`);
	}
	const ca = state.cardAnims || [];
	const cc = state.cardCount ?? 0;
	if (cc > 0) {
		const waapi = ca.filter((c) => c.startsWith('waapi'));
		console.log(
			`  卡片上的動畫  : ${ca.length ? ca.join('  ') : '（無）'}${
				waapi.length ? '  ⚠️ 有 motion 驅動的動畫' : '  ✅ 沒有多餘動畫'
			}（頁面卡片數 ${cc}）`,
		);
	} else {
		console.log(`  卡片上的動畫  : 此頁沒有卡片，跳過`);
	}
	if (dip >= 25) console.log('  ⚠️  亮度明顯凹陷 → 這就是「閃一下」');
	return { dip, worst, p95 };
}

async function run(label, selector, startPath = '/') {
	await page.goto(`${BASE}${startPath}`, { waitUntil: 'networkidle2', timeout: 60000 });
	await page.waitForFunction(
		() => window.swup && document.documentElement.classList.contains('swup-enabled'),
		{ timeout: 30000 },
	);
	await new Promise((r) => setTimeout(r, 1200));
	if (SLOW) {
		await page.addStyleTag({
			content: '::view-transition-new(root){animation-duration:2.4s !important}',
		});
	}
	if (LITE) {
		await page.evaluate((css) => {
			const s = document.createElement('style');
			s.id = 'lite-probe';
			s.textContent = css;
			document.body.appendChild(s);
		}, LITE_CSS);
	}
	await instrument();
	const reqs = [];
	const onReq = (r) => reqs.push(`${r.method()} ${r.url()}`);
	page.on('request', onReq);
	if (selector) {
		// --js-click 用頁面內 element.click()，繞過 CDP 的輸入派送，
		// 用來分辨「卡的是 App」還是「卡的是自動化輸入通道」。
		if (JS_CLICK) await page.evaluate((s) => document.querySelector(s).click(), selector);
		else await page.click(selector);
	}
	const samples = await sample(VT_MS);
	page.off('request', onReq);
	const state = await page.evaluate(() => ({
		marker: window.__marker,
		vt: window.__vt,
		url: location.href,
		bodyClass: document.body.className,
		toc: !!document.getElementById('toc'),
		frames: window.__frames,
		longtasks: window.__longtasks,
		phases: window.__phases,
		cardAnims: window.__cardAnims,
		cardCount: document.querySelectorAll('main .post-card').length,
	}));
	state.reqs = reqs;
	return report(label, samples, state);
}

const results = [];
// 基準線：完全不互動，量環境本身的幀間隔
results.push(await run('基準線（不點擊）', null));
// 對照組：點一個不會導覽的元素，分辨卡點是不是自動化輸入造成的
results.push(await run('對照（點不會導覽的區塊）', 'main .post-card__excerpt'));
results.push(await run('點文章（首頁第一張卡）', 'main a[href^="/posts/"]'));
results.push(await run('點頂端導覽「課表」', '#navbar a[href="/schedule/"]'));
// 這筆才會落到有卡片的頁面，用來確認換頁後沒有任何多餘的落定動畫
results.push(
	await run(
		'文章頁 → 回首頁（卡片會出現）',
		'#left-panel-wrapper a[href="/"]',
		'/posts/typelin-arena-2026-09/',
	),
);

await browser.close();

const bad = results.filter((r) => r.dip >= 25 || r.worst >= 120);
console.log(bad.length === 0 ? '\nALL GREEN' : `\n${bad.length} 項有問題`);