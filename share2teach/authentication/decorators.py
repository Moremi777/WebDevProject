from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseForbidden
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication, SessionAuthentication

class SomeProtectedView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    
    def get(self, request):
        return Response({'message': 'This is a protected route.'})

def is_educator(user):
    return user.is_authenticated and user.user_type == 'educator'

def is_moderator(user):
    return user.is_authenticated and user.user_type == 'moderator'

def is_administrator(user):
    return user.is_authenticated and user.user_type == 'administrator'

def educator_required(view_func):
    decorated_view_func = user_passes_test(is_educator, login_url='login')(view_func)
    return decorated_view_func

def moderator_required(view_func):
    decorated_view_func = user_passes_test(is_moderator, login_url='login')(view_func)
    return decorated_view_func

def administrator_required(view_func):
    decorated_view_func = user_passes_test(is_administrator, login_url='login')(view_func)
    return decorated_view_func
