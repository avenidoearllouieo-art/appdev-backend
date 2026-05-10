#!/bin/bash
# Smart Locker System Backend - Quick Start Guide

echo "=========================================="
echo "  Smart Locker Backend - Quick Start"
echo "=========================================="
echo ""

# Step 1: Navigate to backend directory
cd backend

# Step 2: Create admin user if doesn't exist
echo "📝 Creating admin user (if needed)..."
python manage.py shell << EOF
from django.contrib.auth.models import User
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print("✅ Admin user created: admin / admin123")
else:
    print("✅ Admin user already exists")
EOF

echo ""
echo "📦 Creating test lockers..."
python manage.py shell << EOF
from lockers.models import Locker
# Clear existing lockers
Locker.objects.all().delete()
# Create fresh set
for i in range(1, 6):
    Locker.objects.create(number=i, status='Available')
    print(f"   ✅ Locker {i} created")
print(f"📊 Total lockers: {Locker.objects.count()}")
EOF

echo ""
echo "=========================================="
echo "  ✅ Backend Ready!"
echo "=========================================="
echo ""
echo "📌 Quick Start Steps:"
echo ""
echo "1️⃣  Start the server:"
echo "   python manage.py runserver"
echo ""
echo "2️⃣  Access Django Admin:"
echo "   http://localhost:8000/admin/"
echo "   Username: admin"
echo "   Password: admin123"
echo ""
echo "3️⃣  Test the API:"
echo "   POST /api/register/"
echo "   POST /api/login/"
echo "   GET /api/lockers/"
echo "   POST /api/lockers/{id}/rent/"
echo ""
echo "4️⃣  Run all tests:"
echo "   python manage.py test lockers.tests"
echo ""
echo "📚 Full documentation: ../BACKEND_COMPLETE_GUIDE.md"
echo ""
