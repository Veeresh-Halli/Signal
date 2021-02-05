from django.contrib.auth.models import User
from django.contrib.auth.signals import user_logged_in,user_logged_out
from django.dispatch import receiver
from django.core.cache import cache
from .models import LoggedUsers

@receiver(user_logged_in, sender=User)
def login_success(sender, request, user, **kwargs):
    count = cache.get('count',0 )
    new_count = count + 1
    cache.set('count', new_count, 60*60*24)

@receiver(user_logged_in, sender=User)
def user_login_success(sender, request, user, **kwargs):
    count1 = cache.get('count1',0 ,version=user.pk)
    new_count1 = count1 + 1
    cache.set('count1', new_count1, 60*60*24, version=user.pk)
    ip = request.META.get('REMOTE_ADDR')
    browser = request.META.get('HTTP_USER_AGENT')
    request.session['ip'] = ip
    request.session['browser'] = browser
    LoggedUsers(user=user).save()
 
    
@receiver(user_logged_out, sender=User)
def user_logout(sender,request, user, **kwargs):
    u = LoggedUsers.objects.get(user=user)
    u.delete()