import requests
from bs4 import BeautifulSoup
import csv
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Your script description here'

    def handle(self, *args, **kwargs):
        # URLリスト
        urls = ['https://www.minkou.jp/hischool/search/pref=aichi/',
                'https://www.minkou.jp/hischool/search/pref=gifu/',
                'https://www.minkou.jp/hischool/search/pref=mie/']

        # データを取得してCSVに書き込む
        for url in urls:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')

            data_list = []
            for item in soup.find_all('div', class_='Deviation_value'):
                data_list.append(item.text)

            # 各URLから取得したデータを別のCSVファイルに書き込む場合
            with open('output.csv', 'a', newline='') as csv_file:
                writer = csv.writer(csv_file)
                for item in data_list:
                    writer.writerow([item])

        self.stdout.write(self.style.SUCCESS('Script executed successfully'))
