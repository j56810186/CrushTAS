import csv
from pathlib import Path

import requests
from lxml import html


CCTV_PATH = Path('cctv_fetcher/臺中市交通影像靜態資訊.csv')


def get_MJPEG_URLs() -> list[tuple[str, str]]:
    '''取得 MJPEG 串流 URL'''
    # Load CCTV data
    with open(CCTV_PATH, 'r', encoding='UTF-8') as f:
        reader = csv.reader(f)
        csv_data = [row for row in reader if row[-1]][1:]
    raw_urls = [(row[1], row[4]) for row in csv_data]  # (地點, URL)

    result = []
    for road_name, r_url in raw_urls:
        response = requests.get(r_url)
        tree = html.fromstring(response.text)
        url = tree.xpath('//td/img')[0].get('src')
        result.append((road_name, url))

    return result




