---
title: "我癱坐在核彈上！猶如看到椅子爆炸！本地開源模型相同提示詞拉爆各大廠小丑模型"
published: 2026-08-15
updated: 2026-08-15
description: "接續上一篇雲端 6 大模型批鬥大會！實測開源本地端 Qwen3.8-27B 在 LM Studio 上的逆襲：純思考 9 分鐘手搓競賽立體幾何動態二面角極值，並以 2-Bone 逆向運動學（IK）、七層海濱視差、空白鍵加速與吞小魚彩蛋，寫出擊潰雲端大模型的《鵜鶘，踩呀！》互動小遊戲。文內分享 42 分鐘思維鏈，以及 24G 顯卡留顯存打遊戲看 B 站、160k 上下文不爆顯存的實戰設定。"
image: "/images/posts/local-ai-pelican-2026-08/cover.png"
tags: ["AI 模型", "本地模型", "LM Studio", "Qwen 3.8", "DeepSeek", "SVG 動畫", "逆向運動學", "思維鏈", "硬體調優", "開源 AI"]
category: "💻 技術實戰"
draft: false
---

> 💻 **實測電腦配置**：
> * **GPU**：RTX 5090 Mobile（24GB VRAM）
> * **RAM**：64GB DDR5-5600 記憶體
> * **最低門檻**：照這套量化與快取設定，一般 **16G 顯存 + 32G DDR5 記憶體** 也是完全可以順暢玩起來的！

在上一篇文章[《實測！6 個模型跑相同 Prompt：誰是野狗誰是豆包？是小男梁還是梁太祖？GPT、Gemini、Grok、Deepseek批鬥大會。》](/posts/ai-model-wars-2026-08-gemini-grok-deepseek)中，我測了六大主流雲端模型跑「鵜鶘騎自行車 SVG 2D 動畫」的表現。當時戰況慘烈：xAI Grok 4.6 遇到 IP 風控降智導致座標吸回左上角、Gemini 3.7 Flash 畫得漂亮但輪胎直接飛出去、DeepSeek V4 Pro 溢價嚴重但跟 Flash 沒拉開差距。

當時我差點以為，在沒有視覺即時反饋的情況下，純文本 LLM 盲寫空間物理連動代碼是大模型無法逾越的死穴。

結果今天我在本地端使用 **LM Studio** 載入開源的 **Qwen3.8-27B-Uncensored** 跑同一套提示詞，直接看傻了——這顆 27B 的本地模型不僅手搓出毫無 Bug 的 2-Bone 逆向運動學（IK）自行車動畫，還順手解出了一道競賽級立體幾何二面角極值題。

---

## 一、 第一戰：純思考 9 分鐘，手搓高中/競賽級立體幾何極值

為了先摸清本地端在符號代數與空間幾何上的硬邏輯能力，我給本地模型出了一道經典的立體幾何動態翻折題：

> **題目**：  
> 在平面四邊形 $ABCD$ 中，$AB = AC = CD = 1, \angle ADC = 30^\circ, \angle DAB = 120^\circ$。將 $\triangle ACD$ 沿 $AC$ 翻折至 $\triangle ACP$，其中 $P$ 為動點。求二面角 $A-CP-B$ 的餘弦值的最小值。  
> **要求**：不用 Python、不用聯網、不用工具，純思考，告訴我答案。

### 1. 本地模型的解題表現

模型在 LM Studio 中進入深度長考（Thought for 9 minutes 35 seconds），在完全沒用外部代碼執行器的情況下，輸出了完全無瑕疵的幾何代數證明：

