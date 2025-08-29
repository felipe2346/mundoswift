from django.core.management.base import BaseCommand
import csv
from account.models import CountryLocation  # Change if needed

class Command(BaseCommand):
    help = 'Load countries from CSV into CountryLocation model'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file')

    def handle(self, *args, **options):
        csv_file = options['csv_file']
        with open(csv_file, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # Skip the header row
            count = 0
            for row in reader:
                print(row)
                country_name, lat, lng = row
                CountryLocation.objects.update_or_create(
                    country_name=country_name.title(),
                    defaults={'latitude': float(lat), 'longitude': float(lng)}
                )
                count += 1
        self.stdout.write(self.style.SUCCESS(f'Successfully loaded {count} countries'))
