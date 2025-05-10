import os
import re
import urllib.request
import asyncio
from playwright.async_api import async_playwright

# ==== USER CONFIG ====
urls_file = "urls.txt"  # Contains list of thread page URLs
download_root = "downloaded_images"
debug_port = 9222  # Chromium must be launched with remote debugging enabled
# =====================

def sanitize_thread_name(raw_title):
    raw_title = raw_title.strip()[:32]
    return re.sub(r"[^\w\s.-]", "", raw_title).strip()

async def process_thread(page, thread_url):
    print(f"\nNavigating to: {thread_url}")
    await page.goto(thread_url)

    print("Waiting for image links to load (CAPTCHA, slow images, etc)...")
    await page.wait_for_selector("a.fileThumb", timeout=0)

    print("Extracting thread title...")
    subject = await page.query_selector("span.subject")
    raw_title = await subject.inner_text() if subject else "untitled_thread"
    folder_name = sanitize_thread_name(raw_title)
    print(f"Thread folder: {folder_name}")

    script_dir = os.path.dirname(os.path.abspath(__file__))
    download_path = os.path.join(script_dir, download_root, folder_name)
    os.makedirs(download_path, exist_ok=True)

    elements = await page.query_selector_all("a.fileThumb")
    if not elements:
        print("No images found.")
        return

    print(f"Found {len(elements)} image(s)")

    for i, el in enumerate(elements):
        href = await el.get_attribute("href")
        if not href:
            continue

        if href.startswith("//"):
            href = "https:" + href

        filename = os.path.basename(href)
        path = os.path.join(download_path, filename)

        print(f"[{i + 1}/{len(elements)}] Downloading {filename}...", end=" ", flush=True)
        try:
            urllib.request.urlretrieve(href, path)
            print("OK")
        except Exception as e:
            print(f"FAILED: {e}")

    print(f"Done with: {thread_url}")
    print(f"Saved to: {download_path}")

async def run():
    # Read all thread URLs from file
    try:
        with open(urls_file, "r") as f:
            thread_urls = [line.strip() for line in f if line.strip()]
    except Exception as e:
        print(f"Failed to read {urls_file}: {e}")
        return

    if not thread_urls:
        print("No URLs found in urls.txt.")
        return

    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp(f"http://localhost:{debug_port}")
        context = await browser.new_context()
        page = await context.new_page()

        for thread_url in thread_urls:
            try:
                await process_thread(page, thread_url)
            except Exception as e:
                print(f"Failed to process {thread_url}: {e}")

        await context.close()

asyncio.run(run())
