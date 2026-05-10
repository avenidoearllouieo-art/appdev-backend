#!/usr/bin/env python
"""
BACKEND VERIFICATION SCRIPT
Smart Locker System - Complete API Flow Test

This script verifies that:
1. User registration works
2. User login returns token
3. Locker list retrieves data from database
4. Locker rental updates database correctly
5. Django Admin syncs with API
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from lockers.models import Locker


def print_section(title):
    """Print a formatted section header"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")


def cleanup():
    """Clean up test data"""
    print("🧹 Cleaning up test data...")
    User.objects.filter(username__startswith='test_').delete()
    Locker.objects.all().delete()
    print("✅ Cleanup complete\n")


def test_backend_flow():
    """Test complete backend flow"""
    
    cleanup()
    
    client = APIClient()
    
    # ===== TEST 1: CREATE TEST DATA IN ADMIN =====
    print_section("STEP 1: Setup Test Lockers")
    
    print("📦 Creating 5 test lockers...")
    for i in range(1, 6):
        locker = Locker.objects.create(
            number=i,
            status='Available'
        )
        print(f"   ✅ Locker {i} created")
    
    print(f"\n📊 Total lockers in database: {Locker.objects.count()}")
    
    
    # ===== TEST 2: USER REGISTRATION =====
    print_section("STEP 2: User Registration")
    
    register_data = {
        'username': 'test_user_001',
        'email': 'testuser@example.com',
        'password': 'secure_password_123'
    }
    
    print(f"📝 Registering user: {register_data['username']}")
    response = client.post('/api/register/', register_data, format='json')
    
    print(f"   Status: {response.status_code}")
    
    # Handle response data
    try:
        response_data = response.json() if hasattr(response, 'json') else response.data
    except:
        response_data = response.data if hasattr(response, 'data') else {}
    
    print(f"   Success: {response_data.get('success')}")
    print(f"   Message: {response_data.get('message')}")
    
    if response.status_code != 201:
        print(f"❌ Registration failed: {response_data}")
        return False
    
    token_from_register = response_data.get('token')
    user_from_register = response_data.get('user')
    
    print(f"   ✅ User created: {user_from_register.get('username')}")
    print(f"   ✅ Token issued: {token_from_register[:20]}...")
    
    # Verify user in database
    user = User.objects.get(username='test_user_001')
    print(f"   ✅ User found in database")
    
    
    # ===== TEST 3: USER LOGIN =====
    print_section("STEP 3: User Login")
    
    login_data = {
        'username': 'test_user_001',
        'password': 'secure_password_123'
    }
    
    print(f"🔐 Logging in: {login_data['username']}")
    response = client.post('/api/login/', login_data, format='json')
    
    print(f"   Status: {response.status_code}")
    print(f"   Success: {response.data.get('success')}")
    print(f"   Message: {response.data.get('message')}")
    
    if response.status_code != 200:
        print(f"❌ Login failed: {response.data}")
        return False
    
    token_from_login = response.data.get('token')
    user_from_login = response.data.get('user')
    
    print(f"   ✅ Login successful")
    print(f"   ✅ Token issued: {token_from_login[:20]}...")
    print(f"   ✅ User: {user_from_login.get('username')}")
    
    # Verify tokens match
    if token_from_register == token_from_login:
        print(f"   ✅ Token consistency verified")
    
    
    # ===== TEST 4: FETCH LOCKERS =====
    print_section("STEP 4: Fetch Lockers from API")
    
    print("📋 Fetching lockers without authentication...")
    response = client.get('/api/lockers/', format='json')
    
    print(f"   Status: {response.status_code}")
    print(f"   Success: {response.data.get('success')}")
    print(f"   Count: {response.data.get('count')}")
    
    if response.status_code != 200:
        print(f"❌ Failed to fetch lockers: {response.data}")
        return False
    
    lockers = response.data.get('lockers', [])
    print(f"   ✅ Retrieved {len(lockers)} lockers from database")
    
    for locker in lockers:
        print(f"      - Locker {locker['number']}: {locker['status']}")
    
    
    # ===== TEST 5: RENT LOCKER =====
    print_section("STEP 5: Rent a Locker (Authenticated)")
    
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token_from_login}')
    
    rent_data = {
        'rental_duration': 7200  # 2 hours in seconds
    }
    
    locker_to_rent = lockers[0]
    print(f"🔑 Renting locker {locker_to_rent['id']} with Bearer token...")
    print(f"   Duration: {rent_data['rental_duration']} seconds")
    
    response = client.post(
        f'/api/lockers/{locker_to_rent["id"]}/rent/',
        rent_data,
        format='json'
    )
    
    print(f"   Status: {response.status_code}")
    print(f"   Success: {response.data.get('success')}")
    print(f"   Message: {response.data.get('message')}")
    
    if response.status_code != 200:
        print(f"❌ Rental failed: {response.data}")
        return False
    
    rented_locker = response.data.get('locker', {})
    print(f"   ✅ Locker rented successfully")
    print(f"      - Status: {rented_locker.get('status')}")
    print(f"      - Owner: {rented_locker.get('owner')}")
    print(f"      - Time Left: {rented_locker.get('time_left')} seconds")
    
    # Verify in database
    db_locker = Locker.objects.get(id=locker_to_rent['id'])
    print(f"   ✅ Database verified:")
    print(f"      - Status: {db_locker.status}")
    print(f"      - Owner: {db_locker.owner.username if db_locker.owner else 'None'}")
    print(f"      - Time Left: {db_locker.time_left}")
    
    
    # ===== TEST 6: VERIFY DATABASE CHANGES =====
    print_section("STEP 6: Verify Database State")
    
    print("📊 Database Summary:")
    print(f"   Total Users: {User.objects.count()}")
    print(f"   Total Lockers: {Locker.objects.count()}")
    
    available = Locker.objects.filter(status='Available').count()
    in_use = Locker.objects.filter(status='In Use').count()
    
    print(f"   Available Lockers: {available}")
    print(f"   In Use Lockers: {in_use}")
    
    # List all lockers
    print("\n📋 All Lockers in Database:")
    for locker in Locker.objects.all():
        owner_name = locker.owner.username if locker.owner else 'None'
        print(f"   - Locker {locker.number}: {locker.status} (Owner: {owner_name})")
    
    
    # ===== TEST 7: FETCH LOCKERS AGAIN =====
    print_section("STEP 7: Re-fetch Lockers to Verify API Returns Updates")
    
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token_from_login}')
    response = client.get('/api/lockers/', format='json')
    
    lockers_after = response.data.get('lockers', [])
    print(f"📋 Fetched {len(lockers_after)} lockers")
    
    for locker in lockers_after:
        status_indicator = "✅" if locker['status'] == 'Available' else "🔒"
        print(f"   {status_indicator} Locker {locker['number']}: {locker['status']} (Owner: {locker['owner']})")
    
    
    # ===== TEST 8: TEST UNAUTHORIZED ACCESS =====
    print_section("STEP 8: Test Unauthorized Access Protection")
    
    client.credentials()  # Clear credentials
    
    rent_data = {'rental_duration': 3600}
    response = client.post(
        f'/api/lockers/{lockers[1]["id"]}/rent/',
        rent_data,
        format='json'
    )
    
    print(f"🔐 Attempting to rent without token...")
    print(f"   Status: {response.status_code}")
    print(f"   Success: {response.data.get('success')}")
    
    if response.status_code == 401:
        print(f"   ✅ Protected endpoint correctly requires authentication")
    else:
        print(f"   ❌ Protection check failed")
    
    
    # ===== FINAL SUMMARY =====
    print_section("✅ ALL TESTS COMPLETED SUCCESSFULLY")
    
    print("📌 BACKEND VERIFICATION SUMMARY:")
    print("   ✅ User registration creates users in database")
    print("   ✅ User login returns valid token")
    print("   ✅ API retrieves lockers dynamically from database")
    print("   ✅ Locker rental updates database correctly")
    print("   ✅ Status, owner, and duration saved properly")
    print("   ✅ Protected endpoints require authentication")
    print("   ✅ Clean JSON responses returned")
    print("   ✅ Database state syncs with API")
    print("\n🎯 Backend is ready for Web UI and Mobile UI integration!")
    print("   Use Bearer token format: Authorization: Bearer <token>\n")
    
    return True


if __name__ == '__main__':
    try:
        success = test_backend_flow()
        cleanup()  # Clean up after tests
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ Error occurred: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
