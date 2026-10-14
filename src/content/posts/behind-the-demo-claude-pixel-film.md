---
title: "我跟 Claude 做了一支動畫短片《幕後》：每一格畫面都是程式碼"
published: 2026-10-15
updated: 2026-10-15
description: "一支 4 分 12 秒的像素動畫短片，沒有用生成影片或生成音樂的工具，每一格畫面、每一個音都是 Claude 寫程式算出來的。這篇放影片，順便聊聊它是怎麼做出來的、前後改了哪六版。"
image: "/images/posts/behind-the-demo-2026-10/thumb.png"
tags: ["Claude", "Claude Code", "像素動畫", "程式化影片", "ESP32", "物聯網", "YouTube"]
category: "💻 技術實戰"
draft: false
---

這幾天跟 Claude 一起做了一支動畫短片，叫《幕後》（Behind the Demo），已經放上 YouTube 了。

<div style="position:relative;padding-bottom:56.25%;height:0;overflow:hidden;border-radius:12px;margin:1rem 0;">
  <iframe src="https://www.youtube-nocookie.com/embed/T5c3rG8xEw4" title="《幕後》Behind the Demo" style="position:absolute;top:0;left:0;width:100%;height:100%;border:0;" loading="lazy" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
</div>

👉 YouTube 連結：[https://youtu.be/T5c3rG8xEw4](https://youtu.be/T5c3rG8xEw4)

劇情是編的，不過做專題做到半夜、最後靠 AI 救回來這種事，我想應該不少人都有經驗 XD
內容就不劇透了，有興趣可以直接看片，下面聊聊它是怎麼做出來的。

---

## 每一格畫面都是程式碼

整支片沒有用生成影片、生成音樂的工具，也沒有手繪。

做法其實很單純：**給程式一個時間點，它就把那一瞬間的畫面畫出來。**
60fps、4 分 12 秒，就是讓程式從第 0 秒畫到最後一秒，一共畫了 **15,120 張**，再接成影片。

同一個時間點畫兩次，結果會一模一樣（我們真的有拿兩次渲染的雜湊值去比），所以要改哪裡就改那段程式，重渲那幾秒就好，不會牽一髮動全身。

幾個比較有趣的部分：

- **畫面**：底層是一張 480×270 的像素畫布，最後放大成 1080p。字用的是開源的像素字型「俐方體 11 號」。
- **筆電**：是自己寫的簡單 3D（光線投射），蓋子開闔是真的在轉，不是把圖片壓扁。這是我念了一次「筆電怎麼那麼扁」之後才重寫的 😂
- **介面**：Claude Code 的視窗、網頁儀表板、手機畫面、Clawd（就是那隻橘色小螃蟹），全部是程式一個像素一個像素畫出來的。
- **配樂跟音效**：用 Python 的 numpy 從聲波開始合成。鼓、弦樂、鐘琴、鍵盤聲、水滴聲，全部從正弦波和雜訊做起。
- **畫面、聲音、字幕讀的是同一份時間軸**：所以按 Enter 的那一下、水流出來的那一刻，聲音都會剛好對上。

![開場：3D 筆電慢慢打開](/images/posts/behind-the-demo-2026-10/lid-3d.png)

*開場的筆電。從斜角繞到正面，這個角度才看得出它有厚度。*

![片中的 Claude Code 介面](/images/posts/behind-the-demo-2026-10/claude-code.png)

*Claude Code 的介面也是程式畫的，狀態列、待辦清單、auto-accept 都有做出來。*

---

## 前後改了六版

一開始只有 120 秒，叫《你是誰？》。後來我一直挑毛病，一路改到現在的版本：

| 版本 | 我念了什麼 | 改了什麼 |
| :--- | :--- | :--- |
| v1 | — | 120 秒，比較像自我介紹 |
| v2 | 想要更有故事、更多實際內容 | 改成一個完整的專題故事，拉到 210 秒 |
| v3 | 筆電太扁、字一半糊一半清楚、音效太重複 | 重寫 3D 筆電；螢幕上的字改成 1:1 直接貼上；音效重做 |
| v4 | 結尾太草率 | 結尾加長 30 秒，改成回家查結果 |
| v5 | 對話太刻意、筆電不用每次都轉、結尾要更像電影 | 對話改自然；加了一段回憶蒙太奇和最後的大字 |
| 定稿 | 音樂最後沒有好好收尾 | 改成一個完整的終止和弦，餘音剛好收在最後一格 |

![展場畫面：網頁儀表板與 Claude 小視窗](/images/posts/behind-the-demo-2026-10/hall-offline.png)

*「字一半糊一半清楚」修好之後的展場畫面。*

我做的事基本上就是出點子、看片、一直念；把每一句意見變成程式碼的是 Claude。
它看不到動態，也聽不到聲音，所以每一版都是先自己量數據（響度、靜音段、字幕閱讀時間、畫面有沒有卡住），再等我看完聽完給意見。這個來回其實滿有意思的。

---

## 最後

做完最大的感覺是：現在很多作品背後，其實都多了一個熬夜陪你的 AI。
就想說做一支片，記錄一下這件事。

![片尾的大字](/images/posts/behind-the-demo-2026-10/ending.png)

如果你也有過那種比賽前一晚的經驗，歡迎到 [YouTube](https://youtu.be/T5c3rG8xEw4) 看完整版，留言跟我說說 🙌

:::note
片中的比賽名稱、組別、得獎名單與網址都是虛構的。
:::
