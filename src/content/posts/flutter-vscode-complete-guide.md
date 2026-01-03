---
title: "🚀 Flutter 完整開發環境建置指南 - 從零開始在 VS Code 寫 App"
published: 2026-01-03
description: "一篇超詳細的 Flutter 環境配置教學，包含 Flutter SDK 安裝、Android Studio 設定、VS Code 擴充套件安裝，以及常用指令整理。附帶圖解說明，讓你快速上手跨平台 App 開發！"
image: "/images/articles/flutter-hello-world.png"
tags: ["Flutter", "VS Code", "App開發", "教學", "Android"]
category: "技術探索"
draft: false
---

# Flutter 完整開發環境建置指南

> 🎯 **本篇目標**：帶領你從零開始配置 Flutter 開發環境，在 VS Code 中寫出第一個 App！

Flutter 是 Google 推出的開源跨平台 UI 框架，使用 Dart 語言開發，一套程式碼即可同時編譯 **Android**、**iOS**、**Web**、**桌面應用**。其「Hot Reload」功能讓開發效率大幅提升！

---

# Part 1：前置作業

這個階段我們要準備好所有必要的開發工具。

---

## 📦 1.1 下載與安裝 Flutter SDK

### Step 1: 下載 Flutter

前往 Flutter 官方網站下載最新 Stable 版本：

