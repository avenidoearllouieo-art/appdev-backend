from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from .models import Locker, UserProfile, ActivityLog

class LockerAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.user_profile = UserProfile.objects.create(user=self.user)
        self.locker = Locker.objects.create(number=1, status='Available')

    def test_get_lockers(self):
        """Test retrieving all lockers"""
        response = self.client.get('/api/lockers/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['number'], 1)

    def test_open_locker(self):
        """Test opening a locker"""
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/api/lockers/1/open/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.locker.refresh_from_db()
        self.assertEqual(self.locker.status, 'In Use')
        self.assertEqual(self.locker.time_left, 60)

    def test_user_registration(self):
        """Test user registration"""
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpass123'
        }
        response = self.client.post('/api/register/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username='newuser').exists())
        self.assertTrue(UserProfile.objects.filter(user__username='newuser').exists())

    def test_user_login(self):
        """Test user login"""
        data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        response = self.client.post('/api/login/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_duplicate_registration(self):
        """Test registration with existing username"""
        data = {
            'username': 'testuser',
            'email': 'duplicate@example.com',
            'password': 'newpass123'
        }
        response = self.client.post('/api/register/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_login(self):
        """Test login with invalid credentials"""
        data = {
            'username': 'testuser',
            'password': 'wrongpass'
        }
        response = self.client.post('/api/login/', data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_activity_logging(self):
        """Test that activities are logged"""
        self.client.force_authenticate(user=self.user)
        self.client.post('/api/lockers/1/open/')
        
        # Check if activity was logged
        activity = ActivityLog.objects.filter(user=self.user, action='Opened locker 1').first()
        self.assertIsNotNone(activity)
        self.assertEqual(activity.action, 'Opened locker 1')
