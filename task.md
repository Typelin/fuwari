# 任務清單 (Task List)

> 最後更新: 2026-01-03 14:35

---

## 📌 當前任務

- [x] **側邊欄類別與標籤組件**
    - [x] 從 fuwari-main 複製 WidgetLayout、ButtonLink、ButtonTag
    - [x] 適配 Categories.astro（移除 i18n 依賴）
    - [x] 適配 Tags.astro（移除 i18n 依賴）
    - [x] 更新 content-utils.ts 添加 getCategoryList/getTagList
    - [x] 更新 url-utils.ts 添加 getCategoryUrl/getTagUrl
    - [x] 更新 content/config.ts 添加 category 欄位
    - [x] 修復類別數量 -1 錯誤（實際是 i18n 模組問題）
    - [x] 瀏覽器驗證通過

- [x] **文章卡片樣式優化**
    - [x] PostMeta.astro 添加類別顯示（書本圖標）
    - [x] PostMeta.astro 添加標籤顯示（# 圖標）
    - [x] PostCard.astro 移除重複的瀏覽量/訪客數圖標
    - [x] PostPage.astro 傳入 tags/category props
    - [x] 瀏覽器驗證通過

- [x] **類別/標籤連結 404 修復**
    - [x] 創建 `/archive/category/[slug].astro` 動態路由
    - [x] 創建 `/archive/tag/[slug].astro` 動態路由
    - [x] 恢復瀏覽量/訪客數圖標到底部小字行
    - [x] 瀏覽器驗證通過（連結正常）

---

## ✅ 已完成任務 (2026-01-03)

- [x] **文章頁面修改**
    - [x] 移除「這篇文章是否對你有幫助？」區塊
    - [x] 移除 Giscus 評論（待配置自己的 repo）
    - [x] 添加「評論功能尚未開放」佔位區塊

- [x] **贊助頁面修改**
    - [x] 替換為「此頁面尚未開放」狀態頁

---

## 📋 歷史任務 (2026-01-02)

- [x] **白框/白槓問題修復**
    - [x] 嘗試 1~7 多種方案
    - [x] 最終方案：限制 transition 為顏色屬性 + 移除 will-change

- [x] **瀏覽量/訪客數顯示**
    - [x] PostCard.astro UI 實作
    - [x] CFCounter.astro 邏輯整合

- [x] **文檔規範建立**
    - [x] USER_PROMPT_BACKUP.md
    - [x] task.md
    - [x] CHANGELOG.md


---

## 🆕 新任務 (2026-01-03 13:00)

- [x] **修復 About 頁面**
    - [x] 修正 Bilibili 連結 (325903362 → 383913921)
    - [x] 修正 GitHub 連結 (afoim → Typelin)
    - [x] 添加 Discord 連結 (typelin#1109)
    - [x] 修復 Footer.astro 中的舊連結

- [x] **創建 Flutter 開發教學文章**
    - [x] `flutter-vscode-complete-guide.md`
    - [x] 內容：SDK 安裝路徑、Android Studio 勾選選項
    - [x] 內容：VS Code 擴充套件、常用指令表格
    - [x] 內容：flutter doctor 診斷與問題修復

- [x] **創建資料庫比較文章**
    - [x] `database-comparison-guide.md`
    - [x] 比較：Firebase, MongoDB, MySQL, PostgreSQL
    - [x] 分析：雲端託管 vs 本地架設優缺點
    - [x] 推薦：學生免費方案 (GitHub Student Pack)

- [x] **修復文章圖片品質**
    - [x] Flutter 文章添加封面配圖 (`/images/articles/flutter-logo.svg`)
    - [x] Flutter 文章修復損壞圖片連結 (替換為本地 SVG)
    - [x] Flutter Hello World 範例圖片本地化 (`flutter-hello-world.png`)
    - [x] 資料庫文章添加封面配圖 (`/images/articles/mongodb-logo.svg`)
    - [x] 各資料庫添加官方 Logo + 跳轉連結
    - [x] 將 ASCII 框線改為表格（修復對齊問題）
    - [x] 本地化圖片資源 (8 個檔案)

- [x] **文章結構規範化** (2026-01-03 13:48)
    - [x] Flutter 文章重構為三段式：Part 1 前置作業 / Part 2 創建專案 / Part 3 驗收
    - [x] 資料庫文章重構為三段式：Part 1 認識類型 / Part 2 詳細分析 / Part 3 選擇建議
    - [x] 移除所有「點擊圖片前往」
    - [x] 連結改用 `🔗 域名` 格式，統一放結尾表格
    - [x] AI 生成圖 (`flutter-hello-world.png`) 改用作封面而非內文
    - [x] 瀏覽器驗證通過

- [x] **創建 AI 大語言模型比較文章** (2026-01-03 14:35)
    - [x] `ai-llm-comparison-guide.md`
    - [x] 比較：GPT-4o, Claude 3.5, Gemini 2.0, DeepSeek V3, Grok 2
    - [x] 內容：常規問答、程式碼、多模態、圖片影片生成
    - [x] 內容：API 定價、網頁訂閱方案、企業方案
    - [x] 引用權威數據：GPQA, SWE-bench, HumanEval, LLM-Stats
    - [x] 三段式結構：Part 1 概覽 / Part 2 能力比較 / Part 3 定價方案
    - [x] 封面圖：`ai-models-comparison.png`
    - [x] 瀏覽器驗證通過

---

## 📝 文章規範備忘

> **每篇文章必須包含：**
> 1. 封面圖 (`image:` frontmatter)
> 2. 三段式結構：Part 1 前置 / Part 2 實作 / Part 3 驗收
> 3. 表格使用 Markdown 語法（避免 ASCII 框線）
> 4. **圖片規範**：內文圖片純顯示 `![alt](url)`，不可跳轉
> 5. **連結規範**：使用 `🔗 域名` 格式，放開頭或結尾表格
> 6. 類別和標籤齊全

---

## ⏳ 待處理任務

- [ ] **🌐 域名 typelin.me 設定** (2026-01-04)
    - [x] 域名已轉移至 Cloudflare
    - [ ] 將當前修改提交至 GitHub
    - [ ] 設定 Cloudflare Pages 部署
    - [ ] 配置 DNS 記錄指向網站
    - [ ] 驗證 HTTPS 正常運作

- [ ] 配置 Giscus 評論系統（需創建自己的 GitHub Discussion）
- [ ] 設計贊助頁面內容
- [ ] 添加 TOC 側邊目錄組件
- [ ] 優化行動裝置 RWD 顯示
- [ ] 添加網站搜尋功能
- [ ] 創建更多技術教學文章

---

## 📌 重要資訊

| 項目 | 值 |
|-----|-----|
| 域名 | `typelin.me` |
| DNS 託管 | Cloudflare |
| 原始碼 | GitHub: Typelin/fuwari |
| 框架 | Astro v5.7.9 |
