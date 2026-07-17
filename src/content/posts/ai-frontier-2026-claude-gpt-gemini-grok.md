---
title: "2026年中：Claude / GPT / Gemini / Grok 怎麼選？從排行、價格、速度到審查與封號，為什麼我最後用 Super Grok + Grok Build"
published: 2026-07-17
description: "對比 Claude、GPT、Gemini（含 Antigravity）、Grok 在智能、成本、速度、實際用量與審查；說明為何主力選 Super Grok + Grok Build。"
image: "/images/posts/ai-frontier-2026-cover.png"
tags: ["AI 技術", "大語言模型", "技術選型", "Grok", "Antigravity", "開發工具"]
category: "💻 技術實戰"
draft: false
---

只看榜單第一名，很容易以為「最貴、reasoning 拉滿」就是答案。  
真正寫專案、跑 agent、改一整個 repo 時，我更在意：**智能夠不夠用、成本扛不扛得住、回得快不快、會不會動不動拒答或砍方案**。

本文對比 **Claude、GPT、Gemini（含 Antigravity）、Grok**，並說明為什麼我把主力放在 **Super Grok + Grok Build**。

---

# 一、先看總表

## 1.1 五項一次對齊

數字取公開榜與報導的**量級**，再疊使用體感。榜會動，重點看相對位置。

| 項目 | Claude | GPT | Gemini | Grok |
|------|--------|-----|--------|------|
| **智能（排行）** | 常居頂或貼頂（Fable／Opus 區） | 頂～次頂（5.6 Sol 等） | 強，尖端常略後 | 近前沿（4.5 high ≈ 54 檔） |
| **成本** | 高（尤其 Opus／Fable） | 中高 | 中（帳號／Credits 另計） | **偏低** |
| **速度** | 中～偏慢（深思時） | 中 | 中～快 | **偏快** |
| **實際使用量（約 $20 級）** | 聊天夠；整天 agent 易見底 | 聊天夠；高峰限速／降智 | 看 Credits；冷卻／加購常見 | **重開發較撐** |
| **審查程度** | 偏嚴 | 中嚴 | 中（常綁政策／帳號） | **相對鬆** |

## 1.2 工具鏈也要算進去

| 廠商 | 能「動手」的產品 |
|------|------------------|
| Claude | Claude Code 等 |
| GPT | Codex／ChatGPT 生態 |
| **Gemini** | **Antigravity**（開發向工作台／配額體系）＋ Workspace |
| Grok | **Grok Build**（改檔、跑指令、接 repo） |

Gemini 不能只當聊天窗看：上了 **Antigravity** 之後，價值在工作流，痛點也常在 **Credits／冷卻**，而不只是 Index 少兩分。

---

# 二、智能（排行）

## 2.1 榜在量什麼

