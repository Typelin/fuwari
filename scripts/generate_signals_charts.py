"""
訊號與系統期末考 - 圖表生成腳本
生成所有題目所需的專業圖表
🌙 深色主題 + 繁體中文 (ZH_TW) 完整支援
"""
import matplotlib.pyplot as plt
import numpy as np
import matplotlib
import matplotlib.font_manager as fm
import os

# =====================================================
# 中文字體設定 - 確保繁體中文正確顯示
# =====================================================
def setup_chinese_font():
    """設定繁體中文字體，優先順序：微軟正黑體 > 微軟雅黑 > 思源黑體"""
    
    # Windows 常見中文字體路徑
    font_candidates = [
        'C:/Windows/Fonts/msjh.ttc',      # 微軟正黑體
        'C:/Windows/Fonts/msjhbd.ttc',    # 微軟正黑體 Bold
        'C:/Windows/Fonts/msyh.ttc',      # 微軟雅黑
        'C:/Windows/Fonts/msyhbd.ttc',    # 微軟雅黑 Bold
        'C:/Windows/Fonts/simsun.ttc',    # 新宋體
        'C:/Windows/Fonts/simhei.ttf',    # 黑體
        'C:/Windows/Fonts/kaiu.ttf',      # 標楷體
    ]
    
    # 嘗試找到可用的字體
    font_path = None
    for path in font_candidates:
        if os.path.exists(path):
            font_path = path
            print(f"✅ 找到中文字體: {path}")
            break
    
    if font_path:
        # 使用找到的字體
        font_prop = fm.FontProperties(fname=font_path)
        plt.rcParams['font.family'] = font_prop.get_name()
        # 也設定為全域使用
        matplotlib.rcParams['font.sans-serif'] = [font_prop.get_name(), 'Microsoft JhengHei', 'Microsoft YaHei', 'SimHei', 'DejaVu Sans']
    else:
        # 備援：使用系統字體名稱
        print("⚠️ 找不到指定字體檔案，嘗試使用系統字體名稱...")
        plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei', 'Microsoft YaHei', 'SimHei', 'DejaVu Sans']
    
    # 確保負號正確顯示
    plt.rcParams['axes.unicode_minus'] = False
    
    return font_path

# 執行字體設定
FONT_PATH = setup_chinese_font()

# 設定輸出目錄
OUTPUT_DIR = "d:/Blog/public/images/articles/"

# =====================================================
# 🌙 深色主題設定
# =====================================================
# 深色背景色系
DARK_BG = '#1a1a2e'           # 主背景色（深紫藍）
DARK_AXES_BG = '#16213e'      # 坐標軸背景
DARK_GRID = '#2d3a4f'         # 網格線
TEXT_COLOR = '#e8e8e8'        # 主要文字顏色
ACCENT_COLORS = {
    'blue': '#4ecdc4',        # 青藍色
    'red': '#ff6b6b',         # 珊瑚紅
    'green': '#51cf66',       # 亮綠色
    'purple': '#b197fc',      # 淡紫色
    'orange': '#ffa94d',      # 橙色
    'yellow': '#ffd43b',      # 黃色
    'pink': '#f783ac',        # 粉紅色
    'cyan': '#66d9ef',        # 青色
}

def setup_dark_style():
    """設定專業深色主題樣式"""
    plt.style.use('dark_background')
    
    # 自訂深色主題
    plt.rcParams.update({
        'figure.facecolor': DARK_BG,
        'axes.facecolor': DARK_AXES_BG,
        'axes.edgecolor': '#4a5568',
        'axes.labelcolor': TEXT_COLOR,
        'axes.titlecolor': TEXT_COLOR,
        'xtick.color': TEXT_COLOR,
        'ytick.color': TEXT_COLOR,
        'text.color': TEXT_COLOR,
        'grid.color': DARK_GRID,
        'grid.alpha': 0.4,
        'grid.linestyle': '--',
        'font.size': 12,
        'axes.titlesize': 14,
        'axes.labelsize': 12,
        'legend.facecolor': DARK_AXES_BG,
        'legend.edgecolor': '#4a5568',
        'legend.fontsize': 10,
        'savefig.facecolor': DARK_BG,
        'savefig.edgecolor': DARK_BG,
    })

# 如果找到字體檔案，創建字體屬性對象供每個圖表使用
if FONT_PATH and os.path.exists(FONT_PATH):
    FONT_PROP = fm.FontProperties(fname=FONT_PATH, size=12)
    FONT_PROP_TITLE = fm.FontProperties(fname=FONT_PATH, size=14, weight='bold')
    FONT_PROP_SMALL = fm.FontProperties(fname=FONT_PATH, size=10)
else:
    FONT_PROP = None
    FONT_PROP_TITLE = None
    FONT_PROP_SMALL = None

def get_font_prop(size=12, bold=False):
    """取得指定大小的字體屬性"""
    if FONT_PATH and os.path.exists(FONT_PATH):
        weight = 'bold' if bold else 'normal'
        return fm.FontProperties(fname=FONT_PATH, size=size, weight=weight)
    return None

