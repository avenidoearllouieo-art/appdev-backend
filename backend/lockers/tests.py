from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token
from .models import Locker


class LockerAPITestCase(TestCase):
    """Test suite for Smart Locker System API endpoints"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.client = APIClient()
        
        # Create test user
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        # Create test token
        self.token = Token.objects.create(user=self.user)
        
        # Create test lockers
        self.locker1 = Locker.objects.create(
            number=1,
            status='Available'
        )
        self.locker2 = Locker.objects.create(
            number=2,
            status='In Use',
            owner=self.user,
            rental_duration=3600,
            time_left=3600
        )

    def test_user_registration_success(self):
        """Test successful user registration"""
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpass123'
        }
        response = self.client.post('/api/register/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data['success'])
        self.assertIn('token', response.data)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_user_registration_duplicate_username(self):
        """Test registration with duplicate username"""
        data = {
            'username': 'testuser',  # Already exists
            'email': 'another@example.com',
            'password': 'pass123'
        }
        response = self.client.post('/api/register/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(response.data['success'])

    def test_user_login_success(self):
        """Test successful user login"""
        data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        response = self.client.post('/api/login/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        self.assertIn('token', response.data)
        self.assertEqual(response.data['user']['username'], 'testuser')

    def test_user_login_invalid_credentials(self):
        """Test login with invalid credentials"""
        data = {
            'username': 'testuser',
            'password': 'wrongpassword'
        }
        response = self.client.post('/api/login/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertFalse(response.data['success'])

    def test_get_lockers_list(self):
        """Test retrieving all lockers"""
        response = self.client.get('/api/lockers/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        self.assertEqual(response.data['count'], 2)
        self.assertEqual(len(response.data['lockers']), 2)

    def test_get_lockers_list_authenticated(self):
        """Test retrieving lockers with authentication"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token.key}')
        response = self.client.get('/api/lockers/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        self.assertEqual(response.data['count'], 2)

    def test_rent_locker_success(self):
        """Test successful locker rental"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token.key}')
        data = {
            'rental_duration': 3600
        }
        response = self.client.post(f'/api/lockers/{self.locker1.id}/rent/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        self.assertEqual(response.data['locker']['status'], 'In Use')
        self.assertEqual(response.data['locker']['owner'], 'testuser')
        
        # Verify locker was updated in database
        self.locker1.refresh_from_db()
        self.assertEqual(self.locker1.status, 'In Use')
        self.assertEqual(self.locker1.owner, self.user)

    def test_rent_locker_without_authentication(self):
        """Test that renting locker requires authentication"""
        data = {
            'rental_duration': 3600
        }
        response = self.client.post(f'/api/lockers/{self.locker1.id}/rent/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertFalse(response.data['success'])

    def test_rent_locker_invalid_duration(self):
        """Test renting locker with invalid duration"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token.key}')
        data = {
            'rental_duration': -100
        }
        response = self.client.post(f'/api/lockers/{self.locker1.id}/rent/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(response.data['success'])

    def test_rent_locker_not_found(self):
        """Test renting a locker that doesn't exist"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token.key}')
        data = {
            'rental_duration': 3600
        }
        response = self.client.post('/api/lockers/9999/rent/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertFalse(response.data['success'])

    def test_rent_locker_already_in_use(self):
        """Test renting a locker that's already in use"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token.key}')
        data = {
            'rental_duration': 3600
        }
        response = self.client.post(f'/api/lockers/{self.locker2.id}/rent/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(response.data['success'])
        self.assertIn('not available', response.data['error'])

    def test_release_locker_success(self):
        """Test successfully releasing a rented locker"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token.key}')
        
        # First rent a locker
        rent_data = {'rental_duration': 3600}
        self.client.post(f'/api/lockers/{self.locker1.id}/rent/', rent_data, format='json')
        
        # Then release it
        response = self.client.post(f'/api/lockers/{self.locker1.id}/release/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        
        released_locker = response.data.get('locker', {})
        self.assertEqual(released_locker.get('status'), 'Available')
        self.assertIsNone(released_locker.get('owner'))
        self.assertEqual(released_locker.get('time_left'), 0)
        self.assertEqual(released_locker.get('rental_duration'), 0)
        
        # Verify in database
        self.locker1.refresh_from_db()
        self.assertEqual(self.locker1.status, 'Available')
        self.assertIsNone(self.locker1.owner)
        self.assertEqual(self.locker1.time_left, 0)
        self.assertEqual(self.locker1.rental_duration, 0)

    def test_release_locker_without_authentication(self):
        """Test that releasing locker requires authentication"""
        response = self.client.post(f'/api/lockers/{self.locker2.id}/release/', format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertFalse(response.data['success'])

    def test_release_locker_not_found(self):
        """Test releasing a locker that doesn't exist"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token.key}')
        response = self.client.post('/api/lockers/9999/release/', format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertFalse(response.data['success'])

    def test_release_locker_not_in_use(self):
        """Test releasing a locker that's not in use"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token.key}')
        response = self.client.post(f'/api/lockers/{self.locker1.id}/release/', format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(response.data['success'])
        self.assertIn('not in use', response.data['error'])
