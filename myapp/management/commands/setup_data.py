from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from myapp.models import Participant, CleanupEvent
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = 'Setup initial data for EcoBayanihan'

    def handle(self, *args, **options):
        # Create superuser
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@ecobayanihan.com', 'admin123')
            self.stdout.write('✅ Admin user created: admin/admin123')

        # Create test participant
        if not Participant.objects.filter(email='test@example.com').exists():
            participant = Participant.objects.create(
                fullname='Test User',
                username='testuser',
                email='test@example.com',
                contact_number='09123456789',
                address='Test Address, Manila',
                birthdate=datetime(1998, 1, 1).date()
            )
            participant.set_password('test123')
            participant.save()
            self.stdout.write('✅ Test participant created: test@example.com / test123')

        # Create sample cleanup event
        if not CleanupEvent.objects.filter(name='Beach Cleanup Drive').exists():
            event = CleanupEvent.objects.create(
                name='Beach Cleanup Drive',
                description='Join us for a community beach cleanup to protect marine life.',
                place='beach',
                specific_location='Manila Bay, Roxas Boulevard',
                date=datetime.now().date() + timedelta(days=7),
                start_time=datetime.now().time().replace(hour=8, minute=0),
                duration=4,
                max_participants=50,
                points=15
            )
            self.stdout.write('✅ Sample event created: Beach Cleanup Drive')

        self.stdout.write('🌿 Setup complete! You can now login.')
        self.stdout.write('Admin: admin/admin123')
        self.stdout.write('Participant: test@example.com/test123')