```markdown
最小值是：
\boxed{\frac{\sqrt{3}}{3}}

下面給一個純推導：

在 △ACD 中，AC = CD = 1, ∠ADC = 30°，所以 ∠CAD = 30°, ∠ACD = 120°。
又 ∠DAB = 120°，按通常的平面四邊形理解，AC 在 ∠DAB 內，因此：
∠CAB = 120° - 30° = 90°。

取座標：
A = (0, 0, 0), C = (1, 0, 0), B = (0, -1, 0)
D = (3/2, √3/2, 0)

沿 AC 翻折後，令翻折角為 θ，則 P = (3/2, (√3/2)cosθ, (√3/2)sinθ)。
稜為 CP，單位方向向量為 e = (1/2, (√3/2)cosθ, (√3/2)sinθ)。
令 u = √3 cosθ, u ∈ [-√3, √3]。

計算垂直分量投影長度：
|a| = √3/2
|b|² = (7 - 2u - u²) / 4
|b - a|² = 1 - u²/4

由餘弦定理代入得：
cosφ = (3 - u) / (√3 √(7 - 2u - u²))
cos²φ = (3 - u)² / [3(7 - 2u - u²)]

令 H(u) = (3 - u)² / (7 - 2u - u²)，求導得臨界點 u = 1，H(1) = 1。
因此 cos²φ_min = 1/3，二面角餘弦值最小值為：
\boxed{\frac{\sqrt{3}}{3}}
```

### 2. 技術亮點復盤

* **空間座標系降維**：模型精準捕捉到 $\angle CAB = 90^\circ$，迅速以 $A$ 為原點建立三維直角座標系。
* **避開繁瑣法向量外積**：傳統立體幾何求二面角常需要計算兩個半平面的法向量並做點積，運算量極大且極易算錯符號；模型巧妙利用**「向稜線 $CP$ 的垂直投影分量與餘弦定理」**，將問題轉化為單一變數 $u$ 的極值函數 $H(u)$。
* **嚴謹求導與端點驗證**：精確求導得出駐點 $u = 1$，並代入端點 $u = \pm\sqrt{3}$ 驗證邊界，得出嚴謹無誤的 $\frac{\sqrt{3}}{3}$。

一句話總結：**本地端純思考開源模型，在數理硬邏輯上已經完全具備解開奧賽/高考壓軸題的實力。**

---

## 二、 第二戰：代碼空間幾何天花板——《鵜鶘，踩呀！》

如果說數理是基本功，那麼「生成 SVG 鵜鶘騎自行車 2D 動畫」則是考驗模型的幾何空間架構、圖層層次與動態物理連動。

測試用的提示詞完全相同：
```text
提示詞：給我 HTML，內容是 SVG 繪製一個鵜鶘騎自行車的 2D 動畫。
檔案名稱：你的模型+XXX+.html
```

### 1. 回顧：上一篇雲端 6 大模型在同一句 Prompt 下的實測戰況

為了讓大家不用特意切回上一篇文章對照，這裡直接把雲端各大模型跑同一句 Prompt 的實測截圖搬過來：

* **GPT 5.6 Sol（xhigh / Codex 體系）**：腳部有旋轉，空間結構完整無 Bug，滿血旗艦水準。
![GPT 5.6 Sol 鵜鶘騎自行車實測截圖](/images/posts/model-eval-2026-08/pelican-test-01-gpt-56-sol.png)

* **DeepSeek V4 Pro（Max 思考檔位）**：腳部正常轉動無 Bug，但消耗 5 萬 Token、耗時近 8 分鐘。
![DeepSeek V4 Pro 鵜鶘騎自行車實測截圖](/images/posts/model-eval-2026-08/pelican-test-02-deepseek-v4-pro.png)

* **DeepSeek V4 Flash（Max 思考檔位）**：腳部正常轉動，生成質量完全比肩 Pro 版，性價比極高。
![DeepSeek V4 Flash 鵜鶘騎自行車實測截圖](/images/posts/model-eval-2026-08/pelican-test-06-deepseek-v4-flash.png)

* **Gemini 3.7 Flash high**：靜態色彩美感全場最高，但輪胎直接飛出畫面外、腳部完全沒動。
![Gemini 3.7 Flash high 鵜鶘騎自行車實測截圖](/images/posts/model-eval-2026-08/pelican-test-05-gemini-37-flash.png)

* **Grok 4.5 high（Console 渠道）**：腳沒有旋轉只有前後擺動，踏板完全對不上。
![Grok 4.5 high Console 鵜鶘騎自行車實測截圖](/images/posts/model-eval-2026-08/pelican-test-04-grok-45-console.png)

* **Grok 4.6 high（Build 渠道）**：因遭遇 xAI IP 風控降智，生成幾何嚴重錯位，全是 Bug。
![Grok 4.6 high Build 鵜鶘騎自行車實測截圖](/images/posts/model-eval-2026-08/pelican-test-03-grok-46-build.png)

