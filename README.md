# 🌟 My Personal Blog Website

A modern, colorful, fully responsive, and feature-rich **Personal Blog Website** built with **Python**, **Django**, and modern frontend standards. Designed with a custom **Navy-Blue and Teal theme**, **Purple Gradients**, **Orange Highlights**, rounded glassmorphism accents, shadows, and smooth interactions.

---

## 🚀 Key Features

* **🎨 Modern & Responsive Design:**
  * Clean Navy-Blue (`#0b132b`), vibrant Teal (`#0d9488`), Purple gradient highlights, and warm Orange call-to-actions.
  * Fully responsive across mobile smartphones, tablets, and desktop displays.
  * Interactive reading progress indicator, live image preview on file uploads, and auto-dismissing toast notifications.

* **👥 Secure Authentication & Profiles:**
  * User Registration, Login, and Logout powered by Django's robust authentication system and PBKDF2 password hashing.
  * Personal Author Profile settings: profile picture / avatar upload, headline, bio, and social links (GitHub, Twitter, LinkedIn, personal website).

* **✍️ Complete Blog Post Management (CRUD):**
  * Authenticated authors can create, view, edit, and delete their own posts.
  * **Draft & Published Statuses:** Draft posts are strictly private and visible only to the author in their dashboard and preview mode.
  * Quick status toggle (Draft ↔ Published) directly from the Author Dashboard.
  * **Permission Protection:** Users cannot edit, modify, or delete another author's posts.

* **📊 Author Studio Dashboard:**
  * Comprehensive analytics: Total articles, live published count, drafts count, total article views, and reader comments.
  * Filter posts by status tab (*All*, *Published*, *Drafts*) and in-dashboard search.
  * One-click management actions (View, Edit, Delete, Toggle Status).

* **🏷️ Organization & Discovery:**
  * Categorize posts with color-coded badges and icons.
  * Comma-separated tag support (`#python`, `#django`, `#webdev`).
  * Search bar (searching titles, content, summaries, tags, and authors).
  * Fast pagination on archive and category pages (preserving active search filters).

* **💬 Reader Comments Section:**
  * Logged-in readers can leave comments on published posts.
  * Real-time character counter (max 1000 characters).
  * Authors and comment owners can safely delete comments.

* **⚙️ Database Flexibility:**
  * Works out-of-the-box with **SQLite** for instant zero-configuration development.
  * Seamlessly toggle to **MySQL** via Django ORM using simple environment variables or settings toggle.

* **🛠️ Django Admin Portal:**
  * Customized administration interface to inspect and moderate posts, categories, tags, comments, and author profiles.

---

## 📂 Project Architecture

```text
c:\prnl_blog\
├── blog\                           # Main Django Blog application
│   ├── management\commands\        # Custom management commands
│   │   └── seed_blog.py            # Automated demo data and Pillow banner generator
│   ├── templatetags\               # Custom template filters
│   │   └── blog_extras.py          # Reading time, query params, content formatting
│   ├── admin.py                    # Django admin customization
│   ├── apps.py                     # Blog application configuration
│   ├── context_processors.py       # Global categories and stats in navbar/footer
│   ├── forms.py                    # Post, Registration, Profile & Comment forms
│   ├── models.py                   # Category, Tag, Post, Comment, Profile models
│   ├── tests.py                    # 13 automated tests (models, permissions, views)
│   ├── urls.py                     # Application URL patterns
│   └── views.py                    # Home, Post detail, CRUD, Dashboard, Search views
├── media\                          # User uploads (Cover images & Avatars)
├── personal_blog\                  # Project root configuration
│   ├── settings.py                 # Django settings, MySQL toggle, Media/Static config
│   ├── urls.py                     # Main project URL routing
│   ├── wsgi.py                     # WSGI server entry point
│   └── asgi.py                     # ASGI server entry point
├── static\                         # Static CSS, JS, and image assets
│   ├── css\styles.css              # Custom Navy, Teal & Purple styles and animations
│   └── js\main.js                  # Reading progress, image preview, toast helpers
├── templates\                      # HTML templates (Django Template Language)
│   ├── base.html                   # Master layout with navbar, alerts, footer
│   ├── blog\
│   │   ├── author_posts.html       # Public author profile & published posts
│   │   ├── category_posts.html     # Posts filtered by category
│   │   ├── dashboard.html          # Author Studio dashboard with analytics
│   │   ├── home.html               # Hero banner, featured post, latest articles
│   │   ├── post_confirm_delete.html# Delete post confirmation card
│   │   ├── post_detail.html        # Full article, comments, author card, share
│   │   ├── post_form.html          # Create and edit post form
│   │   ├── post_list.html          # Archive, search, filtering, pagination
│   │   └── tag_posts.html          # Posts filtered by tag
│   └── registration\
│       ├── login.html              # Custom sign-in page
│       ├── profile.html            # Author profile settings
│       └── register.html           # Custom user registration page
├── manage.py                       # Django CLI runner
├── requirements.txt                # Python dependencies
├── seed_data.py                    # One-step database migration and seed script
└── README.md                       # Beginner-friendly setup documentation
```

