// 直接從 TimeWeatherCard.astro 抽出實際的 script 內容來測，
// 不是另外抄一份 —— 抄一份就失去驗證意義。
// 用法：node scripts/test-weather.mjs [--live]
import { readFileSync } from 'node:fs';

const src = readFileSync(
	new URL('../src/components/widget/TimeWeatherCard.astro', import.meta.url),
	'utf8',
);
const m = /<script is:inline>([\s\S]*?)<\/script>/.exec(src);
if (!m) throw new Error('找不到 script is:inline 區塊');

// 去掉 IIFE 外層，讓裡面用 var 宣告的函式變成這個 scope 的區域變數
const body = m[1].replace(/^\s*\(function\s*\(\)\s*\{/, '').replace(/\}\)\(\);\s*$/, '');

const noop = () => {};
const stub = {
	document: { getElementById: () => null, querySelectorAll: () => [] },
	localStorage: { getItem: () => null, setItem: noop },
	fetch: () => new Promise(noop),
	setInterval: noop,
};
const factory = new Function(
	'document',
	'localStorage',
	'fetch',
	'setInterval',
	`${body}
	return { resolveCondition, pickRainChance, normalizeLocationLabel, weatherUrl };`,
);
const api = factory(stub.document, stub.localStorage, stub.fetch, stub.setInterval);

let fails = 0;
const eq = (name, got, want) => {
	const ok = JSON.stringify(got) === JSON.stringify(want);
	console.log(
		`${ok ? 'PASS' : 'FAIL'}  ${name}${ok ? '' : `\n       got ${JSON.stringify(got)} want ${JSON.stringify(want)}`}`,
	);
	if (!ok) fails++;
};

const cur = (o) => ({
	weather_code: 0,
	precipitation: 0,
	cloud_cover: 0,
	is_day: 1,
	...o,
});

// ---- resolveCondition：以降水量為準，沒降水就不講雨 ----
eq('有降水 + 雷雨代碼 → 雷雨', api.resolveCondition(cur({ weather_code: 95, precipitation: 3 })), 'thunder');
eq('降水 0.2mm → 小雨', api.resolveCondition(cur({ weather_code: 61, precipitation: 0.2 })), 'drizzle');
eq('降水 1.0mm → 有雨', api.resolveCondition(cur({ weather_code: 63, precipitation: 1 })), 'rain');
eq('降水 5.0mm → 大雨', api.resolveCondition(cur({ weather_code: 65, precipitation: 5 })), 'heavy-rain');
eq('降水 0.8mm + 雪代碼 → 降雪', api.resolveCondition(cur({ weather_code: 73, precipitation: 0.8 })), 'snow');
eq('降水 1.2mm + 陣雪代碼 → 降雪', api.resolveCondition(cur({ weather_code: 85, precipitation: 1.2 })), 'snow');

eq('無降水 + 雲量 8% 白天 → 晴朗', api.resolveCondition(cur({ cloud_cover: 8 })), 'clear');
eq('無降水 + 雲量 8% 夜晚 → 晴朗', api.resolveCondition(cur({ cloud_cover: 8, is_day: 0 })), 'clear-night');
eq('無降水 + 雲量 30% → 局部多雲', api.resolveCondition(cur({ cloud_cover: 30 })), 'partly-cloudy');
eq('無降水 + 雲量 70% → 多雲', api.resolveCondition(cur({ cloud_cover: 70 })), 'cloudy');
eq('無降水 + 雲量 90% → 陰天', api.resolveCondition(cur({ cloud_cover: 90 })), 'overcast');
eq('霧代碼 → 有霧', api.resolveCondition(cur({ weather_code: 45 })), 'fog');

