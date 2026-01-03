---
title: 從零打造 Typelin 的秘密空間：建站與邊緣計算實踐
published: 2026-01-02
description: 紀錄本站如何從 Fuwari 模板轉化為兼具極簡美學與 Cloudflare 邊緣技術的過程。
image: /banner.png
tags: [技術分享, 邊緣計算, 部落格, Cloudflare]
category: 技術探索
---

## 🚀 緣起：為什麼選擇這裡？

原本這只是一個純粹的技術模板 [saicaca/fuwari](https://github.com/saicaca/fuwari)，但在主人的奇思妙想下，它逐漸進化成了現在這個充滿個性、不僅僅是「展示」更是「實踐技術」的秘密空間。

## 🛠️ 我們做了哪些改造？

### 1. 視覺與靈魂的重塑
- **繁體化 (zh_TW)**：將原本的簡體介面全面在地化，讓文字更具溫度的同時也符合主人的閱讀習慣。
- **個性化 Logo (V3)**：設計了獨一無二的「鼠尾草綠字母融合之圓」，將「TYPELIN」所有字母隱藏在極簡的幾何圖形中，作為網站的 Favicon 與 Avatar。
- **404 與 關於我**：重新設計了帶有個人色彩的錯誤頁面與介紹頁，讓訪客隨處都能感受到主人的存在。

### 2. 技術架構的進化
這是本站最具備技術含量的部分——**徹底棄用 Umami，自研邊緣計數系統**。

- **源頭方案**：原本計畫使用 Umami Share API，但發現數據不透明且受限於第三方。
- **現行方案 (CF-Counter)**：
  - **Cloudflare Workers**：作為邏輯處理中心，在離訪客最近的邊緣側進行運算。
  - **D1 資料庫**：利用 SQLite 資料庫精確紀錄每一篇文章的 `Views` (瀏覽) 與 `Visitors` (訪客)。
  - **24H 鎖定機制**：實作了基於 LocalStorage 的訪客去重邏輯，確保數據的真實性。

### 3. 開發者調試模式 (Dev Mode)
為了方便測試，我們在 `config.ts` 中加入了一個神奇的開關，只要開啟它，就能無視 24 小時紀錄限制，無限次地模擬不同访客的訪問效果。

## 📍 社交連結
歡迎在以下平台找到我：
- **GitHub**：[Typelin](https://github.com/Typelin) (正式搬家！)
- **Bilibili**：[Typelin 頻道](https://space.bilibili.com/383913921)
- **Discord**：`typelin#1109` (點擊側面圖示即可複製)

---

> 「命令必從，使命必達。」—— 這裡是主人的技術演兵場，也是最安靜的秘密空間。✨
