from django.core.management.base import BaseCommand
from accounts.models import User
from queues.models import Queue, Service


class Command(BaseCommand):
    help = 'Seed sample data for Navbat.uz'

    def handle(self, *args, **kwargs):
        admin_user, _ = User.objects.get_or_create(
            email='admin@navbat.uz', defaults={'username': 'admin@navbat.uz', 'role': 'admin', 'is_staff': True, 'is_superuser': True}
        )
        admin_user.set_password('Admin123!')
        admin_user.save()

        samples = [
            ('AIIMS Delhi', 'hospital', 'Ansari Nagar, New Delhi - 110029', 45),
            ('Apollo Hospital Sarita Vihar', 'hospital', 'Mathura Road, Delhi - 110076', 35),
            ('State Bank Connaught Place', 'bank', 'Connaught Place, New Delhi', 20),
        ]

        for name, category, location, wait in samples:
            service, _ = Service.objects.get_or_create(
                name=name,
                defaults={
                    'category': category,
                    'location': location,
                    'description': 'Sample service',
                    'created_by': admin_user,
                },
            )
            Queue.objects.get_or_create(service=service, defaults={'estimated_wait_minutes': wait, 'created_by': admin_user})

        self.stdout.write(self.style.SUCCESS('Sample data created successfully.'))
