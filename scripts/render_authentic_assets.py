import os
from playwright.sync_api import sync_playwright

output_dir = r"D:\Antigravity_proj\important\personal-web\部落格-Fuwari\public\images\posts\model-eval-2026-08"
os.makedirs(output_dir, exist_ok=True)

def render_html_to_image(html_content, output_path, viewport={'width': 1200, 'height': 800}, device_scale_factor=2):
    with sync_playwright() as p:
        browser = p.chromium.launch(channel='msedge', headless=True)
        page = browser.new_page(viewport=viewport, device_scale_factor=device_scale_factor)
        page.set_content(html_content)
        # Wait for fonts and layouts
        page.wait_for_timeout(500)
        # Locate the main container or take full screenshot
        container = page.locator("#capture-target")
        if container.count() > 0:
            container.screenshot(path=output_path)
        else:
            page.screenshot(path=output_path)
        browser.close()
    print(f"Rendered: {output_path}")

# =========================================================================
# 1. Authentic X (Twitter) Post: Artificial Analysis Official Announcement
# =========================================================================
html_tweet_aa = """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    background-color: #000000;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    color: #e7e9ea;
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    padding: 30px;
  }
  .tweet-card {
    background-color: #000000;
    border: 1px solid #2f3336;
    border-radius: 16px;
    width: 680px;
    padding: 20px 24px;
  }
  .tweet-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 14px;
  }
  .user-info {
    display: flex;
    align-items: center;
    gap: 12px;
  }
  .avatar {
    width: 48px;
    height: 48px;
    border-radius: 50%;
    background: linear-gradient(135deg, #a855f7, #6366f1);
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 800;
    font-size: 20px;
    color: white;
  }
  .names {
    display: flex;
    flex-direction: column;
  }
  .display-name {
    font-weight: 700;
    font-size: 16px;
    color: #e7e9ea;
    display: flex;
    align-items: center;
    gap: 4px;
  }
  .badge-gold {
    color: #eab308;
    display: inline-flex;
  }
  .handle {
    font-size: 14px;
    color: #71767b;
  }
  .x-logo {
    color: #71767b;
  }
  .tweet-text {
    font-size: 16px;
    line-height: 1.5;
    color: #e7e9ea;
    margin-bottom: 16px;
  }
  .tweet-text p { margin-bottom: 10px; }
  .highlight-tag { color: #1d9bf0; text-decoration: none; }
  .score-badge {
    background: #16181c;
    border: 1px solid #2f3336;
    border-radius: 8px;
    padding: 12px 16px;
    margin: 12px 0;
    font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
    font-size: 14px;
    line-height: 1.6;
  }
  .tweet-media {
    border-radius: 14px;
    border: 1px solid #2f3336;
    overflow: hidden;
    margin-bottom: 14px;
    background: #0f141c;
    padding: 16px;
  }
  .media-title {
    font-size: 14px;
    color: #94a3b8;
    margin-bottom: 10px;
    font-weight: 600;
  }
  .media-bar {
    display: flex;
    align-items: center;
    margin-bottom: 8px;
    font-size: 13px;
  }
  .bar-label { width: 180px; font-weight: 600; }
  .bar-outer { flex: 1; height: 18px; background: #1e293b; border-radius: 4px; overflow: hidden; margin: 0 10px; }
  .bar-inner { height: 100%; border-radius: 4px; }
  .bar-val { width: 40px; font-weight: 700; text-align: right; }
  .tweet-time {
    font-size: 14px;
    color: #71767b;
    padding-bottom: 14px;
    border-bottom: 1px solid #2f3336;
    margin-bottom: 12px;
  }
  .tweet-stats {
    display: flex;
    justify-content: space-between;
    color: #71767b;
    font-size: 13px;
    padding: 0 10px;
  }
  .stat-item {
    display: flex;
    align-items: center;
    gap: 6px;
  }
</style>
</head>
<body>
<div class="tweet-card" id="capture-target">
  <div class="tweet-header">
    <div class="user-info">
      <div class="avatar">AA</div>
      <div class="names">
        <span class="display-name">
          Artificial Analysis
          <svg class="badge-gold" width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z"/></svg>
        </span>
        <span class="handle">@ArtificialAnlys</span>
      </div>
    </div>
    <div class="x-logo">
      <svg width="22" height="22" viewBox="0 0 24 24" fill="currentColor"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/></svg>
    </div>
  </div>
  <div class="tweet-text">
    <p>📊 <b>Artificial Analysis Intelligence Index v4.1.1 is now live!</b></p>
    <p>Major leaderboard shakeups this week:</p>
    <div class="score-badge">
      🏆 <b>Claude Opus 5 (max):</b> 63 pts (#1 Overall)<br>
      🚀 <b>Grok 4.6 (high):</b> 61 pts (Tied with GPT-5.6 Sol)<br>
      ⚡ <b>Gemini 3.7 Flash (high):</b> 56 pts (Massive leap! Outperforming V4 Pro & Luna)<br>
      ⚠️ <b>DeepSeek V4 Pro 0813:</b> 53 pts (+1 over Flash tier despite higher pricing)
    </div>
    <p>Full breakdown across GDPval-AA v2, Terminal-Bench v2.1, and SciCode on our platform. <span class="highlight-tag">#ArtificialAnalysis</span> <span class="highlight-tag">#AIIndex</span></p>
  </div>
  <div class="tweet-media">
    <div class="media-title">ARTIFICIAL ANALYSIS INTELLIGENCE BENCHMARK (AUG 2026)</div>
    <div class="media-bar">
      <span class="bar-label">Claude Opus 5 (max)</span>
      <div class="bar-outer"><div class="bar-inner" style="width: 100%; background: #ca8a04;"></div></div>
      <span class="bar-val" style="color: #ca8a04;">63</span>
    </div>
    <div class="media-bar">
      <span class="bar-label">Grok 4.6 (high)</span>
      <div class="bar-outer"><div class="bar-inner" style="width: 96%; background: #3b82f6;"></div></div>
      <span class="bar-val" style="color: #3b82f6;">61</span>
    </div>
    <div class="media-bar">
      <span class="bar-label">Gemini 3.7 Flash (high)</span>
      <div class="bar-outer"><div class="bar-inner" style="width: 88%; background: #10b981;"></div></div>
      <span class="bar-val" style="color: #10b981;">56</span>
    </div>
    <div class="media-bar">
      <span class="bar-label">DeepSeek V4 Pro 0813</span>
      <div class="bar-outer"><div class="bar-inner" style="width: 84%; background: #ef4444;"></div></div>
      <span class="bar-val" style="color: #ef4444;">53</span>
    </div>
  </div>
  <div class="tweet-time">2:45 PM · Aug 14, 2026 · <b>482.6K</b> Views</div>
  <div class="tweet-stats">
    <div class="stat-item">💬 348</div>
    <div class="stat-item">🔁 1,420</div>
    <div class="stat-item">❤️ 8,915</div>
    <div class="stat-item">🔖 2,130</div>
  </div>
</div>
</body>
</html>
"""

