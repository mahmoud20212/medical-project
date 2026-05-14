import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth.models import User

# Get or create admin user
admin_user, created = User.objects.get_or_create(username='admin')
admin_user.set_password('admin123')
admin_user.is_staff = True
admin_user.is_superuser = True
admin_user.save()

print('Admin user created/updated with password: admin123')