---

### 2. 本地 Qwen3.8-27B 一句 Prompt 的實測成果

看完上面雲端各家的表現，再來看我們本地這顆 27B 模型的輸出：

當我向本地 Qwen3.8-27B 下達完全相同的提示詞後，它長考並跑了 42 分鐘，直接輸出一整段 400+ 行、零外部圖片依賴、單一 HTML 檔打開就能跑的互動小遊戲——**《鵜鶘，踩呀！》**。

![本地 Qwen 3.8 27B 生成之鵜鶘騎自行車實際運行截圖](/images/posts/local-ai-pelican-2026-08/pelican-masterpiece-browser.png)

*實測畫面：在瀏覽器中直接開啟本地 Qwen3.8-27B 產出的 HTML 檔案（歸檔於專案目錄），包含完整貼紙風 UI、七層視差背景、IK 踩踏連桿與即時 HUD 儀表板。*

---

## 三、 完整思維鏈（CoT）解密：代碼是如何在模型「大腦」中構建的？

很多雲端百億甚至千億參數的閉源大模型寫出來全是殘疾與 Bug，而這顆 27B 的本地模型卻能一次性寫出工業級前端動畫。

從導出的完整 Thinking 思維鏈中，可以看到它非常清晰的架構推導：

### 1. 幾何空間與五通高度約束（防止踏板插地）
模型在寫代碼前，先在思維鏈中精確計算了自行車各部件的物理座標：
> *"Wheels: front wheel center (830, 470), rear wheel center (560, 470), radius ~95. Ground at y=565... BB around (655, 462), crank radius 40 — pedal travel from y=422 to 502. Pedal at lowest point: 462+40=502 < 565 ✓."*

它主動驗證了踏板最低點 $502 < 565$（地面），徹底避免了多數模型常犯的「踏板插進柏油路裡」的幾何錯誤。

### 2. 否定純 CSS 動畫，主動上馬 2-Bone 逆向運動學（IK）
多數模型偷懶使用 CSS `@keyframes` 旋轉腿部，導致大腿和踏板永遠各轉各的。Qwen3.8 在思考鏈中果斷否決了這種假動畫：
> *"Technical approach: For legs connected to pedals... to match pedal position exactly you need IK. Alternatively we could compute pedal positions over time with JS and update legs with proper 2-bone IK in a requestAnimationFrame loop — that would be the most accurate and impressive!"*

它在思維鏈中當場推導了 2-Link 關節的幾何餘弦定理：
$$d = \|P - H\|, \quad \cos\theta = \frac{L_1^2 + d^2 - L_2^2}{2 L_1 d}$$
並確定以 $\theta_t = \varphi - \alpha$ 確保膝蓋向車頭方向前彎（$+x$ 正方向），從而在數學上保證了兩條腿 360 度踩踏時關節絕不脫節：

```javascript
/* ── 兩節鏈條 IK：髖 → 膝（前彎）→ 踏板 ── */
function knee(hx, hy, px, py) {
  const dx = px - hx, dy = py - hy;
  let d = Math.hypot(dx, dy);
  d = Math.min(Math.max(d, Math.abs(L2 - L1) + .01), L1 + L2 - .01);
  const a = Math.atan2(dy, dx), c = (L1 * L1 + d * d - L2 * L2) / (2 * L1 * d);
  return [
    hx + L1 * Math.cos(a - Math.acos(Math.max(-1, Math.min(1, c)))),
    hy + L1 * Math.sin(a - Math.acos(Math.max(-1, Math.min(1, c))))
  ];
}
```

### 3. 七層海濱視差景深與自轉光束
模型規劃了完整的圖層渲染順序（Z-Order），構建了從遠及近的 7 層視差滾動：
1. **極遠景**：太陽（42s 緩慢自轉光芒 + 6s 呼吸光暈）+ 遠島
2. **遠景**：海島燈塔（CSS 動態掃掠光束，以 $\pm 18^\circ$ 扇形掃過海面）
3. **中遠景**：雙速海浪（`seaA` 速度 0.38x、`seaB` 速度 0.24x）
4. **中景**：沙岸圓點（0.5x 滾動）
5. **近景**：公路瀝青與白色虛線（1.0x 基準速度）+ 漂浮海鳥與雲朵
6. **主體層**：自行車與鵜鶘（車鏈條 `stroke-dashoffset` 齒輪傳動 + 眨眼動畫）
7. **前景層**：最底部的草叢以 **1.35x 超高速掠過**，營造出強烈的前進感。

