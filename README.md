# LITREVIEW

LITREVIEW is a Django web app for sharing book reviews.
Users can sign up, log in, create books, write reviews, follow other users, and browse review feeds.

## Project Structure

This project contains two Django apps:

- `reviews`: book and review models, book/review pages, home feed, and search
- `users`: custom user model, auth-related pages, profiles, follow/unfollow, and user search


## Tech Stack

- Python 3
- Django 4.0.5
- SQLite (default development DB)
- Bootstrap 5 (CDN in base template)

## Setup

1. Create and activate a virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Apply migrations:

```bash
python manage.py migrate
```

4. (Optional) Create an admin account:

```bash
python manage.py createsuperuser
```

5. Run the development server:

```bash
python manage.py runserver
```

App will be available at:

- `http://127.0.0.1:8000/`

## Data Seeding and Export

### Use existing DB

You can keep and submit `db.sqlite3` as your populated database file.

### Export sample data

Export users + reviews app data:

```bash
python manage.py dumpdata users reviews --indent 2 > seed_data.json
```

Export full database:

```bash
python manage.py dumpdata --indent 2 > full_dump.json
```

### Load fixture data

```bash
python manage.py loaddata seed_data.json
```

If you need a clean reload first:

```bash
python manage.py flush
python manage.py loaddata seed_data.json
```

## Media and Static Files

- Static files are served from `/static/` (development)
- Uploaded book covers are served from `/media/` (development, when `DEBUG=True`)

Configured in:

- `/Users/agrandbe/PycharmProjects/PythonProject4/P4-SoftDev-USApp/litreview/settings.py`

## URL Routes

### Reviews Routes (root namespace)

- `/` - Home feed
  - Logged-in users: reviews from users they follow
  - Anonymous users: all reviews
- `/all/` - All reviews (paginated)
- `/books/` - All books (paginated)
- `/books/<pk>/` - Book detail page with reviews
- `/search/books/?q=...` - Book search by title
- `/book/new/` - Create book (logged-in users only)
- `/book/<pk>/review/new/` - Create review for a book (logged-in users only)
- `/book/<pk>/review/<review_id>/edit/` - Edit review (owner only)
- `/book/<pk>/review/<review_id>/delete/` - Delete review (owner only)

### User Routes (`/users/` namespace)

- `/users/signup/` - Sign up
- `/users/login/` - Log in
- `/users/logout/` - Log out (POST)
- `/users/profile/` - Logged-in user's profile
- `/users/profile/<pk>/` - Public user profile
- `/users/search/?q=...` - Search users by first name, last name, or username (logged-in users only)
- `/users/follow/<user_id>/` - Follow/unfollow toggle (POST, logged-in users only)

### Admin

- `/admin/` - Django admin

## Main Features

- Authentication: sign up, login, logout
- Custom user model with follow relationships
- Book listing and detail pages
- Book creation (authenticated users)
- Review creation/edit/delete with ownership checks
- Home feed behavior based on authentication/follow graph
- User search and follow/unfollow workflow
- Book search by partial title
- Review links from feeds jump to the specific review anchor in the book detail page

## Running Tests

```bash
python manage.py test
```

## Notes

- In development, this project uses SQLite (`db.sqlite3`).
- If reviewer names appear blank, ensure users have first and last name values populated.
