from django.urls import path
from .views import LoginView, MeView, StaffView

urlpatterns = [
    path('login/', LoginView.as_view()),
    path('me/', MeView.as_view()),
    path('staff/', StaffView.as_view()),
]