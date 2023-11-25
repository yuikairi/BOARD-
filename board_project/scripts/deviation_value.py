import requests
from bs4 import BeautifulSoup
import csv
from django.core.management.base import BaseCommand
from boards.models import School  # Import your School model

class Command(BaseCommand):
    help = 'Populate deviation values for schools'

    def handle(self, *args, **kwargs):
        # Your web scraping logic here
        urls = ['https://www.minkou.jp/hischool/search/pref=aichi/',
                'https://www.minkou.jp/hischool/search/pref=gifu/',
                'https://www.minkou.jp/hischool/search/pref=mie/']

        for url in urls:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')

            for item in soup.find_all('div', class_='Deviation_value'):
                school_name = item.get_text(strip=True)
                deviation_value = int(school_name.split(':')[-1].strip())  

               
                try:
                    school = School.objects.get(name=school_name)
                    school.deviation_value = deviation_value
                    school.save()
                    self.stdout.write(self.style.SUCCESS(f'Successfully updated {school_name}'))
                except School.DoesNotExist:
                    self.stdout.write(self.style.WARNING(f'School {school_name} not found in the database'))

        self.stdout.write(self.style.SUCCESS('Deviation values updated successfully'))
