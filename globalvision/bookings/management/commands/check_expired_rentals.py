from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import date
from bookings.models import Booking
from notifications.utils import create_notification

class Command(BaseCommand):
    help = 'Checks for expired rentals and sends notifications to users'

    def handle(self, *args, **kwargs):
        today = timezone.localdate()
        
        # Find bookings that have ended and are still active or confirmed
        expired_bookings = Booking.objects.filter(
            end_date__lt=today,
            status__in=['Active', 'Confirmed']
        )
        
        count = expired_bookings.count()
        if count == 0:
            self.stdout.write(self.style.SUCCESS("No expired rentals found to process."))
            return
            
        for booking in expired_bookings:
            # Update status
            booking.status = 'Completed'
            booking.save()
            
            # Send Notification & Email
            item_name = booking.item.name if booking.item else "your rental item"
            title = "Rental Period Completed"
            message = f"Hi {booking.user.user_name},\n\nThe rental period for {item_name} has ended. We hope you had a great time! Please ensure the item has been returned successfully.\n\nThank you for choosing GlobalVision."
            
            try:
                create_notification(
                    user=booking.user,
                    title=title,
                    message=message,
                    type='rental', # Using rental type based on models.py
                    link='/user-dashboard/history/',
                    send_email=True
                )
                self.stdout.write(self.style.SUCCESS(f"Processed booking #{booking.id} - Notification sent to {booking.user.user_name}"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error sending notification for booking #{booking.id}: {e}"))
                
        self.stdout.write(self.style.SUCCESS(f"Successfully processed {count} expired rental(s)."))