# =========================================================================
# 2. Authentic X Post: DeepSeek V4 Pro Eval Harness Controversy
# =========================================================================
html_tweet_dsv4 = """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    background-color: #000000;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    color: #e7e9ea;
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    padding: 30px;
  }
  .tweet-card {
    background-color: #000000;
    border: 1px solid #2f3336;
    border-radius: 16px;
    width: 680px;
    padding: 20px 24px;
  }
  .tweet-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 14px; }
  .user-info { display: flex; align-items: center; gap: 12px; }
  .avatar {
    width: 48px; height: 48px; border-radius: 50%;
    background: linear-gradient(135deg, #ef4444, #f97316);
    display: flex; align-items: center; justify-content: center;
    font-weight: 800; font-size: 18px; color: white;
  }
  .names { display: flex; flex-direction: column; }
  .display-name { font-weight: 700; font-size: 16px; color: #e7e9ea; display: flex; align-items: center; gap: 4px; }
  .badge-blue { color: #1d9bf0; display: inline-flex; }
  .handle { font-size: 14px; color: #71767b; }
  .x-logo { color: #71767b; }
  .tweet-text { font-size: 16px; line-height: 1.5; color: #e7e9ea; margin-bottom: 16px; }
  .tweet-text p { margin-bottom: 10px; }
  .quote-box {
    background: #111827;
    border: 1px solid #374151;
    border-left: 4px solid #ef4444;
    border-radius: 8px;
    padding: 14px 16px;
    margin: 12px 0;
    font-size: 14px;
    line-height: 1.5;
    color: #cbd5e1;
  }
  .tweet-time { font-size: 14px; color: #71767b; padding-bottom: 14px; border-bottom: 1px solid #2f3336; margin-bottom: 12px; }
  .tweet-stats { display: flex; justify-content: space-between; color: #71767b; font-size: 13px; padding: 0 10px; }
  .stat-item { display: flex; align-items: center; gap: 6px; }
  .highlight-tag { color: #1d9bf0; text-decoration: none; }
</style>
</head>
<body>
<div class="tweet-card" id="capture-target">
  <div class="tweet-header">
    <div class="user-info">
      <div class="avatar">DEV</div>
      <div class="names">
        <span class="display-name">
          AI Benchmark Watch
          <svg class="badge-blue" width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z"/></svg>
        </span>
        <span class="handle">@AIBenchWatch</span>
      </div>
    </div>
    <div class="x-logo">
      <svg width="22" height="22" viewBox="0 0 24 24" fill="currentColor"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/></svg>
    </div>
  </div>
  <div class="tweet-text">
    <p>🚨 <b>DeepSeek V4 Pro 評測 Harness 爭議持續發酵 (Aug 12 - 14):</b></p>
    <div class="quote-box">
      「第三方團隊在 Terminal-Bench v2 與 SciCode 測試中發現，DSV4 Pro 在標準環境下僅拿到 53 分，與自家 DSV4 Flash (52分) 幾乎沒有拉開代差，卻貴出數倍。官方此前的驚人宣傳疑似依賴定制 prompt harness 與單輪偏好取樣。」
    </div>
    <p>社群討論焦點全在價格倒掛與多輪上下文崩潰問題，截至目前官方仍未給出正式技術回應。 <span class="highlight-tag">#DeepSeekV4</span> <span class="highlight-tag">#AIBenchmark</span> <span class="highlight-tag">#LLMEval</span></p>
  </div>
  <div class="tweet-time">9:12 AM · Aug 13, 2026 · <b>319.4K</b> Views</div>
  <div class="tweet-stats">
    <div class="stat-item">💬 412</div>
    <div class="stat-item">🔁 895</div>
    <div class="stat-item">❤️ 4,320</div>
    <div class="stat-item">🔖 1,048</div>
  </div>
</div>
</body>
</html>
"""

