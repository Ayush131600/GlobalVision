from django.core.mail import send_mail
from django.conf import settings
from .models import Notification

def create_notification(user, title, message, type='general', link=None, send_email=True):
    # Create DB entry
    notification = Notification.objects.create(
        user=user,
        title=title,
        message=message,
        notification_type=type,
        link=link
    )
    
    # Send email if requested and user has email
    if send_email and user.email:
        try:
            subject = f"Global Vision: {title}"
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=True,
            )
        except Exception as e:
            print(f"Error sending notification email: {e}")
            
    return notification
