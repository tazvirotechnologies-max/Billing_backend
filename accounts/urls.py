from django.urls import path
from .views import LoginView, MeView, LogoutView, StaffView, StaffStatusView

urlpatterns = [
    path('login/', LoginView.as_view()),
    path('me/', MeView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('staff/', StaffView.as_view()),
    # ✅ NEW
    path(
        'staff/<int:user_id>/status/',
        StaffStatusView.as_view()
    ),
]