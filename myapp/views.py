from rest_framework import viewsets
from .services.webpush_service import send_web_push
from .models import Trigger, NotificationTemplate, PushSubscription
from rest_framework.authentication import SessionAuthentication
from .serializers import TriggerSerializer, NotificationTemplateSerializer
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes
)
from rest_framework.response import Response
from .services.email_service import send_email_notification
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAdminUser
from django.views.decorators.csrf import ensure_csrf_cookie


class TriggerViewSet(viewsets.ModelViewSet):
    queryset = Trigger.objects.all()
    serializer_class = TriggerSerializer
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAdminUser]


class NotificationTemplateViewSet(viewsets.ModelViewSet):
    queryset = NotificationTemplate.objects.all()
    serializer_class = NotificationTemplateSerializer
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAdminUser]
    
    
@api_view(['GET'])
def test_email(request):

    response = send_email_notification(
        to_email="sahanipriyanka969@gmail.com",
        subject="Notification System Test",
        content="<h2>Hello!</h2><p>This is a test email from Django.</p>"
    )

    return Response({
        "status_code": response.status_code,
        "response": response.json()
    })
    

@api_view(['GET'])
@authentication_classes([])
@permission_classes([AllowAny])
@ensure_csrf_cookie
def get_csrf_token(request):

    return Response({
        "message": "CSRF cookie set"
    })
    
@ensure_csrf_cookie
@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def admin_login(request):

    username = request.data.get("username")
    password = request.data.get("password")

    user = authenticate(
        username=username,
        password=password
    )

    if user is None:
        return Response(
            {"error": "Invalid username or password"},
            status=400
        )

    if not user.is_staff:
        return Response(
            {"error": "Admin access required"},
            status=403
        )

    login(request, user)


    return Response({
        "message": "Admin login successful",
        "username": user.username
    })    
    
        
@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def login_user(request):

    username = request.data.get("username")
    password = request.data.get("password")

    user = authenticate(
        username=username,
        password=password
    )

    if user is None:
        return Response(
            {"error": "Invalid username or password"},
            status=400
        )

    login(request, user)

    # Find active Login trigger
    trigger = Trigger.objects.filter(
        slug="login",
        is_active=True
    ).first()

    # Find active Email template for Login
    if trigger:
        template = NotificationTemplate.objects.filter(
            trigger=trigger,
            channel="email",
            is_active=True
        ).first()

        # Send email using the template
        if template and user.email:
            send_email_notification(
                to_email=user.email,
                subject=template.subject or "Login Notification",
                content=template.content
            )
            
            # Find active Web Push template for Login
    if trigger:
        push_template = NotificationTemplate.objects.filter(
            trigger=trigger,
            channel="web_push",
            is_active=True
        ).first()

        if push_template:
            subscriptions = PushSubscription.objects.filter(user=user)

            for subscription in subscriptions:
                subscription_info = {
                    "endpoint": subscription.endpoint,
                    "keys": {
                        "p256dh": subscription.p256dh,
                        "auth": subscription.auth,
                    }
                }

                send_web_push(
                    subscription_info=subscription_info,
                    title=push_template.subject or "Login Notification",
                    message=push_template.content
                )    

    return Response({
        "message": "Login successful",
        "username": user.username,
        "email": user.email
    })
    
    #----------------logout user section ----------
    
@api_view(['POST'])
def logout_user(request):

    # Save current user before logout
    username = request.data.get("username")

    user = User.objects.filter(
        username=username
    ).first()

    # Logout user
    logout(request)

    # Find active Logout trigger
    trigger = Trigger.objects.filter(
        slug="logout",
        is_active=True
    ).first()

    if trigger:

        # Find active Email template
        email_template = NotificationTemplate.objects.filter(
            trigger=trigger,
            channel="email",
            is_active=True
        ).first()

        # Send email
        if email_template and user and user.email:
            send_email_notification(
                to_email=user.email,
                subject=email_template.subject or "Logout Notification",
                content=email_template.content
            )

        # Find active Web Push template
        push_template = NotificationTemplate.objects.filter(
            trigger=trigger,
            channel="web_push",
            is_active=True
        ).first()

        # Send Web Push
        if push_template:
            subscriptions = PushSubscription.objects.filter(user=user)

            for subscription in subscriptions:
                subscription_info = {
                    "endpoint": subscription.endpoint,
                    "keys": {
                        "p256dh": subscription.p256dh,
                        "auth": subscription.auth,
                    }
                }

                send_web_push(
                    subscription_info=subscription_info,
                    title=push_template.subject or "Logout Notification",
                    message=push_template.content
                )

    return Response({
        "message": "Logout successful"
    })
#-----------api for PushSubscription---------------------------

@api_view(['POST'])
def save_push_subscription(request):

    if not request.user.is_authenticated:
        return Response(
            {"error": "Please login first."},
            status=401
        )

    subscription = request.data

    endpoint = subscription.get("endpoint")
    keys = subscription.get("keys", {})

    p256dh = keys.get("p256dh")
    auth = keys.get("auth")

    if not endpoint or not p256dh or not auth:
        return Response(
            {"error": "Invalid subscription data"},
            status=400
        )

    push_subscription, created = PushSubscription.objects.update_or_create(
        endpoint=endpoint,
        defaults={
            "user": request.user,
            "p256dh": p256dh,
            "auth": auth,
        }
    )

    return Response({
        "message": "Push subscription saved successfully",
        "created": created
    })   
    
#-------------------------------------------------------
# 
@api_view(['GET'])
def test_web_push(request):
    subscription = PushSubscription.objects.first()

    if not subscription:
        return Response(
            {"error": "No push subscription found"},
            status=404
        )

    trigger = Trigger.objects.filter(
        slug="login",
        is_active=True
    ).first()

    if not trigger:
        return Response(
            {"error": "Login trigger not found"},
            status=404
        )

    template = NotificationTemplate.objects.filter(
        trigger=trigger,
        channel="web_push",
        is_active=True
    ).first()

    if not template:
        return Response(
            {"error": "Web Push template not found"},
            status=404
        )

    subscription_info = {
        "endpoint": subscription.endpoint,
        "keys": {
            "p256dh": subscription.p256dh,
            "auth": subscription.auth,
        }
    }

    response = send_web_push(
        subscription_info=subscription_info,
        title=template.subject or "Notification",
        message=template.content
    )

    if response is None:
        return Response(
            {"error": "Failed to send web push"},
            status=500
        )

    return Response({
        "message": "Web push sent successfully",
        "trigger": trigger.name,
        "template": template.content
    })
    
    
@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def register_user(request):

    username = request.data.get("username")
    email = request.data.get("email")
    password = request.data.get("password")

    if not username or not email or not password:
        return Response(
            {"error": "Username, email and password are required."},
            status=400
        )

    if User.objects.filter(username=username).exists():
        return Response(
            {"error": "Username already exists."},
            status=400
        )

    if User.objects.filter(email=email).exists():
        return Response(
            {"error": "Email already exists."},
            status=400
        )

    user = User.objects.create_user(
        username=username,
        email=email,
        password=password
    )

    return Response(
        {
            "message": "Registration successful",
            "username": user.username,
            "email": user.email
        },
        status=201
    )