### 4. 主動加戲：互動加速與吞小魚彩蛋 🐟
在思維鏈末尾，模型甚至主動提出要加互動彩蛋：
> *"Also 'pouch' can show fish when boosted?! Actually fun: when b>0.6, a small fish appears in pouch (opacity toggle with pop scale)... Pouch rotates so fish rides along ✓ delightful detail."*

```javascript
/* ── 互動：按住畫面 / 空白鍵 → 狂踩加速！ ── */
b += (targetB - b) * Math.min(1, dt * 3.2); // 慣性平滑過渡
const sp = (1 + b * 1.7) * RM;

th   += 7.4 * dt * sp; // 踩踏頻率從 1.2 Hz 飆升至 ~3.0 Hz
dist += 600 * dt * sp;

// 加速彩蛋：喉囊大張並冒出小魚
const fishOn = b > 0.55;
E.fishG.setAttribute('opacity', fishOn ? 1 : 0);
E.fishInner.style.transform = `scale(${fishOn ? 1 : 0.4})`;
```

* **操作反饋**：按住滑鼠或鍵盤空白鍵，踏板轉速瞬間翻倍。
* **速度感拉滿**：車體後方自動浮現動漫式的白色車速破風線（Speedlines），右下角 HUD 儀表板指針飆破 **80+ km/h**，紅色「加速中！」標籤亮起脈動。
* **細節彩蛋**：當車速超過閾值時，鵜鶘因衝刺而把大黃嘴喉囊張開，嘴裡還彈出一隻活蹦亂跳的小藍魚！

![LM Studio 運行 Qwen 3.8 27B 生成代碼截圖](/images/posts/local-ai-pelican-2026-08/lmstudio-qwen-code.png)

*LM Studio 終端生成實錄：Qwen3.8-27B 完整輸出 IK 求解器與多層視差邏輯，無任何截斷或語法錯誤。*

---

## 四、 本地硬體設定：一邊打遊戲看 B 站，一邊背景跑模型

這次實測在 LM Studio 上的生成速度大概是 **每秒 15 個 Tokens (15 tok/s)，總共跑了 42 分鐘**。

為什麼沒有把 RTX 5090 Mobile 的 24G 顯卡拉到全滿速（30~50 tok/s）？

原因很簡單：**因為我就是想要一邊用電腦打遊戲、看 B 站 4K 影片，一邊讓模型在背景慢慢跑**，所以不想把顯卡顯存直接塞滿發熱。

### 1. 混合卸載（GPU + 系統記憶體）
* **具體配置**：模型總共 65 層，我只把 58~60 層卸載到 GPU，剩下少數幾層留在 64G DDR5-5600 記憶體裡。
* **日常體驗**：這樣顯卡隨時留有幾個 GB 的顯存餘量，日常看片、打遊戲完全不卡頓，而且在 160K（16 萬）超大上下文下依然穩健運行、絕不爆顯存。
* **如果要全速跑**：直接 100% 把 65 層全塞進 24G 顯存，生成速度就會飆到 **35~50 tok/s**。

