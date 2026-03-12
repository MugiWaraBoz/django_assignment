import os
import random
import django
from faker import Faker

# ---- Setup Django environment ----
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "event_management.settings")
django.setup()

# ---- Import models ----
# CustomUser is now AUTH_USER_MODEL (user.CustomUser), has profile_images + bio fields
from django.contrib.auth.models import Group
from django.core.files import File
from django.conf import settings
from events.models import Category, Event, RSVP
from user.models import CustomUser

# ---- Initialize Faker ----
fake = Faker()

# ---- Collect available images ----
allowed_exts = {".png", ".jpg", ".jpeg", ".webp"}
image_paths = []
profile_image_paths = []

media_event_dir   = os.path.join(settings.MEDIA_ROOT, "event_images")
media_profile_dir = os.path.join(settings.MEDIA_ROOT, "profile_images")
events_images_dir = os.path.join(os.path.dirname(__file__), "images")
demo_images_dir   = os.path.join(settings.BASE_DIR, "demo_images")

for image_dir in [media_event_dir, events_images_dir, demo_images_dir]:
    if os.path.isdir(image_dir):
        for filename in os.listdir(image_dir):
            if os.path.splitext(filename)[1].lower() in allowed_exts:
                image_paths.append(os.path.join(image_dir, filename))

for filename in (os.listdir(media_profile_dir) if os.path.isdir(media_profile_dir) else []):
    if os.path.splitext(filename)[1].lower() in allowed_exts:
        profile_image_paths.append(os.path.join(media_profile_dir, filename))

# Fall back to event images for profile pictures if no dedicated ones exist
if not profile_image_paths:
    profile_image_paths = image_paths

# ---- Generate fake categories ----
categories_data = [
    ("Technology",    "Events related to technology, programming, and innovation"),
    ("Sports",        "Athletic events, competitions, and sports activities"),
    ("Music",         "Concerts, festivals, and musical performances"),
    ("Art & Culture", "Art exhibitions, cultural events, and creative workshops"),
    ("Business",      "Conferences, networking events, and business seminars"),
    ("Education",     "Workshops, training sessions, and educational seminars"),
    ("Food & Beverage","Food festivals, cooking classes, and dining events"),
    ("Entertainment", "Comedy shows, movie screenings, and entertainment events"),
]

if Category.objects.exists():
    print("ℹ️  Categories already exist. Skipping category creation.")
else:
    for name, description in categories_data:
        Category.objects.create(name=name, description=description)
    print("✅ 8 categories created.")

# ---- Ensure all three groups exist ----
admin_group,       _ = Group.objects.get_or_create(name="Admin")
organizer_group,   _ = Group.objects.get_or_create(name="Organizer")
participant_group, _ = Group.objects.get_or_create(name="Participants")

# ---- Generate fake users ----
# CustomUser fields beyond AbstractUser: profile_images (ImageField), bio (TextField)
users = []
DEFAULT_PASSWORD = "Password123!"

for _ in range(20):
    full_name  = fake.name()
    first_name = full_name.split()[0]
    last_name  = " ".join(full_name.split()[1:])
    email      = fake.unique.email()
    username   = email.split("@")[0]

    user, created = CustomUser.objects.get_or_create(
        username=username,
        defaults={
            "email":      email,
            "first_name": first_name,
            "last_name":  last_name,
            "bio":        fake.paragraph(nb_sentences=2),
            "is_active":  True,
        }
    )

    if created:
        user.set_password(DEFAULT_PASSWORD)

        # Profile image stored directly on CustomUser.profile_images
        if profile_image_paths:
            img_path = random.choice(profile_image_paths)
            with open(img_path, "rb") as f:
                user.profile_images.save(os.path.basename(img_path), File(f), save=False)

        user.save()
        print(f"✅ Created: {username} | Password: {DEFAULT_PASSWORD}")
    else:
        print(f"ℹ️  Already exists: {username}")

    users.append(user)

# ---- Assign users to groups ----
# Split: 1 admin, ~25% organizers, rest participants
random.shuffle(users)

admin_users       = users[:1]
organizer_users   = users[1 : max(2, len(users) // 4)]
participant_users = users[max(2, len(users) // 4):]

for u in admin_users:
    u.groups.set([admin_group])

for u in organizer_users:
    u.groups.set([organizer_group])

for u in participant_users:
    u.groups.set([participant_group])

print(f"✅ Groups assigned — Admin: {len(admin_users)}, Organizers: {len(organizer_users)}, Participants: {len(participant_users)}")

# ---- Generate fake events ----
categories = list(Category.objects.all())

for _ in range(15):
    event = Event.objects.create(
        name        = fake.sentence(nb_words=4).rstrip("."),
        description = fake.paragraph(nb_sentences=3),
        location    = fake.city(),
        date        = fake.date_between(start_date="-30d", end_date="+60d"),
        time        = fake.time(),
        category    = random.choice(categories),
    )

    # Assign organizers (from Organizer group pool)
    org_pool = organizer_users if organizer_users else users
    event.organizers.set(
        random.sample(org_pool, k=min(random.randint(1, 3), len(org_pool)))
    )

    # Assign event image
    if image_paths:
        img_path = random.choice(image_paths)
        with open(img_path, "rb") as f:
            event.image.save(os.path.basename(img_path), File(f), save=True)

    # Create RSVPs from participant pool
    prt_pool = participant_users if participant_users else users
    rsvp_count = random.randint(3, min(10, len(prt_pool)))
    for participant in random.sample(prt_pool, k=rsvp_count):
        RSVP.objects.get_or_create(
            event=event,
            participants=participant,
            defaults={"is_going": random.choice([True, False])},
        )

    print(f"📅 Event '{event.name}' — {rsvp_count} RSVPs")

print("✅ 15 fake events created successfully!")
