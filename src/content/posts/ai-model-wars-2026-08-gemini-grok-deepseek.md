---
title: "實測！6 個模型跑相同 Prompt：誰是野狗誰是豆包？是小男梁還是梁太祖？GPT、Gemini、Grok、Deepseek批鬥大會。"
published: 2026-08-14
updated: 2026-08-14
description: "實測 6 大模型跑相同 Prompt！結合 grok2api 自建中轉與 xAI IP 降智假說（Issue #916/#839）、DeepSeek V4 Pro 評測爭議與定價倒掛，以及 Gemini 3.7 Flash 在日常開發與「鵜鶘騎自行車 SVG 動畫」實戰中的具體表現，提供客觀的性價比選型參考。"
image: "/images/posts/model-eval-2026-08/cover-banner-2026-08.png"
tags: ["AI 模型", "Gemini 3.7", "Grok 4.6", "DeepSeek V4", "grok2api", "模型評測", "技術選型", "Artificial Analysis"]
category: "💻 技術實戰"
draft: false
---

這幾天在自建 `grok2api` 轉發服務，並密集測試新出的 DeepSeek V4 系列與 Google Gemini 3.7 Flash 後，我深刻體會到模型宣傳跑分與實際工程落地之間的巨大斷層。

很多時候，排行榜上的高分並不能直接轉化為日常生產力。真正決定一個模型能否放進開發工作流的，往往是長上下文下的穩定性、是否有隱蔽的風控降階、多輪代碼生成的空間幾何閉環能力，以及調用成本與推論延遲。