### 2. 模型選型：保留 MTP 推測解碼頭的 Q4_K_M
這次測試使用的模型來自 Hugging Face 開源社群：
* **模型倉庫**：[`JonathanColetti/Qwen3.8-27B-Uncensored-GGUF`](https://huggingface.co/JonathanColetti/Qwen3.8-27B-Uncensored-GGUF)
* **量化規格**：`Q4_K_M`（體積約 16.8 GB）
* **核心優勢**：該版本透過 Heretic 移除了拒絕方向（Abliteration），並且**完美保留並驗證了多 Token 預測頭（MTP, Multi-Token Prediction）**。草稿 Token 命中率約 43.9%，對長代碼生成加速非常有感。

![HuggingFace Qwen3.8 27B Uncensored 模型卡截圖](/images/posts/local-ai-pelican-2026-08/huggingface-qwen38-27b.png)

*模型來源：HuggingFace 上的 JonathanColetti/Qwen3.8-27B-Uncensored-GGUF 模型主頁。*

### 3. 160K 上下文不爆顯存的三大實用設定
1. **`Max Concurrent Predictions` 設為 `1`**：防止 LM Studio 預先為多個請求劃分 4 份顯存空間，直接省下大筆快取空間。
2. **開啟 `Q4_0` KV Cache 快取量化**：將 K 快取與 V 快取由 FP16 轉為 `Q4_0`，顯存體積暴降 75%，推理質量完全無損。
3. **開啟 `Flash Attention` 與 `Unified KV Cache`**：徹底消除長上下文時中間矩陣的顯存平方暴增。

![LM Studio 160K 上下文與 GPU 卸載設定截圖](/images/posts/local-ai-pelican-2026-08/lmstudio-config-panel.png)

*實測 LM Studio 配置面板：上下文長度拉到 160,000 Token、GPU 卸載 58 層、開啟 Unified KV Cache 與批次優化。*

---

## 五、 橫向對比總結：雲端 vs 本地模型實戰天梯

回顧這兩天的全方位實測，實力對比如下：

| 評測維度 | 雲端 Grok 4.6 (Build 渠道) | 雲端 Gemini 3.7 Flash | 雲端 DeepSeek V4 Pro | 本地 Qwen 3.8 27B (LM Studio) |
| :--- | :--- | :--- | :--- | :--- |
| **數理幾何推理** | 基礎常識頻繁出錯 (IP降智) | 良好 | 良好 | **卓越** (純思考 9m 手搓競賽二面角) |
| **幾何代碼物理性** | 差 (肢體分離、座標吸回0,0) | 中 (美工好但動畫有Bug) | 良好 (正常旋轉) | **頂級封神** (2-Bone IK + 7層視差互動) |
| **思維鏈深度** | 常見偷懶跳步、座標幻覺 | 良好但偶有物理斷層 | 扎實但成本昂貴 | **極其嚴謹** (完整推導五通、連桿、彩蛋) |
| **API 穩定度 / 風控** | 極差 (動態分流降階) | 極佳 (官方額度充足) | 普通 (價格即將調漲) | **100% 絕對穩定** (端側離線零風控) |
| **調用成本 / 隱私** | 依賴中轉或付費 Console | 極低成本 | 偏高 | **完全免費 + 留顯存打遊戲** |

---

## 六、 結語：開源本地模型的時代真的來了

這場測試確實刷新了我的認知：
1. **空間物理不是大模型的死穴**：只要提示詞引導與模型推理深度夠，LLM 完全能夠手寫出工業級的逆向運動學（IK）與物理動態方程。
2. **不用迷信雲端大廠光環**：在雲端閉源模型天天面臨風控降階、隱私疑慮、商業調價的今天，一顆調優得當的 **27B 本地開源模型**，配上一張消費級顯卡，在很多複雜工程與幾何代碼任務上已經完全不輸雲端旗艦，甚至能正面反殺。

這次實測的完整幾何推導與純 SVG/JS 空間連動架構已完整記錄於本文，希望對各位在本地端側跑長思維鏈、榨乾顯卡硬體的玩家與開發者有所啟發！

---

### 相關資源與延伸閱讀

* **上一篇評測**：[實測！6 個模型跑相同 Prompt：誰是野狗誰是豆包？GPT、Gemini、Grok、Deepseek批鬥大會](/posts/ai-model-wars-2026-08-gemini-grok-deepseek)
* **Qwen 官方開源庫**：[https://github.com/QwenLM/Qwen2.5](https://github.com/QwenLM/Qwen2.5)
* **JonathanColetti/Qwen3.8-27B-Uncensored-GGUF**：[https://huggingface.co/JonathanColetti/Qwen3.8-27B-Uncensored-GGUF](https://huggingface.co/JonathanColetti/Qwen3.8-27B-Uncensored-GGUF)
* **LM Studio 官方下載**：[https://lmstudio.ai/](https://lmstudio.ai/)
* **2D 逆向運動學 (Inverse Kinematics) 原理參考**：[Fabrik: A fast, iterative solver for the Inverse Kinematics problem](https://www.researchgate.net/publication/220632147_FABRIK_A_fast_iterative_solver_for_the_Inverse_Kinematics_problem)
