---
title: "我靠，125B 本地模型跑到 91 tok/s：24GB RTX 5090 Laptop 的 Qwen3.8-Flash-Next 實戰"
published: 2026-09-29
updated: 2026-09-29
description: "在 RTX 5090 Laptop 24GB + 64GB DDR5 主機上，用 Strata 跑 Qwen3.8-Flash-Next 125B MoE：IQ2_XS、262K context、INT8 KV、MTP、GPU Vision，顯存控制在約 18GB，DSH 實際 SVG 任務一輪顯示 91 tok/s。這篇記錄完整配置、CPU/GPU 混合推理原理與真實使用代價。"
image: "/images/posts/strata-qwen38-2026-09/dsh-91tps.png"
tags: ["本地 AI", "Qwen 3.8", "Qwen3.8-Flash-Next", "Strata", "MoE", "RTX 5090", "DSH", "MTP", "Vision", "硬體調優"]
category: "💻 技術實戰"
draft: false
---

我本來只是想把本地模型接進自己的 DSH 當一個日常供應商。

結果凌晨三點，我盯著右下角那個數字看了幾秒：

**91 tok/s。**

而且這次不是 7B、14B、27B，也不是整顆塞進顯存的小模型。

是 **Qwen3.8-Flash-Next，125B MoE**。