# =====================================================
# 第 3 題：正弦訊號的頻譜分析
# =====================================================
def problem3_spectrum():
    """生成第3題的單邊和雙邊頻譜圖"""
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.patch.set_facecolor(DARK_BG)
    
    # 頻率和振幅數據
    freqs_single = [30, 50]
    amps_single = [2, 4]
    phases_single = [45, 180]  # 度
    
    freqs_double = [-50, -30, 30, 50]
    amps_double = [2, 1, 1, 2]  # 雙邊要除以2
    phases_double = [-180, -45, 45, 180]
    
    fp = get_font_prop(12)
    fp_title = get_font_prop(14, bold=True)
    
    # (a) 單邊振幅譜
    ax = axes[0, 0]
    ax.set_facecolor(DARK_AXES_BG)
    markerline, stemlines, baseline = ax.stem(freqs_single, amps_single, linefmt='-', markerfmt='o', basefmt=' ')
    plt.setp(stemlines, color=ACCENT_COLORS['blue'], linewidth=2)
    plt.setp(markerline, color=ACCENT_COLORS['blue'], markersize=10)
    for i, (f, a) in enumerate(zip(freqs_single, amps_single)):
        ax.annotate(f'振幅={a}', (f, a), textcoords="offset points", xytext=(0, 10), ha='center', fontsize=11, color=ACCENT_COLORS['yellow'], fontproperties=fp)
    ax.set_xlabel('頻率 f (Hz)', fontsize=12, fontproperties=fp)
    ax.set_ylabel('振幅', fontsize=12, fontproperties=fp)
    ax.set_title('(a) 單邊振幅頻譜', fontsize=14, fontweight='bold', fontproperties=fp_title)
    ax.set_xlim(0, 70)
    ax.set_ylim(0, 5)
    ax.axhline(y=0, color=TEXT_COLOR, linewidth=0.5)
    ax.grid(True, alpha=0.3)
    
    # (b) 單邊相位譜
    ax = axes[0, 1]
    ax.set_facecolor(DARK_AXES_BG)
    markerline, stemlines, baseline = ax.stem(freqs_single, phases_single, linefmt='-', markerfmt='s', basefmt=' ')
    plt.setp(stemlines, color=ACCENT_COLORS['green'], linewidth=2)
    plt.setp(markerline, color=ACCENT_COLORS['green'], markersize=10)
    for i, (f, p) in enumerate(zip(freqs_single, phases_single)):
        ax.annotate(f'φ={p}°', (f, p), textcoords="offset points", xytext=(0, 10), ha='center', fontsize=11, color=ACCENT_COLORS['yellow'], fontproperties=fp)
    ax.set_xlabel('頻率 f (Hz)', fontsize=12, fontproperties=fp)
    ax.set_ylabel('相位 (度)', fontsize=12, fontproperties=fp)
    ax.set_title('(b) 單邊相位頻譜', fontsize=14, fontweight='bold', fontproperties=fp_title)
    ax.set_xlim(0, 70)
    ax.set_ylim(-30, 220)
    ax.axhline(y=0, color=TEXT_COLOR, linewidth=0.5)
    ax.grid(True, alpha=0.3)
    
    # (c) 雙邊振幅譜
    ax = axes[1, 0]
    ax.set_facecolor(DARK_AXES_BG)
    markerline, stemlines, baseline = ax.stem(freqs_double, amps_double, linefmt='-', markerfmt='o', basefmt=' ')
    plt.setp(stemlines, color=ACCENT_COLORS['cyan'], linewidth=2)
    plt.setp(markerline, color=ACCENT_COLORS['cyan'], markersize=10)
    for i, (f, a) in enumerate(zip(freqs_double, amps_double)):
        ax.annotate(f'{a}', (f, a), textcoords="offset points", xytext=(0, 10), ha='center', fontsize=11, color=ACCENT_COLORS['yellow'])
    ax.set_xlabel('頻率 f (Hz)', fontsize=12, fontproperties=fp)
    ax.set_ylabel('振幅', fontsize=12, fontproperties=fp)
    ax.set_title('(c) 雙邊振幅頻譜（÷2）', fontsize=14, fontweight='bold', fontproperties=fp_title)
    ax.set_xlim(-70, 70)
    ax.set_ylim(0, 3)
    ax.axhline(y=0, color=TEXT_COLOR, linewidth=0.5)
    ax.axvline(x=0, color=ACCENT_COLORS['orange'], linewidth=1, linestyle='--', alpha=0.7)
    ax.grid(True, alpha=0.3)
    
    # (d) 雙邊相位譜
    ax = axes[1, 1]
    ax.set_facecolor(DARK_AXES_BG)
    markerline, stemlines, baseline = ax.stem(freqs_double, phases_double, linefmt='-', markerfmt='s', basefmt=' ')
    plt.setp(stemlines, color=ACCENT_COLORS['pink'], linewidth=2)
    plt.setp(markerline, color=ACCENT_COLORS['pink'], markersize=10)
    for i, (f, p) in enumerate(zip(freqs_double, phases_double)):
        offset = -25 if p < 0 else 10
        ax.annotate(f'{p}°', (f, p), textcoords="offset points", xytext=(0, offset), ha='center', fontsize=11, color=ACCENT_COLORS['yellow'])
    ax.set_xlabel('頻率 f (Hz)', fontsize=12, fontproperties=fp)
    ax.set_ylabel('相位 (度)', fontsize=12, fontproperties=fp)
    ax.set_title('(d) 雙邊相位頻譜（共軛對稱）', fontsize=14, fontweight='bold', fontproperties=fp_title)
    ax.set_xlim(-70, 70)
    ax.set_ylim(-220, 220)
    ax.axhline(y=0, color=TEXT_COLOR, linewidth=0.5)
    ax.axvline(x=0, color=ACCENT_COLORS['orange'], linewidth=1, linestyle='--', alpha=0.7)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}problem3_spectrum.png', dpi=150, bbox_inches='tight', facecolor=DARK_BG)
    plt.close()
    print(f"✅ 已儲存: problem3_spectrum.png")

