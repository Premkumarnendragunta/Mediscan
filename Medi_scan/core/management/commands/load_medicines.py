import csv
from django.core.management.base import BaseCommand
from core.models import Medicine
from django.conf import settings
from pathlib import Path

class Command(BaseCommand):
    help = "Load sample medicines into DB from CSV"

    def handle(self, *args, **kwargs):
        csv_path = Path(settings.BASE_DIR) / 'core' / 'data' / 'medicines_sample.csv'
        count = 0
        with open(csv_path, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                obj, created = Medicine.objects.get_or_create(
                    name=row['name'].strip(),
                    defaults={
                        'generic_name': row.get('generic_name', '').strip(),
                        'uses': row.get('uses', '').strip(),
                        'side_effects': row.get('side_effects', '').strip(),
                    }
                )
                if created:
                    count += 1
        self.stdout.write(self.style.SUCCESS(f'Loaded {count} medicines from {csv_path}'))
