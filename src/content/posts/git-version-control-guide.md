---
title: "GitHub 入門基礎：Git 版本控制完整指南，從零開始到團隊協作"
published: 2026-01-21
description: "Git 版本控制完整教學，從安裝、基礎指令、分支管理到 GitHub 協作流程，附實戰範例與常見問題解決方案，學生專題必備技能！"
image: "/images/articles/git-guide.png"
tags: ["Git", "版本控制", "開發工具"]
category: "💻 技術實戰"
draft: false
---

## 🚀 Chapter 1：Git 核心基礎

### 🎯 這篇文章適合誰？

- 從沒用過 Git 的完全新手
- 學過但指令常常搞混的人
- 想學會團隊協作流程的學生

---

### 📦 Part 1：安裝與設定

#### Windows 安裝

1. 前往 [git-scm.com](https://git-scm.com/download/win) 下載
2. 一路 Next（預設選項即可）
3. 安裝完成後，打開 **Git Bash** 或 **PowerShell**

#### macOS 安裝

```bash
# 使用 Homebrew
brew install git
```

#### Linux 安裝

```bash
# Ubuntu/Debian
sudo apt install git

# Fedora
sudo dnf install git
```

#### 初次設定（必做！）

安裝完成後，設定你的身份：

```bash
git config --global user.name "你的名字"
git config --global user.email "你的email@example.com"
```

> 💡 這個 email 建議用你的 GitHub 帳號 email，這樣 commit 才會正確連結到你的帳號。

---

### 🔧 Part 2：Git 基礎指令

#### 核心概念圖

```
工作目錄 (Working Directory)
    ↓ git add
暫存區 (Staging Area)
    ↓ git commit
本地儲存庫 (Local Repository)
    ↓ git push
遠端儲存庫 (Remote Repository - GitHub)
```

#### 建立新專案

```bash
# 方法 1：在現有資料夾初始化
cd 你的專案資料夾
git init

# 方法 2：從 GitHub 複製現有專案
git clone https://github.com/使用者/專案名.git
```

#### 日常三連發：add → commit → push

這是你每天會用到的三個指令：

```bash
# 1. 查看目前狀態（養成好習慣，每次操作前先看一下）
git status

# 2. 將修改加入暫存區
git add .                    # 加入所有修改
git add 檔案名稱             # 只加入特定檔案

# 3. 提交到本地儲存庫
git commit -m "簡短描述這次修改"

# 4. 推送到 GitHub
git push origin main
```

#### 查看歷史紀錄

```bash
# 查看提交紀錄
git log --oneline

# 輸出範例：
# a1b2c3d (HEAD -> main) 新增登入功能
# e4f5g6h 修正首頁排版
# i7j8k9l 初始化專案
```

---

## 🌿 Chapter 2：進階分支與團隊協作

### 🌿 Part 3：分支 (Branch) 管理

分支是 Git 最強大的功能之一——你可以在不影響主程式的情況下開發新功能。

#### 分支基礎操作

```bash
# 查看所有分支
git branch

# 建立新分支
git branch feature-login

# 切換到該分支
git checkout feature-login

# 建立 + 切換（一步到位）
git checkout -b feature-login
```

#### 合併分支

開發完成後，把分支合併回主線：

```bash
# 1. 先切回 main
git checkout main

# 2. 合併 feature-login 到 main
git merge feature-login

# 3. 刪除已合併的分支（可選）
git branch -d feature-login
```

#### 分支命名建議

| 類型 | 命名格式 | 範例 |
|------|---------|------|
| 新功能 | `feature-功能名` | `feature-login` |
| 修 Bug | `fix-問題描述` | `fix-header-overflow` |
| 緊急修復 | `hotfix-問題` | `hotfix-security-patch` |

---

### 🤝 Part 4：GitHub 協作流程

#### Fork & Pull Request 流程

這是開源專案最常見的協作方式：

1. **Fork**（複製）別人的專案到你的帳號
2. **Clone** 到本地開發
3. 建立新分支，開始修改
4. **Push** 到你的 Fork
5. 發送 **Pull Request** 請求合併
6. 原作者審核後合併

#### 團隊協作流程

如果你是團隊成員，不需要 Fork：

```bash
# 1. Clone 專案
git clone https://github.com/team/project.git

# 2. 建立你的功能分支
git checkout -b feature-你的功能

# 3. 開發完成後推送
git push origin feature-你的功能

# 4. 在 GitHub 上發送 Pull Request
```

#### 同步遠端更新

團隊協作時，記得經常拉取最新版本：

```bash
# 拉取並合併遠端更新
git pull origin main

# 或者分兩步（更安全）
git fetch origin
git merge origin/main
```

---

### 🎬 Part 4.5：團隊協作實戰演練

這裡模擬幾個學生做專題時最容易遇到的「崩潰現場」，告訴你怎麼優雅解決。

#### 🎭 現場一：「我只想提交一個檔案，不要全部上傳」

**情境**：你改了 `index.html`（新功能完成了），但也順手改了 `App.css`（只是暫時調一下顏色，很亂），這時候如果你 `git add .` 就會把亂七八糟的 code 也傳上去了。

**解法：只 Add 你確定要的檔案**

```bash
# ❌ 不要用這個 (這會全加)
# git add .

# ✅ 用這個 (指定檔案)
git add index.html
git commit -m "feat: 完成首頁排版"
git push origin main
```

> 💡 **為什麼這麼做？** 這叫「原子化提交 (Atomic Commit)」。讓每個 commit 只做一件事，這樣如果 `index.html` 出問題要撤回，才不會連無辜的 `App.css` 一起被撤掉。

#### 🎭 現場二：「Push 失敗！說遠端版本比我的新」

**情境**：你開開心心寫完 code，輸入 `git push`，結果出現紅字：
`error: failed to push some refs to '...'`
`hint: Updates were rejected because the remote contains work that you do not have locally`

**這代表**：你的隊友（或是另一個電腦的你）在你寫 code 的這段時間，已經先 push 了新版本上去。

**解法：先 Pull 再 Push**

1. **先拉取 (Pull)**：把遠端的新程式碼抓下來跟你的合併。
    ```bash
    git pull origin main
    ```
2. **處理合併**：
    - 如果沒有衝突，Git 會自動跳出一個編輯器（通常是 Vim 或 VS Code）要你輸入 commit 訊息。
    - **Vim 苦手請注意**：如果看到畫面凍結，試著輸入 `:wq` (存檔離開)。
    - **建議設定 VS Code**：執行 `git config --global core.editor "code --wait"`，這樣以後編輯訊息會直接開 VS Code，關掉視窗就算存檔完成。
3. **再推送 (Push)**：
    ```bash
    git push origin main
    ```

#### 🎭 現場三：「發生衝突 (Conflict) 了怎麼辦？」

**情境**：承上，當你 `git pull` 的時候，Git 告訴你：
`CONFLICT (content): Merge conflict in index.html`
`Automatic merge failed; fix conflicts and then commit the result.`

**這代表**：你跟隊友剛好改了 **同一個檔案的同一行**，Git 不知道要聽誰的。

**解法：使用 VS Code 手動修復**

1. **打開衝突的檔案** (例如 `index.html`)，你會看到 VS Code 貼心地把衝突標出來：
   - 綠色 `Current Change`：你原本寫的
   - 藍色 `Incoming Change`：隊友寫的

2. **決定留誰的**：
   - 如果你的對，點擊上方小按鈕 **Accept Current Change**
   - 如果隊友對，點擊 **Accept Incoming Change**
   - 都要留，點擊 **Accept Both Changes**

3. **告訴 Git 你修好了**：

    ```bash
    git add index.html
    git commit -m "fix: 解決標題合併衝突"
    git push origin main
    ```

---

## 🛠️ Chapter 3：實戰疑難雜症與規範

### 🆘 Part 5：常見問題與解決方案

#### Q1：不小心 commit 錯了，怎麼撤回？

```bash
# 撤回最後一次 commit，但保留修改
git reset --soft HEAD~1

# 撤回最後一次 commit，丟棄修改（危險！）
git reset --hard HEAD~1
```

#### Q2：改到一半想放棄，回到上次 commit 的狀態？

```bash
# 放棄單一檔案的修改
git checkout -- 檔案名稱

# 放棄所有修改
git checkout -- .
```

#### Q3：Push 被拒絕，說遠端有更新？

```bash
# 先拉取遠端更新
git pull origin main

# 如果有衝突，手動解決後
git add .
git commit -m "解決合併衝突"
git push origin main
```

#### Q4：合併衝突 (Merge Conflict) 怎麼辦？

衝突時，Git 會在檔案中標記：

```
<<<<<<< HEAD
你的修改
=======
別人的修改
>>>>>>> branch-name
```

解決方式：
1. 手動編輯檔案，決定要保留哪個版本
2. 刪除 `<<<<<<`, `======`, `>>>>>>` 標記
3. `git add .` → `git commit`

#### Q5：想忽略某些檔案（如 node_modules）？

建立 `.gitignore` 檔案：

```gitignore
# 依賴目錄
node_modules/
vendor/

# 編譯產物
dist/
build/

# 環境變數
.env
.env.local

# IDE 設定
.vscode/
.idea/

# 系統檔案
.DS_Store
Thumbs.db
```

---

### 📋 Part 6：Commit 訊息規範

好的 commit 訊息能讓歷史紀錄更清晰：

#### 常用前綴

| 前綴 | 用途 | 範例 |
|------|------|------|
| `feat:` | 新功能 | `feat: 新增會員登入功能` |
| `fix:` | 修復 Bug | `fix: 修正手機版選單無法展開` |
| `docs:` | 文件更新 | `docs: 更新 README 安裝說明` |
| `style:` | 程式碼格式 | `style: 統一縮排為 2 空格` |
| `refactor:` | 重構 | `refactor: 優化資料庫查詢效率` |
| `test:` | 測試相關 | `test: 新增登入功能單元測試` |
| `chore:` | 雜項 | `chore: 更新依賴版本` |

#### 範例

```bash
# ✅ 好的 commit 訊息
git commit -m "feat: 新增使用者頭像上傳功能"
git commit -m "fix: 修正 iOS Safari 無法播放影片問題"

# ❌ 不好的 commit 訊息
git commit -m "更新"
git commit -m "修改程式碼"
git commit -m "asdfasdf"
```

---

### 🚀 Part 7：進階技巧

#### Stash：暫存未完成的修改

工作到一半要切換分支？用 stash 暫存：

```bash
# 暫存目前修改
git stash

# 切換分支處理其他事情
git checkout main
# ... 處理完畢 ...
git checkout feature-login

# 取回暫存的修改
git stash pop
```

#### Rebase：整理 commit 歷史

```bash
# 互動式 rebase，整理最近 3 個 commit
git rebase -i HEAD~3
```

#### Cherry-pick：摘取特定 commit

```bash
# 把某個 commit 複製到目前分支
git cherry-pick a1b2c3d
```

---

## 📚 Chapter 4：總結與資源庫

### 📚 推薦資源

| 資源 | 說明 |
|------|------|
| [Pro Git 電子書](https://git-scm.com/book/zh-tw/v2) | 官方免費完整教學 |
| [Learn Git Branching](https://learngitbranching.js.org/) | 互動式視覺化學習 |
| [GitHub Skills](https://skills.github.com/) | GitHub 官方教學 |
| [Oh My Git!](https://ohmygit.org/) | 遊戲化學習 Git |

---

### 💡 速查表

```bash
# 初始化
git init                          # 建立新 repo
git clone <url>                   # 複製遠端 repo

# 日常操作
git status                        # 查看狀態
git add .                         # 加入所有修改
git commit -m "訊息"              # 提交
git push origin main              # 推送
git pull origin main              # 拉取

# 分支
git branch                        # 列出分支
git checkout -b <name>            # 建立並切換分支
git merge <branch>                # 合併分支
git branch -d <name>              # 刪除分支

# 撤回
git reset --soft HEAD~1           # 撤回 commit，保留修改
git checkout -- <file>            # 放棄檔案修改

# 其他
git log --oneline                 # 簡潔歷史
git stash                         # 暫存修改
git stash pop                     # 取回暫存
```

---

> 💡 **小提示**：Git 的學習曲線可能有點陡，但一旦熟悉後，你會發現它是開發過程中不可或缺的好夥伴。先從 `add` → `commit` → `push` 開始練習，其他指令用到再查就好！
