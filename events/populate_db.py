import os
import random
import django
from faker import Faker

# ---- Setup Django environment ----
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_assignment.settings")
django.setup()

# ---- Import your models ----
from django.contrib.auth.models import User
from events.models import Category, Event

# ---- Initialize Faker ----
fake = Faker()

# ---- Generate fake categories (skip if already exists) ----
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

if Category.objects.exists():
    print("ℹ️  Categories already exist. Skipping category creation.")
else:
    for name, description in categories_data:
        Category.objects.create(name=name, description=description)

    print("✅ 8 fake categories created successfully!")

# ---- Generate fake users ----
users = []
for _ in range(20):
    full_name = fake.name()
    email = fake.unique.email()
    username = email.split("@")[0]

    user = User.objects.create_user(
        username=username,
        email=email,
        password="Password123!"
    )
    user.first_name = full_name.split(" ")[0]
    user.last_name = " ".join(full_name.split(" ")[1:])
    user.save()
    users.append(user)

print("✅ 20 fake users created successfully!")

# ---- Generate fake events ----
categories = list(Category.objects.all())
for _ in range(15):
    event = Event.objects.create(
        name=fake.sentence(nb_words=4).rstrip("."),
        description=fake.paragraph(nb_sentences=3),
        location=fake.city(),
        date=fake.date_between(start_date="-30d", end_date="+60d"),
        time=fake.time(),
        category=random.choice(categories),
    )

    # add random participants
    participant_count = random.randint(3, 10)
    event.participants.add(*random.sample(users, k=participant_count))

print("✅ 15 fake events created successfully!")
