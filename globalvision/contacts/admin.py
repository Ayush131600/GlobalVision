from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import ContactMessage

from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings

@admin.register(ContactMessage)
class ContactMessageAdmin(ModelAdmin):
    model_icon = 'mail'
    list_display = ('name', 'email', 'subject', 'status', 'is_read', 'created_at', 'replied_at')
    list_filter = ('status', 'is_read', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message', 'reply_message')
    readonly_fields = ('created_at', 'replied_at')
    fieldsets = (
        (None, {
            'fields': ('status', 'is_read')
        }),
        ('User Inquiry', {
            'fields': ('user', 'name', 'email', 'phone', 'subject', 'message', 'created_at')
        }),
        ('Admin Response', {
            'fields': ('reply_message', 'replied_at')
        }),
    )

    def save_model(self, request, obj, form, change):
        # Check if reply_message is being added/updated and start the email process
        if change and 'reply_message' in form.changed_data and obj.reply_message:
            item_name = "your inquiry"
            if obj.subject:
                item_name = f"'{obj.subject}'"
            
            email_subject = f"Response to your inquiry: {obj.subject}"
            email_body = f"Hello {obj.name},\n\nThank you for reaching out to Global Vision.\n\nOur team has reviewed your message regarding {item_name} and provided the following response:\n\n---\n{obj.reply_message}\n---\n\nIf you have any further questions, feel free to reply to this email.\n\nBest regards,\nThe Global Vision Team"
            
            try:
                send_mail(
                    email_subject,
                    email_body,
                    settings.DEFAULT_FROM_EMAIL,
                    [obj.email],
                    fail_silently=False,
                )
                obj.replied_at = timezone.now()
                obj.status = 'Resolved'
            except Exception as e:
                # You might want to log this or notify the admin
                pass
                
        super().save_model(request, obj, form, change)
