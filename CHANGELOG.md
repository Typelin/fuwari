# 更新日誌 (Changelog)

所有時間皆為當地時間 (Local Time)。

## [2026-01-04] 🚀 正式上線準備

### 03:55 - 網站正式對外準備 ✅
- **[修復]** 移除 `officialSites` 配置，解決首頁彈窗問題
- **[更新]** README.md 改為繁體中文，更新專案說明
- **[更新]** 標語統一為「吾心吾行澄如明鏡，所作所為皆為正義」
- **[更新]** 文章「從零打造技術部落格」增加上游專案致謝 (saicaca/fuwari, afoim/fuwari)

### 03:40 - 專案清理 ✅
- **[刪除]** `.github/workflows/` - GitHub Actions 工作流程
- **[刪除]** `.obsidian/` - Obsidian 編輯器設定
- **[刪除]** `edgeone.json` - EdgeOne 配置
- **[刪除]** `wrangler.jsonc` - Wrangler 配置
- **[刪除]** `frontmatter.json` - Frontmatter 設定

### 03:35 - 隱私文件處理 ✅
- **[新增]** `.private/` 資料夾（不上傳至 GitHub）
- **[移動]** `task.md` → `.private/`
- **[移動]** `USER_PROMPT_BACKUP.md` → `.private/`
- **[移動]** `PROJECT_STATUS.md` → `.private/`
- **[移動]** `STARTUP_COMMANDS.md` → `.private/`
- **[移動]** `訊號與系統期末考_考古題 (1).pdf` → `.private/`
- **[更新]** `.gitignore` 添加 `.private/`、`fuwari-main/`、`*.pdf`、`.obsidian/`

### 03:30 - 移除「主人」「女僕」字樣 ✅
- **[修改]** `config.ts` - 網站名稱改為「Typelin 的技術空間」
- **[修改]** `config.ts` - 個人資料名稱改為「Typelin」
- **[修改]** `config.ts` - 導航改為「關於我」
- **[修改]** `about.astro` - 頁面標題和內容更新
- **[修改]** `404.astro` - 錯誤訊息更新
- **[修改]** `hello-master.md` - 文章內容更新
- **[修改]** `how-to-build-typelin-space.md` - 文章內容更新

### 02:00 - 訊號與系統文章增強 ✅
- **[新增]** 8 題考試答題模板
- **[新增]** 卷積過程圖解（翻轉、滑動、重疊區域）
- **[新增]** `conv_step1_flip.png` - 翻轉過程圖
- **[新增]** `conv_sliding_animation.png` - 滑動動畫圖
- **[新增]** `conv_complete_process.png` - 完整過程圖
- **[新增]** `generate_convolution_steps.py` - 圖表生成腳本

---

## [2026-01-03]

### 13:20 - 文章圖片與格式修復 ✅
- **[修復]** Flutter 文章添加封面配圖 (Flutter 官方 Logo)
- **[修復]** 資料庫文章添加封面配圖 (MongoDB 主題圖)
- **[修復]** 各資料庫添加 Logo + 點擊跳轉官網連結
- **[修復]** 將 ASCII 框線改為 Markdown 表格（解決對齊問題）
- **[修復]** 損壞圖片 URL 替換為可用連結
- **[更新]** task.md 添加詳細任務項目和文章規範備忘
- **[更新]** USER_PROMPT_BACKUP.md 添加文章圖片規範