# =====================================================
# 卷積暖身題：矩形脈衝卷積
# =====================================================
def convolution_warmup():
    """生成矩形脈衝卷積的圖解"""
    fig, axes = plt.subplots(2, 3, figsize=(15, 8))
    fig.patch.set_facecolor(DARK_BG)
    
    fp = get_font_prop(12)
    fp_title = get_font_prop(12, bold=True)
    
    # 上排：原始訊號和翻轉
    # (a) x(τ)
    ax = axes[0, 0]
    ax.set_facecolor(DARK_AXES_BG)
    ax.fill_between([0, 3], 0, 1, alpha=0.6, color=ACCENT_COLORS['blue'])
    ax.plot([0, 0, 3, 3], [0, 1, 1, 0], color=ACCENT_COLORS['blue'], linewidth=2)
    ax.axhline(y=0, color=TEXT_COLOR, linewidth=1)
    ax.axvline(x=0, color=TEXT_COLOR, linewidth=1)
    ax.set_xlim(-1, 5)
    ax.set_ylim(-0.2, 1.5)
    ax.set_xlabel('τ', fontsize=12, fontproperties=fp)
    ax.set_ylabel('x(τ)', fontsize=12, fontproperties=fp)
    ax.set_title('(a) 訊號 x(τ)', fontsize=14, fontweight='bold', fontproperties=fp_title)
    ax.grid(True, alpha=0.3)
    
    # (b) h(τ)
    ax = axes[0, 1]
    ax.set_facecolor(DARK_AXES_BG)
    ax.fill_between([0, 3], 0, 1, alpha=0.6, color=ACCENT_COLORS['red'])
    ax.plot([0, 0, 3, 3], [0, 1, 1, 0], color=ACCENT_COLORS['red'], linewidth=2)
    ax.axhline(y=0, color=TEXT_COLOR, linewidth=1)
    ax.axvline(x=0, color=TEXT_COLOR, linewidth=1)
    ax.set_xlim(-1, 5)
    ax.set_ylim(-0.2, 1.5)
    ax.set_xlabel('τ', fontsize=12, fontproperties=fp)
    ax.set_ylabel('h(τ)', fontsize=12, fontproperties=fp)
    ax.set_title('(b) 訊號 h(τ)', fontsize=14, fontweight='bold', fontproperties=fp_title)
    ax.grid(True, alpha=0.3)
    
    # (c) h(-τ) 翻轉
    ax = axes[0, 2]
    ax.set_facecolor(DARK_AXES_BG)
    ax.fill_between([-3, 0], 0, 1, alpha=0.6, color=ACCENT_COLORS['red'])
    ax.plot([-3, -3, 0, 0], [0, 1, 1, 0], color=ACCENT_COLORS['red'], linewidth=2)
    ax.axhline(y=0, color=TEXT_COLOR, linewidth=1)
    ax.axvline(x=0, color=TEXT_COLOR, linewidth=1)
    ax.set_xlim(-5, 2)
    ax.set_ylim(-0.2, 1.5)
    ax.set_xlabel('τ', fontsize=12, fontproperties=fp)
    ax.set_ylabel('h(-τ)', fontsize=12, fontproperties=fp)
    ax.set_title('(c) 翻轉 h(-τ)', fontsize=14, fontweight='bold', fontproperties=fp_title)
    ax.grid(True, alpha=0.3)
    
    # 下排：三種重疊情況
    t_values = [1.5, 3, 4.5]
    titles = ['(d) 部分重疊 t=1.5', '(e) 完全重疊 t=3', '(f) 部分重疊 t=4.5']
    
    for idx, (t, title) in enumerate(zip(t_values, titles)):
        ax = axes[1, idx]
        ax.set_facecolor(DARK_AXES_BG)
        
        # x(τ)
        ax.fill_between([0, 3], 0, 1, alpha=0.3, color=ACCENT_COLORS['blue'])
        ax.plot([0, 0, 3, 3], [0, 1, 1, 0], color=ACCENT_COLORS['blue'], linewidth=2, label='x(τ)')
        
        # h(t-τ) 滑動後
        ax.fill_between([t-3, t], 0, 1, alpha=0.3, color=ACCENT_COLORS['red'])
        ax.plot([t-3, t-3, t, t], [0, 1, 1, 0], color=ACCENT_COLORS['red'], linewidth=2, label=f'h(t-τ), t={t}')
        
        # 重疊區域
        overlap_start = max(0, t-3)
        overlap_end = min(3, t)
        if overlap_end > overlap_start:
            ax.fill_between([overlap_start, overlap_end], 0, 1, alpha=0.7, color=ACCENT_COLORS['green'])
            overlap_area = overlap_end - overlap_start
            ax.annotate(f'y({t})={overlap_area:.1f}', (1.5, 1.2), fontsize=12, ha='center', fontweight='bold', color=ACCENT_COLORS['yellow'], fontproperties=fp)
        
        ax.axhline(y=0, color=TEXT_COLOR, linewidth=1)
        ax.axvline(x=0, color=TEXT_COLOR, linewidth=1)
        ax.set_xlim(-2, 6)
        ax.set_ylim(-0.2, 1.6)
        ax.set_xlabel('τ', fontsize=12, fontproperties=fp)
        ax.set_title(title, fontsize=12, fontweight='bold', fontproperties=fp_title)
        ax.legend(loc='upper right', fontsize=9, facecolor=DARK_AXES_BG, edgecolor='#4a5568')
        ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}convolution_warmup.png', dpi=150, bbox_inches='tight', facecolor=DARK_BG)
    plt.close()
    print(f"✅ 已儲存: convolution_warmup.png")

