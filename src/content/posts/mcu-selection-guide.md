---
title: "學生專題 MCU 選用指南：Arduino、ESP32、STM32、Raspberry Pi Pico 完整比較"
published: 2026-01-15
description: "學生專題開發板選用指南，完整比較 Arduino、ESP32、STM32、Raspberry Pi Pico 的記憶體規格、適用場景、知名開源專案，幫你選對開發板！"
image: "/images/articles/mcu-comparison.png"
tags: ["MCU", "Arduino", "ESP32", "STM32", "Raspberry Pi Pico"]
category: "💻 技術實戰"
draft: false
---

# 學生專題 MCU 選用指南

做專題選錯開發板，輕則卡關重寫，重則整個打掉重練。本文整理四大主流 MCU/開發板的規格與適用場景，幫你一次選對！

---

## 🎯 快速選擇指南

| 我想做... | 推薦選擇 |
|-----------|---------|
| 入門學習、簡單感測器 | Arduino Uno |
| IoT、WiFi/藍牙連接 | ESP32 |
| 馬達控制、即時系統 | STM32 |
| 較複雜邏輯、MicroPython | Raspberry Pi Pico |
| 跑 Linux、影像處理 | Raspberry Pi 4/5 |

---

## 📊 規格比較表

<table>
  <thead>
    <tr>
      <th>開發板</th>
      <th>核心</th>
      <th>Flash</th>
      <th>SRAM</th>
      <th>WiFi/BT</th>
      <th>價格 (約)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>Arduino Uno</strong></td>
      <td>ATmega328P (8-bit, 16MHz)</td>
      <td>32 KB</td>
      <td>2 KB</td>
      <td>❌</td>
      <td>NT$200~400</td>
    </tr>
    <tr>
      <td><strong>ESP32</strong></td>
      <td>Xtensa LX6 雙核 (240MHz)</td>
      <td>4 MB+</td>
      <td>520 KB</td>
      <td>✅ WiFi + BT</td>
      <td>NT$150~300</td>
    </tr>
    <tr>
      <td><strong>STM32F103</strong></td>
      <td>ARM Cortex-M3 (72MHz)</td>
      <td>64~128 KB</td>
      <td>20 KB</td>
      <td>❌</td>
      <td>NT$50~150</td>
    </tr>
    <tr>
      <td><strong>STM32F4</strong></td>
      <td>ARM Cortex-M4 (168MHz)</td>
      <td>512 KB~1 MB</td>
      <td>128~192 KB</td>
      <td>❌</td>
      <td>NT$200~500</td>
    </tr>
    <tr>
      <td><strong>Raspberry Pi Pico</strong></td>
      <td>RP2040 雙核 (133MHz)</td>
      <td>2 MB</td>
      <td>264 KB</td>
      <td>❌ (Pico W 有)</td>
      <td>NT$150~250</td>
    </tr>
    <tr>
      <td><strong>Raspberry Pi 4</strong></td>
      <td>ARM Cortex-A72 四核 (1.5GHz)</td>
      <td>SD 卡</td>
      <td>2~8 GB</td>
      <td>✅ WiFi + BT</td>
      <td>NT$1500~3000</td>
    </tr>
  </tbody>
</table>

---

## 🔧 各平台詳細介紹

### Arduino Uno

**適合對象**：完全初學者、基礎電子學習

**優點**：
- 超簡單的 Arduino IDE，上手零門檻
- 海量教學資源與範例程式
- 豐富的擴展板 (Shield) 生態

**缺點**：
- 記憶體極小 (2KB SRAM)，複雜程式跑不動
- 無內建無線功能
- 8-bit 處理速度較慢

**適合專題**：
- LED 燈光控制
- 簡單感測器讀取 (溫濕度、超音波)
- 基礎馬達控制
- 入門級機器人

