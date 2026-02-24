import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'globalvision.settings')
django.setup()

from account.models import Vehicle, Equipment

def seed():
    # Clear existing data to avoid category mismatches
    Equipment.objects.all().delete()
    Vehicle.objects.all().delete()

    # Seed Vehicles
    vehicles = [
        {
            'name': 'Lamborghini Urus',
            'price_per_day': 800.00,
            'description': 'The ultimate luxury SUV. Experience power and comfort in the Lamborghini Urus, perfect for high-end travel.',
            'category': 'luxury'
        },
        {
            'name': 'Jeep Wrangler',
            'price_per_day': 120.00,
            'description': 'Go anywhere with the Jeep Wrangler. Built for off-road adventures and rugged terrain.',
            'category': 'off_road'
        },
        {
            'name': 'Ford Transit',
            'price_per_day': 150.00,
            'description': 'Spacious and reliable. The Ford Transit is ideal for group travel and long journeys with heavy luggage.',
            'category': 'van'
        }
    ]

    for v in vehicles:
        Vehicle.objects.get_or_create(
            name=v['name'],
            defaults={
                'price_per_day': v['price_per_day'],
                'description': v['description'],
                'category': v['category'],
                'is_available': True
            }
        )

    # Seed Trekking Equipment
    trekking_gear = [
        {
            'name': 'North Face 4-Season Tent',
            'price_per_day': 25.00,
            'description': 'High-alpine 4-season tent designed for extreme conditions. Perfect for Himalayan trekking.',
            'category': 'gear'
        },
        {
            'name': 'Osprey Aether 70L Backpack',
            'price_per_day': 12.00,
            'description': 'Ergonomic 70L backpack with custom-molded hipbelt. Ideal for multi-day expeditions.',
            'category': 'gear'
        },
        {
            'name': 'Gore-Tex Hardshell Jacket',
            'price_per_day': 10.00,
            'description': 'Waterproof and breathable hardshell jacket for extreme weather protection.',
            'category': 'clothing'
        },
        {
            'name': 'Trekking Pole Set',
            'price_per_day': 5.00,
            'description': 'Lightweight carbon fiber trekking poles for stability on rugged terrain.',
            'category': 'essentials'
        },
        {
            'name': 'High-Altitude Sleeping Bag (-20\u00b0C)',
            'price_per_day': 15.00,
            'description': 'Professional down sleeping bag rated for -20 degrees Celsius. Essential for high-altitude camps.',
            'category': 'gear'
        },
        {
            'name': 'Professional First Aid Kit',
            'price_per_day': 3.00,
            'description': 'Comprehensive medical kit equipped for common trekking injuries and altitude sickness essentials.',
            'category': 'essentials'
        }
    ]

    for item in trekking_gear:
        Equipment.objects.get_or_create(
            name=item['name'],
            defaults={
                'price_per_day': item['price_per_day'],
                'description': item['description'],
                'category': item['category'],
                'is_available': True
            }
        )

    print("Seeding completed successfully!")

if __name__ == '__main__':
    seed()