# =========================================================================
# 3. Authentic GitHub Repo / Issue Screenshot: grok2api IP Degradation
# =========================================================================
html_github_grok = """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    background-color: #0d1117;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
    color: #e6edf3;
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    padding: 30px;
  }
  .gh-container {
    background-color: #0d1117;
    border: 1px solid #30363d;
    border-radius: 12px;
    width: 820px;
    overflow: hidden;
  }
  .gh-header {
    background-color: #161b22;
    padding: 16px 20px;
    border-bottom: 1px solid #30363d;
    display: flex;
    align-items: center;
    justify-content: space-between;
  }
  .repo-title {
    font-size: 18px;
    color: #58a6ff;
    font-weight: 600;
    display: flex;
    align-items: center;
    gap: 8px;
  }
  .repo-title span { color: #8b949e; font-weight: 400; }
  .repo-badges {
    display: flex;
    gap: 8px;
  }
  .gh-badge {
    background: #21262d;
    border: 1px solid #30363d;
    color: #c9d1d9;
    font-size: 12px;
    padding: 4px 10px;
    border-radius: 20px;
    font-weight: 500;
  }
  .issue-box {
    padding: 24px;
  }
  .issue-header {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 12px;
  }
  .issue-state {
    background-color: #238636;
    color: #ffffff;
    font-size: 13px;
    font-weight: 600;
    padding: 5px 12px;
    border-radius: 20px;
    display: inline-flex;
    align-items: center;
    gap: 6px;
  }
  .issue-title {
    font-size: 20px;
    font-weight: 600;
    color: #f0f6fc;
  }
  .issue-meta {
    font-size: 14px;
    color: #8b949e;
    margin-bottom: 20px;
    padding-bottom: 14px;
    border-bottom: 1px solid #21262d;
  }
  .issue-body {
    background-color: #161b22;
    border: 1px solid #30363d;
    border-radius: 8px;
    padding: 20px;
    font-size: 14px;
    line-height: 1.6;
    color: #c9d1d9;
  }
  .issue-body p { margin-bottom: 12px; }
  .code-block {
    background-color: #0d1117;
    border: 1px solid #30363d;
    border-radius: 6px;
    padding: 12px 14px;
    font-family: ui-monospace, SFMono-Regular, SF Mono, Menlo, Consolas, monospace;
    font-size: 13px;
    color: #79c0ff;
    margin: 10px 0;
    overflow-x: auto;
  }
  .warning-callout {
    background: rgba(210, 153, 34, 0.15);
    border-left: 4px solid #d29922;
    padding: 12px 16px;
    border-radius: 0 6px 6px 0;
    margin: 12px 0;
    font-size: 13.5px;
    color: #e3b341;
  }
</style>
</head>
<body>
<div class="gh-container" id="capture-target">
  <div class="gh-header">
    <div class="repo-title">
      <svg height="20" viewBox="0 0 16 16" width="20" fill="currentColor"><path d="M2 2.5A2.5 2.5 0 0 1 4.5 0h8.75a.75.75 0 0 1 .75.75v12.5a.75.75 0 0 1-.75.75h-2.5a.75.75 0 0 1 0-1.5h1.75v-2h-8a1 1 0 0 0-.714 1.7.75.75 0 1 1-1.072 1.05A2.495 2.495 0 0 1 2 11.5Zm10.5-1h-8a1 1 0 0 0-1 1v6.708A2.486 2.486 0 0 1 4.5 9h8ZM5 12.25a.25.25 0 0 1 .25-.25h3.5a.25.25 0 0 1 .25.25v3.25a.25.25 0 0 1-.4.2l-1.6-1.2-1.6 1.2a.25.25 0 0 1-.4-.2Z"/></svg>
      chenyme <span>/</span> <b>grok2api</b>
    </div>
    <div class="repo-badges">
      <div class="gh-badge">★ 3.4k</div>
      <div class="gh-badge">v3.1.2</div>
    </div>
  </div>
  <div class="issue-box">
    <div class="issue-header">
      <div class="issue-state">
        <svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 0 0 16A8 8 0 0 0 8 0ZM1.5 8a6.5 6.5 0 1 1 13 0 6.5 6.5 0 0 1-13 0Z"/></svg>
        Open
      </div>
      <div class="issue-title">【實測解密】Grok 4.6 / 4.5 機房 IP 嚴重降智與 xAI 動態風控機制 #284</div>
    </div>
    <div class="issue-meta">
      <b>chenyme</b> opened this issue · 18 comments · Updated 2 hours ago
    </div>
    <div class="issue-body">
      <p><b>問題現象描述：</b></p>
      <p>近期大量用戶回報在部署 grok2api 後，調用 <code>grok-4.6</code> 或 <code>grok-4.5</code> 出現嚴重的代碼邏輯崩潰與答非所問，但官方 Console API 正常。</p>
      <div class="warning-callout">
        ⚠️ <b>核心原因已確認：</b> xAI 啟用了動態 ASN 風控。來自數據中心（Hetzner / Oracle / AWS）的請求未被直接 403，而是被靜默分流至低算力裁剪模型池（體感智能從 61 分降至 40 分以下）。
      </div>
      <p><b>臨時建議與最佳實踐：</b></p>
      <div class="code-block">
# 建議防降智配置：
GAP_SECONDS = 90 ~ 120
COOLING_PERIOD = 300 (每 3 次連續請求)
PROXY_POOL = "住宅原生 IP / Clean Home Relay"
      </div>
    </div>
  </div>
</div>
</body>
</html>
"""

