import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'personal_blog.settings')
django.setup()

from django.core.management import call_command

if __name__ == '__main__':
    print("Running database migrations...")
    call_command('migrate')
    print("Seeding blog data...")
    call_command('seed_blog')
    print("Database is ready! You can now run: python manage.py runserver")