# =====================================================
# 矩形卷積結果：三角形波形
# =====================================================
def convolution_result_triangle():
    """矩形脈衝卷積結果 - 三角形波形"""
    fig, ax = plt.subplots(figsize=(10, 5))
    fig.patch.set_facecolor(DARK_BG)
    ax.set_facecolor(DARK_AXES_BG)
    
    fp = get_font_prop(12)
    fp_title = get_font_prop(16, bold=True)
    
    t = np.linspace(-1, 7, 1000)
    y = np.piecewise(t, 
        [t < 0, (t >= 0) & (t <= 3), (t > 3) & (t <= 6), t > 6],
        [0, lambda t: t, lambda t: 6 - t, 0])
    
    ax.fill_between(t, y, alpha=0.4, color=ACCENT_COLORS['green'])
    ax.plot(t, y, linewidth=3, color=ACCENT_COLORS['green'], label='y(t) = x(t) * h(t)')
    
    # 標記重要點
    ax.plot([0, 3, 6], [0, 3, 0], 'o', color=ACCENT_COLORS['yellow'], markersize=10)
    ax.annotate('(0, 0)', (0, 0), textcoords="offset points", xytext=(-20, -20), fontsize=11, color=TEXT_COLOR, fontproperties=fp)
    ax.annotate('(3, 3) 峰值', (3, 3), textcoords="offset points", xytext=(10, 10), fontsize=11, color=ACCENT_COLORS['yellow'], fontproperties=fp)
    ax.annotate('(6, 0)', (6, 0), textcoords="offset points", xytext=(10, -20), fontsize=11, color=TEXT_COLOR, fontproperties=fp)
    
    ax.axhline(y=0, color=TEXT_COLOR, linewidth=1)
    ax.axvline(x=0, color=TEXT_COLOR, linewidth=1)
    ax.set_xlim(-1, 7)
    ax.set_ylim(-0.5, 4)
    ax.set_xlabel('t', fontsize=14, fontproperties=fp)
    ax.set_ylabel('y(t)', fontsize=14, fontproperties=fp)
    ax.set_title('矩形卷積結果：三角波形', fontsize=16, fontweight='bold', fontproperties=fp_title)
    ax.legend(fontsize=12, facecolor=DARK_AXES_BG, edgecolor='#4a5568')
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}convolution_triangle.png', dpi=150, bbox_inches='tight', facecolor=DARK_BG)
    plt.close()
    print(f"✅ 已儲存: convolution_triangle.png")

# =====================================================
# 第 4 題：指數衰減卷積
# =====================================================
def problem4_step_response():
    """第4題：步階響應波形"""
    fig, axes = plt.subplots(1, 3, figsize=(15, 4))
    fig.patch.set_facecolor(DARK_BG)
    
    fp = get_font_prop(12)
    fp_title = get_font_prop(14, bold=True)
    
    t = np.linspace(-1, 3, 1000)
    t_pos = t[t >= 0]
    
    # (a) 輸入 x(t) = u(t)
    ax = axes[0]
    ax.set_facecolor(DARK_AXES_BG)
    x = np.where(t >= 0, 1, 0)
    ax.plot(t, x, linewidth=3, color=ACCENT_COLORS['blue'])
    ax.fill_between(t[t >= 0], 0, 1, alpha=0.3, color=ACCENT_COLORS['blue'])
    ax.axhline(y=0, color=TEXT_COLOR, linewidth=1)
    ax.axvline(x=0, color=TEXT_COLOR, linewidth=1)
    ax.set_xlim(-1, 3)
    ax.set_ylim(-0.2, 1.5)
    ax.set_xlabel('t', fontsize=12, fontproperties=fp)
    ax.set_ylabel('x(t)', fontsize=12, fontproperties=fp)
    ax.set_title('(a) 輸入: x(t) = u(t)', fontsize=14, fontweight='bold', fontproperties=fp_title)
    ax.grid(True, alpha=0.3)
    
    # (b) 脈衝響應 h(t) = e^(-3t)u(t)
    ax = axes[1]
    ax.set_facecolor(DARK_AXES_BG)
    h = np.where(t >= 0, np.exp(-3 * t), 0)
    ax.plot(t, h, linewidth=3, color=ACCENT_COLORS['red'])
    ax.fill_between(t_pos, 0, np.exp(-3 * t_pos), alpha=0.3, color=ACCENT_COLORS['red'])
    ax.axhline(y=0, color=TEXT_COLOR, linewidth=1)
    ax.axvline(x=0, color=TEXT_COLOR, linewidth=1)
    ax.set_xlim(-1, 3)
    ax.set_ylim(-0.2, 1.5)
    ax.set_xlabel('t', fontsize=12, fontproperties=fp)
    ax.set_ylabel('h(t)', fontsize=12, fontproperties=fp)
    ax.set_title(r'(b) 脈衝響應: h(t) = $e^{-3t}$u(t)', fontsize=14, fontweight='bold', fontproperties=fp_title)
    ax.grid(True, alpha=0.3)
    
    # (c) 輸出 y(t) = (1/3)(1 - e^(-3t))u(t)
    ax = axes[2]
    ax.set_facecolor(DARK_AXES_BG)
    y = np.where(t >= 0, (1/3) * (1 - np.exp(-3 * t)), 0)
    ax.plot(t, y, linewidth=3, color=ACCENT_COLORS['green'], label='y(t)')
    ax.fill_between(t_pos, 0, (1/3) * (1 - np.exp(-3 * t_pos)), alpha=0.3, color=ACCENT_COLORS['green'])
    
    # 標記終值和時間常數
    ax.axhline(y=1/3, color=ACCENT_COLORS['red'], linestyle='--', linewidth=2, label='終值 = 1/3')
    ax.axhline(y=0.632 * (1/3), color=ACCENT_COLORS['orange'], linestyle=':', linewidth=2, label='63.2%')
    ax.axvline(x=1/3, color=ACCENT_COLORS['orange'], linestyle=':', linewidth=2)
    ax.annotate('τ = 1/3 秒', (1/3, 0.02), textcoords="offset points", xytext=(10, 0), fontsize=11, color=ACCENT_COLORS['orange'], fontproperties=fp)
    
    ax.axhline(y=0, color=TEXT_COLOR, linewidth=1)
    ax.axvline(x=0, color=TEXT_COLOR, linewidth=1)
    ax.set_xlim(-1, 3)
    ax.set_ylim(-0.05, 0.5)
    ax.set_xlabel('t', fontsize=12, fontproperties=fp)
    ax.set_ylabel('y(t)', fontsize=12, fontproperties=fp)
    ax.set_title(r'(c) 輸出: y(t) = $\frac{1}{3}$(1 - $e^{-3t}$)u(t)', fontsize=14, fontweight='bold', fontproperties=fp_title)
    ax.legend(fontsize=10, loc='right', facecolor=DARK_AXES_BG, edgecolor='#4a5568')
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}problem4_convolution.png', dpi=150, bbox_inches='tight', facecolor=DARK_BG)
    plt.close()
    print(f"✅ 已儲存: problem4_convolution.png")

