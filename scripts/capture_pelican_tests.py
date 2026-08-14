import os
import shutil
from playwright.sync_api import sync_playwright

out_dir = r"D:\Antigravity_proj\important\personal-web\部落格-Fuwari\public\images\posts\model-eval-2026-08"
os.makedirs(out_dir, exist_ok=True)

# Copy user screenshot
src_ss = r"C:\Users\Typelin_Station\Pictures\Screenshots\螢幕擷取畫面 2026-08-14 134255.png"
dst_ss = os.path.join(out_dir, "deepseek-v4-flash-harness-ui.png")
if os.path.exists(src_ss):
    shutil.copy2(src_ss, dst_ss)
    print("User screenshot copied successfully:", dst_ss)

html_tests = [
    ("pelican-test-01-gpt-56-sol.png", r"D:\Antigravity_proj\outputs\tasks\pelican_bicycle_svg_20260814\index.html"),
    ("pelican-test-02-deepseek-v4-pro.png", r"D:\Antigravity_proj\other\agents\Deepseek_harness\deepseek-v4-pro-pelican-bike.html"),
    ("pelican-test-03-grok-46-build.png", r"D:\Antigravity_proj\other\agents\Deepseek_harness\DeepSeek_PelicanBike.html"),
    ("pelican-test-04-grok-45-console.png", r"D:\Antigravity_proj\other\agents\Deepseek_harness\grok-4.5-pelican-bike.html"),
    ("pelican-test-05-gemini-37-flash.png", r"D:\Antigravity_proj\other\agents\Deepseek_harness\gemini-3.7-flash-high-pelican-bike.html"),
    ("pelican-test-06-deepseek-v4-flash.png", r"D:\Antigravity_proj\other\agents\Deepseek_harness\deepseek-v4-flash-pelican-bike.html")
]

with sync_playwright() as p:
    browser = p.chromium.launch(channel="msedge", headless=True)
    for out_name, file_path in html_tests:
        if os.path.exists(file_path):
            page = browser.new_page(viewport={"width": 1280, "height": 800}, device_scale_factor=1.5)
            normalized_path = file_path.replace("\\", "/")
            url = f"file:///{normalized_path}"
            page.goto(url, wait_until="load", timeout=15000)
            page.wait_for_timeout(2000) # wait for animation
            target_path = os.path.join(out_dir, out_name)
            page.screenshot(path=target_path)
            print(f"Rendered screenshot: {out_name}")
            page.close()
    browser.close()

print("All screenshots successfully generated!")
