import os
import django
from faker import Faker

# ---- Setup Django environment ----
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_assignment.settings")
django.setup()

# ---- Import your models ----
from events.models import Participant, Category

# ---- Initialize Faker ----
fake = Faker()

# ---- Generate 50 fake participants ----
for _ in range(50):
    name = fake.name()
    email = fake.unique.email()
    
    # Create and save participant
    Participant.objects.create(name=name, email=email)

print("✅ 50 fake participants created successfully!")

# ---- Generate fake categories ----
categories_data = [
    ("Technology", "Events related to technology, programming, and innovation"),
    ("Sports", "Athletic events, competitions, and sports activities"),
    ("Music", "Concerts, festivals, and musical performances"),
    ("Art & Culture", "Art exhibitions, cultural events, and creative workshops"),
    ("Business", "Conferences, networking events, and business seminars"),
    ("Education", "Workshops, training sessions, and educational seminars"),
    ("Food & Beverage", "Food festivals, cooking classes, and dining events"),
    ("Entertainment", "Comedy shows, movie screenings, and entertainment events"),
]

for name, description in categories_data:
    Category.objects.create(name=name, description=description)

print("✅ 8 fake categories created successfully!")
