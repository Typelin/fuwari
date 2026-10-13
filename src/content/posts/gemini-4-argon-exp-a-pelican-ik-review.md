---
title: "Gemini 終於抓回來了？拆包驗證 gemini-3.8-flash-exp-a（Gemini 4 Argon 路由）：檢測方法、三大特徵與鵜鶘單車 2-Bone IK 實測"
published: 2026-10-13
updated: 2026-10-13
description: "自從 Opus 4.6 之後一路掉隊的 Gemini，這次在亞太區灰測抽中 MODEL_PLACEHOLDER_M318（gemini-3.8-flash-exp-a / Gemini 4 Argon 路由）後表現判若兩人。本文整理 Google 放棄 3.5 Pro 直上 Argon 的情報脈絡、本機 SQLite gen_metadata Protobuf 拆包檢測腳本，以及同題「鵜鶘騎自行車 SVG 動畫」的 2-Bone IK 與自動看圖修 Bug 實錄。"
image: "/images/posts/gemini-argon-2026-10/cover-sunset-fish.png"
tags: ["AI 模型", "Gemini 4 Argon", "gemini-3.8-flash-exp-a", "Antigravity", "模型評測", "SVG 動畫", "逆向運動學", "Protobuf"]
category: "💻 技術實戰"
draft: false
---

不得不說一句實話：自從 Claude Opus 4.6 之後，Gemini 在我手上的實戰表現幾乎是一路脫隊。

在 8 月的[《6 個模型跑相同 Prompt 批鬥大會》](/posts/ai-model-wars-2026-08-gemini-grok-deepseek/)裡，Gemini 3.7 Flash 畫出來的鵜鶘雖然顏色漂亮，但輪胎直接飛出畫面外、兩條腿完全不動；到了 9 月的[《TYPELIN ARENA 六模實測展廳》](/posts/typelin-arena-2026-09/)，舊版 Gemini 更因為把題目明令禁止的純黑背景加神經網格全用上，拿到全場墊底的 **61 分**，被我留在展廳裡當負面教材。

結果今天在 Antigravity 裡開工時，我馬上察覺對面的模型不對勁：

1. **思考時間佔比明顯變大**，遇到空間幾何不再秒吐半成品，但遇到簡單指令又能瞬間收斂；
2. **任務完成度極高**，不再以「快速交差」為目標，而是寫完自己跑 Headless 瀏覽器截圖、自己看圖抓出手機版裁切 Bug、修完重驗才交付；
3. **空間物理思維直接躍升**，畫鵜鶘騎單車不再用簡單的 CSS 旋轉糊弄，而是直接手搓 **2-Bone 逆向運動學（IK）** 連桿解算。

拆開本機的會話資料庫一查，果然——帳號已經被路由到 **`MODEL_PLACEHOLDER_M318`（後端實際端點 `gemini-3.8-flash-exp-a`，即社群熱議的 Gemini 4 Argon 灰測路由）**。

![gemini-3.8-flash-exp-a 生成之鵜鶘騎自行車：夕陽主題＋張嘴拋接鮮魚＋單車銅鈴聲波](/images/posts/gemini-argon-2026-10/cover-sunset-fish.png)

*實測畫面：由 `gemini-3.8-flash-exp-a` 生成並經過雙視口自檢修正的《鵜鶘單車海濱巡航》2D SVG 動畫。*

---

## 一、 情報背景：為什麼 Google 放棄 Gemini 3.5 Pro，直接跑 Argon？

如果你最近有追蹤大模型圈的動態，會發現 Google 在 2026 年 9 月底做了一個非常關鍵的戰略轉向：

| 時間節點 / 代號 | 定位與規格重點 | 實務觀察 |
| :--- | :--- | :--- |
| **Gemini 3.5 Pro（中止／跳過）** | 原訂的中期旗艦迭代，因訓練週期拉長與世代定位重疊而直接被繞過 | 避免重蹈「擠牙膏卻打不過競品」的覆轍 |
| **Gemini 3.8 Flash（2026-09-02）** | 日常高頻 Agent 工作流主力，64K 輸出上限，支援動態思考預算（Thinking Levels） | 補齊高速 Coding 與工具呼叫穩定度 |
| **Gemini 4 Argon（2026-09-30 發表）** | Gemini 4 世代首發旗艦架構，支援高達 **100 萬（1M）Output Tokens**，主打長時程（Long-horizon）軟體工程、企業知識工作與自主資安防禦（Fairwind 計畫） | 先針對特定白名單、Google AI Ultra 與開發者通道進行灰度放量 |
| **`gemini-3.8-flash-exp-a`（`M318`）** | Antigravity 內透過佔位符 `MODEL_PLACEHOLDER_M318`（Enum `1318`）路由的 `-exp-a` 實驗端點 | 社群實測對應 Argon 世代的深度推理與完整閉環行為特徵 |

