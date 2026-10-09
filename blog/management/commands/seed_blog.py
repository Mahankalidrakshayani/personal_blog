import os
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.files.base import ContentFile
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import datetime

from blog.models import Category, Tag, Post, Comment, Profile


def generate_banner_image(title, subtitle, bg_color_1=(15, 23, 42), bg_color_2=(13, 148, 136)):
    """
    Generate a modern gradient banner image using Pillow.
    """
    width, height = 1200, 630
    img = Image.new("RGB", (width, height))
    draw = ImageDraw.Draw(img)

    # Linear gradient interpolation
    for y in range(height):
        ratio = y / height
        r = int(bg_color_1[0] * (1 - ratio) + bg_color_2[0] * ratio)
        g = int(bg_color_1[1] * (1 - ratio) + bg_color_2[1] * ratio)
        b = int(bg_color_1[2] * (1 - ratio) + bg_color_2[2] * ratio)
        draw.line([(0, y), (width, y)], fill=(r, g, b))

    # Decorative geometric accent shapes
    draw.ellipse([850, -100, 1300, 350], outline=(255, 255, 255, 30), width=4)
    draw.ellipse([950, -50, 1350, 350], fill=(20, 184, 166))
    draw.rectangle([60, 50, 140, 56], fill=(249, 115, 22))

    # Text drawings
    draw.text((60, 80), "DEVBLOG • FEATURED STORY", fill=(45, 212, 191))
    draw.text((60, 140), title[:45], fill=(255, 255, 255))
    if len(title) > 45:
        draw.text((60, 200), title[45:90], fill=(255, 255, 255))
    draw.text((60, 290), subtitle, fill=(203, 213, 225))
    draw.text((60, 540), "READ MORE AT DEVBLOG.IO", fill=(251, 146, 60))

    buffer = BytesIO()
    img.save(buffer, format='JPEG', quality=90)
    return ContentFile(buffer.getvalue())


