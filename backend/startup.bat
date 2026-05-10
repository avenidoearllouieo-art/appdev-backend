@echo off
REM Smart Locker System Backend - Quick Start Guide (Windows)

echo.
echo ==========================================
echo   Smart Locker Backend - Quick Start
echo ==========================================
echo.

REM Step 1: Ensure we're in the backend directory
if not exist "manage.py" (
    echo Error: manage.py not found. Please run from backend directory.
    echo Usage: cd backend && startup.bat
    exit /b 1
)

echo 📝 Creating admin user (if needed)...
python manage.py shell -c "
from django.contrib.auth.models import User
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('✅ Admin user created: admin / admin123')
else:
    print('✅ Admin user already exists')
"

echo.
echo 📦 Creating test lockers...
python manage.py shell -c "
from lockers.models import Locker
Locker.objects.all().delete()
for i in range(1, 6):
    Locker.objects.create(number=i, status='Available')
    print(f'   ✅ Locker {i} created')
print(f'📊 Total lockers: {Locker.objects.count()}')
"

echo.
echo ==========================================
echo   ✅ Backend Ready!
echo ==========================================
echo.
echo 📌 Quick Start Steps:
echo.
echo 1️⃣  Start the server:
echo    python manage.py runserver
echo.
echo 2️⃣  Access Django Admin:
echo    http://localhost:8000/admin/
echo    Username: admin
echo    Password: admin123
echo.
echo 3️⃣  Test the API:
echo    POST /api/register/
echo    POST /api/login/
echo    GET /api/lockers/
echo    POST /api/lockers/{id}/rent/
echo.
echo 4️⃣  Run all tests:
echo    python manage.py test lockers.tests
echo.
echo 📚 Full documentation: ..\BACKEND_COMPLETE_GUIDE.md
echo.

pause