# =====================================================
# 第 5 題：濾波器頻率響應
# =====================================================
def problem5_filters():
    """第5題：四種濾波器的頻率響應和輸出"""
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.patch.set_facecolor(DARK_BG)
    
    fp = get_font_prop(12)
    fp_title = get_font_prop(14, bold=True)
    
    # 輸入頻率
    input_freqs = [200, 400, 450, 600, 4500]
    input_amps = [3, 4, 8, 1, 3]
    
    filter_configs = [
        ('低通濾波器 (LPF)', 'fc=500 Hz', lambda f: f < 500, ACCENT_COLORS['blue']),
        ('高通濾波器 (HPF)', 'fc=500 Hz', lambda f: f > 500, ACCENT_COLORS['red']),
        ('帶通濾波器 (BPF)', '550 < f < 700 Hz', lambda f: 550 < f < 700, ACCENT_COLORS['green']),
        ('帶拒濾波器 (BSF)', '阻擋 550-700 Hz', lambda f: not (550 < f < 700), ACCENT_COLORS['purple']),
    ]
    
    for idx, (name, desc, pass_func, color) in enumerate(filter_configs):
        ax = axes[idx // 2, idx % 2]
        ax.set_facecolor(DARK_AXES_BG)
        
        # 畫輸入頻譜（灰色）
        markerline, stemlines, baseline = ax.stem(input_freqs, input_amps, linefmt='--', markerfmt='o', basefmt=' ')
        plt.setp(stemlines, color='#6c757d', linewidth=1, alpha=0.5)
        plt.setp(markerline, color='#6c757d', markersize=6, alpha=0.5)
        
        # 畫通過的頻率（亮色）
        passed_freqs = [f for f in input_freqs if pass_func(f)]
        passed_amps = [a for f, a in zip(input_freqs, input_amps) if pass_func(f)]
        
        if passed_freqs:
            markerline, stemlines, baseline = ax.stem(passed_freqs, passed_amps, 
                linefmt='-', markerfmt='D', basefmt=' ')
            plt.setp(stemlines, color=color, linewidth=3)
            plt.setp(markerline, color=color, markersize=10)
        
        # 標記通過的頻率
        for f, a in zip(passed_freqs, passed_amps):
            ax.annotate(f'{f}Hz', (f, a), textcoords="offset points", xytext=(0, 10), 
                       ha='center', fontsize=10, fontweight='bold', color=ACCENT_COLORS['yellow'], fontproperties=fp)
        
        ax.set_xlabel('頻率 f (Hz)', fontsize=12, fontproperties=fp)
        ax.set_ylabel('振幅', fontsize=12, fontproperties=fp)
        ax.set_title(f'{name}\n{desc}', fontsize=14, fontweight='bold', fontproperties=fp_title)
        ax.set_xlim(0, 5000)
        ax.set_ylim(0, 10)
        ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}problem5_filters.png', dpi=150, bbox_inches='tight', facecolor=DARK_BG)
    plt.close()
    print(f"✅ 已儲存: problem5_filters.png")

