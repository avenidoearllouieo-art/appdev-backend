# Locker Management System - Backend API

A Django REST Framework backend API for a smart locker management system that supports web and mobile frontend applications.

## Features

- **User Authentication**: Registration and login system with activity logging
- **Locker Management**: View available lockers and open lockers with time tracking
- **Activity Logging**: Track all user actions with IP addresses and timestamps
- **User Profiles**: Extended user profiles with avatars and bio information

## Technology Stack

- **Backend**: Django 6.0.3
- **API Framework**: Django REST Framework
- **Database**: SQLite (development)
- **Authentication**: Django's built-in authentication system

## API Endpoints

### Authentication
- `POST /api/register/` - User registration
- `POST /api/login/` - User login

### Lockers
- `GET /api/lockers/` - Get all lockers
- `POST /api/lockers/<id>/open/` - Open a specific locker

## Models

### User
Extended Django User model with additional profile information.

### UserProfile
- `user`: One-to-one relationship with User
- `avatar`: Profile picture (optional)
- `bio`: User biography (500 characters max)
- `created_at`: Profile creation timestamp
- `updated_at`: Last update timestamp

### Locker
- `number`: Locker identifier
- `status`: Current status (Available, In Use)
- `time_left`: Time remaining in minutes
- `owner`: User who owns the locker (nullable)
- `created_at`: Locker creation timestamp
- `updated_at`: Last update timestamp
- `is_active`: Whether locker is active

### ActivityLog
- `user`: User who performed the action
- `action`: Description of the action performed
- `timestamp`: When the action occurred
- `ip_address`: IP address of the user (optional)

## Setup Instructions

1. **Install dependencies**:
```bash
pip install django djangorestframework
```

2. **Navigate to the backend directory**:
```bash
cd backend
```

3. **Run migrations**:
```bash
python manage.py migrate
```

4. **Create superuser** (optional):
```bash
python manage.py createsuperuser
```

5. **Start the development server**:
```bash
python manage.py runserver
```

The API will be available at `http://127.0.0.1:8000/api/`

## Testing

Run the test suite:
```bash
python manage.py test
```

The test suite covers:
- User registration and login
- Locker operations
- Activity logging
- Error handling

## API Usage Examples

### Register a new user
```bash
http POST http://127.0.0.1:8000/api/register/ username=newuser email=newuser@example.com password=password123
```

### Login
```bash
http POST http://127.0.0.1:8000/api/login/ username=newuser password=password123
```

### Get all lockers
```bash
http GET http://127.0.0.1:8000/api/lockers/
```

### Open a locker
```bash
http POST http://127.0.0.1:8000/api/lockers/1/open/
```

## Project Structure

```
backend/
├── backend/          # Django project settings
├── lockers/          # Main app
│   ├── models.py     # Database models
│   ├── views.py      # API views
│   ├── serializers.py # DRF serializers
│   ├── urls.py       # URL routing
│   └── tests.py      # Test suite
├── manage.py         # Django management script
└── db.sqlite3        # SQLite database
```

## Future Enhancements

- Token-based authentication
- Locker reservation system
- Payment integration
- Mobile app integration
- Admin dashboard
- Email notifications
- Locker maintenance tracking
