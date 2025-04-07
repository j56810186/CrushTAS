#!/usr/bin/env python
import asyncio
from pathlib import Path

import arrow

from utils import get_MJPEG_URLs


# MJPEG URLs
ROADNAME_MJPEG_URL = get_MJPEG_URLs()

# Save directory
SAVE_DIR = Path('.') / 'media' / 'cctv'
if not SAVE_DIR.exists():
    SAVE_DIR.mkdir(parents=True, exist_ok=True)


async def capture_frame(url):
    '''使用 FFmpeg 擷取 MJPEG 串流單張圖片'''
    output_dir = SAVE_DIR / url.split('/')[-1]
    timestamp = arrow.now().strftime('%Y%m%d_%H%M%S')
    output_file = output_dir / f'{timestamp}-%04d.jpg'

    # 使用 asyncio.create_subprocess_exec 來非同步執行 FFmpeg
    proc = await asyncio.create_subprocess_exec(
        'ffmpeg', '-i', url, '-vf', 'fps=30', str(output_file),
        stdout=asyncio.subprocess.DEVNULL,
        stderr=asyncio.subprocess.DEVNULL
    )
    await proc.wait()

async def main():
    # 建立所有必要的目錄
    for roadname, url in ROADNAME_MJPEG_URL:
        output_dir = SAVE_DIR / url.split('/')[-1]
        if not output_dir.exists():
            output_dir.mkdir(parents=True, exist_ok=True)

    # 同時啟動所有擷取任務
    tasks = [capture_frame(url) for roadname, url in ROADNAME_MJPEG_URL]
    await asyncio.gather(*tasks)

if __name__ == '__main__':
    asyncio.run(main())
