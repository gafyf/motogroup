from django.urls import path, include
from . import views


app_name = 'account'

urlpatterns = [
    path("signup/", views.register, name="signup"),
    path("activate/<str:uidb64>/<str:token>/", views.activate, name="activate"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("password_reset/", views.PasswordResetView.as_view(), name="password_reset_form"),
    path("reset/<str:uidb64>/<str:token>/", views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path("password_reset/done/", views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path("password_reset/complete/", views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),
    path("password_change/", views.PasswordChangeView.as_view(), name="password_change_form"),
    path('password_change/done/',  views.password_change_done, name='password_change_done'),
    path('edit_user/<str:pk>/', views.edit_user, name='edit_user'),
    path('delete_user/<str:pk>/', views.DeleteUser.as_view(), name='delete_user'),
    path('edit_profile/<str:pk>/', views.ProfileUpdateView.as_view(), name='edit_profile'),
    path('detail_profile/<str:pk>/', views.detail_profile, name='detail_profile'),
    path('delete_profile/<str:pk>/', views.delete_profile, name='delete_profile'),
    path('', include("django.contrib.auth.urls")),
]
