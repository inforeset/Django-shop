from django.urls import path
from .views import validate_email, validate_phone, ProfileView, MyRegistration, MyLogoutView, MyLoginView, \
    MyPasswordResetView, MyPasswordResetDoneView, MyPasswordResetConfirmView, MyPasswordResetCompleteView, \
    ModalLoginView, OrderRegistrationUser

urlpatterns = [path('login/', MyLoginView.as_view(redirect_authenticated_user=True), name='login'),
               path('log_in/', ModalLoginView.as_view(), name='login_modal'),
               path('logout/', MyLogoutView.as_view(), name='logout'),
               path('registration/', MyRegistration.as_view(), name='registration'),
               path('registration_order/', OrderRegistrationUser.as_view(), name='registration_order'),
               path('validate_email', validate_email, name='validate_email'),
               path('validate_phone', validate_phone, name='validate_phone'),
               path('profile/', ProfileView.as_view(), name='profile'),
               path('password-reset/', MyPasswordResetView.as_view(), name='password_reset'),
               path('password-reset/done/', MyPasswordResetDoneView.as_view(),
                    name='password_reset_done'),
               path('password-reset/confirm/<uidb64>/<token>/', MyPasswordResetConfirmView.as_view(),
                    name='password_reset_confirm'),
               path('password-reset/complete/', MyPasswordResetCompleteView.as_view(),
                    name='password_reset_complete'),
               ]
