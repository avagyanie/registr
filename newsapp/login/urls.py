from django.urls import path, include
from .views import Register, terms_conditions, ProfileTemplate, update_profile, PasswordChangeView, simple_logout
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView


urlpatterns = [
    path('', include("django.contrib.auth.urls")),
    path('register/', Register.as_view(), name = "register"),
    path("terms-conditions/", terms_conditions, name="terms_conditions"),
    path('simple-logout/', simple_logout, name='simple_logout'),
    path('profile/', ProfileTemplate.as_view(), name = "profile"),
    path('update-profile/', update_profile, name = "update_profile"),
    path('change-password/', PasswordChangeView.as_view(), name = "change_password"),
    path('password_reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password_reset_confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
