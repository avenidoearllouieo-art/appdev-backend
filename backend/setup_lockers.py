#!/usr/bin/env python
"""
Setup script to initialize Smart Locker System
Creates sample lockers for testing
"""

import os
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
import django
django.setup()

from lockers.models import Locker

def create_sample_lockers():
    """Create sample lockers"""
    print("Creating sample lockers...")
    
    # Delete existing lockers
    Locker.objects.all().delete()
    print("✓ Cleared existing lockers")
    
    # Create 10 sample lockers
    for i in range(1, 11):
        locker = Locker.objects.create(
            locker_number=i,
            status="Available",
            rented_by=None,
            rental_hours=0,
            is_active=True
        )
        print(f"✓ Created Locker {i}")
    
    print("\n✓ Setup complete! 10 lockers created")
    print("\nLocker Summary:")
    for locker in Locker.objects.all().order_by('locker_number'):
        print(f"  Locker {locker.locker_number}: {locker.status} | Rented by: {locker.rented_by} | Hours: {locker.rental_hours}h")

if __name__ == '__main__':
    create_sample_lockers()