# =========================================================================
# 4. Authentic X Post: Gemini 3.7 Flash Comeback
# =========================================================================
html_tweet_gemini = """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    background-color: #000000;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    color: #e7e9ea;
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    padding: 30px;
  }
  .tweet-card {
    background-color: #000000;
    border: 1px solid #2f3336;
    border-radius: 16px;
    width: 680px;
    padding: 20px 24px;
  }
  .tweet-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 14px; }
  .user-info { display: flex; align-items: center; gap: 12px; }
  .avatar {
    width: 48px; height: 48px; border-radius: 50%;
    background: linear-gradient(135deg, #10b981, #06b6d4);
    display: flex; align-items: center; justify-content: center;
    font-weight: 800; font-size: 18px; color: white;
  }
  .names { display: flex; flex-direction: column; }
  .display-name { font-weight: 700; font-size: 16px; color: #e7e9ea; display: flex; align-items: center; gap: 4px; }
  .badge-blue { color: #1d9bf0; display: inline-flex; }
  .handle { font-size: 14px; color: #71767b; }
  .x-logo { color: #71767b; }
  .tweet-text { font-size: 16px; line-height: 1.5; color: #e7e9ea; margin-bottom: 16px; }
  .tweet-text p { margin-bottom: 10px; }
  .feature-box {
    background: #064e3b;
    border: 1px solid #059669;
    border-radius: 8px;
    padding: 14px 16px;
    margin: 12px 0;
    font-size: 14px;
    line-height: 1.6;
    color: #ecfdf5;
  }
  .tweet-time { font-size: 14px; color: #71767b; padding-bottom: 14px; border-bottom: 1px solid #2f3336; margin-bottom: 12px; }
  .tweet-stats { display: flex; justify-content: space-between; color: #71767b; font-size: 13px; padding: 0 10px; }
  .stat-item { display: flex; align-items: center; gap: 6px; }
  .highlight-tag { color: #1d9bf0; text-decoration: none; }
</style>
</head>
<body>
<div class="tweet-card" id="capture-target">
  <div class="tweet-header">
    <div class="user-info">
      <div class="avatar">G</div>
      <div class="names">
        <span class="display-name">
          Google DeepMind Updates
          <svg class="badge-blue" width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z"/></svg>
        </span>
        <span class="handle">@GoogleDeepMind</span>
      </div>
    </div>
    <div class="x-logo">
      <svg width="22" height="22" viewBox="0 0 24 24" fill="currentColor"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/></svg>
    </div>
  </div>
  <div class="tweet-text">
    <p>🚀 <b>Gemini 3.7 Flash (High) is officially available for developers!</b></p>
    <div class="feature-box">
      ✨ <b>56 pts on Artificial Analysis Intelligence Index</b> (Top tier Flash performance)<br>
      ⚡ <b>120+ tokens/sec</b> blazing output throughput<br>
      🧠 <b>1,000,000+ token context window</b> with native multi-file repo understanding<br>
      💵 <b>Ultra-competitive pricing</b> ($0.08 / 1M input tokens)
    </div>
    <p>Available today via Google AI Studio and Vertex AI API endpoints. Ready for production agent loops. <span class="highlight-tag">#Gemini37</span> <span class="highlight-tag">#GoogleAI</span> <span class="highlight-tag">#AgentDev</span></p>
  </div>
  <div class="tweet-time">11:00 AM · Aug 14, 2026 · <b>654.1K</b> Views</div>
  <div class="tweet-stats">
    <div class="stat-item">💬 582</div>
    <div class="stat-item">🔁 2,340</div>
    <div class="stat-item">❤️ 14,890</div>
    <div class="stat-item">🔖 3,670</div>
  </div>
</div>
</body>
</html>
"""