[Artificial Analysis](https://artificialanalysis.ai/) 的 **Intelligence Index** 是多項評測加權後的綜合分；另有 **Coding Agent Index** 專看代理式寫碼與終端任務。

## 2.2 前沿大概長怎樣

| 梯隊 | 代表 | Index 量級 | 備註 |
|------|------|------------|------|
| S | Claude Fable 5 max 類 | ~60 | 榜首區 |
| S− | GPT-5.6 Sol max／xhigh／high | ~56–59 | 緊咬榜首 |
| A+ | Claude Opus 4.8 等 | ~56 | 穩、貴 |
| A | **Grok 4.5 (high)** | **~54** | 近前沿 |
| A− | Gemini 旗艦檔 | 多在 Grok 後 | 生態另算 |

## 2.3 GPT 家族：同一代也要分檔

同一「GPT-5.6」底下還有 Sol／Terra／Luna 等檔位，智力與成本策略不同，不能混成一款。

![GPT-5.6 Sol / Terra / Luna 分檔對照](/images/posts/aa-2026-07/aa-chart-sol-terra-luna.png)

*圖：Artificial Analysis 文章原圖（[GPT-5.6 has landed](https://artificialanalysis.ai/articles/gpt-5-6-has-landed)）。*

## 2.4 智能小結

- **卷面第一**：多半仍在 Claude 最高檔或 GPT-5.6 Sol max。  
- **近前沿又付得起**：Grok 4.5 很常落在甜區。  
- **Gemini**：尖端 Index 未必第一，但接 Antigravity + Google 生態時，決策維度不同。

---

# 三、成本

## 3.1 API 單價量級（$/M tokens）

| 模型族 | Input | Output |
|--------|-------|--------|
| **Grok 4.5** | ~$2 | ~$6 |
| Claude Opus 級 | ~$5 | ~$25 |
| Claude Fable 級 | ~$10 | ~$50 |
| GPT-5.5／5.6 旗艦 | 常見 ~\$5／~\$30 區 | |

## 3.2 任務成本：比單價更接近實戰

跑完一題智力評測要花多少錢，比「標價多少一兆 token」更接近日常。Grok 4.5 多次出現在「智力還行、每任務成本明顯低」的位置。

![Cost per Intelligence Index Task（2026-07-16）](/images/posts/aa-2026-07/aa-cost-per-task-2026-07-16.png)

*圖：Artificial Analysis · Cost per Intelligence Index Task（2026-07-16）。*

## 3.3 訂閱隱形成本

| | Claude | GPT | Gemini | Grok |
|--|--------|-----|--------|------|
| API | 貴 | 中高 | 中 | **低** |
| 訂閱側 | 配額／升級壓力 | 高峰降智 | **Credits／冷卻** | 相對單純 |

API 便宜不等于 Chat 方案好用；agent 回合、長文、高峰限速都會吃掉體感。

---

# 四、速度

## 4.1 輸出速度（tok/s）

公開數據裡，Grok 4.x／4.5 常見落在 **約 80–110 tok/s** 的偏快區。深度 reasoning 還要看**首 token**：有的模型先想很久再吐字。

![Output Speed（2026-07-16）](/images/posts/aa-2026-07/aa-output-speed-2026-07-16.png)

*圖：Artificial Analysis · Output Speed（2026-07-16）。*

## 4.2 Agent 任務耗時

長任務不只看 tok/s，還看回合數與總牆鐘時間。Grok 4.5 在部分 agent 評測上，以較少回合跑完任務的敘事較常見。

![Coding Agent 相關圖](/images/posts/aa-2026-07/aa-chart-coding-agent.png)

*圖：Artificial Analysis · Coding Agent 相關圖表。*

## 4.3 速度小結

| | Claude | GPT | Gemini | Grok |
|--|--------|-----|--------|------|
| 串流輸出 | 中上 | 中上 | 中～快 | **快** |
| 多輪除錯體感 | 穩但可能慢 | 穩 | 看負載 | **少拖** |

---

# 五、實際使用量（約 $20 方案）

## 5.1 為什麼這項比榜更痛

榜首模型若一天只能認真用兩小時，對 side project 等於沒買到生產力。  
「$20 能撐幾小時 agent」往往比 Index 差兩分更關鍵。

## 5.2 體感對照

| 方案族（約 $20/月） | 日常聊天 | 整天 coding agent | 常見痛點 |
|---------------------|----------|-------------------|----------|
| Claude Pro 級 | 夠 | **易見底** | 貴模吃配額兇 |
| ChatGPT Plus 級 | 夠 | 高峰限速 | 有號但慢／降智 |
| Google／Gemini（含 **Antigravity**） | 視 Credits | **Credits 很痛** | 冷卻、加購、方案分級 |
| **Super Grok 級** | 夠 | **較撐** | 外掛生態較少 |

## 5.3 Gemini + Antigravity

- 價值：開發向工作台、接 Google 生態。  
- 風險：配額敘事常變成 **Credits／長冷卻**，workflow 會整條斷。  
- 延伸：[配額與方案變動筆記](/posts/ai-quota-crisis-2026/)。

## 5.4 小結

| | Claude | GPT | Gemini＋Antigravity | Grok |
|--|--------|-----|----------------------|------|
| $20 重開發 | 偏緊 | 不穩 | Credits 風險高 | **相對扛** |

---

# 六、審查程度與服務穩定性

## 6.1 審查

| | Claude | GPT | Gemini | Grok |
|--|--------|-----|--------|------|
| 整體 | **偏嚴** | 中嚴 | 中 | **相對鬆** |
| 常見表現 | 合規強、灰區易擋 | 政策常變 | 帳號／地區綁得深 | 少說教、技術題較順 |

## 6.2 封號／砍配額（比永久 ban 更常見）

常見形態：學生方案砍模型、Pro 改 Credits、低價檔長冷卻。  
結果都是 **workflow 斷掉**。Grok／xAI 訂閱敘事相對單純（Super Grok + 工具面），較少「同一 $20 每季換隱形貨幣」。

## 6.3 分數背後不一樣

智力分相近，不代表「怎麼拿分」一樣：有的更準、有的更會拒答、有的 token 燒得很兇。選模型時要連 **token 效率與拒答風格** 一起看。

![前沿／智力對照相關圖](/images/posts/aa-2026-07/aa-chart-frontier.png)

*圖：Artificial Analysis · 前沿模型對照。*

---

# 七、寫碼 Agent：Claude、GPT、Grok Build、Antigravity

## 7.1 產品對照

| | Claude | GPT | Gemini | Grok |
|--|--------|-----|--------|------|
| Agent 產品 | Claude Code | Codex 等 | **Antigravity** | **Grok Build** |
| 特色 | 穩、貴 | 生態全 | 綁 Google 配額 | 一體化、成本感佳 |

## 7.2 公開敘事

Coding Agent 榜上，GPT-5.6 Sol 在 Codex 常居前列；Grok 4.5 在 **Grok Build** harness 也有並列與成本優勢的說法。重點不是「誰永遠第一」，而是：**你實際用的那個 harness 能不能天天開。**

![Coding Agent 推文節圖](/images/posts/aa-2026-07/aa-x-coding-agent-gpt56.jpg)

*圖：@ArtificialAnlys · Coding Agent Index 相關。*

---

# 八、場景怎麼選

```text
你的主場景？
├─ 合規長文／極穩推理
│    → Claude 高階
├─ 外掛生態、多模態全家桶
│    → GPT
├─ Google 文件／雲／搜尋 + 開發台
│    → Gemini（含 Antigravity，先算清 Credits）
└─ 長時間寫碼 + agent + 要快 + 控成本
     → Grok 4.5 + Grok Build
```

---

# 九、為什麼我最終選 Super Grok + Grok Build

## 9.1 需求：專案要推得完

作品集大改、部落格、本機橋接、多檔重構——  
這種負載下，**配額牆比 Index 差 2 分更致命**。

## 9.2 Super Grok：主腦

1. 近前沿（~54）夠用  
2. 成本量級低於 Opus／Fable／高檔 GPT  
3. 輸出快  
4. 審查少說教  
5. 訂閱用量撐重開發  

## 9.3 Grok Build：手

聊天窗再強也是聊天窗。Build 負責讀 repo、改檔、跑指令、接 git／部署。

```text
Super Grok（腦）+ Grok Build（手）= 可交付的變更
```

## 9.4 若主力只買別家約 $20

| 主力 | 常見結局 |
|------|----------|
| 只 Claude Pro | 文筆香，agent 整天燒爆 |
| 只 ChatGPT Plus | 生態好，高峰與政策不穩 |
| 只 Gemini／Antigravity | 功能多，Credits／冷卻一改就斷 |
| **Super Grok + Build** | 智力讓一檔，**換可預期的量與速度** |

Claude／GPT 仍適合攻堅與特定 harness；  
在 **2026年中、獨立開發者重度寫碼** 前提下，Grok 鏈的總擁有成本（錢 + 時間 + 心理）對我最優。

---

# 十、實務建議

1. 先定場景，再看榜  
2. 把「$20 實際 agent 工時」寫進決策表  
3. 主力 1 + 備援 1  
4. Gemini 若上 Antigravity，先搞懂 Credits／冷卻  
5. 本機模型當保險  
6. 每季重估榜，不要每週為 1 分搬家  

---

# 十一、延伸閱讀

- [Artificial Analysis](https://artificialanalysis.ai/)  
- [GPT-5.6 專文](https://artificialanalysis.ai/articles/gpt-5-6-has-landed)  
- [@ArtificialAnlys](https://x.com/ArtificialAnlys)  
- 站內：[AI 配額筆記](/posts/ai-quota-crisis-2026/) · [較早 LLM 比較](/posts/ai-llm-comparison-guide/)  

---

# 結語

榜首會換，**工時與荷包不會**。

- **Claude／GPT**：智力與 coding harness 常在最尖  
- **Gemini + Antigravity**：Google 生態與開發台，配額邏輯要算進去  
- **Grok 4.5 + Grok Build**：夠強、更快、更便宜、更好聊、用量較扛  

> **Super Grok + Grok Build = 我付得起、用得完、推得動專案的那一套。**

*Typelin · 2026-07-17*
