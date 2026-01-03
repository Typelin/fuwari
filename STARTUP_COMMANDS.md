# Fuwari 部落格專案啟動指令

## 開發環境

### 啟動開發伺服器
```bash
cd d:\Blog
npm run dev
```
開發伺服器將在 `http://localhost:4321/` 運行

### 建構生產版本
```bash
npm run build
```

### 預覽生產版本
```bash
npm run preview
```

---

## 專案資訊

| 項目 | 值 |
|------|-----|
| 框架 | Astro v5.7.9 |
| UI 框架 | Svelte v5.28.2 |
| CSS | TailwindCSS v3.4.17 |
| 套件管理 | pnpm v9.14.4 |

---

## 常用指令

| 指令 | 說明 |
|------|------|
| `npm run dev` | 啟動開發伺服器 (熱重載) |
| `npm run build` | 建構靜態網站 |
| `npm run preview` | 預覽建構結果 |
| `npm run astro` | 執行 Astro CLI |

---

## 注意事項

1. 開發伺服器預設埠號為 `4321`，若被佔用會自動遞增 (如 `4322`)
2. 檔案變更會自動觸發熱重載
3. 若需外部網路存取，使用 `npm run dev -- --host`