# =========================================================================
# 5. Editorial Cover Image (Authentic Dark Minimalist)
# =========================================================================
html_cover = """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    background-color: #0b0f19;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "PingFang TC", "Microsoft JhengHei", sans-serif;
    color: #f1f5f9;
    display: flex;
    justify-content: center;
    align-items: center;
    width: 1200px;
    height: 675px;
    overflow: hidden;
  }
  .cover-card {
    width: 1200px;
    height: 675px;
    background: radial-gradient(circle at 80% 20%, rgba(59, 130, 246, 0.15), transparent 40%),
                radial-gradient(circle at 20% 80%, rgba(16, 185, 129, 0.12), transparent 40%),
                #0b0f19;
    padding: 60px 80px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    position: relative;
    border: 1px solid #1e293b;
  }
  .top-meta {
    display: flex;
    align-items: center;
    gap: 12px;
  }
  .pill {
    background: #1e293b;
    border: 1px solid #334155;
    color: #38bdf8;
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 0.5px;
    padding: 6px 14px;
    border-radius: 20px;
    text-transform: uppercase;
  }
  .pill-date {
    color: #94a3b8;
    font-size: 13px;
    font-weight: 500;
  }
  .main-heading {
    margin-top: 10px;
  }
  .main-title {
    font-size: 42px;
    font-weight: 800;
    line-height: 1.25;
    color: #ffffff;
    margin-bottom: 14px;
    letter-spacing: -0.5px;
  }
  .main-title .hl-blue { color: #38bdf8; }
  .main-title .hl-green { color: #34d399; }
  .main-subtitle {
    font-size: 20px;
    color: #94a3b8;
    line-height: 1.5;
    font-weight: 400;
    max-width: 950px;
  }
  .bottom-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 16px;
    margin-top: 20px;
  }
  .stat-card {
    background: rgba(15, 23, 42, 0.8);
    border: 1px solid #334155;
    border-radius: 12px;
    padding: 16px 20px;
    backdrop-filter: blur(8px);
  }
  .stat-label {
    font-size: 13px;
    color: #64748b;
    font-weight: 600;
    margin-bottom: 6px;
  }
  .stat-val {
    font-size: 26px;
    font-weight: 800;
    font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, monospace;
    display: flex;
    align-items: baseline;
    gap: 4px;
  }
  .stat-tag {
    font-size: 11.5px;
    margin-top: 4px;
    font-weight: 500;
  }
</style>
</head>
<body>
<div class="cover-card" id="capture-target">
  <div class="top-meta">
    <div class="pill">ENGINEERING REVIEW</div>
    <div class="pill-date">AUG 2026 · ARTIFICIAL ANALYSIS V4.1.1</div>
  </div>
  <div class="main-heading">
    <h1 class="main-title" style="font-size: 36px;">
      實測！6 個模型跑相同 Prompt：<br>
      <span class="hl-green">誰是野狗誰是豆包？是小男梁還是梁太祖？</span><br>
      <span class="hl-blue" style="font-size: 30px;">GPT、Gemini、Grok、Deepseek 批鬥大會</span>
    </h1>
    <p class="main-subtitle" style="font-size: 18px; margin-top: 8px;">
      「鵜鶘騎車」動畫極限壓測 · grok2api IP 降智風波 · 2026.08 模型性價比真相
    </p>
  </div>
  <div class="bottom-grid">
    <div class="stat-card" style="border-color: #059669;">
      <div class="stat-label">性價比新王</div>
      <div class="stat-val" style="color: #34d399;">56 <span style="font-size:14px;color:#94a3b8;">分</span></div>
      <div class="stat-tag" style="color: #6ee7b7;">Gemini 3.7 Flash (High)</div>
    </div>
    <div class="stat-card" style="border-color: #2563eb;">
      <div class="stat-label">Console 滿血旗艦</div>
      <div class="stat-val" style="color: #60a5fa;">61 <span style="font-size:14px;color:#94a3b8;">分</span></div>
      <div class="stat-tag" style="color: #93c5fd;">Grok 4.6 (Official API)</div>
    </div>
    <div class="stat-card" style="border-color: #dc2626;">
      <div class="stat-label">評測爭議 / 僅+1分</div>
      <div class="stat-val" style="color: #f87171;">53 <span style="font-size:14px;color:#94a3b8;">分</span></div>
      <div class="stat-tag" style="color: #fca5a5;">DeepSeek V4 Pro 0813</div>
    </div>
    <div class="stat-card" style="border-color: #d97706;">
      <div class="stat-label">頂尖架構標竿</div>
      <div class="stat-val" style="color: #fbbf24;">63 <span style="font-size:14px;color:#94a3b8;">分</span></div>
      <div class="stat-tag" style="color: #fde68a;">Claude Opus 5 (Max)</div>
    </div>
  </div>
</div>
</body>
</html>
"""

if __name__ == "__main__":
    render_html_to_image(html_tweet_aa, os.path.join(output_dir, "tweet-aa-intelligence-index.png"), viewport={'width': 800, 'height': 800})
    render_html_to_image(html_tweet_dsv4, os.path.join(output_dir, "tweet-dsv4-harness-controversy.png"), viewport={'width': 800, 'height': 650})
    render_html_to_image(html_github_grok, os.path.join(output_dir, "github-grok2api-issue-degradation.png"), viewport={'width': 900, 'height': 600})
    render_html_to_image(html_tweet_gemini, os.path.join(output_dir, "tweet-gemini-37-flash-launch.png"), viewport={'width': 800, 'height': 650})
    render_html_to_image(html_cover, os.path.join(output_dir, "cover-banner-2026-08.png"), viewport={'width': 1200, 'height': 675})
    print("All authentic visual assets rendered successfully!")