// 這是換掉 wttr.in 的原因：它對「雲量 84%、降水 0.0mm」吐 "Patchy rain nearby"。
// 新的判定必須講天空，不能講雨。
eq(
	'回歸測試：雲量 84% + 降水 0 → 不可以是雨',
	['thunder', 'heavy-rain', 'rain', 'drizzle'].includes(
		api.resolveCondition(cur({ weather_code: 176, precipitation: 0, cloud_cover: 84 })),
	),
	false,
);
eq('回歸測試：同上應判為多雲', api.resolveCondition(cur({ precipitation: 0, cloud_cover: 84 })), 'cloudy');

eq('欄位全缺 → null', api.resolveCondition({}), null);

// ---- pickRainChance：用當地時間字串比對，不做時區換算 ----
const hourly = {
	time: ['2026-09-19T14:00', '2026-09-19T15:00', '2026-09-19T16:00'],
	precipitation_probability: [10, 55, 20],
};
eq('比對到同一小時 → 取該小時機率', api.pickRainChance(hourly, '2026-09-19T15:15'), 55);
eq('比對到整點 → 取該小時機率', api.pickRainChance(hourly, '2026-09-19T14:00'), 10);
eq('找不到對應小時 → null', api.pickRainChance(hourly, '2026-09-20T03:00'), null);
eq('機率為 null → null', api.pickRainChance({ time: ['2026-09-19T14:00'], precipitation_probability: [null] }, '2026-09-19T14:30'), null);
eq('沒有 hourly → null', api.pickRainChance(null, '2026-09-19T14:00'), null);
eq('hourly 空陣列 → null', api.pickRainChance({ time: [], precipitation_probability: [] }, '2026-09-19T14:00'), null);

// ---- 其他 ----
eq('地點標籤去重', api.normalizeLocationLabel('Tainan, Tainan'), 'Tainan');
eq('地點標籤保留城市與國名', api.normalizeLocationLabel('Tainan, Taiwan'), 'Tainan, Taiwan');
eq(
	'URL 帶經緯度與必要欄位',
	api
		.weatherUrl({ lat: 22.99, lon: 120.21 })
		.includes('latitude=22.99&longitude=120.21&current=temperature_2m'),
	true,
);
eq('URL 使用當地時區', api.weatherUrl({ lat: 22.99, lon: 120.21 }).includes('timezone=auto'), true);

// --live：真實端到端（Open-Meteo + ipapi.co）
if (process.argv.includes('--live')) {
	let loc = { lat: 22.9909, lon: 120.2128, label: 'Tainan, Taiwan' };
	let located = false;
	try {
		const geo = await (await fetch('https://ipapi.co/json/')).json();
		if (geo && !geo.error && geo.latitude) {
			loc = { lat: geo.latitude, lon: geo.longitude, label: `${geo.city}, ${geo.country_name}` };
			located = true;
		} else {
			console.log(`\n  ipapi.co: 限流或失敗（${geo?.reason || 'unknown'}）→ 退回 Tainan`);
		}
	} catch (e) {
		console.log(`\n  ipapi.co: 請求失敗 → 退回 Tainan`);
	}

	const w = await (await fetch(api.weatherUrl(loc))).json();
	const c = w.current;
	const cond = api.resolveCondition(c);
	console.log('\n── 真實端到端（Open-Meteo）──');
	console.log(`  定位         : ${located ? `${loc.label}（ipapi.co）` : `${loc.label}（後備值）`}`);
	console.log(`  當地時間     : ${c.time}`);
	console.log(`  溫度 / 濕度  : ${Math.round(c.temperature_2m)}°C / ${Math.round(c.relative_humidity_2m)}%`);
	console.log(`  降水 / 雲量  : ${c.precipitation}mm / ${c.cloud_cover}%`);
	console.log(`  WMO 代碼     : ${c.weather_code}`);
	console.log(`  判定         : ${cond}`);
	console.log(`  降雨機率     : ${api.pickRainChance(w.hourly, c.time)}%`);
	console.log('');
}

console.log(fails === 0 ? '\nALL GREEN' : `\n${fails} FAILURES`);
process.exit(fails === 0 ? 0 : 1);