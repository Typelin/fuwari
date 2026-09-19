// 逐幀抓換頁過程，偵測「閃一下」。截圖取樣太慢會漏掉單幀閃光，
// 所以走 CDP screencast，每個畫面都收到。
// 用法：node scripts/cast-transition.mjs [selector]
import puppeteer from 'file:///D:/Antigravity_proj/important/typlin-arena/node_modules/puppeteer-core/lib/puppeteer/puppeteer-core.js';

const BASE = process.env.BLOG_URL || 'http://localhost:4321';
const SELECTOR = process.argv[2] || 'main a[href^="/posts/"]';

const browser = await puppeteer.launch({
	executablePath: 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
	headless: true,
	args: ['--no-sandbox', '--disable-dev-shm-usage'],
});
const page = await browser.newPage();
await page.setViewport({ width: 1440, height: 900 });

const brightnessOf = async (b64) =>
	page.evaluate(async (d) => {
		const img = new Image();
		img.src = 'data:image/jpeg;base64,' + d;
		await img.decode();
		const c = document.createElement('canvas');
		c.width = 80;
		c.height = 50;
		const ctx = c.getContext('2d');
		ctx.drawImage(img, 0, 0, 80, 50);
		const px = ctx.getImageData(0, 0, 80, 50).data;
		let sum = 0;
		for (let i = 0; i < px.length; i += 4) sum += (px[i] + px[i + 1] + px[i + 2]) / 3;
		return Math.round(sum / (px.length / 4));
	}, b64);

async function cast(selector, label) {
	await page.goto(`${BASE}/`, { waitUntil: 'networkidle2', timeout: 60000 });
	await page.waitForFunction(
		() => window.swup && document.documentElement.classList.contains('swup-enabled'),
		{ timeout: 30000 },
	);
	await new Promise((r) => setTimeout(r, 1500));

	const client = await page.createCDPSession();
	let frames = [];
	let t0 = null;
	client.on('Page.screencastFrame', async ({ data, sessionId, metadata }) => {
		if (t0 === null) t0 = metadata.timestamp;
		frames.push({ t: Math.round((metadata.timestamp - t0) * 1000), data });
		await client.send('Page.screencastFrameAck', { sessionId });
	});

	await client.send('Page.startScreencast', { format: 'jpeg', quality: 40, everyNthFrame: 1 });
	await new Promise((r) => setTimeout(r, 600));

	// 靜止基準
	const idle = frames;
	frames = [];
	const idleB = [];
	for (const f of idle) idleB.push(await brightnessOf(f.data));
	const base = idleB.length ? idleB[idleB.length - 1] : null;

	const clickT = idle.length ? idle[idle.length - 1].t : 0;
	await page.click(selector);
	await new Promise((r) => setTimeout(r, 2500));
	await client.send('Page.stopScreencast');
	await client.detach();

	// 注意：亮度必須在關掉瀏覽器之前算完
	const timeline = [];
	for (const f of frames) timeline.push({ t: f.t - clickT, b: await brightnessOf(f.data) });

	const b = timeline.map((f) => f.b);
	const min = b.length ? Math.min(...b) : null;
	const max = b.length ? Math.max(...b) : null;

	// 換頁前後的頁面本身亮度就不同（首頁比課表頁亮），所以不能拿「起始亮度」當基準。
	// 真正的「閃一下」是瞬時凹陷：亮度掉到比起點和終點都還低，然後又回來。
	const startB = base ?? (b.length ? b[0] : 0);
	const tail = b.slice(-10);
	const endB = tail.length ? tail.slice().sort((x, y) => x - y)[Math.floor(tail.length / 2)] : 0;
	const floor = Math.min(startB, endB);
	const dip = floor - min;

	console.log(`\n── ${label} ──`);
	console.log(`  起始/結束亮度: ${startB} / ${endB}`);
	console.log(`  換頁幀數     : ${timeline.length}`);
	console.log(`  亮度 最低/最高: ${min} / ${max}`);
	console.log(`  瞬時凹陷     : ${dip}（低於起點與終點兩者的程度）`);
	console.log(`  逐幀 t:亮度  : ${timeline.map((f) => `${f.t}:${f.b}`).join('  ')}`);
	const dips = timeline.filter((f) => f.t >= 0 && floor - f.b >= 15);
	console.log(
		dips.length
			? `  ⚠️  ${dips.length} 幀低於起終點：${dips.map((d) => `${d.t}ms(${d.b})`).join(' ')}`
			: '  ✅ 沒有低於起終點的幀 → 沒有閃光',
	);
	return { dip, frames: timeline.length };
}

const a = await cast('main a[href^="/posts/"]', '點文章');
const b2 = await cast('#navbar a[href="/schedule/"]', '點頂端導覽「課表」');
await browser.close();
console.log(
	Math.max(a.dip, b2.dip) >= 20 ? '\n有偵測到閃光' : '\nALL GREEN（沒有閃光）',
);