class Command(BaseCommand):
    help = "Seed database with initial categories, tags, demo authors, sample rich posts, and comments"

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("Seeding My Personal Blog database..."))

        # 1. Create Superuser / Admin
        admin_user, created = User.objects.get_or_create(
            username="admin",
            defaults={
                'email': "admin@personalblog.dev",
                'first_name': "Alex",
                'last_name': "Rivers",
                'is_staff': True,
                'is_superuser': True,
            }
        )
        if created:
            admin_user.set_password("admin123")
            admin_user.save()
            self.stdout.write(self.style.SUCCESS("Created superuser: admin (password: admin123)"))
        else:
            admin_user.set_password("admin123")
            admin_user.save()

        # Update Admin profile
        profile, _ = Profile.objects.get_or_create(user=admin_user)
        profile.headline = "Lead Software Architect & Tech Writer"
        profile.bio = "Obsessed with clean architecture, distributed systems, Python internals, and responsive user experiences."
        profile.website = "https://personalblog.dev"
        profile.github = "https://github.com/alexrivers"
        profile.twitter = "https://twitter.com/alexrivers_dev"
        profile.linkedin = "https://linkedin.com/in/alexrivers"
        profile.save()

        # 2. Create Second Author (Sarah)
        sarah_user, created = User.objects.get_or_create(
            username="sarah_dev",
            defaults={
                'email': "sarah@personalblog.dev",
                'first_name': "Sarah",
                'last_name': "Chen",
            }
        )
        if created:
            sarah_user.set_password("password123")
            sarah_user.save()
            self.stdout.write(self.style.SUCCESS("Created author: sarah_dev (password: password123)"))

        profile2, _ = Profile.objects.get_or_create(user=sarah_user)
        profile2.headline = "Frontend Specialist & Design Engineer"
        profile2.bio = "Designing intuitive interfaces, color systems, and lightning-fast web experiences."
        profile2.github = "https://github.com/sarahchen"
        profile2.twitter = "https://twitter.com/sarahchen_ui"
        profile2.save()

        # 3. Create Categories
        categories_data = [
            {
                'name': "Python & Backend",
                'description': "Deep dives into Python 3, Django ORM, REST architectures, and backend patterns.",
                'color': "#0d9488",
                'icon': "bi-filetype-py"
            },
            {
                'name': "Frontend & UI Design",
                'description': "Modern CSS techniques, color theory, animations, and accessible web components.",
                'color': "#7c3aed",
                'icon': "bi-palette"
            },
            {
                'name': "System Architecture",
                'description': "Database indexing, scalability, fault tolerance, and software engineering principles.",
                'color': "#ea580c",
                'icon': "bi-diagram-3"
            },
            {
                'name': "DevOps & Cloud",
                'description': "Containerization with Docker, CI/CD automation, and deployment strategies.",
                'color': "#0284c7",
                'icon': "bi-cloud-arrow-up"
            },
            {
                'name': "Productivity & Career",
                'description': "Engineering habits, developer workflows, code review wisdom, and growth.",
                'color': "#10b981",
                'icon': "bi-lightning-charge"
            },
        ]

        cat_objs = {}
        for cdata in categories_data:
            cat, _ = Category.objects.get_or_create(
                name=cdata['name'],
                defaults={
                    'description': cdata['description'],
                    'color': cdata['color'],
                    'icon': cdata['icon'],
                }
            )
            cat_objs[cat.name] = cat

        # 4. Create Tags
        tag_names = ["Python", "Django", "WebDev", "CSS", "Architecture", "Docker", "Database", "Performance", "Tutorial", "Security"]
        tag_objs = {}
        for tname in tag_names:
            tag, _ = Tag.objects.get_or_create(name=tname)
            tag_objs[tname] = tag

        # 5. Create Sample Blog Posts
        posts_data = [
            {
                'title': "Building High-Performance REST APIs with Django and Modern Python",
                'slug': "building-high-performance-rest-apis-django",
                'author': admin_user,
                'category': cat_objs["Python & Backend"],
                'tags': ["Python", "Django", "Performance", "Tutorial"],
                'status': 'published',
                'is_featured': True,
                'views_count': 1420,
                'published_at': timezone.now() - datetime.timedelta(days=2),
                'summary': "A comprehensive guide to optimizing Django applications using selected queries, database indexing, caching layers, and asynchronous background tasks.",
                'content': """Building web APIs that scale effortlessly requires an understanding of both framework mechanics and database execution.

### 1. Optimize Database Queries with select_related & prefetch_related
One of the most frequent performance bottlenecks in Django applications is the infamous N+1 query problem. When retrieving related foreign keys or many-to-many relationships in a loop, Django makes a separate query for every single child object.

Use `select_related` for single-valued relationships (ForeignKey, OneToOne):
```python
# Bad: 1 query for posts + N queries for authors
posts = Post.objects.all()

# Good: 1 single SQL JOIN query
posts = Post.objects.select_related('author', 'category').all()
```

Use `prefetch_related` for multi-valued relationships (ManyToManyField):
```python
# Fetches all related tags efficiently in two SQL queries
posts = Post.objects.prefetch_related('tags').filter(status='published')
```

### 2. Implement Database Indexing
Indexing fields that frequently appear in `filter()`, `order_by()`, or `lookup` expressions will drastically accelerate read performance. Ensure that search fields such as `slug`, `published_at`, and `status` are indexed appropriately.

> **Key Takeaway:** Always profile queries using Django Debug Toolbar or database slow query logs before attempting caching!

### 3. Graceful Caching Layers
For data that changes infrequently (such as categories, tags, or public blog lists), integrate Redis or localized template fragment caching. Combining proper database querying with smart caching will let your Django backend handle thousands of concurrent requests seamlessly.""",
                'colors': ((11, 19, 43), (13, 148, 136)),
            },
            {
                'title': "The Modern Color Palette: Mastering Navy, Teal, and Purple Gradients",
                'slug': "modern-color-palette-navy-teal-purple",
                'author': sarah_user,
                'category': cat_objs["Frontend & UI Design"],
                'tags': ["CSS", "WebDev", "Tutorial"],
                'status': 'published',
                'is_featured': False,
                'views_count': 890,
                'published_at': timezone.now() - datetime.timedelta(days=4),
                'summary': "Discover how thoughtful color harmony, subtle gradients, and high contrast elevate user interfaces from standard to world-class.",
                'content': """Color plays a decisive role in visual hierarchy, readability, and brand identity. When combined thoughtfully, deep navy, vibrant teal, and purple gradients create a modern, futuristic yet grounded aesthetic.

### Why Deep Navy Outperforms Pure Black
Using deep navy (`#0b132b` or `#0f172a`) instead of pure black (`#000000`) creates a softer, more sophisticated look. It blends naturally with ambient lighting and avoids the extreme contrast strain that pure pitch black creates against white text.

### The Power of Vibrant Teal as Primary Accent
Teal (`#0d9488` / `#14b8a6`) represents innovation, clarity, and technology. It provides superior contrast for badges, call-to-action buttons, and interactive states.

### Accenting with Purple Gradients
Using linear gradients combining royal purple (`#7c3aed`) and bright cyan-teal (`#2dd4bf`):
```css
background: linear-gradient(135deg, #1e1b4b 0%, #312e81 45%, #0f766e 100%);
```
This produces an engaging depth effect that instantly makes cards, headers, and hero banners feel sleek and tactile.""",
                'colors': ((30, 27, 75), (124, 58, 237)),
            },
            {
                'title': "Demystifying Database Indexing: From B-Trees to Query Optimization",
                'slug': "demystifying-database-indexing-b-trees",
                'author': admin_user,
                'category': cat_objs["System Architecture"],
                'tags': ["Database", "Architecture", "Performance"],
                'status': 'published',
                'is_featured': False,
                'views_count': 1120,
                'published_at': timezone.now() - datetime.timedelta(days=7),
                'summary': "Understand how database engines utilize B-Tree indices to turn sequential scans into logarithmic lookups, and how to design compound keys.",
                'content': """Indexes are the single most effective tool for accelerating relational database performance. Without an index, the database engine must scan every single row on disk from first to last (a Full Table Scan).

### How B-Trees Function
Most relational database management systems (PostgreSQL, MySQL, SQLite) implement B-Tree (Balanced Tree) structures for standard indexes. 

1. **Root & Branch Nodes:** Contain navigational keys directing the search engine.
2. **Leaf Nodes:** Contain the actual pointer (RowID or primary key) to where the record physically lives on disk.
3. **Logarithmic Time Complexity:** A table containing 1,000,000 rows can be searched in approximately 3 to 4 disk reads instead of 1,000,000!

### Choosing Compound Index Orders
When indexing multiple columns (e.g. `(category_id, published_at)`), place the column with highest equality selectivity first, followed by range fields.

> Remember: Every index speeds up reads, but carries a modest cost on inserts and updates as the tree must be rebalanced.""",
                'colors': ((15, 23, 42), (234, 88, 12)),
            },
            {
                'title': "Containerizing Python Web Applications with Docker and Multi-Stage Builds",
                'slug': "containerizing-python-docker-multi-stage",
                'author': sarah_user,
                'category': cat_objs["DevOps & Cloud"],
                'tags': ["Docker", "Python", "Architecture"],
                'status': 'published',
                'is_featured': False,
                'views_count': 640,
                'published_at': timezone.now() - datetime.timedelta(days=10),
                'summary': "Learn how to build lightweight, secure, and production-ready Docker containers for Django applications using multi-stage compilation.",
                'content': """Shipping containerized applications guarantees parity between local development and production servers. However, default Docker images often end up exceeding 1 GB in size.

### Using Multi-Stage Builds
By separating the build environment (compilers, build tools, wheels) from the runtime environment, you can reduce final image sizes down to under 150 MB!

```dockerfile
# Stage 1: Build dependencies
FROM python:3.14-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Stage 2: Minimal runtime image
FROM python:3.14-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY . .
ENV PATH=/root/.local/bin:$PATH
CMD ["gunicorn", "personal_blog.wsgi:application", "--bind", "0.0.0.0:8000"]
```

This guarantees that build tools and temporary caches are completely omitted from your deployment artifacts.""",
                'colors': ((2, 132, 199), (13, 148, 136)),
            },
            {
                'title': "10 Core Engineering Habits for Clean, Scalable Software",
                'slug': "10-engineering-habits-clean-scalable-software",
                'author': admin_user,
                'category': cat_objs["Productivity & Career"],
                'tags': ["Architecture", "Tutorial", "WebDev"],
                'status': 'published',
                'is_featured': False,
                'views_count': 780,
                'published_at': timezone.now() - datetime.timedelta(days=14),
                'summary': "Timeless mental models, pragmatic refactoring techniques, and architectural conventions for building long-lasting software.",
                'content': """Great engineering is less about writing clever code and more about writing code that is easy to understand, test, modify, and delete.

1. **Favor Explicit over Implicit:** Magic shortcuts cause debugging nightmares months later.
2. **Encapsulate Domain Logic:** Don't let business rules spill across random views and templates.
3. **Small, Atomic Pull Requests:** Reviewing 50 lines of code yields 10 insights; reviewing 1,000 lines yields a nod of approval.
4. **Treat Tests as First-Class Citizens:** Tests document how your system is intended to function.
5. **Optimize for Deletion:** If a feature is decoupled, removing it when requirements evolve is trivial.""",
                'colors': ((16, 185, 129), (15, 23, 42)),
            },
            {
                'title': "Upcoming Trends in Python 3.14 and Web Framework Evolution",
                'slug': "upcoming-trends-python-web-frameworks",
                'author': admin_user,
                'category': cat_objs["Python & Backend"],
                'tags': ["Python", "Tutorial"],
                'status': 'draft',
                'is_featured': False,
                'views_count': 45,
                'published_at': None,
                'summary': "[DRAFT] Exploring free-threaded Python (nogil), subinterpreters, and next-generation async capabilities.",
                'content': """This is a working draft exploring Python 3.14 features including free threading, improved JIT optimizations, and how modern web frameworks like Django will take advantage of true multicore concurrency without the Global Interpreter Lock.""",
                'colors': ((30, 41, 59), (100, 116, 139)),
            },
        ]

        for pdata in posts_data:
            post, pcreated = Post.objects.get_or_create(
                slug=pdata['slug'],
                defaults={
                    'title': pdata['title'],
                    'author': pdata['author'],
                    'category': pdata['category'],
                    'summary': pdata['summary'],
                    'content': pdata['content'],
                    'status': pdata['status'],
                    'is_featured': pdata['is_featured'],
                    'views_count': pdata['views_count'],
                    'published_at': pdata['published_at'],
                }
            )

            # Assign tags
            for tname in pdata['tags']:
                post.tags.add(tag_objs[tname])

            # Generate cover image if not set
            if not post.featured_image:
                try:
                    c1, c2 = pdata.get('colors', ((15, 23, 42), (13, 148, 136)))
                    banner_file = generate_banner_image(post.title, post.category.name, c1, c2)
                    filename = f"{post.slug}.jpg"
                    post.featured_image.save(filename, banner_file, save=True)
                except Exception as e:
                    self.stdout.write(self.style.WARNING(f"Image generation skipped: {e}"))

            self.stdout.write(self.style.SUCCESS(f"Post ready: '{post.title}' ({post.status})"))

        # 6. Add Sample Comments
        first_post = Post.objects.filter(slug="building-high-performance-rest-apis-django").first()
        if first_post:
            comments_info = [
                (sarah_user, "Super helpful explanation of select_related vs prefetch_related! The code snippet made it click immediately."),
                (admin_user, "Thanks Sarah! Profiling queries in local development with SQLite before deploying to production saves so many headaches."),
            ]
            for author, text in comments_info:
                Comment.objects.get_or_create(
                    post=first_post,
                    author=author,
                    content=text,
                    defaults={'is_approved': True}
                )

        self.stdout.write(self.style.SUCCESS("\n[SUCCESS] Database seeded successfully!"))
        self.stdout.write(self.style.NOTICE("Credentials for testing:"))
        self.stdout.write(self.style.NOTICE("  Admin / Superuser : username = admin     | password = admin123"))
        self.stdout.write(self.style.NOTICE("  Author 2          : username = sarah_dev | password = password123"))
