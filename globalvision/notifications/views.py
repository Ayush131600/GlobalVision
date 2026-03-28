from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Notification
from django.contrib import messages
from django.contrib.auth import get_user_model

User = get_user_model()

@login_required
def notification_list(request):
    notifications = Notification.objects.filter(user=request.user)
    return render(request, 'notifications/list.html', {'notifications': notifications})


@login_required
def get_notifications(request):
    notifications = Notification.objects.filter(user=request.user)[:10]
    unread_count = Notification.objects.filter(user=request.user, is_read=False).count()
    
    data = []
    for n in notifications:
        data.append({
            'id': n.id,
            'title': n.title,
            'message': n.message,
            'type': n.notification_type,
            'is_read': n.is_read,
            'created_at': n.created_at.strftime("%b %d, %H:%M"),
            'link': n.link
        })
        
    return JsonResponse({'notifications': data, 'unread_count': unread_count})

@login_required
def mark_read(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id, user=request.user)
    notification.is_read = True
    notification.save()
    if notification.link:
        return redirect(notification.link)
    return redirect(request.META.get('HTTP_REFERER', '/'))

@login_required
def mark_all_read(request):
    Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
    return JsonResponse({'status': 'success'})

@login_required
def send_admin_notification(request):
    if not (request.user.is_staff or getattr(request.user, 'role', '') == 'admin'):
        return JsonResponse({'status': 'unauthorized'}, status=433)
        
    if request.method == 'POST':
        user_id = request.POST.get('user_id') # 'all' or specific ID
        title = request.POST.get('title')
        message = request.POST.get('message')
        type = request.POST.get('type', 'admin')
        
        from .utils import create_notification
        
        if user_id == 'all':
            users = User.objects.all()
            for user in users:
                create_notification(user, title, message, type=type)
            messages.success(request, f'Global notification sent to {users.count()} users.')
        elif user_id:
            user = get_object_or_404(User, pk=user_id)
            create_notification(
                user=user,
                title=title,
                message=message,
                type=type,
                link='/dashboard/user/history/'
            )
            messages.success(request, f'Notification sent to {user.user_name}.')
            
        return redirect(request.META.get('HTTP_REFERER', 'admin_notifications'))

    users = User.objects.all()
    return render(request, 'notifications/admin_send.html', {'users': users})
