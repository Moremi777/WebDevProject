from django.core.mail import EmailMessage
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.http import HttpResponse
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializers import RegisterSerializer, LoginSerializer
import threading
from django.urls import reverse
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
import json
from django.http import HttpResponseRedirect
from rest_framework import generics, permissions
from rest_framework.authtoken.models import Token
from .serializers import LoginSerializer
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from .forms import UserEditForm  # Import your form if you have one
from django.shortcuts import render, get_object_or_404, redirect
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer
from .permissions import IsAdminUser
from django.contrib.auth.decorators import permission_required
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import PermissionDenied
from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import user_passes_test
from .forms import UserUpdateForm
from django.contrib.auth import update_session_auth_hash
from base.models import Report 

class EmailThread(threading.Thread):
    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()

def send_activation_email(user, request):
    current_site = get_current_site(request)
    email_subject = 'Activate your account'
    email_body = render_to_string('authentication/activate.html', {
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),
    })

    email = EmailMessage(subject=email_subject, body=email_body,
                         from_email=settings.DEFAULT_FROM_EMAIL,
                         to=[user.email]
                         )
    if not settings.TESTING:
        EmailThread(email).start()

def verify_email(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.is_email_verified = True  # Update the is_verified field
        user.save()  # Save the updated user object
        messages.success(request, 'Your email has been verified successfully!')
        return redirect('email_verified_success')  # Redirect to a success page
    else:
        messages.error(request, 'Email verification failed!')
        return redirect('home')

def email_verified_success(request):
    return render(request, 'authentication/email_verified_success.html')

# Ensure that you include `email_verified_su

class RegisterAPIView(APIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully. Please check your email to verify your account."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginAPIView(APIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            data = request.data  # Use request.data instead of json.loads(request.body)
            username = data.get('username')
            password = data.get('password')

            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return Response({'message': 'Login successful!'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'error': 'Invalid method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

class AdminLoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        
        # Check if the user is an admin
        if user is not None and user.is_superuser and user.user_type == 'Administrator':
            login(request, user)
            # Redirect to the admin dashboard
            return redirect('admin_dashboard')  # Replace with your actual dashboard URL name
        else:
            messages.error(request, "Invalid credentials or unauthorized access.")
            return redirect('admin_login')

        # Create or retrieve the auth token
        token, created = Token.objects.get_or_create(user=user)
        
        return Response({
            "token": token.key,
            "username": user.username,
            "email": user.email,
            "user_type": user.user_type
        })


def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')  # Redirect to a home page or any other page if user is already logged in

    return render(request, 'authentication/register.html')

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')  # Redirect to a home page or any other page if user is already logged in

    return render(request, 'authentication/login.html')

def admin_login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_superuser:
            login(request, user)
            return redirect('admin_dashboard')  # Redirect to admin dashboard
        else:
            messages.error(request, 'Invalid credentials or not authorized.')
    return render(request, 'authentication/admin/admin-login.html')


@user_passes_test(lambda u: u.is_superuser)
def add_user(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_manage_users')  # Redirect after successful creation
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'admin/admin_add_user.html', {'form': form})


class AdminDashboardView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        # Collect user statistics
        total_users = User.objects.count()
        reported_documents = Report.objects.all()
        admin_users = User.objects.filter(user_type='administrator').count()
        educator_users = User.objects.filter(user_type='educator').count()
        moderator_users = User.objects.filter(user_type='moderator').count()

        # Initialize Google Analytics client
        client = BetaAnalyticsDataClient.from_service_account_file(
            'templates/admin/serviceapp-427100-5bbd9962ded2.json'
        )

        # Request for page views and active users
        report_request = RunReportRequest(
            property='properties/454885155',  # Use your actual property ID
            dimensions=[{'name': 'pagePath'}],
            metrics=[
                {'name': 'screenPageViews'},
                {'name': 'activeUsers'},
                {'name': 'engagementRate'}  # Corrected metric
            ],
            date_ranges=[{'start_date': '20daysAgo', 'end_date': 'today'}]
        )

        # Request for daily active users
        ga_request = RunReportRequest(
            property='properties/454885155',
            dimensions=[{'name': 'date'}],
            metrics=[{'name': 'activeUsers'}],
            date_ranges=[{'start_date': '30daysAgo', 'end_date': 'today'}]
        )

        # Fetch analytics data
        analytics_data = self.fetch_analytics_data(client, report_request)
        daily_active_users_data = self.fetch_analytics_data(client, ga_request, is_daily=True)

        # Prepare context for rendering
        context = {
            'reported_documents': reported_documents,
            'total_users': total_users,
            'admin_users': admin_users,
            'educator_users': educator_users,
            'moderator_users': moderator_users,
            'page_views_data': [item['page_views'] for item in analytics_data],
            'active_users_data': [item['active_users'] for item in analytics_data],
            'avg_engagement_data': [item['engagementRate'] for item in analytics_data],  # Use engagementRate
            'daily_labels': [item['date'] for item in daily_active_users_data],
            'daily_active_users_data': [item['active_users'] for item in daily_active_users_data],
        }

        return render(request, 'admin/administrator.html', context)

    def fetch_analytics_data(self, client, request, is_daily=False):
        """Fetches analytics data from Google Analytics."""
        try:
            response = client.run_report(request)
            if is_daily:
                return [{'date': row.dimension_values[0].value, 'active_users': row.metric_values[0].value} for row in response.rows]
            else:
                return [{
                    'page_path': row.dimension_values[0].value,
                    'page_views': row.metric_values[0].value,
                    'active_users': row.metric_values[1].value,
                    'engagementRate': row.metric_values[2].value,  # Use engagementRate
                } for row in response.rows]
        except Exception as e:
            print(f"Error fetching Google Analytics data: {e}")
            return []
    def get(self, request, *args, **kwargs):
        # Collect user statistics
        total_users = User.objects.count()
        reported_documents = Report.objects.all()
        admin_users = User.objects.filter(user_type='administrator').count()
        educator_users = User.objects.filter(user_type='educator').count()
        moderator_users = User.objects.filter(user_type='moderator').count()

        # Initialize Google Analytics client
        client = BetaAnalyticsDataClient.from_service_account_file(
            'templates/admin/serviceapp-427100-5bbd9962ded2.json'
        )

        # Request for page views and active users
        report_request = RunReportRequest(
            property='properties/454885155',  # Use your actual property ID
            dimensions=[{'name': 'pagePath'}],
            metrics=[
                {'name': 'screenPageViews'},
                {'name': 'activeUsers'},
                {'name': 'averageEngagementTime'}
            ],
            date_ranges=[{'start_date': '20daysAgo', 'end_date': 'today'}]
        )

        # Request for daily active users
        ga_request = RunReportRequest(
            property='properties/454885155',
            dimensions=[{'name': 'date'}],
            metrics=[{'name': 'activeUsers'}],
            date_ranges=[{'start_date': '20daysAgo', 'end_date': 'today'}]
        )

        # Fetch analytics data
        analytics_data = self.fetch_analytics_data(client, report_request)
        daily_active_users_data = self.fetch_analytics_data(client, ga_request, is_daily=True)

        # Prepare context for rendering
        context = {
            'reported_documents': reported_documents,
            'total_users': total_users,
            'admin_users': admin_users,
            'educator_users': educator_users,
            'moderator_users': moderator_users,
            'page_views_data': [item['page_views'] for item in analytics_data],
            'active_users_data': [item['active_users'] for item in analytics_data],
            'avg_engagement_data': [item['avg_engagement_time'] for item in analytics_data],
            'daily_labels': [item['date'] for item in daily_active_users_data],
            'daily_active_users_data': [item['active_users'] for item in daily_active_users_data],
        }

        return render(request, 'admin/administrator.html', context)

    def fetch_analytics_data(self, client, request, is_daily=False):
        """Fetches analytics data from Google Analytics."""
        try:
            response = client.run_report(request)
            if is_daily:
                return [{'date': row.dimension_values[0].value, 'active_users': row.metric_values[0].value} for row in response.rows]
            else:
                return [{
                    'page_path': row.dimension_values[0].value,
                    'page_views': row.metric_values[0].value,
                    'active_users': row.metric_values[1].value,
                    'avg_engagement_time': row.metric_values[2].value,
                } for row in response.rows]
        except Exception as e:
            print(f"Error fetching Google Analytics data: {e}")
            return []
    def get(self, request, *args, **kwargs):
        total_users = User.objects.count()
        reported_documents = Report.objects.all() 
        admin_users = User.objects.filter(user_type='administrator').count()
        educator_users = User.objects.filter(user_type='educator').count()
        moderator_users = User.objects.filter(user_type='moderator').count()

        # Fetching Google Analytics data
        client = BetaAnalyticsDataClient.from_service_account_file(
            'templates/admin/serviceapp-427100-5bbd9962ded2.json'
        )

        ga_request = RunReportRequest(
            property='properties/454885155',  # Replace with your actual property ID
            dimensions=[{'name': 'date'}],
            metrics=[{'name': 'activeUsers'}],
            date_ranges=[{'start_date': '20daysAgo', 'end_date': 'today'}]
        )

        report_request = RunReportRequest(
            property='properties/454885155',  # Replace with your property ID
            dimensions=[{'name': 'pagePath'}],
            metrics=[
                {'name': 'screenPageViews'},
                {'name': 'activeUsers'},
                {'name': 'engagementRate'}
            ],
            date_ranges=[{'start_date': '30daysAgo', 'end_date': 'today'}]
        )

        try:
            response = client.run_report(report_request)
            analytics_data = [
                {
                    'page_path': row.dimension_values[0].value,
                    'page_views': row.metric_values[0].value,
                    'active_users': row.metric_values[1].value,
                }
                for row in response.rows
            ]
        except Exception as e:
            analytics_data = []
            print(f"Error fetching Google Analytics data: {e}")

        # Prepare data for Chart.js
        labels = [item['page_path'] for item in analytics_data]
        page_views_data = [item['page_views'] for item in analytics_data]
        active_users_data = [item['active_users'] for item in analytics_data]

        context = {
            'labels': labels,
            'page_views_data': page_views_data,
            'active_users_data': active_users_data,
        }

        try:
            response = client.run_report(ga_request)
            google_analytics_data = [
                {'date': row.dimension_values[0].value, 'active_users': row.metric_values[0].value}
                for row in response.rows
            ]
        except Exception as e:
            google_analytics_data = []
            print(f"Error fetching Google Analytics data: {e}")

        # Prepare data for Chart.js
        labels = [item['date'] for item in google_analytics_data]
        active_users_data = [item['active_users'] for item in google_analytics_data]

        context = {
            'reported_documents': reported_documents,
            'total_users': total_users,
            'admin_users': admin_users,
            'educator_users': educator_users,
            'moderator_users': moderator_users,
            'labels': labels,  # Dates for the chart
            'active_users_data': active_users_data,  # Active users for the chart
        }

        return render(request, 'admin/administrator.html', context)

class DeleteUserView(APIView):
    permission_classes = [IsAdminUser]

    def delete(self, request, user_id, format=None):
        user = get_object_or_404(User, id=user_id)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

@login_required
def manage_users(request):
    users = User.objects.all()
    return render(request, 'admin/manage_users.html', {'users': users})

@login_required
def edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('admin_manage_users')  # Redirect after saving
    else:
        form = UserEditForm(instance=user)
    return render(request, 'admin/edit_user.html', {'form': form, 'user': user})

@login_required
def site_settings(request):
    # Logic to display and edit site settings
    return render(request, 'admin/site_settings.html')

@login_required
def update_site_settings(request):
    if request.method == 'POST':
        # Logic to handle form submission and update settings
        # For example, update settings in the database
        # settings_form = SettingsForm(request.POST)
        # if settings_form.is_valid():
        #     settings_form.save()
        return redirect('admin_site_settings')  # Redirect after updating settings
    else:
        # Display form for updating settings
        # settings_form = SettingsForm()
        return render(request, 'admin/update_site_settings.html')

@login_required
def site_settings(request):
    # Add logic to handle site settings if necessary
    return render(request, 'admin/site_settings.html')

@login_required
def update_profile(request):
    if request.user.user_type not in ['Educator', 'Moderator']:
        raise PermissionDenied

    if request.method == 'POST':
        form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('update_profile')
    else:
        form = UserUpdateForm(instance=request.user)

    return render(request, 'userprofile/update_profile.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')