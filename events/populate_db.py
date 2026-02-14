import os
import random
import django
from faker import Faker

# ---- Setup Django environment ----
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "event_management.settings")
django.setup()

# ---- Import your models ----
from django.contrib.auth.models import User
from django.core.files import File
from django.conf import settings
from events.models import Category, Event, RSVP

# ---- Initialize Faker ----
fake = Faker()

# ---- Collect available images (media + events/images) ----
allowed_exts = {".png", ".jpg", ".jpeg", ".webp"}
image_paths = []

media_images_dir = os.path.join(settings.MEDIA_ROOT, "event_images")
events_images_dir = os.path.join(os.path.dirname(__file__), "images")

for image_dir in [media_images_dir, events_images_dir]:
    if os.path.isdir(image_dir):
        for filename in os.listdir(image_dir):
            ext = os.path.splitext(filename)[1].lower()
            if ext in allowed_exts:
                image_paths.append(os.path.join(image_dir, filename))

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

    # add random image if available
    if image_paths:
        image_path = random.choice(image_paths)
        with open(image_path, "rb") as image_file:
            event.image.save(os.path.basename(image_path), File(image_file), save=True)

    # add random participants via RSVP
    participant_count = random.randint(3, 10)
    for participant in random.sample(users, k=participant_count):
        RSVP.objects.create(
            event=event,
            participants=participant,
            is_going=True,
        )

print("✅ 15 fake events created successfully!")