# =====================================================
# 第 6 題：取樣頻譜（改進版）
# =====================================================
def problem6_sampling():
    """第6題：原始頻譜與取樣頻譜 - 改進版標註"""
    fig, axes = plt.subplots(2, 1, figsize=(16, 10))
    fig.patch.set_facecolor(DARK_BG)
    
    fp = get_font_prop(12)
    fp_title = get_font_prop(16, bold=True)
    fp_label = get_font_prop(11)
    
    # 原始頻譜
    ax = axes[0]
    ax.set_facecolor(DARK_AXES_BG)
    freqs = [-250, -100, 0, 100, 250]
    amps = [1, 2, 3, 2, 1]
    
    markerline, stemlines, baseline = ax.stem(freqs, amps, linefmt='-', markerfmt='o', basefmt=' ')
    plt.setp(stemlines, color=ACCENT_COLORS['blue'], linewidth=2.5)
    plt.setp(markerline, color=ACCENT_COLORS['blue'], markersize=12)
    
    for f, a in zip(freqs, amps):
        ax.annotate(f'{a}', (f, a), textcoords="offset points", xytext=(0, 12), 
                   ha='center', fontsize=12, fontweight='bold', color=ACCENT_COLORS['yellow'])
    
    # 標記最大頻率
    ax.annotate('fmax = 250 Hz', (250, 1), textcoords="offset points", xytext=(30, 20), 
               fontsize=11, color=ACCENT_COLORS['red'], fontproperties=fp_label,
               arrowprops=dict(arrowstyle='->', color=ACCENT_COLORS['red'], lw=1.5))
    ax.annotate('fmax = -250 Hz', (-250, 1), textcoords="offset points", xytext=(-80, 20), 
               fontsize=11, color=ACCENT_COLORS['red'], fontproperties=fp_label,
               arrowprops=dict(arrowstyle='->', color=ACCENT_COLORS['red'], lw=1.5))
    
    ax.axhline(y=0, color=TEXT_COLOR, linewidth=1)
    ax.axvline(x=0, color=ACCENT_COLORS['orange'], linewidth=1, linestyle='--', alpha=0.7)
    ax.set_xlim(-400, 400)
    ax.set_ylim(0, 4.5)
    ax.set_xlabel('頻率 f (Hz)', fontsize=12, fontproperties=fp)
    ax.set_ylabel('振幅', fontsize=12, fontproperties=fp)
    ax.set_title('原始頻譜 X(f)', fontsize=16, fontweight='bold', fontproperties=fp_title)
    ax.grid(True, alpha=0.3)
    
    # =========================================
    # 取樣後頻譜（改進版標註）
    # =========================================
    ax = axes[1]
    ax.set_facecolor(DARK_AXES_BG)
    fs = 800  # 取樣頻率
    
    # 定義三個複製品
    replicas = [
        (0, ACCENT_COLORS['blue'], '原始 (n=0)'),
        (fs, ACCENT_COLORS['red'], '複製 (n=1)'),
        (-fs, ACCENT_COLORS['green'], '複製 (n=-1)'),
    ]
    
    for shift, color, label in replicas:
        shifted_freqs = [f + shift for f in freqs]
        markerline, stemlines, baseline = ax.stem(shifted_freqs, amps, 
            linefmt='-', markerfmt='o', basefmt=' ', label=label)
        plt.setp(stemlines, color=color, linewidth=2)
        plt.setp(markerline, color=color, markersize=10)
    
    # =========================================
    # 關鍵標註：Fs 間隔
    # =========================================
    # 標記複製品中心位置
    for center, label_text in [(0, '中心\n0 Hz'), (800, '中心\n+800 Hz'), (-800, '中心\n-800 Hz')]:
        ax.axvline(x=center, color=ACCENT_COLORS['purple'], linewidth=1.5, linestyle=':', alpha=0.8)
        ax.annotate(label_text, (center, 4.0), ha='center', va='bottom', fontsize=10, 
                   color=ACCENT_COLORS['purple'], fontweight='bold', fontproperties=fp_label)
    
    # 標記 Fs 間隔（從 0 到 800）
    ax.annotate('', xy=(0, 3.5), xytext=(800, 3.5),
                arrowprops=dict(arrowstyle='<->', color=ACCENT_COLORS['yellow'], lw=2.5))
    ax.text(400, 3.7, 'Fs = 800 Hz', ha='center', fontsize=13, 
           color=ACCENT_COLORS['yellow'], fontweight='bold', fontproperties=fp)
    
    # 標記 Fs/2 = 400 Hz（Nyquist 頻率）
    ax.axvline(x=400, color=ACCENT_COLORS['red'], linestyle='--', linewidth=2.5, label='fs/2 = 400 Hz')
    ax.axvline(x=-400, color=ACCENT_COLORS['red'], linestyle='--', linewidth=2.5)
    
    # 標記無混疊區域
    ax.axvspan(-400, 400, alpha=0.15, color=ACCENT_COLORS['green'])
    ax.text(0, 0.3, '← Nyquist 區間 →\n可完美還原', ha='center', fontsize=11, 
           color=ACCENT_COLORS['green'], fontweight='bold', fontproperties=fp_label)
    
    # 標記原始與複製品的邊界（混疊檢查）
    ax.annotate('原始最右邊\n250 Hz', (250, 1), textcoords="offset points", xytext=(0, -50), 
               fontsize=9, color=ACCENT_COLORS['cyan'], ha='center', fontproperties=fp_label,
               arrowprops=dict(arrowstyle='->', color=ACCENT_COLORS['cyan'], lw=1))
    ax.annotate('複製最左邊\n550 Hz', (550, 1), textcoords="offset points", xytext=(0, -50), 
               fontsize=9, color=ACCENT_COLORS['cyan'], ha='center', fontproperties=fp_label,
               arrowprops=dict(arrowstyle='->', color=ACCENT_COLORS['cyan'], lw=1))
    
    # 間隙標註
    ax.annotate('', xy=(250, 1.5), xytext=(550, 1.5),
                arrowprops=dict(arrowstyle='<->', color=ACCENT_COLORS['cyan'], lw=2))
    ax.text(400, 1.7, '間隙 = 300 Hz\n(無混疊!)', ha='center', fontsize=10, 
           color=ACCENT_COLORS['cyan'], fontweight='bold', fontproperties=fp_label)
    
    ax.axhline(y=0, color=TEXT_COLOR, linewidth=1)
    ax.set_xlim(-1200, 1200)
    ax.set_ylim(0, 4.8)
    ax.set_xlabel('頻率 f (Hz)', fontsize=12, fontproperties=fp)
    ax.set_ylabel('振幅', fontsize=12, fontproperties=fp)
    ax.set_title(f'取樣後頻譜 (fs = {fs} Hz)：無混疊！', fontsize=16, fontweight='bold', fontproperties=fp_title)
    ax.legend(fontsize=10, loc='upper right', facecolor=DARK_AXES_BG, edgecolor='#4a5568')
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}problem6_sampling.png', dpi=150, bbox_inches='tight', facecolor=DARK_BG)
    plt.close()
    print(f"✅ 已儲存: problem6_sampling.png (改進版)")