簡單講，Google 終於意識到在長鏈路 Agent 時代，「只會快、卻在複雜幾何與跨檔案工程裡偷工減料」是沒有活路的。跳過 3.5 Pro、直接把資源砸在 Argon 與新一代 Agentic 閉環上，才有了這次體感上的大翻盤。

---

## 二、 網路上的檢測方式：如何從本機 DB 驗明正身？

在 Antigravity 客戶端裡，UI 下拉選單看到的往往只是人類可讀的顯示名稱（例如 `Gemini 3.8 Flash (High)`），或者在新模型正式翻牌前掛在預設的佔位符槽位上。

要確認自己到底有沒有被分流到灰度實驗端點，最準確、零猜測的方法就是**直接以唯讀模式檢查本機會話資料庫 `conversations/*.db` 裡的 `gen_metadata` Protobuf 二進位紀錄**。

### 1. 資料表結構與關鍵 Protobuf 欄位

Antigravity 會在 `%USERPROFILE%\.gemini\antigravity\conversations\<會話ID>.db` 的 `gen_metadata` 表中，把每一輪後端回傳的 Generator Metadata 原封不動存進 `data`（BLOB 欄位，Protobuf Wire Format）：

![SQLite gen_metadata Protobuf 拆包實測結果](/images/posts/gemini-argon-2026-10/gen-metadata-protobuf-inspect.png)

核心驗證欄位共有三個：

| 檢測項目 | Protobuf 路徑（`gen_metadata.data`） | Wire Type | 實測原始值（Raw Value） | 欄位意義 |
| :--- | :--- | :---: | :--- | :--- |
| **實際模型端點 ID** | `field 1.19` | `2` (`string`) | `'gemini-3.8-flash-exp-a'` | 後端伺服器實際回傳並記錄的模型端點名稱 |
| **內部模型列舉名稱** | `field 1.20` (`key='model_enum'`) | `2` (`map<string,string>`) | `'MODEL_PLACEHOLDER_M318'` | 客戶端與後端交握使用的佔位符 Enum 名稱 |
| **內部模型列舉整數** | `field 1.3`、`1.4.1`、`1.17.2.1` | `0` (`varint`) | `1318` | 對應 `M318` 的內部整數編號 |
| **非 Gemini / Claude 標記** | `field 1.20` (`used_claude` 等) | `2` (`map<string,string>`) | `'false'` | 確認非第三方模型轉發，為原生 Gemini 端點 |

### 2. 一鍵唯讀檢測腳本（Python，零外部依賴、不印憑證）

下面這段腳本使用 SQLite 唯讀 URI（`mode=ro`）直接解析最新會話或指定會話的 `gen_metadata`，不需要安裝 `protobuf` 套件，也不會讀取或輸出任何 Token／憑證：