### 13:15 - About 頁面修復 + 新文章 ✅
- **[修復]** About 頁面社交連結更正為正確網址
- **[新增]** Discord 聯繫方式 (typelin#1109)
- **[新增]** Flutter 開發教學文章 `flutter-vscode-complete-guide.md`
- **[新增]** 資料庫比較文章 `database-comparison-guide.md`

### 04:35 - 類別/標籤連結 404 修復 ✅
- **[新增]** `/archive/category/[slug].astro` 動態路由頁面
- **[新增]** `/archive/tag/[slug].astro` 動態路由頁面
- **[恢復]** 瀏覽量/訪客數圖標放入底部小字行（視覺平衡）
- **[驗證]** 類別/標籤連結正常工作，無 404

### 04:25 - 文章卡片樣式優化 ✅
- **[修改]** PostMeta.astro 添加類別顯示（書本圖標）
- **[修改]** PostMeta.astro 添加標籤顯示（# 圖標）
- **[移除]** PostCard.astro 重複的瀏覽量/訪客數圖標（底部小的）
- **[保留]** 只顯示字數和閱讀時間在底部行

### 04:15 - 側邊欄類別與標籤組件 ✅
- **[新增]** 從 fuwari-main 適配 Categories、Tags、WidgetLayout 組件
- **[新增]** ButtonLink、ButtonTag 控制組件
- **[新增]** content-utils.ts 添加 getCategoryList/getTagList 函數
- **[新增]** url-utils.ts 添加 getCategoryUrl/getTagUrl 函數
- **[修復]** 移除 i18n 依賴，改用硬編碼繁體中文
- **[修復]** content/config.ts 添加 category 欄位定義

### 03:50 - 文章頁面與贊助頁修改
- **[移除]** 文章頁「這篇文章是否對你有幫助？」區塊
- **[移除]** Giscus 評論區（待配置自己的 repo）
- **[新增]** 「評論功能尚未開放」佔位區塊
- **[修改]** 贊助頁替換為「此頁面尚未開放」狀態頁

### 01:15 - 焦點觸發背景變化問題終極修復 ✅✅✅
- **[修復]** **根本原因**: 全域 `transition` 規則對 `<a>` 連結應用過渡效果，導致元素焦點時觸發 `backdrop-filter` GPU 層重新合成。
- **[修復]** 將 `@apply transition;` 替換為 `@apply transition-colors duration-150;`，限制過渡僅作用於顏色屬性。
- **[修復]** 移除 `.card-base` 上的 `will-change: backdrop-filter`，防止瀏覽器採取導致渲染偽影的 GPU 合成「捷徑」。
- **[驗證]** 測試 Discord 圖標點擊、GitHub 圖標點擊、搜尋框焦點、導航連結懸停，全部通過——文章卡片背景保持穩定。

---

## [2026-01-02]

### 16:52 - 白框問題徹底根除 ✅✅
- **[修復]** **根本原因已解決**: `.expand-animation` 中的 `before:scale` 動畫與 `backdrop-filter` 發生 GPU 合成衝突。
- **[修復]** 將 `before:scale-[0.85] hover:before:scale-100` 替換為 `before:opacity-0 hover:before:opacity-100`。
- **[驗證]** 自動化瀏覽器測試**通過**：無白框、無透明度異常。

### 16:30 - 白框問題最終修復 ✅
- **[修復]** (`Fix 5.2`) 成功修復白框/白槓問題：
    - 移除 `PostCard.astro` 中隱藏的分隔線元素 (Line 116)。
    - 為標題連結添加 `overflow-hidden` 以限制偽元素範圍。
    - 經自動化瀏覽器測試驗證通過。

### 16:15 - 文檔與規範更新
- **[文檔]** 重寫 `USER_PROMPT_BACKUP.md`，加入文檔規範。
- **[文檔]** 建立 `d:\Blog\task.md`，採用標準化格式 (繁體中文)。

### 15:42 - 功能實作與嘗試修復
- **[功能]** (`Fix 5.1`) 首頁文章列表加入瀏覽量與訪客數顯示。
- **[修復]** (`Fix 5.2`) 多次嘗試修復白槓問題：
    - 嘗試 1: `overflow-hidden` on PostCard
    - 嘗試 2: `isolation: isolate`
    - 嘗試 3: 背景圖 CSS 修正
    - 嘗試 4: 移除 `active:scale` 動畫
    - 嘗試 5: 全域禁用 `outline`
