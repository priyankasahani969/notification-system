from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TriggerViewSet, NotificationTemplateViewSet


router = DefaultRouter()

router.register(
    r'triggers',
    TriggerViewSet,
    basename='trigger'
)

router.register(
    r'templates',
    NotificationTemplateViewSet,
    basename='notification-template'
)

from .views import (
    TriggerViewSet,
    NotificationTemplateViewSet,
    test_email
)

from .views import (
    TriggerViewSet,
    NotificationTemplateViewSet,
    test_email,
    login_user,
    logout_user,
    save_push_subscription,
    test_web_push,register_user,admin_login,get_csrf_token
)


urlpatterns = [
    path('', include(router.urls)),
    path('test-email/', test_email),
    path('login/', login_user),
    path('logout/', logout_user),
    path('save-push-subscription/', save_push_subscription),
    path('test-web-push/', test_web_push),
    path('register/', register_user),
    path('admin-login/', admin_login),
    path('csrf/', get_csrf_token),

]