```python
import glob
import os
import sqlite3

def read_varint(buf, pos):
    result, shift = 0, 0
    while True:
        if pos >= len(buf):
            raise ValueError("EOF")
        b = buf[pos]
        pos += 1
        result |= (b & 0x7F) << shift
        if not (b & 0x80):
            return result, pos
        shift += 7

def parse_pb(buf, prefix="", depth=0):
    if depth > 6:
        return []
    pos, items = 0, []
    while pos < len(buf):
        try:
            tag, pos = read_varint(buf, pos)
        except Exception:
            return None
        field_num, wire_type = tag >> 3, tag & 0x7
        if field_num == 0 or field_num > 500000:
            return None
        path = f"{prefix}.{field_num}" if prefix else str(field_num)
        if wire_type == 0:
            val, pos = read_varint(buf, pos)
            items.append((path, "varint", val))
        elif wire_type == 1:
            pos += 8
        elif wire_type == 5:
            pos += 4
        elif wire_type == 2:
            length, pos = read_varint(buf, pos)
            sub = buf[pos : pos + length]
            pos += length
            is_str = False
            try:
                s = sub.decode("utf-8")
                is_str = all(c.isprintable() or c in "\r\n\t" for c in s)
            except Exception:
                pass
            sub_items = parse_pb(sub, path, depth + 1) if sub else []
            if is_str and (not sub_items or all(32 <= b < 127 for b in sub)):
                items.append((path, "str", s))
            elif sub_items:
                items.extend(sub_items)
        else:
            return None
    return items

conv_dir = os.path.expanduser(r"~\.gemini\antigravity\conversations")
latest_db = max(glob.glob(os.path.join(conv_dir, "*.db")), key=os.path.getmtime)

conn = sqlite3.connect(f"file:{latest_db}?mode=ro", uri=True)
cur = conn.cursor()
cur.execute("SELECT idx, size, data FROM gen_metadata ORDER BY idx")

for idx, size, data in cur.fetchall():
    items = parse_pb(data) or []
    endpoint = [v for p, _, v in items if p == "1.19"]
    enum_int = [v for p, _, v in items if p == "1.3"]
    kv, last_k = {}, None
    for p, _, v in items:
        if p == "1.20.1":
            last_k = v
        elif p == "1.20.2" and last_k:
            kv[last_k] = v
            last_k = None
    print(
        f"idx={idx:2d} | 1.19={endpoint} | 1.3={enum_int} "
        f"| model_enum={kv.get('model_enum')} | step={kv.get('last_step_index')}"
    )
```

---

## 三、 實測驗收：同題再戰「鵜鶘騎自行車 SVG 2D 動畫」

驗明正身之後，當然要直接上我們部落格的保留曲目——完全相同的兩行提示詞：

```text
提示詞：給我 HTML，內容是 SVG 繪製一個鵜鶘騎自行車的 2D 動畫。
檔案名稱：你的模型+XXX+.html
```

先看一眼兩個月前 **Gemini 3.7 Flash high** 在同一道題目交出來的車禍現場（輪胎飛出畫面、腳完全不會動）：

![2026 年 8 月 Gemini 3.7 Flash high 鵜鶘騎自行車翻車截圖](/images/posts/model-eval-2026-08/pelican-test-05-gemini-37-flash.png)

再看今天 **`gemini-3.8-flash-exp-a`** 交出來的成品 **`gemini-3.8-flash-exp-a-pelican-on-a-bike.html`** 實際渲染畫面：

![gemini-3.8-flash-exp-a 鵜鶘騎自行車：晴晝海濱巡航模式 (1280x720)](/images/posts/gemini-argon-2026-10/pelican-day-1280x720.png)

*晴晝海濱巡航模式（1280×720 桌面視口）：包含水手單車帽、橘黃大上喙與紅鉤、隨踩踏節奏晃動的彈性大喉囊、車頭藤編菜籃裡的鮮魚、海島燈塔與五層視差捲動背景。*

點下底部控制列的 **「切換夕陽」** 與 **「拋接鮮魚 & 響鈴 (Space)」**：

![gemini-3.8-flash-exp-a 鵜鶘騎自行車：夕陽餘暉＋張嘴拋魚＋單車銅鈴聲波](/images/posts/gemini-argon-2026-10/cover-sunset-fish.png)

*夕陽餘暉模式＋互動彩蛋觸發：按下空白鍵或按鈕時，鵜鶘上喙張開 24°、喉囊下沉，裡面的銀藍色小魚直接從上下喙之間躍起，同時車把上的黃銅車鈴發出金色聲波紋。*

---

## 四、 我注意到的三大核心特徵：為什麼一眼就能認出是 Argon？

這次跟 `gemini-3.8-flash-exp-a` 合作下來，最明顯的改變不是「多背了幾個 API」，而是底層思維模式與工程習慣的三個質變：

### 特徵 1：動態思考預算（Adaptive Thinking）——重型幾何肯長考，簡單指令不囉嗦

以前很多模型要嘛「不管三七二十一先水三大段廢話思考」，要嘛「連座標都沒算就直接硬寫」。

