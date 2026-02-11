from django.urls import path
from .views import LoginView, MeView, LogoutView, StaffView

urlpatterns = [
    path('login/', LoginView.as_view()),
    path('me/', MeView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('staff/', StaffView.as_view()),
]