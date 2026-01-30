import os
import django
from faker import Faker

# ---- Setup Django environment ----
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_assignment.settings")
django.setup()

# ---- Import your model ----
from events.models import Participant

# ---- Initialize Faker ----
fake = Faker()

# ---- Generate 50 fake participants ----
for _ in range(50):
    name = fake.name()
    email = fake.unique.email()
    
    # Create and save participant
    Participant.objects.create(name=name, email=email)

print("✅ 50 fake participants created successfully!")
