# 2026-07-17 網站效能、安全與維護性優化紀錄

## 基準與範圍

- 專案：Typelin Blog（Fuwari / Astro）
- 基準 commit：`dbfd709`（日曆 Swup 初始化修復）
- 部署模式：Astro 純靜態輸出（`output: "static"`）
- 本次目標：降低首屏第三方腳本負擔、清理失效服務、更新安全相依、縮短內容掃描與建置時間，並建立可重複的驗證流程。

## 主要變更

### 效能與前端載入

- 新增 `DeferredAnalytics.astro`，將 Google Analytics、AdSense、百度統計及 Microsoft Clarity 延後至瀏覽器閒置時載入。
- Cloudflare Web Analytics 與既有 Cloudflare Counter 保留；第三方分析不再阻塞主要內容渲染。
- 隨機背景 `random.js` 改為 `defer`。
- 移除已失效的 Vercel Analytics 載入碼及 `@vercel/analytics`、`@astrojs/vercel` 相依，消除 `/_vercel/insights/script.js` 404。
- 新增 Cloudflare Pages `public/_headers`：
  - `X-Content-Type-Options: nosniff`
  - `Referrer-Policy: strict-origin-when-cross-origin`
  - `Permissions-Policy`（停用相機、麥克風、定位）
  - `X-Frame-Options: SAMEORIGIN`
  - `Cross-Origin-Opener-Policy: same-origin-allow-popups`
  - `_astro` 雜湊資源一年 immutable 快取
  - 圖片七天快取及 stale-while-revalidate

### 內容與建置清理

- 136 篇舊文章移至本機 `archive/posts_backup`。
- 964 個舊素材（194,392,440 bytes）移至本機 `archive/content-assets`。
- `archive/` 已加入 `.gitignore`，避免約 195 MB 封存檔進入部署倉庫；原始內容仍存在本機封存及 Git 基準 commit `dbfd709`。
- 移除不再使用的 `assets` content collection，消除舊素材掃描警告。
- 移除舊 Astro patch 與無效 `.npmrc` 設定，改用官方 `passthroughImageService()`。
- 修正失效短網址 `/tit`，改為原文章所指向的 Telegram 群組，避免導向已封存的 `/posts/pin/`。

### 相依與安全

- Astro：`5.7.9` → `5.18.2`（維持 Astro 5 安全線，避免未驗證的大版本遷移）。
- 更新 Svelte、Fancybox、Iconify、KaTeX、Sharp、sanitize-html、Tailwind 及其他同主版本相依。
- 以精確 `pnpm.overrides` 修補間接相依中的 Babel、Iconify tools、Rollup、esbuild、serialize-javascript、glob、minimatch、PostCSS、YAML 等已知漏洞。
- 移除 Vercel adapter/analytics，減少未使用的供應鏈表面。

安全稽核（`pnpm audit --prod`）：

| 等級 | 更新前 | 更新後 |
| --- | ---: | ---: |
| Critical | 2 | 0 |
| High | 69 | 2 |
| Moderate | 62 | 2 |
| Low | 17 | 1 |

剩餘 5 個 advisory 全部來自 Astro 5.18.2 本身，修補版本要求 Astro 6.1.6～6.4.6。現階段未強升 Astro 6，原因是既有 `@astrojs/svelte`、`@astrojs/tailwind` 與站內整合仍需完整遷移驗證。風險目前受以下條件限制：網站為純靜態輸出、沒有 Astro SSR / server islands、內容由受信任的本機 Markdown 建置。未來應以獨立分支完成 Astro 6 升級後再移除這項保留風險。

### 品質與維護性

- `type-check` 改為官方 `astro check`。
- 修復原有 Astro / TypeScript 診斷，包括 DOM 型別、未使用 import、Fancybox 6 設定及 inline script 變數。
- 修正 Bilibili 名稱、Contact 路徑、友鏈申請倉庫與外部連結 `rel`。
- 修正 Markdown code fence、KaTeX 中文下標及美元符號警告。
- 新增 `scripts/check-built-links.mjs`，驗證正式輸出內的本機 `href` / `src`。
- 新增 `pnpm run verify`，依序執行型別檢查、正式建置與站內連結掃描。

## 驗收結果

### 自動化

- `astro check`：60 個檔案，0 errors、0 warnings、0 hints。
- `astro build`：58 個頁面，約 12.45 秒；優化前約 19 秒，縮短約 34%。
- 建置連結掃描：70 個 HTML、5,426 個本機引用，0 broken references。
- 正式輸出未包含 `/_vercel/insights/script.js`。

### 實際瀏覽器

- 首頁：導覽、文章列表、Profile 與延遲分析腳本正常。
- 歸檔、關於、課表：標題及主要內容正常。
- 日曆：由首頁經 Swup 進入後完整展開；日期備忘視窗可開啟；切至歸檔再返回仍會重新初始化。
- 文章：內文正常，Fancybox 圖片燈箱可開啟。
- 390 × 844 手機版：首頁與日曆無水平溢出，導覽與月曆可用。
- Browser Console：0 errors、0 warnings。

`ERR_BLOCKED_BY_CLIENT` 通常代表瀏覽器廣告／追蹤阻擋器主動攔截第三方分析，並非網站 JavaScript 故障。本次已把這些服務延後載入，因此即使被攔截也不影響主要內容與日曆功能。

## 重複驗證

```powershell
corepack pnpm install
corepack pnpm run verify
corepack pnpm audit --prod
```

## 回滾與內容還原

- 完整回滾本次程式變更：對本次優化 commit 執行 `git revert <commit>`。
- 從基準 commit 還原舊內容：

```powershell
git restore --source=dbfd709 -- src/content/assets src/content/posts_backup
```

- 本機封存位置：`archive/posts_backup`、`archive/content-assets`。

## 後續建議

1. 在獨立分支測試 Astro 6.4.6 以上與新版 Svelte / Tailwind integrations，通過相同驗收後再升級。
2. 若不需要同時使用四套分析服務，可再精簡為 Cloudflare Analytics 加一套行為分析，進一步減少第三方請求。
3. 每次新增或移除文章後執行 `corepack pnpm run verify`，避免短網址或文章內連結再次指向不存在頁面。
