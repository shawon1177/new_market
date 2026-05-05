from .models import Profile

def notifications(request):
    try:
        if request.user.is_authenticated:
            from listings.models import Notification

            count = Notification.objects.filter(
                user=request.user,
                is_read=False
            ).count()

            return {"notifications_count": count}

    except Exception:
        return {"notifications_count": 0}

    return {"notifications_count": 0}


def user_profile(request):
    if request.user.is_authenticated:
        profile, _ = Profile.objects.get_or_create(user=request.user)
        return {"nav_profile": profile}
    return {"nav_profile": None}


