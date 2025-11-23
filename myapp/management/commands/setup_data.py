from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from myapp.models import Volunteer, CleanupEvent
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = 'Setup initial data for EcoBayanihan'

    def handle(self, *args, **options):
        # Create superuser
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@ecobayanihan.com', 'admin123')
            self.stdout.write('✅ Admin user created: admin/admin123')

        # Create test volunteer
        if not Volunteer.objects.filter(email='test@example.com').exists():
            volunteer = Volunteer.objects.create(
                first_name='Test',
                last_name='User',
                email='test@example.com',
                phone='09123456789',
                address='Test Address',
                age=25,
                gender='Male'
            )
            self.stdout.write('✅ Test volunteer created: test@example.com')

        # Create sample cleanup event
        if not CleanupEvent.objects.filter(name='Beach Cleanup Drive').exists():
            event = CleanupEvent.objects.create(
                name='Beach Cleanup Drive',
                description='Join us for a community beach cleanup to protect marine life.',
                location='Manila Bay',
                date=datetime.now().date() + timedelta(days=7),
                time=datetime.now().time().replace(hour=8, minute=0),
                max_participants=50,
                points_reward=10
            )
            self.stdout.write('✅ Sample event created: Beach Cleanup Drive')

        self.stdout.write('🌿 Setup complete! You can now login.')