---

## 💻 Beginner-Friendly Setup Instructions (Windows & VS Code)

### Prerequisites

Ensure you have **Python 3.10+** installed on your Windows computer. Check by running:

```powershell
python --version
```

---

### Step 1: Open the Project in VS Code

1. Launch **Visual Studio Code**.
2. Go to **File -> Open Folder...** and select `C:\prnl_blog`.
3. Open a new PowerShell terminal in VS Code using the shortcut:
   `Ctrl + ~` (or `Terminal -> New Terminal`).

---

### Step 2: Create and Activate a Virtual Environment (Recommended)

In your VS Code terminal, run:

```powershell
# Create a virtual environment named 'venv'
python -m venv venv

# Activate the virtual environment on Windows
.\venv\Scripts\Activate.ps1
```

*(Note: If PowerShell shows an Execution Policy message, run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` once, then re-activate).*

---

### Step 3: Install Required Dependencies

Install Django and Pillow from `requirements.txt`:

```powershell
python -m pip install -r requirements.txt
```

---

### Step 4: Apply Database Migrations

Set up the database tables (SQLite by default):

```powershell
python manage.py migrate
```

---

### Step 5: Populate Sample Content & Demo Accounts

We have included a seed script that automatically configures demo categories, tags, blog posts with custom banners, author profiles, and sample comments:

```powershell
python manage.py seed_blog
```

*(Alternatively, you can run `python seed_data.py` which executes migrations and seeding together).*

#### 🔑 Pre-Configured Demo Credentials:

| Role | Username | Password | Notes |
| :--- | :--- | :--- | :--- |
| **Admin & Author** | `admin` | `admin123` | Full access to Django Admin & Author Studio |
| **Author 2** | `sarah_dev` | `password123` | Author account with sample published articles |

---

### Step 6: (Optional) Create Your Own Custom Superuser

If you want your own personal administrator account:

```powershell
python manage.py createsuperuser
```

Follow the prompts to enter your desired username, email, and password.

---

### Step 7: Run the Development Server

Start the local Django server:

```powershell
python manage.py runserver
```

Now open your browser and navigate to:
👉 **[http://127.0.0.1:8000/](http://127.0.0.1:8000/)**

To access the Django Admin Portal:
👉 **[http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)**

---

## 🧪 Running Automated Tests & Verification

The project includes an automated test suite verifying model logic, slug generation, author permission barriers, draft privacy, and comment moderation.

Run all tests:

```powershell
python manage.py test blog
```

Check Django system configuration:

```powershell
python manage.py check
```

---

## 🐬 Switching from SQLite to MySQL

The project uses Django's ORM and is completely database-agnostic. To switch from SQLite to MySQL:

1. **Install a MySQL client library:**
   ```powershell
   python -m pip install pymysql
   # Or install mysqlclient:
   # python -m pip install mysqlclient
   ```

2. **Create your MySQL database:**
   ```sql
   CREATE DATABASE personal_blog_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```

3. **Configure Settings or Environment Variables:**
   You can enable MySQL by setting environment variables in PowerShell:
   ```powershell
   $env:USE_MYSQL="True"
   $env:MYSQL_DATABASE="personal_blog_db"
   $env:MYSQL_USER="root"
   $env:MYSQL_PASSWORD="your_mysql_password"
   $env:MYSQL_HOST="127.0.0.1"
   $env:MYSQL_PORT="3306"
   ```

   *Or edit `personal_blog/settings.py` around line 50 directly to configure your database credentials.*

4. **Run migrations to create tables in MySQL:**
   ```powershell
   python manage.py migrate
   python manage.py seed_blog
   ```

---

## 🎨 Theme & Styling Customization

All styling variables are organized at the top of `static/css/styles.css`:

```css
:root {
  --color-navy-950: #070d1e;
  --color-teal-500: #0d9488;
  --color-teal-400: #14b8a6;
  --color-purple-500: #7c3aed;
  --color-orange-500: #f97316;
  --gradient-hero: linear-gradient(135deg, #070d1e 0%, #1e1b4b 45%, #0f766e 100%);
}
```

Adjust these variables at any time to customize the color palette, card shadows, or typography.

---

## 📄 License

This project is created for personal and educational use. Feel free to modify and expand it!