這次在同一個 Session 裡連續觀察 30 多步 `gen_metadata`：
- **遇到 SVG 幾何與連桿動畫時**：思考佔比顯著拉大，在動手寫碼前先把車輪軸心 `(±136, 0)`、輪徑 `R = 68`、五通 `BB = (-8, 8)`、曲柄半徑 `26`、座墊位置 `(-56, -114)` 與大小腿連桿長度 `L1 = L2 = 65` 全部對齊。
- **遇到單純任務時**（例如請它拉取 `https://github.com/morluto/rea` 倉庫或查證本機欄位）：因為路徑明確、無分歧，思考鏈瞬間收斂，直接呼叫 `git clone` 並驗證 `HEAD` commit 與工作樹狀態。中間我一度以為它因為思考變快是不是被後端降級了，結果一查 `gen_metadata` 的 `idx=0..30`，100% 全部穩定維持在 `gemini-3.8-flash-exp-a`。

### 特徵 2：以「完整交付」為主導，而不是「快速交付」——自己看截圖抓 Bug

這是區分「玩具模型」與「真正可用的工程 Agent」的分水嶺。

它在寫出第一版 `gemini-3.8-flash-exp-a-pelican-on-a-bike.html` 後，**沒有立刻宣布完工**，而是自己寫腳本喚起 Headless Chromium，分別用桌面（`1280×720`）和手機直向（`390×844`）視口渲染截圖，並呼叫視覺工具親自檢視畫面。

一看圖，它自己抓出了初版（v1）的兩個視覺缺陷：
1. 初版 SVG 設為 `preserveAspectRatio="xMidYMid slice"`，導致在 `390×844` 手機直向視口下，自行車前後輪外緣與鵜鶘大嘴尖端被左右邊界截斷；
2. 觸發拋魚動畫時，初版上喙只張開 `12°`，但小魚往上跳了 `46px`，導致魚身直接穿過上喙（穿模）。

接著它主動用 `replace_file_content` 補上窄螢幕動態 `viewBox` 計算與 `24°` 張嘴角度，重新跑第二次渲染截圖確認完全修復後，才把結果交給我：

![模型透過 Headless Chromium 自檢看圖修正前後對比（v1 裁切穿模 vs v2 完整閉環）](/images/posts/gemini-argon-2026-10/pelican-mobile-self-fix-compare.png)

*左圖（v1 修正前）：初版在 390×844 窄螢幕下左右車輪與嘴尖被切掉，小魚穿過上喙；右圖（v2 修正後）：模型自己看圖發現問題後，改用動態 `viewBox` 與修正張嘴包絡線，手機直向視口完整呈現且 0 水平溢出。*

### 特徵 3：思維躍升——主動採用 2-Bone 逆向運動學（IK）與次級物理動效

以前測過的大多數雲端模型，在畫自行車踩踏時都會偷懶用簡單的旋轉或前後平移，結果就是腳掌跟踏板永遠對不上，或是膝蓋往後折成骨折鳥。

這次 `gemini-3.8-flash-exp-a` 直接在 JS 渲染迴圈裡實作了標準的 **雙連桿解析逆向運動學（2-Bone Analytical IK）**，即時解算髖關節 `hip` 到踏板 `foot` 的兩圓交點，並強制膝蓋往車頭正方向（`+x`）彎曲：

```javascript
// 2-bone Inverse Kinematics for Pelican legs (Knee bends forward: +x)
function solveKnee(hip, foot, l1, l2) {
  var dx = foot.x - hip.x;
  var dy = foot.y - hip.y;
  var d = Math.hypot(dx, dy);
  var maxReach = l1 + l2 - 0.5;
  if (d > maxReach) d = maxReach;
  if (d < Math.abs(l1 - l2) + 0.5) d = Math.abs(l1 - l2) + 0.5;

  var a = (l1 * l1 - l2 * l2 + d * d) / (2 * d);
  var h = Math.sqrt(Math.max(0, l1 * l1 - a * a));
  var mx = hip.x + (a * dx) / d;
  var my = hip.y + (a * dy) / d;

  // 確保膝關節朝車頭方向 (+x) 前彎
  return {
    x: mx + (h * dy) / d,
    y: my - (h * dx) / d
  };
}
```

