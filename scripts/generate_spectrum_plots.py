"""
訊號與系統期末考 - 頻譜圖生成腳本
生成專業的頻譜圖（振幅譜 + 相位譜）
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # 非 GUI 模式
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei', 'SimHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

# 設定樣式
plt.style.use('dark_background')
COLORS = {
    'magnitude': '#00D4FF',
    'phase': '#FF6B6B',
    'grid': '#333333',
    'accent': '#FFD93D'
}

def save_plot(fig, name):
    """儲存圖片到部落格 images 資料夾"""
    path = f'd:/Blog/public/images/articles/{name}.png'
    fig.savefig(path, dpi=150, bbox_inches='tight', facecolor='#1a1a2e', edgecolor='none')
    plt.close(fig)
    print(f'✅ 已儲存: {path}')
    return path

# =============================================
# 第 3 題：正弦訊號的傅立葉分析
# x(t) = 2cos(60πt + π/4) - 4cos(100πt)
# =============================================

def plot_problem3_spectra():
    """第 3 題：單邊/雙邊頻譜（振幅 + 相位）"""
    
    # 頻率成分
    f1, A1, phi1 = 30, 2, np.pi/4       # 2cos(60πt + π/4)
    f2, A2, phi2 = 50, 4, np.pi         # -4cos(100πt) = 4cos(100πt + π)
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('第 3 題：訊號頻譜分析\n$x(t) = 2\\cos(60\\pi t + \\frac{\\pi}{4}) - 4\\cos(100\\pi t)$', 
                 fontsize=16, color='white', fontweight='bold')
    
    # --- 單邊振幅頻譜 ---
    ax1 = axes[0, 0]
    freqs = [f1, f2]
    amps = [A1, A2]
    ax1.stem(freqs, amps, basefmt=' ', linefmt=COLORS['magnitude'], markerfmt='o')
    ax1.set_title('單邊振幅頻譜 (Magnitude Spectrum)', fontsize=12, color='white')
    ax1.set_xlabel('頻率 $f$ (Hz)', fontsize=11)
    ax1.set_ylabel('振幅 $|X(f)|$', fontsize=11)
    ax1.set_xlim(0, 70)
    ax1.set_ylim(0, 5)
    ax1.grid(True, alpha=0.3, color=COLORS['grid'])
    for f, a in zip(freqs, amps):
        ax1.annotate(f'{a}', (f, a + 0.2), ha='center', fontsize=10, color=COLORS['accent'])
    
    # --- 單邊相位頻譜 ---
    ax2 = axes[0, 1]
    phases = [phi1, phi2]
    phases_deg = [np.degrees(p) for p in phases]
    ax2.stem(freqs, phases_deg, basefmt=' ', linefmt=COLORS['phase'], markerfmt='s')
    ax2.set_title('單邊相位頻譜 (Phase Spectrum)', fontsize=12, color='white')
    ax2.set_xlabel('頻率 $f$ (Hz)', fontsize=11)
    ax2.set_ylabel('相位 $\\angle X(f)$ (度)', fontsize=11)
    ax2.set_xlim(0, 70)
    ax2.set_ylim(-20, 200)
    ax2.axhline(y=0, color='white', linestyle='--', alpha=0.3)
    ax2.grid(True, alpha=0.3, color=COLORS['grid'])
    for f, p in zip(freqs, phases_deg):
        ax2.annotate(f'{p:.0f}°', (f, p + 10), ha='center', fontsize=10, color=COLORS['accent'])
    
    # --- 雙邊振幅頻譜 ---
    ax3 = axes[1, 0]
    freqs_two = [-f2, -f1, f1, f2]
    amps_two = [A2/2, A1/2, A1/2, A2/2]
    ax3.stem(freqs_two, amps_two, basefmt=' ', linefmt=COLORS['magnitude'], markerfmt='o')
    ax3.set_title('雙邊振幅頻譜 (Two-Sided Magnitude)', fontsize=12, color='white')
    ax3.set_xlabel('頻率 $f$ (Hz)', fontsize=11)
    ax3.set_ylabel('振幅 $|X(f)|$', fontsize=11)
    ax3.set_xlim(-70, 70)
    ax3.set_ylim(0, 3)
    ax3.axvline(x=0, color='white', linestyle='--', alpha=0.3)
    ax3.grid(True, alpha=0.3, color=COLORS['grid'])
    for f, a in zip(freqs_two, amps_two):
        ax3.annotate(f'{a:.0f}', (f, a + 0.15), ha='center', fontsize=9, color=COLORS['accent'])
    
    # --- 雙邊相位頻譜 ---
    ax4 = axes[1, 1]
    # 正頻率相位，負頻率相位取反
    phases_two = [-phi2, -phi1, phi1, phi2]
    phases_two_deg = [np.degrees(p) for p in phases_two]
    ax4.stem(freqs_two, phases_two_deg, basefmt=' ', linefmt=COLORS['phase'], markerfmt='s')
    ax4.set_title('雙邊相位頻譜 (Two-Sided Phase)', fontsize=12, color='white')
    ax4.set_xlabel('頻率 $f$ (Hz)', fontsize=11)
    ax4.set_ylabel('相位 $\\angle X(f)$ (度)', fontsize=11)
    ax4.set_xlim(-70, 70)
    ax4.set_ylim(-200, 200)
    ax4.axhline(y=0, color='white', linestyle='--', alpha=0.3)
    ax4.axvline(x=0, color='white', linestyle='--', alpha=0.3)
    ax4.grid(True, alpha=0.3, color=COLORS['grid'])
    for f, p in zip(freqs_two, phases_two_deg):
        offset = 15 if p >= 0 else -25
        ax4.annotate(f'{p:.0f}°', (f, p + offset), ha='center', fontsize=9, color=COLORS['accent'])
    
    plt.tight_layout()
    return save_plot(fig, 'spectrum_problem3')


# =============================================
# 第 4 題：卷積響應波形
# y(t) = (1/3)(1 - e^{-3t})u(t)
# =============================================

def plot_problem4_convolution():
    """第 4 題：卷積響應時域波形"""
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    t = np.linspace(-0.5, 3, 500)
    y = np.where(t >= 0, (1/3) * (1 - np.exp(-3*t)), 0)
    
    ax.plot(t, y, color=COLORS['magnitude'], linewidth=2.5, label='$y(t) = \\frac{1}{3}(1 - e^{-3t})u(t)$')
    ax.axhline(y=1/3, color=COLORS['accent'], linestyle='--', alpha=0.7, label='終值 $= \\frac{1}{3}$')
    ax.axhline(y=0, color='white', linestyle='-', alpha=0.3)
    ax.axvline(x=0, color='white', linestyle='-', alpha=0.3)
    
    # 標記時間常數
    tau = 1/3
    y_tau = (1/3) * (1 - np.exp(-1))  # 63.2% of final value
    ax.plot(tau, y_tau, 'o', color=COLORS['phase'], markersize=10)
    ax.annotate(f'τ = 1/3 秒\n(63.2%)', (tau + 0.1, y_tau), fontsize=10, color=COLORS['phase'])
    
    ax.set_title('第 4 題：卷積響應波形\n$y(t) = x(t) * h(t)$，其中 $x(t) = u(t)$，$h(t) = e^{-3t}u(t)$', 
                 fontsize=14, color='white', fontweight='bold')
    ax.set_xlabel('時間 $t$ (秒)', fontsize=12)
    ax.set_ylabel('$y(t)$', fontsize=12)
    ax.set_xlim(-0.5, 3)
    ax.set_ylim(-0.05, 0.45)
    ax.legend(loc='lower right', fontsize=10)
    ax.grid(True, alpha=0.3, color=COLORS['grid'])
    
    plt.tight_layout()
    return save_plot(fig, 'convolution_problem4')


# =============================================
# 第 6 題：取樣頻譜
# x(t) = 3 + 4cos(200πt) + 2cos(500πt), fs = 800 Hz
# =============================================

def plot_problem6_sampling():
    """第 6 題：原始頻譜與取樣後頻譜"""
    
    fig, axes = plt.subplots(2, 1, figsize=(14, 10))
    fig.suptitle('第 6 題：取樣頻譜分析\n$x(t) = 3 + 4\\cos(200\\pi t) + 2\\cos(500\\pi t)$，$f_s = 800$ Hz', 
                 fontsize=16, color='white', fontweight='bold')
    
    # 原始頻譜成分
    freqs_orig = [0, 100, 250]
    amps_orig = [3, 4, 2]  # 單邊
    
    # --- 原始雙邊頻譜 ---
    ax1 = axes[0]
    freqs_two = [-250, -100, 0, 100, 250]
    amps_two = [1, 2, 3, 2, 1]  # 雙邊 (AC 成分除以 2)
    
    ax1.stem(freqs_two, amps_two, basefmt=' ', linefmt=COLORS['magnitude'], markerfmt='o')
    ax1.set_title('原始訊號頻譜 $X(f)$', fontsize=12, color='white')
    ax1.set_xlabel('頻率 $f$ (Hz)', fontsize=11)
    ax1.set_ylabel('振幅', fontsize=11)
    ax1.set_xlim(-400, 400)
    ax1.set_ylim(0, 4)
    ax1.axvline(x=0, color='white', linestyle='--', alpha=0.3)
    ax1.grid(True, alpha=0.3, color=COLORS['grid'])
    for f, a in zip(freqs_two, amps_two):
        ax1.annotate(f'{a}', (f, a + 0.2), ha='center', fontsize=10, color=COLORS['accent'])
    
    # --- 取樣後頻譜 ---
    ax2 = axes[1]
    fs = 800
    
    # 原始 + 複製 (在 ±fs, ±2fs 處)
    all_freqs = []
    all_amps = []
    for n in [-1, 0, 1]:  # 複製次數
        for f, a in zip(freqs_two, amps_two):
            all_freqs.append(f + n * fs)
            all_amps.append(a)
    
    markerline, stemlines, baseline = ax2.stem(all_freqs, all_amps, basefmt=' ', linefmt=COLORS['magnitude'], markerfmt='o')
    markerline.set_markersize(5)
    
    # 標示頻譜複製
    ax2.axvspan(-250, 250, alpha=0.15, color=COLORS['accent'], label='原始頻譜')
    ax2.axvspan(550, 1050, alpha=0.1, color=COLORS['phase'], label='複製頻譜')
    ax2.axvspan(-1050, -550, alpha=0.1, color=COLORS['phase'])
    
    ax2.set_title('取樣後頻譜 $X_s(f)$（無混疊，$f_s = 800$ Hz $> 2f_{max} = 500$ Hz）', fontsize=12, color='white')
    ax2.set_xlabel('頻率 $f$ (Hz)', fontsize=11)
    ax2.set_ylabel('振幅', fontsize=11)
    ax2.set_xlim(-1200, 1200)
    ax2.set_ylim(0, 4)
    ax2.axvline(x=0, color='white', linestyle='--', alpha=0.3)
    ax2.axvline(x=fs, color=COLORS['phase'], linestyle=':', alpha=0.5)
    ax2.axvline(x=-fs, color=COLORS['phase'], linestyle=':', alpha=0.5)
    ax2.grid(True, alpha=0.3, color=COLORS['grid'])
    ax2.legend(loc='upper right', fontsize=10)
    
    # 標示 LPF 截止範圍
    ax2.annotate('LPF 截止\n$f_c = 400$ Hz', (-350, 3.5), fontsize=10, color=COLORS['accent'])
    
    plt.tight_layout()
    return save_plot(fig, 'sampling_problem6')


# =============================================
# 第 7 題：傅立葉級數頻譜
# =============================================

def plot_problem7_fourier_series():
    """第 7 題：方波傅立葉級數頻譜"""
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    fig.suptitle('第 7 題：方波傅立葉級數頻譜', fontsize=16, color='white', fontweight='bold')
    
    # 傅立葉級數係數 (假設 f0 = 1 Hz)
    f0 = 1
    harmonics = [0, 1, 3, 5, 7, 9]  # DC + 奇次諧波
    
    # 係數：DC = 1/2, 其他 = 2/(n*pi)
    amps = [0.5]  # DC
    for n in harmonics[1:]:
        amps.append(2 / (n * np.pi))
    
    freqs = [n * f0 for n in harmonics]
    
    # --- 單邊振幅頻譜 ---
    ax1 = axes[0]
    ax1.stem(freqs, amps, basefmt=' ', linefmt=COLORS['magnitude'], markerfmt='o')
    ax1.set_title('單邊振幅頻譜 $|c_n|$', fontsize=12, color='white')
    ax1.set_xlabel('頻率 $f/f_0$', fontsize=11)
    ax1.set_ylabel('振幅', fontsize=11)
    ax1.set_xlim(-0.5, 10)
    ax1.set_ylim(0, 0.7)
    ax1.grid(True, alpha=0.3, color=COLORS['grid'])
    for f, a in zip(freqs, amps):
        label = f'{a:.3f}' if f > 0 else '1/2'
        ax1.annotate(label, (f, a + 0.03), ha='center', fontsize=9, color=COLORS['accent'])
    
    # --- 雙邊振幅頻譜 ---
    ax2 = axes[1]
    freqs_two = []
    amps_two = []
    for n, a in zip(harmonics, amps):
        if n == 0:
            freqs_two.append(0)
            amps_two.append(a)
        else:
            freqs_two.extend([-n * f0, n * f0])
            amps_two.extend([a/2, a/2])
    
    # 排序
    sorted_pairs = sorted(zip(freqs_two, amps_two))
    freqs_two, amps_two = zip(*sorted_pairs)
    
    ax2.stem(freqs_two, amps_two, basefmt=' ', linefmt=COLORS['magnitude'], markerfmt='o')
    ax2.set_title('雙邊振幅頻譜（各諧波幅度減半）', fontsize=12, color='white')
    ax2.set_xlabel('頻率 $f/f_0$', fontsize=11)
    ax2.set_ylabel('振幅', fontsize=11)
    ax2.set_xlim(-10, 10)
    ax2.set_ylim(0, 0.6)
    ax2.axvline(x=0, color='white', linestyle='--', alpha=0.3)
    ax2.grid(True, alpha=0.3, color=COLORS['grid'])
    
    plt.tight_layout()
    return save_plot(fig, 'fourier_series_problem7')


# =============================================
# 第 8 題：三角頻譜取樣
# =============================================

def plot_problem8_triangular():
    """第 8 題：三角頻譜與取樣"""
    
    fig, axes = plt.subplots(2, 1, figsize=(14, 10))
    fig.suptitle('第 8 題：三角頻譜取樣分析\n最高頻率 $f_{max} = 200$ Hz，$f_s = 600$ Hz', 
                 fontsize=16, color='white', fontweight='bold')
    
    # 三角頻譜函數
    def triangular_spectrum(f, center, width, height):
        return np.maximum(0, height * (1 - np.abs(f - center) / width))
    
    f = np.linspace(-1500, 1500, 3000)
    
    # --- 原始頻譜 ---
    ax1 = axes[0]
    X_orig = triangular_spectrum(f, 0, 200, 2)
    ax1.fill_between(f, X_orig, alpha=0.4, color=COLORS['magnitude'])
    ax1.plot(f, X_orig, color=COLORS['magnitude'], linewidth=2)
    ax1.set_title('原始三角頻譜 $X(f)$', fontsize=12, color='white')
    ax1.set_xlabel('頻率 $f$ (Hz)', fontsize=11)
    ax1.set_ylabel('$|X(f)|$', fontsize=11)
    ax1.set_xlim(-500, 500)
    ax1.set_ylim(0, 2.5)
    ax1.axvline(x=0, color='white', linestyle='--', alpha=0.3)
    ax1.grid(True, alpha=0.3, color=COLORS['grid'])
    ax1.annotate('峰值 = 2', (0, 2.1), ha='center', fontsize=11, color=COLORS['accent'])
    ax1.annotate('$f_{max} = 200$ Hz', (200, 0.3), fontsize=10, color=COLORS['phase'])
    
    # --- 取樣後頻譜 ---
    ax2 = axes[1]
    fs = 600
    X_sampled = np.zeros_like(f)
    for n in range(-3, 4):
        X_sampled += triangular_spectrum(f, n * fs, 200, 2)
    
    ax2.fill_between(f, X_sampled, alpha=0.4, color=COLORS['magnitude'])
    ax2.plot(f, X_sampled, color=COLORS['magnitude'], linewidth=2)
    
    # 標示 LPF 範圍
    ax2.axvspan(-300, 300, alpha=0.15, color=COLORS['accent'], label='LPF 通過區 ($f_c = 300$ Hz)')
    ax2.axvline(x=fs, color=COLORS['phase'], linestyle=':', alpha=0.7, label=f'$f_s = {fs}$ Hz')
    ax2.axvline(x=-fs, color=COLORS['phase'], linestyle=':', alpha=0.7)
    
    ax2.set_title('取樣後頻譜 $X_s(f)$（無混疊，滿足 Nyquist: $f_s = 600 > 2 \\times 200 = 400$ Hz）', 
                  fontsize=12, color='white')
    ax2.set_xlabel('頻率 $f$ (Hz)', fontsize=11)
    ax2.set_ylabel('$|X_s(f)|$', fontsize=11)
    ax2.set_xlim(-1200, 1200)
    ax2.set_ylim(0, 2.5)
    ax2.grid(True, alpha=0.3, color=COLORS['grid'])
    ax2.legend(loc='upper right', fontsize=10)
    
    plt.tight_layout()
    return save_plot(fig, 'triangular_problem8')


# =============================================
# 主程式
# =============================================

if __name__ == '__main__':
    print('🎨 正在生成訊號與系統頻譜圖...\n')
    
    plots = [
        ('第 3 題', plot_problem3_spectra),
        ('第 4 題', plot_problem4_convolution),
        ('第 6 題', plot_problem6_sampling),
        ('第 7 題', plot_problem7_fourier_series),
        ('第 8 題', plot_problem8_triangular),
    ]
    
    for name, func in plots:
        print(f'📊 生成 {name} 圖表...')
        func()
    
    print('\n✅ 所有圖表已生成完成！')