**知名開源專案**：
- [Grbl](https://github.com/grbl/grbl) - CNC 控制器
- [Marlin](https://github.com/MarlinFirmware/Marlin) - 3D 列印機韌體

---

### ESP32

**適合對象**：IoT 專題、需要無線連接的應用

**優點**：
- 內建 WiFi + 藍牙，免外接模組
- 雙核心處理器，效能強大
- 支援 Arduino / MicroPython / ESP-IDF
- 價格便宜，CP 值超高

**缺點**：
- 電源管理較複雜
- 部分 GPIO 有使用限制
- 深度睡眠喚醒需注意腳位

**適合專題**：
- 智慧家庭 / 家電控制
- 環境監測站 (上傳雲端)
- 藍牙遙控車
- ESP-NOW 無線感測網路
- 網頁伺服器控制

**知名開源專案**：
- [ESPHome](https://esphome.io/) - 智慧家庭整合
- [WLED](https://github.com/Aircoookie/WLED) - LED 燈條控制
- [ESP32-CAM](https://github.com/espressif/esp32-camera) - 網路攝影機

---

### STM32 系列

**適合對象**：進階開發者、需要精準控制的應用

**優點**：
- ARM Cortex-M 核心，工業級穩定性
- 豐富的外設 (ADC、DAC、Timer、PWM)
- 硬體除錯支援完善
- 大量型號可依需求選擇

**缺點**：
- 學習曲線較陡
- 開發環境設定較複雜
- 資源多為英文

**適合專題**：
- 四軸飛行器 (飛控)
- 馬達 FOC 控制
- 數位電源
- 即時訊號處理
- 工業自動化

**知名開源專案**：
- [Betaflight](https://github.com/betaflight/betaflight) - 無人機飛控
- [Marlin 2.0](https://github.com/MarlinFirmware/Marlin) - 3D 列印機 (32-bit 版)
- [SimpleFOC](https://github.com/simplefoc/Arduino-FOC) - 無刷馬達控制

---

### Raspberry Pi Pico

**適合對象**：想用 Python 開發、需要比 Arduino 更多資源

**優點**：
- MicroPython 支援，寫程式更直覺
- 獨特 PIO (可程式化 I/O)，可自訂協議
- 雙核心 + 大 SRAM，跑複雜邏輯沒問題
- 官方文件完整清楚

**缺點**：
- 生態系比 Arduino/ESP32 年輕
- 無內建 WiFi (需選 Pico W)
- ADC 精度一般

**適合專題**：
- USB HID 裝置 (鍵盤/搖桿)
- 自訂通訊協議
- 教學用 Python 專案
- 中等複雜度的控制系統

**知名開源專案**：
- [KMK Firmware](https://github.com/KMKfw/kmk_firmware) - 機械鍵盤韌體
- [PicoVoice](https://github.com/Picovoice/pico-sdk) - 語音辨識

---

### Raspberry Pi 4/5 (單板電腦)

**適合對象**：需要跑完整 Linux、影像處理、AI 推論

**優點**：
- 完整 Linux 系統，可用 Python/C++/Node.js
- 強大運算能力，可跑 ML 模型
- USB、HDMI、Ethernet 完整介面
- 桌面級應用體驗

**缺點**：
- 非即時系統，不適合精準時序控制
- 耗電較大，需穩定電源
- 價格較高
- 開機時間較長

**適合專題**：
- 人臉辨識 / 影像處理
- 機器學習邊緣運算
- 機器人主控 (搭配 MCU 做底層控制)
- 智慧鏡子 / 資訊看板
- 伺服器應用

**知名開源專案**：
- [Home Assistant](https://www.home-assistant.io/) - 智慧家庭中樞
- [OctoPrint](https://octoprint.org/) - 3D 列印機管理
- [RetroPie](https://retropie.org.uk/) - 復古遊戲機

---

## 💡 選擇建議

### 依專題類型選擇

| 專題類型 | 推薦 | 原因 |
|---------|------|------|
| **入門學習** | Arduino Uno | 簡單易學，資源豐富 |
| **IoT / 智慧家庭** | ESP32 | 內建 WiFi，價格便宜 |
| **無人機 / 馬達控制** | STM32 | 精準時序，豐富外設 |
| **USB 裝置開發** | Raspberry Pi Pico | 原生 USB，PIO 彈性大 |
| **影像處理 / AI** | Raspberry Pi 4/5 | 運算能力強，可跑 Linux |

### 依開發語言選擇

| 語言 | 平台 |
|------|------|
| Arduino (C/C++ 簡化版) | Arduino, ESP32, STM32 |
| MicroPython | ESP32, Raspberry Pi Pico |
| Python 3 | Raspberry Pi 4/5 |
| C/C++ (裸機/HAL) | STM32 |

---

## ⚠️ 常見踩坑提醒

1. **Arduino Uno 記憶體不夠**
   - 用 `F()` 巨集把字串放 Flash
   - 避免用 `String` 類別，改用 `char[]`

2. **ESP32 GPIO 踩雷**
   - GPIO 6~11 連接內部 Flash，別用
   - GPIO 34~39 只能輸入，不能輸出

3. **STM32 時鐘設定**
   - 務必用 CubeMX 生成時鐘樹
   - 外設時鐘沒開會完全沒反應

4. **Raspberry Pi 不是即時系統**
   - 精準 PWM 請用 pigpio 或硬體 PWM
   - 毫秒級以下的控制請交給 MCU

---

## 📚 學習資源

| 平台 | 推薦資源 |
|------|---------|
| Arduino | [Arduino 官方教學](https://www.arduino.cc/en/Tutorial/HomePage) |
| ESP32 | [Random Nerd Tutorials](https://randomnerdtutorials.com/) |
| STM32 | [STM32CubeIDE](https://www.st.com/en/development-tools/stm32cubeide.html) |
| Pico | [Raspberry Pi Pico 官方文件](https://www.raspberrypi.com/documentation/microcontrollers/) |

---

> 💡 **小提示**：如果不確定，從 **ESP32** 開始是個好選擇——價格便宜、功能全面、資源豐富，進可 IoT 退可當 Arduino 用！