🔗 [flutter.dev/docs/get-started/install](https://flutter.dev/docs/get-started/install)

### Step 2: 解壓縮到指定路徑

> ⚠️ **重要**：避免放在需要管理員權限的路徑！

**推薦放置位置：**

| 系統 | 建議路徑 |
|------|---------|
| Windows | `C:\src\flutter` 或 `D:\flutter` |
| macOS | `~/development/flutter` |
| Linux | `~/flutter` |

```bash
# 範例：Windows 解壓後的路徑
C:\src\flutter\
├── bin\
├── packages\
├── dev\
└── ...
```

### Step 3: 設定環境變數 PATH

將 Flutter 的 `bin` 資料夾加入系統 PATH：

**Windows：**
1. 搜尋「環境變數」
2. 編輯「系統變數」→「Path」
3. 新增 `C:\src\flutter\bin`

**macOS / Linux：**
```bash
# 編輯 ~/.bashrc 或 ~/.zshrc
export PATH="$PATH:$HOME/flutter/bin"

# 套用變更
source ~/.bashrc
```

---

## 🤖 1.2 Android Studio 安裝與設定

即使你主要使用 VS Code，仍需要 Android Studio 來管理 **Android SDK** 和 **模擬器**。

### Step 1: 下載並安裝

🔗 [developer.android.com/studio](https://developer.android.com/studio)

### Step 2: 安裝時勾選以下元件

在 Setup Wizard 中，確保以下項目被勾選：

```
[✓] Android SDK
[✓] Android SDK Command-line Tools
[✓] Android SDK Build-Tools
[✓] Android SDK Platform-Tools
[✓] Android Emulator
```

![Android Studio Logo](/images/articles/android-studio-logo.svg)

### Step 3: 設定 SDK 元件

1. 開啟 Android Studio
2. 進入 **Settings** → **SDK Manager**
3. 在 **SDK Platforms** 選擇：
   - ✅ Android 14.0 (API 34) 或更新版本
4. 在 **SDK Tools** 確認已安裝：
   - ✅ Android SDK Build-Tools
   - ✅ Android SDK Platform-Tools
   - ✅ Android Emulator
   - ✅ Android SDK Command-line Tools

### Step 4: 安裝 Flutter & Dart 插件

1. **Settings** → **Plugins** → **Marketplace**
2. 搜尋「Flutter」並安裝
3. 這會同時自動安裝 Dart 插件

---

## 💻 1.3 VS Code 設定

VS Code 是輕量級但功能強大的編輯器，非常適合 Flutter 開發！

### Step 1: 安裝 VS Code

🔗 [code.visualstudio.com](https://code.visualstudio.com/)

### Step 2: 安裝必備擴充套件

按 `Ctrl + Shift + X` 開啟擴充套件，安裝以下項目：

| 擴充套件 | 用途 |
|---------|------|
| **Flutter** | 核心開發工具 |
| **Dart** | 語言支援 (自動安裝) |
| **Awesome Flutter Snippets** | 程式碼片段 |
| **Bracket Pair Colorizer** | 括號配色 |
| **Error Lens** | 即時錯誤提示 |

![VS Code Logo](/images/articles/vscode-logo.svg)

### Step 3: 設定 Flutter SDK 路徑

1. 按 `Ctrl + Shift + P` 開啟命令面板
2. 輸入 `Flutter: Change SDK`
3. 選擇你安裝的 Flutter 路徑

---

# Part 2：創建專案

完成前置作業後，接下來建立你的第一個 Flutter 專案！

---

## 🔍 2.1 先用 flutter doctor 檢查環境

這是最重要的一步！`flutter doctor` 會自動檢查你的環境配置。

```bash
flutter doctor
```

**理想輸出：**
```
Doctor summary (to see all details, run flutter doctor -v):
[✓] Flutter (Channel stable, 3.16.5, on Windows 11)
[✓] Windows Version (Installed version of Windows is version 10 or higher)
[✓] Android toolchain - develop for Android devices (Android SDK version 34.0.0)
[✓] Chrome - develop for the web
[✓] Visual Studio - develop Windows apps
[✓] Android Studio (version 2023.1)
[✓] VS Code (version 1.85.1)
[✓] Connected device (2 available)
[✓] Network resources

• No issues found!
```

### 常見問題修復

**❌ Android licenses not accepted：**
```bash
flutter doctor --android-licenses
```
然後一路按 `y` 同意所有授權。

**❌ cmdline-tools 缺失：**
回到 Android Studio → SDK Manager → SDK Tools → 勾選 `Android SDK Command-line Tools`

---

## 🎉 2.2 建立第一個 Flutter 專案

### 方法一：使用命令列

```bash
flutter create my_first_app
cd my_first_app
flutter run
```

### 方法二：使用 VS Code

1. 按 `Ctrl + Shift + P`
2. 輸入 `Flutter: New Project`
3. 選擇 **Application**
4. 選擇儲存位置
5. 輸入專案名稱

---

## 📱 2.3 設定 Android 模擬器

1. 開啟 Android Studio
2. **Tools** → **Device Manager**
3. 點擊 **Create Virtual Device**
4. 選擇裝置類型（推薦：Pixel 6）
5. 選擇系統映像檔（推薦：API 34）
6. 完成建立後點擊 ▶️ 啟動

> 💡 **提示**：若電腦效能允許，開啟 **Hardware Acceleration** 可大幅提升模擬器速度。

---

# Part 3：驗收與常用指令

恭喜完成環境建置！以下是日常開發會用到的指令整理。

---

## ⌨️ 3.1 Flutter 常用指令整理

| 指令 | 用途 |
|------|------|
| `flutter create app_name` | 建立新專案 |
| `flutter run` | 在模擬器/實機執行 |
| `flutter run -d chrome` | 在 Chrome 執行 Web 版 |
| `flutter devices` | 列出可用裝置 |
| `flutter pub get` | 安裝依賴套件 |
| `flutter pub upgrade` | 升級依賴套件 |
| `flutter clean` | 清理建置快取 |
| `flutter build apk` | 打包 Android APK |
| `flutter build ios` | 打包 iOS (需 macOS) |
| `flutter doctor -v` | 詳細環境診斷 |

---

## ⚡ 3.2 Hot Reload vs Hot Restart

| 功能 | 快捷鍵 | 說明 |
|------|--------|------|
| Hot Reload | `r` | 保留狀態，快速更新 UI |
| Hot Restart | `R` | 重啟應用，清除狀態 |

---

## ✅ 3.3 環境建置完成檢查清單

確認你已經擁有：

- ✅ 完整的 Flutter SDK
- ✅ 配置好的 Android Studio 和 SDK
- ✅ 強大的 VS Code 開發環境
- ✅ 可運行的模擬器
- ✅ `flutter doctor` 全部打勾

---

## 🔗 相關資源

| 資源 | 連結 |
|------|------|
| Flutter 官網 | 🔗 [flutter.dev](https://flutter.dev) |
| Flutter 官方教學 | 🔗 [flutter.dev/docs/codelabs](https://flutter.dev/docs/codelabs) |
| Android Studio | 🔗 [developer.android.com/studio](https://developer.android.com/studio) |
| VS Code | 🔗 [code.visualstudio.com](https://code.visualstudio.com/) |

---

> 📝 **作者筆記**：如果這篇文章對你有幫助，歡迎分享給其他也想學 Flutter 的朋友！有任何問題可以透過側邊欄的聯繫方式找到我。