# =====================================================
# 第 7 題：傅立葉級數頻譜（改進版）
# =====================================================
def problem7_fourier_series():
    """第7題：方波傅立葉級數頻譜 - 使用 f0 倍數標示"""
    fig, ax = plt.subplots(figsize=(14, 7))
    fig.patch.set_facecolor(DARK_BG)
    ax.set_facecolor(DARK_AXES_BG)
    
    fp = get_font_prop(12)
    fp_title = get_font_prop(16, bold=True)
    fp_label = get_font_prop(10)
    
    # 使用抽象的 f0 倍數（用數字 1 代表 f0）
    # 實際繪圖用數字，但標籤顯示 f0 倍數
    
    # 雙邊頻譜數據：頻率倍數, 振幅, 振幅標籤
    # DC: 1/2, 其他: 1/(n*pi) for n = 1, 3, 5, 7, 9 (雙邊已除2)
    spectrum_data = [
        (0, 0.5, '1/2 (DC)'),           # DC
        (1, 1/np.pi, '1/π'),            # f0
        (-1, 1/np.pi, '1/π'),           # -f0
        (3, 1/(3*np.pi), '1/3π'),       # 3f0
        (-3, 1/(3*np.pi), '1/3π'),      # -3f0
        (5, 1/(5*np.pi), '1/5π'),       # 5f0
        (-5, 1/(5*np.pi), '1/5π'),      # -5f0
        (7, 1/(7*np.pi), '1/7π'),       # 7f0
        (-7, 1/(7*np.pi), '1/7π'),      # -7f0
        (9, 1/(9*np.pi), '1/9π'),       # 9f0
        (-9, 1/(9*np.pi), '1/9π'),      # -9f0
    ]
    
    freqs = [d[0] for d in spectrum_data]
    amps = [d[1] for d in spectrum_data]
    labels = [d[2] for d in spectrum_data]
    
    # 畫頻譜
    markerline, stemlines, baseline = ax.stem(freqs, amps, 
        linefmt='-', markerfmt='o', basefmt=' ')
    plt.setp(stemlines, color=ACCENT_COLORS['purple'], linewidth=2.5)
    plt.setp(markerline, color=ACCENT_COLORS['purple'], markersize=10)
    
    # 標記每個點的振幅值
    for freq, amp, label in spectrum_data:
        if freq == 0:
            # DC 分量特殊處理
            ax.annotate(label, (freq, amp), textcoords="offset points", 
                       xytext=(30, 10), fontsize=11, fontweight='bold', 
                       color=ACCENT_COLORS['yellow'],
                       arrowprops=dict(arrowstyle='->', color=ACCENT_COLORS['yellow'], lw=1.5),
                       fontproperties=fp)
        else:
            # 所有頻率都標註
            ax.annotate(label, (freq, amp), textcoords="offset points", 
                       xytext=(0, 12), ha='center', fontsize=10, 
                       fontweight='bold', color=ACCENT_COLORS['cyan'],
                       fontproperties=fp_label)
    
    # 設定 x 軸刻度為 f0 倍數
    ax.set_xticks([-9, -7, -5, -3, -1, 0, 1, 3, 5, 7, 9])
    ax.set_xticklabels(['-9f0', '-7f0', '-5f0', '-3f0', '-f0', '0', 
                        'f0', '3f0', '5f0', '7f0', '9f0'], fontproperties=fp_label)
    
    ax.axhline(y=0, color=TEXT_COLOR, linewidth=1)
    ax.axvline(x=0, color=ACCENT_COLORS['orange'], linewidth=1, linestyle='--', alpha=0.7)
    ax.set_xlim(-11, 11)
    ax.set_ylim(0, 0.65)
    ax.set_xlabel('頻率 (f0 的倍數)', fontsize=12, fontproperties=fp)
    ax.set_ylabel('振幅', fontsize=12, fontproperties=fp)
    ax.set_title('方波傅立葉級數 - 雙邊頻譜 (0 到 1 方波)', fontsize=16, fontweight='bold', fontproperties=fp_title)
    ax.grid(True, alpha=0.3)
    
    # 添加說明框
    textstr = '方波: 一半週期為 1, 一半為 0\nDC = 1/2 (平均值)\n諧波: 僅奇數次 (1, 3, 5, 7, 9...)'
    props = dict(boxstyle='round', facecolor=DARK_AXES_BG, edgecolor=ACCENT_COLORS['purple'], alpha=0.9)
    ax.text(0.02, 0.98, textstr, transform=ax.transAxes, fontsize=10,
            verticalalignment='top', fontproperties=fp_label, color=TEXT_COLOR, bbox=props)
    
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}problem7_fourier_series.png', dpi=150, bbox_inches='tight', facecolor=DARK_BG)
    plt.close()
    print(f"✅ 已儲存: problem7_fourier_series.png (使用 f0 倍數標示)")

