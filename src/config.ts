import type {
	ExpressiveCodeConfig,
	GitHubEditConfig,
	ImageFallbackConfig,
	LicenseConfig,
	NavBarConfig,
	ProfileConfig,
	SiteConfig,
	UmamiConfig,
} from "./types/config";
import { LinkPreset } from "./types/config";

export const siteConfig: SiteConfig = {
	title: "Typelin Blog",
	subtitle: "技術分享",
	description: "Typelin 的技術空間：記錄靈感與科技探索。",

	keywords: [
		"Typelin",
		"極簡部落格",
		"技術分享",
		"秘密空間",
		"生活隨筆",
		"Fuwari",
	],
	lang: "zh_TW", // 'en', 'zh_CN', 'zh_TW', 'ja', 'ko', 'es', 'th'
	themeColor: {
		hue: 250, // Default hue for the theme color, from 0 to 360. e.g. red: 0, teal: 200, cyan: 250, pink: 345
		fixed: false, // Hide the theme color picker for visitors
		forceDarkMode: false, // Force dark mode and hide theme switcher
	},
	banner: {
		enable: false, // 暫時關閉 Banner 以免推擠頁面
		src: "/banner.png",
		position: "center",
		credit: {
			enable: true, // Display the credit text of the banner image
			text: "Pixiv @chokei", // Credit text to be displayed

			url: "https://www.pixiv.net/artworks/122782209", // (Optional) URL link to the original artwork or artist's page
		},
	},
	background: {
		enable: true, // Enable background image
		src: "https://pic.typelin.me", // 恢復原本的隨機圖片正式網域
		position: "center", // Background position: 'top', 'center', 'bottom'
		size: "cover", // Background size: 'cover', 'contain', 'auto'
		repeat: "no-repeat", // Background repeat: 'no-repeat', 'repeat', 'repeat-x', 'repeat-y'
		attachment: "fixed", // Background attachment: 'fixed', 'scroll', 'local'
		opacity: 1, // Background opacity (0-1)
	},
	toc: {
		enable: true, // Display the table of contents on the right side of the post
		depth: 2, // Maximum heading depth to show in the table, from 1 to 3
	},
	favicon: [
		// Leave this array empty to use the default favicon
		{
			src: "/avatar_v1.jpg", // 更新頭像作為分頁圖示
			//   theme: 'light',              // (Optional) Either 'light' or 'dark', set only if you have different favicons for light and dark mode
			//   sizes: '32x32',              // (Optional) Size of the favicon, set only if you have favicons of different sizes
		},
	],
	officialSites: [], // 停用官方網站彈窗
};

export const navBarConfig: NavBarConfig = {
	links: [
		LinkPreset.Home,
		LinkPreset.Archive,
		{
			name: "關於",
			url: "/about/",
			external: false,
		},
		{
			name: "課表",
			url: "/schedule/",
			external: false,
		},
		{
			name: "日曆",
			url: "/calendar/",
			external: false,
		},
	],
};

export const profileConfig: ProfileConfig = {
	avatar: "/avatar_v1.jpg", // 更新後的頭像
	name: "Typelin",
	bio: "吾心吾行澄如明鏡，所作所為皆為正義",
	links: [
		{
			name: "Bilibli",
			icon: "fa6-brands:bilibili",
			url: "https://space.bilibili.com/383913921",
		},
		{
			name: "GitHub",
			icon: "fa6-brands:github",
			url: "https://github.com/Typelin",
		},
		{
			name: "Discord",
			icon: "fa6-brands:discord",
			url: "typelin#1109", // 這個欄位將在組件中特殊處理為「點擊複製」
		},
		{
			name: "QQ",
			icon: "fa6-brands:qq",
			url: "3825383356",
		},
		{
			name: "Contact",
			icon: "material-symbols:mail-outline",
			url: "https://typelin.pages.dev/#footer",
		},
	],
};

export const licenseConfig: LicenseConfig = {
	enable: true,
	name: "CC BY-NC-SA 4.0",
	url: "https://creativecommons.org/licenses/by-nc-sa/4.0/",
};

export const imageFallbackConfig: ImageFallbackConfig = {
	enable: false,
	originalDomain: "https://eopfapi.acofork.com/pic?img=ua",
	fallbackDomain: "https://eopfapi.acofork.com/pic?img=ua",
};

export const umamiConfig: UmamiConfig = {
	enable: false, // 禁用 Umami，改用 Cloudflare Workers
	baseUrl: "",
	shareId: "",
	timezone: "Asia/Taipei",
};

// Cloudflare Workers 計數器配置
export const cfCounterUrl = "https://typelin-counter.nankatianchao.workers.dev"; // 已完成對接
export const counterDevMode = false; // [開發者模式] 開啟時無視 24 小時限制，每次刷新都會計入訪客

export const expressiveCodeConfig: ExpressiveCodeConfig = {
	theme: "github-dark",
};

export const gitHubEditConfig: GitHubEditConfig = {
	enable: true,
	baseUrl: "https://github.com/Typelin/fuwari/blob/main/src/content/posts",
};

// todoConfig removed from here
