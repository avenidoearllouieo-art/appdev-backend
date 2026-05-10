#!/usr/bin/env python
"""
API Test Script for Smart Locker System Backend
Tests all endpoints and validates response structure
"""

import os
import sys
import json
import requests
import time

# Django setup
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
import django
django.setup()

from django.contrib.auth.models import User
from lockers.models import Locker

# API Base URL
BASE_URL = 'http://127.0.0.1:8000/api'

# Test data
TEST_USER = {
    'username': 'testuser',
    'email': 'test@example.com',
    'password': 'testpass123'
}

def print_header(text):
    print(f"\n{'='*60}")
    print(f"  {text}")
    print('='*60)

def print_success(text):
    print(f"✓ {text}")

def print_error(text):
    print(f"✗ {text}")

def print_info(text):
    print(f"ℹ {text}")

def test_registration():
    """Test user registration"""
    print_header("TEST 1: User Registration")
    
    try:
        response = requests.post(f'{BASE_URL}/register/', json=TEST_USER)
        print_info(f"Status Code: {response.status_code}")
        data = response.json()
        print_info(f"Response: {json.dumps(data, indent=2)}")
        
        if response.status_code == 201:
            if data.get('success'):
                print_success("User registration successful")
                token = data.get('token')
                user = data.get('user')
                print_success(f"Token: {token[:20]}...")
                print_success(f"User: {user}")
                return token, user
            else:
                print_error(f"Registration returned success=false: {data}")
                return None, None
        else:
            print_error(f"Registration failed: {data}")
            return None, None
    except Exception as e:
        print_error(f"Registration error: {str(e)}")
        return None, None

def test_login():
    """Test user login"""
    print_header("TEST 2: User Login")
    
    try:
        response = requests.post(f'{BASE_URL}/login/', json={
            'username': TEST_USER['username'],
            'password': TEST_USER['password']
        })
        print_info(f"Status Code: {response.status_code}")
        data = response.json()
        print_info(f"Response: {json.dumps(data, indent=2)}")
        
        if response.status_code == 200:
            if data.get('success'):
                print_success("User login successful")
                token = data.get('token')
                return token
            else:
                print_error(f"Login returned success=false: {data}")
                return None
        else:
            print_error(f"Login failed: {data}")
            return None
    except Exception as e:
        print_error(f"Login error: {str(e)}")
        return None

def test_get_lockers(token=None):
    """Test get all lockers"""
    print_header("TEST 3: Get All Lockers")
    
    try:
        headers = {'Authorization': f'Token {token}'} if token else {}
        response = requests.get(f'{BASE_URL}/lockers/', headers=headers)
        print_info(f"Status Code: {response.status_code}")
        data = response.json()
        
        if response.status_code == 200:
            if data.get('success'):
                lockers = data.get('lockers', [])
                print_success(f"Retrieved {data.get('count', 0)} lockers")
                if len(lockers) > 0:
                    print_info(f"Sample locker: {json.dumps(lockers[0], indent=2)}")
                    # Validate structure
                    required_fields = ['id', 'locker_number', 'status', 'rented_by', 'rental_hours', 'created_at']
                    locker = lockers[0]
                    for field in required_fields:
                        if field in locker:
                            print_success(f"Field '{field}' present: {locker[field]}")
                        else:
                            print_error(f"Field '{field}' missing!")
            else:
                print_error(f"API returned success=false: {data}")
        else:
            print_error(f"Unexpected response type: {type(data)}")
    except Exception as e:
        print_error(f"Get lockers error: {str(e)}")

def test_rent_locker(token):
    """Test renting a locker"""
    print_header("TEST 4: Rent Locker")
    
    try:
        # First, get a locker to rent
        response = requests.get(f'{BASE_URL}/lockers/')
        data = response.json()
        lockers = data.get('lockers', [])
        
        if not lockers:
            print_error("No lockers available")
            return
        
        # Find an available locker
        available_locker = None
        for locker in lockers:
            if locker['status'] == 'Available':
                available_locker = locker
                break
        
        if not available_locker:
            print_error("No available lockers to rent")
            return
        
        locker_id = available_locker['id']
        print_info(f"Renting locker ID: {locker_id}")
        
        headers = {'Authorization': f'Token {token}'}
        rental_hours = 1  # 1 hour
        response = requests.post(f'{BASE_URL}/lockers/{locker_id}/rent/', 
                                json={'rental_hours': rental_hours},
                                headers=headers)
        print_info(f"Status Code: {response.status_code}")
        data = response.json()
        print_info(f"Response: {json.dumps(data, indent=2)}")
        
        if response.status_code == 200:
            if data.get('success'):
                print_success("Locker rented successfully")
                locker = data.get('locker', {})
                print_success(f"Status: {locker.get('status')}")
                print_success(f"Rented by: {locker.get('rented_by')}")
                print_success(f"Rental Hours: {locker.get('rental_hours')}h")
            else:
                print_error(f"Rental returned success=false: {data}")
        else:
            print_error(f"Failed to rent locker: {data}")
    except Exception as e:
        print_error(f"Rent locker error: {str(e)}")

def cleanup():
    """Clean up test user"""
    print_header("CLEANUP: Remove Test User")
    
    try:
        user = User.objects.get(username=TEST_USER['username'])
        user.delete()
        print_success(f"Test user '{TEST_USER['username']}' deleted")
    except User.DoesNotExist:
        print_info("Test user not found")

def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("  SMART LOCKER SYSTEM - API TEST SUITE")
    print("="*60)
    
    # Clean up any existing test user
    try:
        User.objects.filter(username=TEST_USER['username']).delete()
    except:
        pass
    
    # Wait a moment for server to be ready
    print_info("Waiting for server to be ready...")
    time.sleep(1)
    
    # Test registration
    token, user = test_registration()
    
    if not token:
        print_error("Cannot continue without valid token")
        return
    
    # Test login
    new_token = test_login()
    
    # Test get lockers
    test_get_lockers(token)
    
    # Test rent locker (requires authentication)
    test_rent_locker(token)
    
    # Cleanup
    cleanup()
    
    print_header("TEST SUITE COMPLETED")

if __name__ == '__main__':
    main()