先把原項目寫在前面：這套能把 125B MoE 拆到 **GPU + CPU + RAM + SSD** 協同推理的核心，來自 **[Niko1221/Strata](https://github.com/Niko1221/Strata)**。Strata 本身提供了 Qwen3.8-Flash-Next 的混合 expert 調度、KV streaming、MTP、Vision 與 OpenAI-compatible API；我這次做的是在自己的 RTX 5090 Laptop 環境上把它完整部署起來，再針對 **18GB 顯存預算、21c CPU、262K context、GPU Vision、DSH provider 與 Windows 背景常駐**做實際調整與整合。

所以這篇不是「我自己寫了一個 125B 推理引擎」，而是一次 **Strata 原項目的實機部署與調優紀錄**。模型則是 Qwen 團隊的 **[Qwen3.8-Flash-Next](https://huggingface.co/Qwen/Qwen3.8-Flash-Next)**，本文使用 Strata 支援的 IQ2_XS 量化版本。

![DSH 實測 Qwen3.8-Flash-Next，該輪顯示 91 tok/s](/images/posts/strata-qwen38-2026-09/dsh-91tps.png)

*這一輪是實際在 DSH 裡跑 SVG/HTML 任務。畫面右下角顯示 2 輪 2 步、91 tok/s；同一會話已到 52.7K tok，快取命中 0%。這是這一輪的實測值，不代表所有 context、prompt 都固定 91 tok/s。*

前陣子我才寫過一篇本地 Qwen3.8-27B，在 LM Studio 裡一邊留顯存、一邊慢慢跑到 15 tok/s，最後手搓出一套有 IK 的鵜鶘自行車動畫。

現在同一台電腦，本地模型直接從 **27B 跳到 125B**，而且不是「能跑就算贏」，是真的進入可以拿來工作的速度。

---

## 先講結果：我現在的常駐配置

這台機器是：

| 硬體 / 設定 | 實際配置 |
| --- | --- |
| GPU | RTX 5090 Laptop，24GB VRAM |
| CPU | Intel Core Ultra 9 275HX，24C / 24T |
| RAM | 64GB DDR5-5600 |
| 模型 | Qwen3.8-Flash-Next 125B MoE |
| 量化 | IQ2_XS |
| 推理引擎 | Strata 0.1.19 |
| Context | 262,144 tokens |
| KV | INT8，完整 KV 在 RAM，32K resident window 在 GPU |
| Expert cache | 6800 設定值，實際 7140 slots / 約 9.56 GiB |
| CPU expert pool | 20 workers + host thread，約 21c 參與 |
| MTP | 開啟 |
| Vision | GPU encoder，開啟 |
| 總 VRAM | `nvidia-smi` 實測約 17,805 MiB |
| API | OpenAI-compatible，`127.0.0.1:8080/v1` |
| 前端 / Agent | DSH，`127.0.0.1:3080` |

我刻意沒有讓 Strata 用 `expert-cache auto`。

因為 auto 很兇。前一次它看到顯卡有空間，直接把 expert cache 吃到 **16.65 GiB**，整張 24GB 顯卡最後只剩四百多 MiB，工作管理員看到 23GB+ 顯存佔用。

那對 benchmark 很爽，對「我還想用這台電腦」就不太爽。

最後我把 expert cache 固定下來，再開 GPU Vision，現在 `nvidia-smi` 是大約：

```text
17805 MiB / 24463 MiB
```

也就是模型常駐時控制在 **約 18GB VRAM**，還有六個多 GB 可以留給桌面、瀏覽器、其他 CUDA 工作。

---

## 125B 為什麼塞得進一張 24GB 顯卡？因為它根本不是「全塞 GPU」

這才是 Strata 最有意思的地方。

Qwen3.8-Flash-Next 是 MoE。Strata README 對這顆模型的描述很直白：它有 **24,576 個 experts**，但每產生一個 token，只需要其中 **10 個**。

所以它不做傳統「模型有多大，VRAM 就硬塞多大」那套。

我的這台機器現在大概是這樣分工：

1. **GPU** 放固定權重、MTP、KV resident window，以及最常用的一批熱門 experts。
2. **RAM** 放完整 expert arena；我這版啟動時實測載入約 **33.02 GiB** experts。
3. 路由命中 GPU expert cache 的部分直接由 GPU 算。
4. 沒命中的 expert 由 CPU 從 RAM 計算，而且和 GPU 並行。
5. 262K context 的 INT8 KV 主體放在 RAM，GPU 只保留 32K resident window。

所以這不是「GPU 跑模型、CPU 幫忙搬資料」。

**CPU 真的在算 MoE expert。**

我一開始用預設配置時，Strata 直接開 **23 個 expert-pool workers + 1 個 host thread**，Core Ultra 9 275HX 生成時幾乎穩定 98～99% CPU。

速度很漂亮，但電腦也真的快被它接管。

現在改成：

```text
--pool-workers 20
```

再加 host thread，大約讓 **21 顆核心參與模型計算**，刻意留幾顆給 Windows、Chrome、DSH。至少我還能正常操作電腦，不需要為了多幾個 tok/s 把整台機器變成推理礦機。

---

## 這輪 91 tok/s 是怎麼測到的？直接拿它寫 SVG，不跑空 prompt

我沒有拿一句 `Hello` 然後截最快的數字。

這次直接在 DSH 裡要求模型：

> 給我 HTML，內容是 SVG 繪製一個鵜鶘騎自行車的 2D 動畫。

而且我刻意要求它不要讀 skill、不要產生實體檔案，直接把 code 吐在聊天裡。

它真的給了我完整 HTML + SVG + SMIL 動畫。

![Qwen3.8-Flash-Next 直接輸出完整 HTML / SVG 程式碼](/images/posts/strata-qwen38-2026-09/dsh-code.png)

這個回答在 DSH 裡顯示單次用量約 **34.3K tok**、耗時 **2 分 54 秒**；整個會話到截圖時累計 **52.7K tok**，最下面的即時統計顯示 **91 tok/s**。

把它丟進 HTML Online Viewer，結果不是一坨語法錯誤，而是真的會動：

![Qwen3.8-Flash-Next 生成的鵜鶘騎自行車 SVG 動畫實際畫面](/images/posts/strata-qwen38-2026-09/pelican-svg.png)

它這次走的是 **Pure SVG + SMIL，沒有 JavaScript**，輪子、腿、曲柄、路面虛線都做了同步動畫。視覺完成度沒有我之前那顆 27B 花 42 分鐘做出的互動版那麼瘋，但速度完全是另一個世界。

更離譜的是，我在不同短任務裡看過大約 **68～91 tok/s** 的 DSH 顯示值。也就是說 91 不是我要拿來宣稱「任何情境都 91」，但這台消費級主機確實已經能把 125B MoE 推到一個我會真的拿來寫東西的區間。

---

## 262K context 沒有把顯存炸掉

這點對 Agent 工作流比單純 tok/s 更重要。

目前配置是：

```text
--max-context 262144
--kv int8
--kv-resident 32768
```

Strata 啟動 log 顯示，262K 的完整 KV 大約 **3.09 GiB pinned RAM**，GPU 只保留 32K resident window。

這就是為什麼我可以把 context 開到 262K，而顯存仍然控制在 18GB 左右。

代價也很直接：context 越長、路由越冷，CPU/RAM 參與越多，速度不可能永遠維持短上下文峰值。之前我也看過長 context decode 明顯掉速，所以這篇的 91 tok/s 我只把它當成「真實工作負載裡跑到的漂亮一輪」，不是拿來偽裝整條性能曲線。

---

## 而且現在它能看圖

這次我順手把 Qwen3.8-Flash-Next 的 Vision encoder 也裝上了。

Strata 這邊是 GPU Vision，額外保留約 1GB 多的 VRAM。DSH provider 也改成 `text + image`，所以現在在 DSH 裡可以直接丟圖片給這顆本地模型。

我沒有只看 `/health` 裡的 `images: true` 就算完成，而是實際生成一張純紅色測試圖，從 OpenAI-compatible API 傳進去。模型的 vision reasoning 正確辨識是 solid red square，最後回答：

```text
red
```

所以目前是完整鏈路：

```text
DSH
  ↓ OpenAI-compatible API
Strata :8080
  ├─ Qwen3.8-Flash-Next IQ2_XS
  ├─ MTP
  ├─ GPU Vision
  ├─ 262K INT8 KV streaming
  ├─ GPU hot expert cache
  └─ CPU + RAM cold experts
```

---

## 最有意思的不是 91，而是「這東西現在真的能常駐」

單看數字，91 tok/s 當然很爽。

但我覺得真正跨過門檻的是：這顆 **125B** 模型現在不是我晚上開一次跑 benchmark、跑完就關掉的玩具。

我把它做成了本機 detached service：

```text
127.0.0.1:8080/v1   # Strata
127.0.0.1:3080      # DSH
```

它不掛在某個 terminal，也不依賴 AgentDock 對話存活。Windows 背景直接常駐，DSH 裡把它當普通 provider 選就好。

這件事的體感和「我成功載入 125B」差很多。

成功載入只是 demo。

**能長 context、能看圖、能寫幾萬 token 的 code、速度夠快、還能讓我繼續操作電腦，才開始像工具。**

---

## 當然不是沒有代價

這套配置不是魔法，幾個坑先寫在這：

- **64GB RAM 幾乎是必要條件**。模型啟動後，完整 expert arena 本身就約 33GB，整機 RAM 使用很容易上 50GB。
- **CPU 真的會被打爆**。這不是 GPU-only inference。現在我用 20 workers + host，生成時依然會大量吃 CPU。
- **IQ2_XS 是激進量化**。它換來的是容量和速度，不代表品質等同高 bit 量化或原始權重。
- **91 tok/s 不是全 context 保證值**。prompt、expert cache hit、MTP 接受率、context 長度都會影響速度。
- **Vision 也要吃 VRAM**。我為了讓它能常駐看圖，把總顯存預算抓在約 18GB，而不是讓 expert cache 吞完整張 24GB 卡。

但對我來說這些 trade-off 完全值得。

因為半年前「125B 本地跑在一張筆電 24GB 卡上」聽起來還像硬體行為藝術；現在它已經在我自己的 DSH 裡變成一個可以點選的模型供應商。

而且剛剛真的跑出了 **91 tok/s**。

我得先把這篇發出去，剩下的 benchmark 之後再補。

---

## 相關連結

- [Strata — Niko1221/Strata](https://github.com/Niko1221/Strata)
- [Qwen3.8-Flash-Next — Hugging Face](https://huggingface.co/Qwen/Qwen3.8-Flash-Next)
- [上一篇：本地 Qwen3.8-27B 鵜鶘自行車實戰](/posts/local-ai-27b-qwen-pelican-masterpiece/)

