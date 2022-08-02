from django.urls import path

from authentication.api import views

# TODO R-4: Сделать удаление пользователя (путем выставление is_active=False)

urlpatterns = [
    path("auth/registration/", views.CustomUserCreateView.as_view(), name="registration"),
    path("auth/login/", views.LoginView.as_view(), name="token-obtain"),
    path("auth/refresh/", views.RefreshView.as_view(), name="token-refresh"),
    path("auth/logout/", views.LogOutView.as_view(), name="logout"),
    path("users/me/", views.UserDetailView.as_view(), name="user-detail"),
]