# =====================================================
# 第 8 題：三角頻譜取樣
# =====================================================
def problem8_triangular():
    """第8題：三角頻譜與取樣"""
    fig, axes = plt.subplots(2, 1, figsize=(14, 8))
    fig.patch.set_facecolor(DARK_BG)
    
    fp = get_font_prop(12)
    fp_title = get_font_prop(16, bold=True)
    
    # 原始三角頻譜
    ax = axes[0]
    ax.set_facecolor(DARK_AXES_BG)
    f = np.linspace(-300, 300, 1000)
    X = np.maximum(0, 2 * (1 - np.abs(f) / 200))
    
    ax.fill_between(f, X, alpha=0.4, color=ACCENT_COLORS['blue'])
    ax.plot(f, X, linewidth=3, color=ACCENT_COLORS['blue'], label='X(f)')
    ax.annotate('峰值 = 2', (0, 2), textcoords="offset points", xytext=(10, 10), 
               fontsize=11, fontweight='bold', color=ACCENT_COLORS['yellow'], fontproperties=fp)
    ax.annotate('fmax = 200 Hz', (200, 0), textcoords="offset points", xytext=(10, 10), 
               fontsize=11, color=ACCENT_COLORS['red'], fontproperties=fp)
    
    ax.axhline(y=0, color=TEXT_COLOR, linewidth=1)
    ax.axvline(x=0, color=ACCENT_COLORS['orange'], linewidth=0.5, linestyle='--', alpha=0.7)
    ax.set_xlim(-400, 400)
    ax.set_ylim(0, 2.5)
    ax.set_xlabel('頻率 f (Hz)', fontsize=12, fontproperties=fp)
    ax.set_ylabel('X(f)', fontsize=12, fontproperties=fp)
    ax.set_title('原始三角形頻譜', fontsize=16, fontweight='bold', fontproperties=fp_title)
    ax.legend(fontsize=12, facecolor=DARK_AXES_BG, edgecolor='#4a5568')
    ax.grid(True, alpha=0.3)
    
    # 取樣後頻譜
    ax = axes[1]
    ax.set_facecolor(DARK_AXES_BG)
    fs = 600
    
    colors = [ACCENT_COLORS['blue'], ACCENT_COLORS['red'], ACCENT_COLORS['green']]
    labels = ['原始 (n=0)', '複製 (n=1)', '複製 (n=-1)']
    shifts = [0, fs, -fs]
    
    for shift, color, label in zip(shifts, colors, labels):
        f_shifted = f + shift
        ax.fill_between(f_shifted, X, alpha=0.2, color=color)
        ax.plot(f_shifted, X, linewidth=2, color=color, label=label)
    
    # 標記無混疊
    ax.axvline(x=200, color=ACCENT_COLORS['red'], linestyle='--', linewidth=2, label='fmax = 200 Hz')
    ax.axvline(x=-200, color=ACCENT_COLORS['red'], linestyle='--', linewidth=2)
    ax.axvline(x=400, color=ACCENT_COLORS['orange'], linestyle=':', linewidth=2, label='fs-fmax = 400 Hz')
    ax.axvline(x=-400, color=ACCENT_COLORS['orange'], linestyle=':', linewidth=2)
    
    # 標註間隙
    ax.annotate('', xy=(200, 1.5), xytext=(400, 1.5),
                arrowprops=dict(arrowstyle='<->', color=ACCENT_COLORS['green'], lw=2))
    ax.text(300, 1.7, '無混疊\n間隙', ha='center', fontsize=11, color=ACCENT_COLORS['green'], fontweight='bold', fontproperties=fp)
    
    ax.axhline(y=0, color=TEXT_COLOR, linewidth=1)
    ax.set_xlim(-900, 900)
    ax.set_ylim(0, 2.5)
    ax.set_xlabel('頻率 f (Hz)', fontsize=12, fontproperties=fp)
    ax.set_ylabel('Xs(f)', fontsize=12, fontproperties=fp)
    ax.set_title(f'取樣後頻譜 (fs = {fs} Hz > 2×200 = 400 Hz)：滿足奈奎斯特！', fontsize=16, fontweight='bold', fontproperties=fp_title)
    ax.legend(fontsize=10, loc='upper right', facecolor=DARK_AXES_BG, edgecolor='#4a5568')
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}problem8_triangular.png', dpi=150, bbox_inches='tight', facecolor=DARK_BG)
    plt.close()
    print(f"✅ 已儲存: problem8_triangular.png")

# =====================================================
# 主程式
# =====================================================
if __name__ == "__main__":
    print("="*60)
    print("📊 訊號與系統期末考 - 圖表生成器")
    print("🌙 深色主題 + 繁體中文 (ZH_TW)")
    print("="*60)
    
    setup_dark_style()
    
    print("\n🎨 開始生成圖表...\n")
    
    problem3_spectrum()
    convolution_warmup()
    convolution_result_triangle()
    problem4_step_response()
    problem5_filters()
    problem6_sampling()
    problem7_fourier_series()
    problem8_triangular()
    
    print("\n" + "="*60)
    print("✅ 所有圖表生成完成！")
    print(f"📁 輸出目錄: {OUTPUT_DIR}")
    print("="*60)