本文結合第三方評測機構 [Artificial Analysis](https://artificialanalysis.ai/) 的 Intelligence Index v4.1.1 基準數據、GitHub 專案 Issues 實錄，以及我親自執行的「鵜鶘騎自行車 SVG 2D 動畫」橫向代碼壓測，記錄這波模型變局下的真實實測反饋與工程選型觀察。

---

## 一、 基準數據：Artificial Analysis Intelligence Index v4.1.1

脫離官方宣傳濾鏡後，客觀第三方評測是觀察模型基礎智能的重要參考。根據 Artificial Analysis 於 2026 年 8 月最新公布的 Intelligence Index v4.1.1（綜合納入 GDPval-AA v2、Terminal-Bench v2.1、SciCode 等 9 項嚴苛基準），當前全球主流模型的得分分佈如下：

![Artificial Analysis Intelligence Index v4.1.1 評測排行榜](/images/posts/model-eval-2026-08/aa-intelligence-index-2026-08-14.png)

*數據來源：[Artificial Analysis Intelligence Index (2026-08)](https://artificialanalysis.ai/)*

### 梯隊實力與得分分佈

| 梯隊定位 | 代表模型 | 綜合智能分 (AA Index) | 工程實務定性 |
| :--- | :--- | :---: | :--- |
| **頂級旗艦** | Claude Opus 5 (max)<br>Claude Fable 5<br>GPT-5.6 Sol (max)<br>Grok 4.6 (high)<br>Kimi K3 (max) | 63<br>62<br>61<br>61<br>60 | 適合複雜架構重構與科研推理，但調用成本高且延遲較大。 |
| **主力實戰** | Qwen3.8 Max<br>Muse Spark 1.2 (xhigh)<br>GPT-5.6 Terra (max)<br>Gemini 3.7 Flash (high) | 58<br>57<br>57<br>56 | 性價比與速度的主戰場，Gemini 3.7 Flash 拿到 56 分，成為近期最大亮點。 |
| **爭議與輕量** | DeepSeek V4 Pro 0813 (max)<br>GLM-5.2 (max)<br>GPT-5.6 Luna (max)<br>Motif 3<br>MiniMax-M3 | 53<br>53<br>52<br>47<br>45 | DeepSeek V4 Pro 僅獲 53 分，與 Flash 版本未能拉開實質代差。 |
| **邊緣基座** | Nemotron 3 Ultra<br>Gemini 3.5 Flash-Lite<br>Solar Open2 250B | 38<br>37<br>37 | 僅適合輕量摘要與超低延遲邊緣任務，不建議用於 Agent 開發。 |

![2026 年 8 月主流 AI 模型實測跑分與性價比對比卡片](/images/posts/model-eval-2026-08/aa-eval-benchmark-card.png)

從基準數據來看，有兩個顯著的趨勢：
1. **Gemini 3.7 Flash (High)** 取得了 56 分，直接跨過了 DeepSeek V4 Pro（53 分）與 GPT-5.6 Luna（52 分），緊追第一線大模型。
2. **DeepSeek V4 Pro**（53 分）相比宣傳預期出現顯著落差，並未展現出旗艦級的代差優勢。

---

## 二、 自建 grok2api 與 Grok 4.6/4.5 的「IP 降智」謎題

為了降低 API 成本，許多開發者基於開源專案 [`chenyme/grok2api`](https://github.com/chenyme/grok2api) 搭建了中轉服務，將 xAI 的 Web/Build 接口轉換為標準 OpenAI 格式。

但在使用過程中，大量自建節點的使用者反饋 Grok 4.6 與 4.5 出現了斷崖式降智：基礎邏輯判斷頻繁出錯、代碼遺漏括號、稍微複雜的多檔案上下文直接崩潰。相反地，只要切換至 xAI 官方付費的 Console API，模型輸出又立刻恢復到 61 分的高水準。

GitHub 專案 Issues 記錄了多起具體測試案例：

### 1. Issue #916：Build 渠道基礎邏輯出錯與降階警告

在 [Issue #916](https://github.com/chenyme/grok2api/issues/916) 中，開發者使用 466 個帳號進行測試，發現 Build 渠道的 `grok-4.6` 在回答「9.11 和 9.9 哪個大」時，會間歇性回答成錯誤的 9.11，甚至直接超時。

同時，響應頭中頻繁出現 `X-Grok2api-Compatibility-Warnings: reasoning_encrypted_content_downgraded` 降階警告；而換到 Console 渠道的 `grok-4.5` 連續測試 10 次則全部正確且穩定。

![grok2api GitHub Issue 916 截圖](/images/posts/model-eval-2026-08/github-issue-916-real.png)

*來源：[grok2api Issue #916: Build 渠道 grok-4.6 经 grok2api 调用时间歇性答错简单问题](https://github.com/chenyme/grok2api/issues/916)*

### 2. Issue #839：不返回推理內容的特徵與「畫鵜鶘」壓力測試

在 [Issue #839](https://github.com/chenyme/grok2api/issues/839) 中，社群指出 Build 渠道的顯著降智特徵是「開啟思考但不返回推理內容」，並提出可透過代理重置與住宅 IP 輪換來改善。討論中也提到了社群常用來檢驗代碼物理邏輯的極限測試題目——「SVG 繪製鵜鶘騎自行車 2D 動畫」。

![grok2api GitHub Issue 839 截圖](/images/posts/model-eval-2026-08/github-issue-839-real.png)

*來源：[grok2api Issue #839: 对于 Build/grok-4.5 开启思考但是不返回推理内容强制中断并重试请求](https://github.com/chenyme/grok2api/issues/839)*

### 3. IP 降智現象與分析假說

對於此現象，我們需要客觀區分「已觀察事實」與「推測假說」：

* **已觀察到的事實**：
  1. Build 渠道在特定機房 IP 調用下，輸出質量顯著劣質化，基礎常識出錯率上升。
  2. 響應標頭出現 `reasoning_encrypted_content_downgraded` 等顯式降階警告。
  3. 官方付費 Console API 在相同測試集下保持穩定，未復現該異常。
* **合理推測與工作假說**：
  * xAI 在 Cloudflare 防火牆或 API Gateway 端，針對數據中心 ASN、非瀏覽器環境與高頻調用啟用了動態風控，可能觸發了靜默分流機制，將請求導向較低算力資源的集群或輕量量化模型池。
* **尚未證實的部分**：
  * xAI 後端的具體權重調度算法、是否經過模型裁剪或量化降階，屬於未公開的內部黑盒架構，仍有待官方進一步說明。

**工程建議**：若使用 `grok2api`，建議搭配乾淨住宅代理並控制請求頻率；若為關鍵業務與代碼重構，建議保留官方 Console 通道以確保輸出質量。

---

## 三、 DeepSeek V4 Pro 的評測爭議與定價落差

過去以性價比引領開源浪潮的 DeepSeek，在本次發布的 V4 系列中引發了社群的廣泛質疑。

### 1. 評測 Harness 爭議
在發布初期，官方宣傳材料中標榜 V4 Pro 在多項基準中比肩頂級旗艦。然而在第三方獨立復現時發現：
* 官方測試疑似採用了特製的評測腳手架（Evaluation Harness），包含特定 Prompt 前綴與針對性取樣。
* 當放入標準化的 Terminal-Bench v2.1、SciCode 與 GDPval-AA 測試集時，V4 Pro 在多輪長上下文狀態下的錯誤率明顯上升，最終在 Artificial Analysis 僅獲得 53 分。

### 2. 邊際提升與定價倒掛
* **DSV4 Flash**：綜合得分約 52 分，調用成本低廉。
* **DSV4 Pro (0813)**：綜合得分 53 分，相比 Flash 僅高出 1 分。
* DSV4 Pro 的定價相比 Flash 翻了數倍，且傳出後續將調漲 API 價格的消息。在實際任務中，多付出數倍成本卻只能換來邊際效應極低的提升，導致 V4 Pro 在性價比維度失去競爭力。

---

## 四、 Google Gemini 3.7 Flash 的實際表現

在 2026 年上半年，Gemini 3.5 與 3.6 Flash 因為上下文幻覺與代碼結構遺漏，常被開發者視為僅能用於基礎摘要的輔助工具。

但新推出的 **Gemini 3.7 Flash (High)** 展現出截然不同的水準：

* **56 分的綜合智能**：超越 DeepSeek V4 Pro（53 分）與 GPT-5.6 Luna（52 分），在邏輯推理與結構化代碼生成上有顯著提升。
* **推論速度與吞吐**：實測輸出速度超過 120 tokens/sec，首字延遲（TTFT）低於 200ms。
* **超長上下文與定價優勢**：延續了 1,000,000+ Token 上下文窗口，搭配低廉的定價（輸入約 $0.08 / 1M Tokens）與充足的官方免費額度，非常適合作為日常 Agent Coding 循環的高頻主力引擎。

---

## 五、 實測壓測：六大模型「鵜鶘騎自行車 SVG 動畫」橫向對比

為了檢驗各模型在幾何座標約束、空間物理理解與複雜代碼生成上的真實表現，我們使用社群經典測試題目進行了標準化壓測：

```text
提示詞：給我 HTML，內容是 SVG 繪製一個鵜鶘騎自行車的 2D 動畫。
檔案名稱：你的模型+XXX+.html
```

> **測試環境說明**：本次測試屬於「模型 + Harness / 工具鏈 + 渠道」的實戰綜合考察。其中 GPT-5.6 Sol 運行於 Codex 深度推理體系，其餘模型運行於 DeepSeek Harness 測試環境中，各模型之步驟、思考檔位與上下文快取記錄於各項指標中。

以下依照測試順序，展示六個模型與檔位的實際生成結果：

---

### 1. GPT 5.6 Sol (xhigh / Codex 體系)
* **耗時**：15 分 09 秒
* **實測表現**：腳部有正常旋轉轉動，自行車與鵜鶘的空間結構完整，動畫無 Bug。展現出頂級模型在深度 Reasoning 檔位下優秀的空間物理理解力。

![GPT 5.6 Sol 鵜鶘騎自行車實測截圖](/images/posts/model-eval-2026-08/pelican-test-01-gpt-56-sol.png)

---

### 2. DeepSeek V4 Pro (MAX 思考檔位 / DeepSeek Harness)
* **指標數據**：1 輪 · 2 步 ｜ LLM 7m43s · 工具調用 0s ｜ 首 Token 平均 1.9s · 75 tok/s ｜ 快取命中 48% ｜ 輸入 50.2K tok · 輸出 34.4K tok ｜ 總耗時 7 分 42 秒
* **實測表現**：腳部正常轉動，幾何構造正確無 Bug。在 Max 思考檔位下表現扎實，但耗時與 Token 消耗相比 Flash 版本大幅增加。

![DeepSeek V4 Pro 鵜鶘騎自行車實測截圖](/images/posts/model-eval-2026-08/pelican-test-02-deepseek-v4-pro.png)

---

### 3. Grok 4.6 high (Build 渠道 / DeepSeek Harness)
* **指標數據**：1 輪 · 2 步 ｜ LLM 57.4s · 工具調用 0s ｜ 首 Token 平均 28.2s · 7020 tok/s ｜ 快取命中 45% ｜ 輸入 17.4K tok · 輸出 7.1K tok
* **實測表現**：全是 Bug。生成的 SVG 幾何嚴重錯位，腳部與踏板完全脫節，印證了 Build 渠道遭 xAI 靜默降階分流的現象。

![Grok 4.6 high Build 鵜鶘騎自行車實測截圖](/images/posts/model-eval-2026-08/pelican-test-03-grok-46-build.png)

---

### 4. Grok 4.5 high (Console 渠道 / DeepSeek Harness)
* **指標數據**：1 輪 · 2 步 ｜ LLM 1m47s · 工具調用 0s ｜ 首 Token 平均 3.3s · 83 tok/s ｜ 快取命中 34% ｜ 輸入 24.6K tok · 輸出 8.4K tok
* **實測表現**：腳沒有旋轉轉動，僅呈現前後擺動，且與自行車踏板完全對不上。物理聯動未達到預期。

![Grok 4.5 high Console 鵜鶘騎自行車實測截圖](/images/posts/model-eval-2026-08/pelican-test-04-grok-45-console.png)

---

### 5. Gemini 3.7 Flash high (DeepSeek Harness)
* **指標數據**：1 輪 · 2 步 ｜ LLM 45.7s · 工具調用 0s ｜ 首 Token 平均 21.7s · 5569 tok/s ｜ 快取命中 0% ｜ 輸入 28.9K tok · 輸出 13.1K tok
* **實測表現**：靜態繪製精緻度與色彩表現全場最佳，但存在動畫邏輯 Bug：腳部完全沒有擺動，輪胎直接跑出畫面外。屬於「美工極佳但在高難度單一幾何代碼上物理閉環失敗」的典型案例。

![Gemini 3.7 Flash high 鵜鶘騎自行車實測截圖](/images/posts/model-eval-2026-08/pelican-test-05-gemini-37-flash.png)

---

### 6. DeepSeek V4 Flash Max (DeepSeek Harness)
* **指標數據**：1 輪 · 5 步 ｜ LLM 6m14s · 工具調用 0.1s ｜ 首 Token 平均 0.8s · 119 tok/s ｜ 快取命中 92% ｜ 輸入 113K tok · 輸出 44.1K tok
* **實測表現**：腳部有正常旋轉轉動，畫面幾何正確無 Bug。生成品質完全比肩昂貴的 Pro 版本，展現出極高的性價比。

![DeepSeek V4 Flash 鵜鶘騎自行車實測截圖](/images/posts/model-eval-2026-08/pelican-test-06-deepseek-v4-flash.png)

---

### 鵜鶘壓測橫向對比總結

| 模型與渠道 | 總耗時 / Token 吞吐 | 動畫正確性 (腳部旋轉/踏板) | 靜態繪製美感 | 實務定性 |
| :--- | :--- | :---: | :---: | :--- |
| **GPT 5.6 Sol (xhigh)** | 15分09秒 | 完美正常轉動 | 良好 | 滿血旗艦，結構無 Bug |
| **DeepSeek V4 Pro Max** | 7分42秒 (75 tok/s) | 正常轉動 | 良好 | 成功通過，但成本偏高 |
| **DeepSeek V4 Flash Max** | 6分14秒 (119 tok/s) | 正常轉動 | 良好 | 性價比首選，無 Bug |
| **Gemini 3.7 Flash high** | 45.7秒 (極速) | 輪胎出界 / 腳不動 | 極佳 | 視覺美感佳，動畫物理邏輯有 Bug |
| **Grok 4.5 high (Console)** | 1分47秒 (83 tok/s) | 僅前後擺動 / 對不上 | 普通 | 物理聯動未閉環 |
| **Grok 4.6 high (Build)** | 57.4秒 | 全是 Bug / 嚴重錯位 | 差 | 遭遇 IP 降智分流 |

---

## 六、 2026 年 8 月主流模型性價比天梯

綜合考量廣泛日常開發基準（如 Terminal-Bench、SciCode）、Token 成本、推論延遲與風控穩定性，當前性價比排序為：

$$\text{Gemini 3.7 Flash} > \text{Grok 4.6 (Console / 乾淨 IP)} > \text{DeepSeek V4 Flash} > \text{DeepSeek V4 Pro}$$

> **說明**：Gemini 3.7 Flash 雖然在單一極限 SVG 動畫生成上出現物理閉環 Bug，但憑藉 56 分的綜合基準分數、超高推論速度（120+ tok/s）與極低成本（輸入約 $0.08 / 1M），依然是目前全天候高頻 Agent 開發循環的首選；若需要零誤差的複雜架構與空間幾何任務，則應交由 GPT-5.6 Sol 或 Claude Opus 5。

### 主流模型綜合指標全景表

| 排名 | 模型名稱 | AA 智能分數 (2026.08) | 推論速度 | 調用成本 (輸入 / 1M) | 穩定性與降智風險 | 實務定位 |
| :---: | :--- | :---: | :---: | :---: | :---: | :--- |
| **1** | **Gemini 3.7 Flash** | 56 分 | 極速 (120+ t/s) | 約 $0.08 (官方高額度) | 極低 (官方高額度) | 日常高頻主力首選 |
| **2** | **Grok 4.6 (Console)** | 61 分 | 高速 (85+ t/s) | 官方標準定價 | 低 (官方 Key 滿血) | 深度任務首選 |
| **3** | **Grok 4.6 / 4.5 (grok2api)** | 40~61 分 (視 IP) | 中等 (受限於代理) | 極低 (自建中轉) | 高 (IP 降智與風控嚴重) | 適合低成本實驗，需防降智 |
| **4** | **DeepSeek V4 Flash** | 52 分 | 極速 (110+ t/s) | 約 $0.15 | 低 (官方穩定) | 表現中規中矩，性價比優秀 |
| **5** | **DeepSeek V4 Pro (0813)** | 53 分 | 中速 (45+ t/s) | 偏高 (即將調漲) | 高 (性價比倒掛 / 爭議) | 較 Flash 僅高 1 分，不推薦 |
| **6** | **Claude Opus 5 (Max)** | 63 分 | 中慢速 (30+ t/s) | 約 $15.00 | 低 (品質封頂) | 頂尖架構標竿，高預算專屬 |

---

## 七、 總結與選型建議

大模型競爭已經不再只是單純比拼宣傳參數，實測智能、推論延遲、API 穩定度與定價策略共同決定了一個模型在真實工程場景中的價值。

* **日常 Agent Coding 與腳本開發**：首選 **Gemini 3.7 Flash** 與 **DeepSeek V4 Flash**。52～56 分的智能足以勝任絕大部分日常編程，速度快且成本極低。
* **高難度架構設計與深度推理**：選擇 **Claude Opus 5**、**GPT 5.6 Sol** 或官方 **Grok 4.6 (Console)**。
* **自建轉發服務**：若使用 `grok2api` 等中轉工具，必須搭配乾淨住宅代理與調用間隔控制，避免被 xAI 靜默分流至降階集群。
* **輕量問答與摘要**：優先選擇 **DeepSeek V4 Flash**，避免花費高額溢價在提升微弱的 DSV4 Pro 上。

---

### 參考資料與延伸連結

* **Artificial Analysis 官方評測數據**：[https://artificialanalysis.ai/](https://artificialanalysis.ai/)
* **grok2api 開源專案**：[https://github.com/chenyme/grok2api](https://github.com/chenyme/grok2api)
* **grok2api Issue #916**：[https://github.com/chenyme/grok2api/issues/916](https://github.com/chenyme/grok2api/issues/916)
* **grok2api Issue #839**：[https://github.com/chenyme/grok2api/issues/839](https://github.com/chenyme/grok2api/issues/839)
* **Google DeepMind / Gemini API 官方文檔**：[https://ai.google.dev/](https://ai.google.dev/)
* **xAI 官方開發者平台 (Console)**：[https://console.x.ai/](https://console.x.ai/)
* **DeepSeek 官方開放平台**：[https://platform.deepseek.com/](https://platform.deepseek.com/)
