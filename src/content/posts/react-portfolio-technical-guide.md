---
title: "從零打造現代化個人作品集：React 19 + Three.js 技術實踐"
published: 2026-01-06
description: "深度解析一個結合 Vite、React 19、Three.js 與 Framer Motion 的前端作品集專案，從架構設計到效能優化的完整技術剖析。"
image: "/images/articles/react-portfolio-cover.png"
tags: ["React", "Three.js", "前端開發", "Vite", "Framer Motion"]
category: "技術分享"
---

在這個前端技術日新月異的時代，一個優秀的個人作品集不僅是展示技能的窗口，更是技術實力的直接體現。本文將深度剖析一個基於 **React 19 + Vite** 的現代化作品集專案，從架構設計到動畫實現，完整呈現「前端審美」與「工程實踐」的結合。

> 🔗 線上預覽：[typelin.pages.dev](https://typelin.pages.dev/)

---

## Part 1：技術架構總覽

### 為什麼選擇 Vite 而非 Next.js？

這個專案選擇了 **Vite + React 19** 的純前端架構，而不是更流行的 Next.js。這個選擇背後有明確的考量：

| 考量點 | Vite | Next.js |
|--------|------|---------|
| 構建速度 | ⚡ 極快 (ESBuild) | 較慢 |
| 複雜度 | 輕量 | 全端框架 |
| SEO 需求 | 作品集不需要 SSR | 內建 SSR/SSG |
| 部署 | 純靜態，任意平台 | 需要 Node.js 或 Vercel |

對於純展示型的作品集網站，Vite 的輕量與極速是更優解。

### 專案結構

```
react-portfolio/
├── src/
│   ├── App.tsx              # 主應用入口 + 路由配置
│   ├── components/          # 所有 UI 組件
│   │   ├── Background/      # 背景效果
│   │   ├── 3D/              # Three.js 3D 組件
│   │   └── *.tsx            # 頁面區塊
│   ├── pages/               # 子路由頁面
│   ├── hooks/               # 自定義 Hooks
│   ├── store/               # Zustand 狀態管理
│   └── styles/              # CSS 樣式
└── dist/                    # 構建輸出
```

### 核心依賴

| 類別 | 技術 |
|------|------|
| 框架 | Vite + React 19 |
| 語言 | TypeScript |
| 樣式 | TailwindCSS 3.4 |
| 動畫 | Framer Motion + GSAP |
| 3D | React Three Fiber + Drei |
| 滾動 | Lenis |
| 狀態 | Zustand |
| 路由 | React Router DOM |
| 部署 | Cloudflare Pages |

---

## Part 2：動畫系統深度解析

這個作品集最令人印象深刻的是其流暢的動畫體驗。讓我們逐一拆解其實現方式。

### A) 捲動動畫 — Framer Motion

```tsx
import { motion } from 'framer-motion';

<motion.div
    initial={{ opacity: 0, x: -50 }}
    whileInView={{ opacity: 1, x: 0 }}
    viewport={{ once: true }}
    transition={{ duration: 0.6 }}
>
    {/* 內容 */}
</motion.div>
```

`whileInView` 配合 `viewport={{ once: true }}` 實現「進入視窗時觸發一次」的效果，既優雅又節省效能。

### B) 平滑捲動 — Lenis

```tsx
import Lenis from 'lenis';

useEffect(() => {
    const lenis = new Lenis({ 
        lerp: 0.1,        // 插值係數
        smoothWheel: true  // 滑鼠滾輪平滑
    });
    
    function raf(time: number) {
        lenis.raf(time);
        requestAnimationFrame(raf);
    }
    requestAnimationFrame(raf);
}, []);
```

Lenis 是目前最流行的平滑滾動庫，它使用 `lerp`（線性插值）實現「慣性滾動」效果。

### C) 星空背景 — React Three Fiber

```tsx
import { Canvas, useFrame } from '@react-three/fiber';
import { Points, PointMaterial } from '@react-three/drei';

const TwinklingStars = () => {
    const materialRef = useRef();
    
    useFrame((state) => {
        // 使用 sin 波動實現閃爍效果
        materialRef.current.opacity = 
            0.6 + Math.sin(state.clock.getElapsedTime()) * 0.4;
    });
    
    return (
        <Points>
            <PointMaterial 
                ref={materialRef}
                size={0.002}
                color="#ffffff"
            />
        </Points>
    );
};
```

### D) 純 CSS 銀河效果（效能優化版）

為了在低端設備上也能流暢運行，專案還提供了純 CSS 的銀河背景作為備選：

```tsx
<motion.div
    style={{
        background: 'conic-gradient(from 0deg, transparent, rgba(136,204,255,0.1), transparent)',
    }}
    animate={{ rotate: 360 }}
    transition={{ duration: 60, repeat: Infinity, ease: 'linear' }}
/>
```

使用 `conic-gradient` + `rotate` 動畫，完全不需要 WebGL，效能消耗極低。

---

## Part 3：自定義 Hooks 與 UI 組件

### 完全手工打造的 UI

這個專案**沒有使用任何 UI 組件庫**（如 shadcn/ui），所有視覺效果都是手工實現：

#### 玻璃質感卡片 (Glassmorphism)

```tsx
<div className="bg-zinc-900/80 backdrop-blur-xl border border-white/10 rounded-3xl">
    {/* 內容 */}
</div>
```

#### 發光邊框

```tsx
style={{
    borderColor: item.color,
    boxShadow: `0 0 20px ${item.color}30`
}}
```

### 實用 Hooks 封裝

```tsx
// hooks/useAdvancedEffects.ts

// 1. 滾動動畫 Hook
export const useScrollAnimation = (threshold, exitThreshold) => {
    // 使用 IntersectionObserver 實現
};

// 2. 滑鼠位置追蹤（含節流）
export const useMousePosition = () => {
    // 60fps 節流的 mousemove 監聽
};

// 3. Hover 狀態
export const useHover = () => {
    // 返回 [ref, isHovered]
};

// 4. 視差滾動
export const useParallax = (speed) => {
    // 根據滾動位置計算偏移
};
```

這些 Hooks 遵循**單一職責原則**，可以輕鬆在其他專案中複用。

---

## Part 4：狀態管理與路由

### Zustand — 輕量級狀態管理

```tsx
import { create } from 'zustand';

export type Theme = 'stars' | 'grid' | 'galaxy' | 'random';

export const useStore = create<AppState>((set) => ({
    theme: 'stars',
    setTheme: (theme) => set({ theme }),
    nextTheme: () => set((state) => {
        const themes: Theme[] = ['stars', 'grid', 'galaxy', 'random'];
        const currentIndex = themes.indexOf(state.theme);
        return { theme: themes[(currentIndex + 1) % themes.length] };
    }),
}));
```

相比 Redux，Zustand 的優勢在於：
- 零樣板代碼
- 不需要 Provider 包裹
- 天然支援 TypeScript

### React Router DOM 路由配置

```tsx
import { Routes, Route } from 'react-router-dom';

<Routes>
    <Route path="/" element={<HomePage />} />
    <Route path="/stust" element={<StustResources />} />
    <Route path="/tools/*" element={<ToolsLayout />} />
</Routes>
```

---

## Part 5：效能優化實踐

在有大量動畫的網站中，效能優化至關重要。以下是專案中採用的優化策略：

| 優化技術 | 實現方式 |
|----------|----------|
| 圖片懶加載 | `<img loading="lazy">` |
| 動畫節流 | 60fps 限制的事件監聽 |
| GPU 加速 | 僅使用 `transform` / `opacity` |
| 減少重繪 | 移除高成本的 `blur-3xl` |
| 純 CSS 背景 | Galaxy 使用 `conic-gradient` 取代 Three.js |

### 節流函數實現

```tsx
const throttle = (func, limit) => {
    let inThrottle = false;
    return (...args) => {
        if (!inThrottle) {
            func(...args);
            inThrottle = true;
            setTimeout(() => (inThrottle = false), limit);
        }
    };
};

// 使用
window.addEventListener('scroll', throttle(handleScroll, 16)); // ~60fps
```

---

## Part 6：部署到 Cloudflare Pages

### 配置方式

專案使用標準 Vite 構建，無需複雜的 `wrangler.toml`：

```json
// package.json
{
    "build": "tsc -b && vite build"
}
```

### SPA 路由處理

為了讓 React Router 在 Cloudflare Pages 上正常工作，需要添加 `_redirects` 規則：

```
// public/_redirects
/*  /index.html  200
```

這確保所有路徑都回退到 `index.html`，由前端路由接管。

---

## 總結

這個作品集專案展示了現代前端開發的多個面向：

1. **架構選擇**：根據需求選擇 Vite 而非 Next.js
2. **動畫實現**：Framer Motion + Three.js + Lenis 的組合運用
3. **狀態管理**：Zustand 的輕量化方案
4. **效能意識**：從 GPU 動畫到純 CSS 替代方案的多層次優化
5. **部署實踐**：Cloudflare Pages 的靜態網站部署

希望這篇技術分析能為你的作品集開發提供參考。如果你對任何技術細節有疑問，歡迎留言討論！

---

## 相關資源

| 資源 | 連結 |
|------|------|
| 線上預覽 | [typelin.pages.dev](https://typelin.pages.dev/) |
| Vite 官方文檔 | [vitejs.dev](https://vitejs.dev/) |
| Framer Motion | [framer.com/motion](https://www.framer.com/motion/) |
| React Three Fiber | [r3f.docs.pmnd.rs](https://r3f.docs.pmnd.rs/) |
| Lenis | [github.com/studio-freight/lenis](https://github.com/studio-freight/lenis) |
