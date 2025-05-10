## README: 4chan Thread Image Downloader

This script automates the download of images from 4chan threads using Python (with Playwright) and a running Chromium browser instance with remote debugging enabled.

### Note
- You must manually solve CAPTCHA in Chromium (if needed) before images can load.

### Requirements
- Ubuntu/Debian-based OS
- Python 3.13
- `chromium` Browser to load pages
- `playwright` Python package with Chromium support

### Setup Instructions

1. Clone This Repo
```bash
https://github.com/canHazUsername/4chan-Image-Downloader.git
cd 4chan-Image-Downloader
```

2. Install Chromium
```bash
sudo apt update
sudo apt install chromium-browser
```

3. Install Python Virtual Environment and Dependencies
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### How to Use

1. Prepare `urls.txt`
Create/Edit `urls.txt` file in the script directory. Each line should contain **one 4chan thread URL**, like this:

```
https://boards.4chan.org/hr/thread/1234
https://boards.4chan.org/hr/thread/5678
...
```

2. Launch Chromium with Remote Debugging
```bash
sh launch_chromium.sh
```

You must leave this browser window open. Manually solve any CAPTCHA if/when prompted.

3. Run the Script
```bash
python main.py
```

The script will:
- Connect to the open Chromium tab
- Navigate to the first URL
- Extract the name of the thread (truncated to 32 chars and sanitized to a friendly directory name format)
- Download all thread images
- Repeat for each thread in `urls.txt`

### Output

Images will be saved under `downloaded_images/<sanitized-thread-title>/`

Each thread gets its own folder.
