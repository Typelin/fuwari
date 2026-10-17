---
title: "我跟 Claude 做了一支動畫短片《幕後》：每一格畫面都是程式碼"
published: 2026-10-15
updated: 2026-10-15
description: "一支 4 分 12 秒的像素動畫短片，沒有用生成影片或生成音樂的工具，每一格畫面、每一個音都是 Claude 寫程式算出來的。這篇放影片，順便聊聊它在技術上是怎麼實現的，以及用到的開源倉庫。"
image: "/images/posts/behind-the-demo-2026-10/thumb.png"
tags: ["Claude", "Claude Code", "像素動畫", "程式化影片", "ESP32", "物聯網", "YouTube"]
category: "💻 技術實戰"
draft: false
---

這幾天跟 Claude 一起做了一支動畫短片，叫《幕後》（Behind the Demo），已經放上 YouTube 了。

👉 YouTube 連結：[https://youtu.be/T5c3rG8xEw4](https://youtu.be/T5c3rG8xEw4)

劇情是編的，不過做專題做到半夜、最後靠 AI 救回來這種事，我想應該不少人都有經驗 XD
內容就不劇透了，有興趣可以直接看片，下面聊聊它是怎麼做出來的。

<div style="position:relative;padding-bottom:56.25%;height:0;overflow:hidden;border-radius:12px;margin:1rem 0;">
  <iframe src="https://www.youtube-nocookie.com/embed/T5c3rG8xEw4" title="《幕後》Behind the Demo" style="position:absolute;top:0;left:0;width:100%;height:100%;border:0;" loading="lazy" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
</div>

---

## 每一格畫面都是程式碼

整支片沒有用生成影片、生成音樂的工具，也沒有手繪。

做法其實很單純：**給程式一個時間點，它就把那一瞬間的畫面畫出來。**
60fps、4 分 12 秒，就是讓程式從第 0 秒畫到最後一秒，一共畫了 **15,120 張**，再接成影片。

同一個時間點畫兩次，結果會一模一樣（我們真的有拿兩次渲染的雜湊值去比），所以要改哪裡就改那段程式，重渲那幾秒就好，不會牽一髮動全身。

幾個比較有趣的部分：

- **畫面**：底層是一張 480×270 的像素畫布，最後放大成 1080p。字用的是開源的像素字型「俐方體 11 號」。
- **筆電**：是自己寫的簡單 3D（光線投射），蓋子開闔是真的在轉，不是把圖片壓扁。
- **介面**：Claude Code 的視窗、網頁儀表板、手機畫面、Clawd（就是那隻橘色小螃蟹），全部是程式一個像素一個像素畫出來的。
- **配樂跟音效**：用 Python 的 numpy 從聲波開始合成。鼓、弦樂、鐘琴、鍵盤聲、水滴聲，全部從正弦波和雜訊做起。
- **畫面、聲音、字幕讀的是同一份時間軸**：所以按 Enter 的那一下、水流出來的那一刻，聲音都會剛好對上。

![開場：3D 筆電慢慢打開](/images/posts/behind-the-demo-2026-10/lid-3d.png)

*開場的筆電。從斜角繞到正面，這個角度才看得出它有厚度。*

![片中的 Claude Code 介面](/images/posts/behind-the-demo-2026-10/claude-code.png)

*Claude Code 的介面也是程式畫的，狀態列、待辦清單、auto-accept 都有做出來。*

---

## 技術上怎麼實現

整條流水線大概是這樣：

```text
timeline.json（全片的時間軸：每一拍發生什麼、每句台詞何時出現）
   │
   ├─▶ 畫面：網頁 Canvas 上的 renderFrame(t)
   │       └─ Playwright 開無頭 Chromium，t = 0, 1/60, 2/60 … 一格一格呼叫
   │          讀出像素 ──▶ 直接用管線送進 FFmpeg 編碼
   │
   ├─▶ 聲音：Python（numpy / scipy）照同一份時間軸合成 → 響度標準化到 -14 LUFS
   │
   └─▶ 字幕：同一份時間軸產生中英文 SRT
                 ↓
          FFmpeg 把畫面、聲音合成 1080p60 的 MP4
```

幾個關鍵做法：

1. **畫面是 t 的純函數**：`renderFrame(t)` 只看時間 t，不記任何狀態。所以可以把全片切成 12 段同時渲染（12 個瀏覽器分頭畫），4 分多鐘的片大約 2 分半就渲完，再無縫接起來。
2. **低解析度畫、最近鄰放大**：所有東西都畫在 480×270 的小畫布上，放大 4 倍輸出，像素邊緣才會方正、不會糊。光影跟漸層用 Bayer 抖動做出色階，維持像素風的質感。
3. **字只用原生字級**：像素字型在非原生大小會缺角，所以大字都是 12px 原生字整數倍放大；筆電螢幕正對鏡頭時，螢幕內容直接 1:1 貼上去，字才會清楚。
4. **3D 筆電**：只有筆電用了一個極簡的透視相機，蓋子、底座、鍵盤都是平面，用光線投射逐像素算出來；螢幕內容是一張貼圖。
5. **聲音全部是合成的**：馬林巴、鐘琴、弦樂、鼓組都是用正弦波疊泛音、雜訊加濾波器做出來，最後過一個前視限幅器，把真峰值壓在 -1.5 dBTP 以下。
6. **用數字代替眼睛和耳朵**：寫程式的 AI 看不到影片動起來、也聽不到聲音，所以每次渲完都會跑一個檢查工具，量畫面有沒有卡住、是不是太暗、響度、靜音段長度、字幕夠不夠時間讀。

![展場畫面：網頁儀表板與 Claude 小視窗](/images/posts/behind-the-demo-2026-10/hall-offline.png)

*展場畫面裡的儀表板、Claude 小視窗、路過的人影，都是同一支 renderFrame(t) 算出來的。*

---

## 用到的開源倉庫

想自己玩玩看程式化影片，可以從這些開始：

| 倉庫 | 用在哪裡 |
| :--- | :--- |
| [alchaincyf/huashu-art-motion](https://github.com/alchaincyf/huashu-art-motion) | 像素動畫引擎的起點（MIT），「網頁畫一格 → 瀏覽器逐格渲染」的架構就是從這裡來的 |
| [ACh-K/Cubic-11](https://github.com/ACh-K/Cubic-11) | 俐方體 11 號，繁中像素字型（SIL OFL 1.1），片中所有中文字 |
| [microsoft/playwright-python](https://github.com/microsoft/playwright-python) | 開無頭瀏覽器、逐格呼叫 renderFrame |
| [FFmpeg/FFmpeg](https://github.com/FFmpeg/FFmpeg) | 把一張張畫面編成 H.264、混音、裁切截圖 |
| [numpy/numpy](https://github.com/numpy/numpy)、[scipy/scipy](https://github.com/scipy/scipy) | 所有樂器與音效的合成、濾波、殘響 |
| [csteinmetz1/pyloudnorm](https://github.com/csteinmetz1/pyloudnorm) | 響度量測，對齊 YouTube 的 -14 LUFS |
| [JohnHeibel/ClaudeAnimationBase](https://github.com/JohnHeibel/ClaudeAnimationBase) | 另一套「讓 Claude 寫動畫」的範本，可以參考 |

這支片本身的原始碼目前還沒公開，整理好之後再放出來。

---

## 最後

做完最大的感覺是：現在很多作品背後，其實都多了一個熬夜陪你的 AI。
就想說做一支片，記錄一下這件事。

![片尾的大字](/images/posts/behind-the-demo-2026-10/ending.png)

如果你也有過那種比賽前一晚的經驗，歡迎到 [YouTube](https://youtu.be/T5c3rG8xEw4) 看完整版，留言跟我說說 🙌

:::note
片中的比賽名稱、組別、得獎名單與網址都是虛構的。
:::
