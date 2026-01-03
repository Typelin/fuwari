"""
卷積過程完整圖解
包含：翻轉 h(τ) → h(-τ)、滑動過程 h(t-τ)、重疊區域
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.gridspec import GridSpec

# 設定中文字體
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei', 'SimHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

# 定義輸出路徑
OUTPUT_DIR = r'd:\Blog\public\images\articles'


def create_flip_diagram():
    """
    圖 1：展示 h(τ) 翻轉成 h(-τ) 的過程
    """
    fig, axes = plt.subplots(1, 3, figsize=(15, 4))
    
    tau = np.linspace(-2, 3, 500)
    
    # (a) 原始 h(τ) = e^(-3τ)u(τ)
    ax = axes[0]
    h_original = np.where(tau >= 0, np.exp(-3 * tau), 0)
    ax.plot(tau, h_original, 'b-', linewidth=2.5, label='h(τ)')
    ax.fill_between(tau, 0, h_original, alpha=0.3, color='blue')
    ax.axhline(y=0, color='black', linewidth=0.5)
    ax.axvline(x=0, color='black', linewidth=0.5, linestyle='--')
    ax.set_xlim(-2, 3)
    ax.set_ylim(-0.1, 1.2)
    ax.set_xlabel('τ', fontsize=14)
    ax.set_ylabel('h(τ)', fontsize=14)
    ax.set_title('Step 1: 原始 h(τ)', fontsize=14, fontweight='bold')
    ax.annotate('尾巴朝右 →', xy=(1.5, 0.1), fontsize=12, color='blue')
    ax.legend(loc='upper right', fontsize=12)
    ax.grid(True, alpha=0.3)
    
    # (b) 翻轉過程示意
    ax = axes[1]
    ax.plot(tau, h_original, 'b--', linewidth=1.5, alpha=0.5, label='原本 h(τ)')
    # 翻轉後 h(-τ)
    h_flipped = np.where(tau <= 0, np.exp(3 * tau), 0)
    ax.plot(tau, h_flipped, 'r-', linewidth=2.5, label='翻轉後 h(-τ)')
    ax.fill_between(tau, 0, h_flipped, alpha=0.3, color='red')
    ax.axhline(y=0, color='black', linewidth=0.5)
    ax.axvline(x=0, color='black', linewidth=0.5, linestyle='--')
    
    # 畫翻轉箭頭
    ax.annotate('', xy=(-0.5, 0.8), xytext=(0.5, 0.8),
                arrowprops=dict(arrowstyle='<->', color='green', lw=2))
    ax.text(0, 0.9, '鏡像翻轉', fontsize=11, ha='center', color='green', fontweight='bold')
    
    ax.set_xlim(-2, 3)
    ax.set_ylim(-0.1, 1.2)
    ax.set_xlabel('τ', fontsize=14)
    ax.set_ylabel('', fontsize=14)
    ax.set_title('Step 2: 翻轉 (τ → -τ)', fontsize=14, fontweight='bold')
    ax.annotate('← 尾巴朝左', xy=(-1.5, 0.1), fontsize=12, color='red')
    ax.legend(loc='upper right', fontsize=12)
    ax.grid(True, alpha=0.3)
    
    # (c) 翻轉後的結果
    ax = axes[2]
    ax.plot(tau, h_flipped, 'r-', linewidth=2.5, label='h(-τ)')
    ax.fill_between(tau, 0, h_flipped, alpha=0.3, color='red')
    ax.axhline(y=0, color='black', linewidth=0.5)
    ax.axvline(x=0, color='black', linewidth=0.5, linestyle='--')
    ax.set_xlim(-2, 3)
    ax.set_ylim(-0.1, 1.2)
    ax.set_xlabel('τ', fontsize=14)
    ax.set_ylabel('h(-τ)', fontsize=14)
    ax.set_title('結果: h(-τ) = e^(3τ)u(-τ)', fontsize=14, fontweight='bold')
    ax.annotate('← 尾巴朝左', xy=(-1.5, 0.1), fontsize=12, color='red')
    ax.legend(loc='upper right', fontsize=12)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/conv_step1_flip.png', dpi=150, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()
    print('已儲存: conv_step1_flip.png')


def create_sliding_diagram():
    """
    圖 2：展示 h(t-τ) 滑動過程，多個時間點
    """
    fig, axes = plt.subplots(2, 3, figsize=(15, 8))
    
    tau = np.linspace(-3, 5, 500)
    
    # x(τ) = u(τ)
    x_tau = np.where(tau >= 0, 1, 0)
    
    # 不同時間點 t
    t_values = [-0.5, 0, 0.5, 1, 2, 3]
    titles = ['t = -0.5 (還沒進入)', 't = 0 (剛接觸)', 't = 0.5 (開始重疊)', 
              't = 1 (更多重疊)', 't = 2 (大部分重疊)', 't = 3 (幾乎完全重疊)']
    
    for idx, (t, title) in enumerate(zip(t_values, titles)):
        ax = axes[idx // 3, idx % 3]
        
        # 畫 x(τ)
        ax.fill_between(tau, 0, x_tau, alpha=0.3, color='blue', label='x(τ) = u(τ)')
        ax.plot(tau, x_tau, 'b-', linewidth=2)
        
        # 畫 h(t-τ) = e^(-3(t-τ))u(t-τ)
        # u(t-τ) = 1 when τ ≤ t
        h_shifted = np.where(tau <= t, np.exp(-3 * (t - tau)), 0)
        ax.fill_between(tau, 0, h_shifted, alpha=0.3, color='red', label=f'h(t-τ)')
        ax.plot(tau, h_shifted, 'r-', linewidth=2)
        
        # 標示重疊區域
        if t > 0:
            overlap_mask = (tau >= 0) & (tau <= t)
            overlap_tau = tau[overlap_mask]
            if len(overlap_tau) > 0:
                overlap_h = h_shifted[overlap_mask]
                ax.fill_between(overlap_tau, 0, overlap_h, alpha=0.5, color='green', 
                               label='重疊區域 (積分範圍)')
        
        ax.axhline(y=0, color='black', linewidth=0.5)
        ax.axvline(x=0, color='black', linewidth=0.5, linestyle='--')
        if t >= 0:
            ax.axvline(x=t, color='gray', linewidth=1, linestyle=':', alpha=0.7)
            ax.annotate(f'τ=t={t}', xy=(t, 1.1), fontsize=10, ha='center', color='gray')
        
        ax.set_xlim(-2, 4)
        ax.set_ylim(-0.1, 1.3)
        ax.set_xlabel('τ', fontsize=12)
        ax.set_title(title, fontsize=12, fontweight='bold')
        
        # 計算並顯示 y(t) 值
        if t < 0:
            y_val = 0
        else:
            y_val = (1 - np.exp(-3 * t)) / 3
        ax.text(3, 1.1, f'y(t) = {y_val:.3f}', fontsize=11, 
                bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.8))
        
        if idx == 0:
            ax.legend(loc='upper left', fontsize=9)
    
    plt.suptitle('卷積滑動過程: y(t) = x(t) * h(t) = 重疊區域的面積', 
                 fontsize=14, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/conv_step2_sliding.png', dpi=150, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()
    print('已儲存: conv_step2_sliding.png')


def create_complete_process():
    """
    圖 3：完整的卷積過程一覽圖
    """
    fig = plt.figure(figsize=(16, 10))
    gs = GridSpec(3, 4, figure=fig, height_ratios=[1, 1, 1.2])
    
    tau = np.linspace(-2, 4, 500)
    t_plot = np.linspace(-0.5, 3, 500)
    
    # Row 1: 原始訊號
    # (a) x(τ)
    ax1 = fig.add_subplot(gs[0, 0])
    x_tau = np.where(tau >= 0, 1, 0)
    ax1.fill_between(tau, 0, x_tau, alpha=0.4, color='blue')
    ax1.plot(tau, x_tau, 'b-', linewidth=2)
    ax1.axhline(y=0, color='black', linewidth=0.5)
    ax1.axvline(x=0, color='black', linewidth=0.5, linestyle='--')
    ax1.set_xlim(-1, 3)
    ax1.set_ylim(-0.1, 1.3)
    ax1.set_title('(a) 輸入 x(τ) = u(τ)', fontsize=11, fontweight='bold')
    ax1.set_xlabel('τ')
    ax1.grid(True, alpha=0.3)
    
    # (b) h(τ)
    ax2 = fig.add_subplot(gs[0, 1])
    h_tau = np.where(tau >= 0, np.exp(-3 * tau), 0)
    ax2.fill_between(tau, 0, h_tau, alpha=0.4, color='red')
    ax2.plot(tau, h_tau, 'r-', linewidth=2)
    ax2.axhline(y=0, color='black', linewidth=0.5)
    ax2.axvline(x=0, color='black', linewidth=0.5, linestyle='--')
    ax2.set_xlim(-1, 3)
    ax2.set_ylim(-0.1, 1.3)
    ax2.set_title('(b) 脈衝響應 h(τ)', fontsize=11, fontweight='bold')
    ax2.set_xlabel('τ')
    ax2.annotate('尾巴朝右 →', xy=(1.2, 0.15), fontsize=10, color='red')
    ax2.grid(True, alpha=0.3)
    
    # (c) h(-τ) 翻轉
    ax3 = fig.add_subplot(gs[0, 2])
    h_flip = np.where(tau <= 0, np.exp(3 * tau), 0)
    ax3.fill_between(tau, 0, h_flip, alpha=0.4, color='orange')
    ax3.plot(tau, h_flip, 'orange', linewidth=2)
    ax3.axhline(y=0, color='black', linewidth=0.5)
    ax3.axvline(x=0, color='black', linewidth=0.5, linestyle='--')
    ax3.set_xlim(-3, 1)
    ax3.set_ylim(-0.1, 1.3)
    ax3.set_title('(c) 翻轉 h(-τ)', fontsize=11, fontweight='bold')
    ax3.set_xlabel('τ')
    ax3.annotate('← 尾巴朝左', xy=(-1.8, 0.15), fontsize=10, color='orange')
    ax3.grid(True, alpha=0.3)
    
    # (d) 箭頭說明
    ax4 = fig.add_subplot(gs[0, 3])
    ax4.axis('off')
    ax4.text(0.5, 0.7, '卷積步驟:', fontsize=14, fontweight='bold', 
             ha='center', transform=ax4.transAxes)
    ax4.text(0.5, 0.5, '1. 固定 x(τ)', fontsize=12, ha='center', transform=ax4.transAxes)
    ax4.text(0.5, 0.35, '2. 翻轉 h(τ) → h(-τ)', fontsize=12, ha='center', transform=ax4.transAxes)
    ax4.text(0.5, 0.2, '3. 滑動 h(t-τ)', fontsize=12, ha='center', transform=ax4.transAxes)
    ax4.text(0.5, 0.05, '4. 計算重疊面積', fontsize=12, ha='center', transform=ax4.transAxes)
    
    # Row 2: 滑動過程 (4個時間點)
    t_vals = [0, 0.5, 1, 2]
    for i, t in enumerate(t_vals):
        ax = fig.add_subplot(gs[1, i])
        
        # x(τ)
        ax.fill_between(tau, 0, x_tau, alpha=0.3, color='blue')
        ax.plot(tau, x_tau, 'b-', linewidth=1.5)
        
        # h(t-τ)
        h_shifted = np.where(tau <= t, np.exp(-3 * (t - tau)), 0)
        ax.fill_between(tau, 0, h_shifted, alpha=0.3, color='red')
        ax.plot(tau, h_shifted, 'r-', linewidth=1.5)
        
        # 重疊區域
        if t > 0:
            overlap_mask = (tau >= 0) & (tau <= t)
            ax.fill_between(tau[overlap_mask], 0, h_shifted[overlap_mask], 
                           alpha=0.6, color='green')
        
        ax.axhline(y=0, color='black', linewidth=0.5)
        ax.axvline(x=0, color='gray', linewidth=0.5, linestyle='--')
        ax.set_xlim(-1, 3)
        ax.set_ylim(-0.1, 1.3)
        ax.set_title(f't = {t}', fontsize=11, fontweight='bold')
        ax.set_xlabel('τ')
        
        y_val = (1 - np.exp(-3 * t)) / 3 if t >= 0 else 0
        ax.text(2, 1.1, f'y={y_val:.2f}', fontsize=10, 
                bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.8))
        ax.grid(True, alpha=0.3)
    
    # Row 3: 最終結果
    ax_result = fig.add_subplot(gs[2, :])
    y_t = np.where(t_plot >= 0, (1 - np.exp(-3 * t_plot)) / 3, 0)
    ax_result.plot(t_plot, y_t, 'g-', linewidth=3, label='y(t) = (1 - e^(-3t))/3 · u(t)')
    ax_result.fill_between(t_plot, 0, y_t, alpha=0.3, color='green')
    
    # 標示關鍵點
    ax_result.axhline(y=1/3, color='red', linestyle='--', alpha=0.7, label='終值 = 1/3')
    ax_result.axhline(y=0.632/3, color='orange', linestyle=':', alpha=0.7, label='63.2% 終值')
    ax_result.axvline(x=1/3, color='purple', linestyle=':', alpha=0.7)
    ax_result.annotate('τ = 1/3 秒\n(時間常數)', xy=(1/3, 0.02), fontsize=10, 
                      color='purple', ha='center')
    
    # 標示滑動過程對應的點
    for t in [0, 0.5, 1, 2]:
        y_val = (1 - np.exp(-3 * t)) / 3 if t >= 0 else 0
        ax_result.plot(t, y_val, 'ko', markersize=8)
        ax_result.annotate(f'({t}, {y_val:.2f})', xy=(t, y_val + 0.02), 
                          fontsize=9, ha='center')
    
    ax_result.axhline(y=0, color='black', linewidth=0.5)
    ax_result.axvline(x=0, color='black', linewidth=0.5, linestyle='--')
    ax_result.set_xlim(-0.5, 3)
    ax_result.set_ylim(-0.02, 0.4)
    ax_result.set_xlabel('t (時間)', fontsize=12)
    ax_result.set_ylabel('y(t)', fontsize=12)
    ax_result.set_title('(e) 輸出: y(t) = x(t) * h(t)', fontsize=12, fontweight='bold')
    ax_result.legend(loc='right', fontsize=10)
    ax_result.grid(True, alpha=0.3)
    
    plt.suptitle('第 4 題：卷積完整過程圖解', fontsize=16, fontweight='bold', y=1.01)
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/conv_complete_process.png', dpi=150, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()
    print('已儲存: conv_complete_process.png')


def create_animation_frames():
    """
    圖 4：動畫幀風格的滑動過程（更直觀）
    """
    fig, axes = plt.subplots(1, 5, figsize=(18, 4))
    
    tau = np.linspace(-2, 4, 500)
    x_tau = np.where(tau >= 0, 1, 0)
    
    t_values = [-0.3, 0.3, 0.7, 1.2, 2.0]
    
    for idx, t in enumerate(t_values):
        ax = axes[idx]
        
        # 畫 x(τ) - 藍色區域
        ax.fill_between(tau, 0, x_tau, alpha=0.4, color='skyblue')
        ax.plot(tau, x_tau, 'b-', linewidth=2)
        
        # 畫 h(t-τ) - 紅色曲線
        h_shifted = np.where(tau <= t, np.exp(-3 * (t - tau)), 0)
        ax.plot(tau, h_shifted, 'r-', linewidth=2.5)
        ax.fill_between(tau, 0, h_shifted, alpha=0.3, color='red')
        
        # 重疊區域 - 綠色
        if t > 0:
            overlap_mask = (tau >= 0) & (tau <= t)
            if np.any(overlap_mask):
                ax.fill_between(tau[overlap_mask], 0, h_shifted[overlap_mask], 
                               alpha=0.7, color='limegreen')
        
        # 畫箭頭表示滑動方向
        if idx < 4:
            ax.annotate('', xy=(t + 0.5, 0.7), xytext=(t, 0.7),
                       arrowprops=dict(arrowstyle='->', color='black', lw=2))
        
        ax.axhline(y=0, color='black', linewidth=0.8)
        ax.axvline(x=0, color='gray', linewidth=1, linestyle='--')
        ax.axvline(x=t, color='red', linewidth=1.5, linestyle=':', alpha=0.8)
        
        ax.set_xlim(-1.5, 3.5)
        ax.set_ylim(-0.1, 1.4)
        ax.set_xlabel('τ', fontsize=12)
        
        if t < 0:
            status = "沒有重疊"
            y_val = 0
        else:
            y_val = (1 - np.exp(-3 * t)) / 3
            if y_val < 0.1:
                status = "剛開始重疊"
            elif y_val < 0.25:
                status = "重疊中"
            else:
                status = "大量重疊"
        
        ax.set_title(f't = {t:.1f}\n{status}', fontsize=11, fontweight='bold')
        
        # y(t) 值
        ax.text(0.95, 0.95, f'y = {y_val:.3f}', transform=ax.transAxes,
                fontsize=11, ha='right', va='top',
                bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.9))
        
        ax.grid(True, alpha=0.3)
    
    # 添加圖例
    from matplotlib.lines import Line2D
    legend_elements = [
        patches.Patch(facecolor='skyblue', alpha=0.6, label='x(τ) = u(τ)'),
        patches.Patch(facecolor='red', alpha=0.4, label='h(t-τ)'),
        patches.Patch(facecolor='limegreen', alpha=0.7, label='重疊區域 (= y(t))'),
    ]
    fig.legend(handles=legend_elements, loc='upper center', ncol=3, fontsize=11,
               bbox_to_anchor=(0.5, 1.08))
    
    plt.suptitle('h(t-τ) 從左往右滑動，綠色區域面積 = y(t) 的值', 
                 fontsize=14, fontweight='bold', y=1.15)
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/conv_sliding_animation.png', dpi=150, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()
    print('已儲存: conv_sliding_animation.png')


if __name__ == '__main__':
    print('開始生成卷積過程圖解...\n')
    
    create_flip_diagram()
    create_sliding_diagram()
    create_complete_process()
    create_animation_frames()
    
    print('\n全部圖片生成完成！')