除了雙腿 IK 之外，它還主動疊加了多組物理細節：
- **大喉囊相位滯後（Phase Lag）**：喉囊不跟身體死板同步，而是以 `Math.sin(cadence * 2 - 0.65)` 產生肉感十足的延遲晃動與彈性縮放；
- **翅膀握把反向補償**：當身體隨踩踏上下起伏（`bodyBob`）時，翅膀以 `-bodyBob * 0.35` 反向微調角度，讓翼尖穩定扣在復古車把的皮握把上；
- **鏈條與齒盤同步傳動**：上下鏈條透過 `stroke-dashoffset` 與車輪轉角、曲柄角速度嚴格耦合。

---

## 五、 歷代「鵜鶘騎自行車」跨模型實測橫向對比

把這次 `gemini-3.8-flash-exp-a`（Gemini 4 Argon 路由）的表現，放進我們從 8 月一路測到 10 月的「鵜鶘單車名人堂」對照：

| 模型與測試環境 | 腿部運動物理機制 | 場景與互動完成度 | 自檢與視口閉環 | 實戰綜合定性 |
| :--- | :--- | :--- | :--- | :--- |
| **`gemini-3.8-flash-exp-a`（本次 Antigravity / Argon 路由）** | **2-Bone 解析 IK（髖→膝前彎→踏板 + 蹼足傾角同步）** | **5 層海濱視差 + 喉囊拋魚 & 單車響鈴 + 晴晝/夕陽切換 + 3 段變速** | **主動跑 Headless 截圖自檢，修掉手機版裁切與張嘴穿模** | **滿血回歸第一梯隊，工程閉環與物理思維兼具** |
| **本地 `Qwen3.8-27B`（LM Studio 42m 長考）** | **2-Bone 解析 IK** | 7 層海濱視差 + 按住加速 + 吞小魚彩蛋 | 單一桌面視口完整 | 本地小模型長考奇蹟（85 分級別） |
| **本地 `Qwen3.8-Flash-Next 125B`（Strata 91 tok/s）** | 純 SVG SMIL 旋轉動畫（無 JS IK） | 基礎道路捲動，無互動控制列 | 單次直出（2m54s 極速） | 勝在本地 91 tok/s 推論極速 |
| **真 `Grok 4.6 high`（官方 Build 滿血版）** | 同相位旋轉連動 | 海濱公路 + 喉囊探頭小魚 + 多層視差 | 單次桌面端完成 | 雲端旗艦美工與動態標竿 |
| **舊版 `Gemini 3.7 Flash high`（2026-08）** | ❌ **腳完全不動、輪胎飛出畫面** | 靜態配色佳，但動態結構崩潰 | ❌ 未自檢直接交差 | 美工及格、物理與工程閉環不及格 |

---

## 六、 結語：當 Gemini 開始肯算數學、肯自己看圖修 Bug

過去大半年，我對 Gemini 系列最大的抱怨從來不是它生成不夠快，而是它在需要嚴謹空間邏輯與長鏈路工程閉環時總是「差一口氣」——要嘛無視約束亂加料，要嘛寫出半殘動畫就急著收工。

這次在 `MODEL_PLACEHOLDER_M318`（`gemini-3.8-flash-exp-a` / Gemini 4 Argon 路由）上看到的改變非常明確：**它開始願意在幾何與架構問題上花時間深思，願意用數學（2-Bone IK）解決視覺問題，更願意在交付前自己跑瀏覽器看截圖、把窄螢幕裁切和穿模修乾淨才端上桌。**

如果你手上的 Antigravity 帳號也選得到 `Gemini 3.8 Flash (High)`，不妨跑一下上面的 `gen_metadata` 檢測腳本，看看自己是不是也已經坐上了這班 Argon 的灰度列車。

### 延伸連結與相關文章

- [我靠，125B 本地模型跑到 91 tok/s：24GB RTX 5090 Laptop 的 Qwen3.8-Flash-Next 實戰](/posts/qwen38-flash-next-strata-91tps-local-125b/)
- [同一道題，六個模型橫評：我的 AI 實測展廳開張了](/posts/typelin-arena-2026-09/)
- [我癱坐在核彈上！猶如看到椅子爆炸！本地開源模型相同提示詞拉爆各大廠小丑模型](/posts/local-ai-27b-qwen-pelican-masterpiece/)
- [實測！6 個模型跑相同 Prompt：GPT、Gemini、Grok、Deepseek 批鬥大會](/posts/ai-model-wars-2026-08-gemini-grok-deepseek/)
