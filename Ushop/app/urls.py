from django.urls import path
from app import views
from django.contrib.auth import views as auth_view
from .forms import *

urlpatterns = [
    # path('', views.home),
    path('', views.ProductView.as_view(), name='home'),
    path('product-detail/<int:pk>', views.ProductDetailView.as_view(), name='product-detail'),
    path('cart/', views.add_to_cart, name='add-to-cart'),
    path('buy/', views.buy_now, name='buy-now'),
    path('profile/', views.profile, name='profile'),
    path('address/', views.address, name='address'),
    path('orders/', views.orders, name='orders'),
    # path('changepassword/', views.change_password, name='changepassword'),
    path('mobile/', views.mobile, name='mobile'),
    path('mobile/<slug:data>', views.mobile, name='mobiledata'),
    path('login/', auth_view.LoginView.as_view(template_name='app/login.html',
                                               authentication_form=LoginForm), name='login'),
    path('logout/', auth_view.LogoutView.as_view(next_page='login'), name='logout'),
    path('registration/', views.CustomerRegistrationView.as_view(), name='customerregistration'),
    path('checkout/', views.checkout, name='checkout'),

    path('passwordchange/', auth_view.PasswordChangeView.as_view(template_name='app/passwordchange.html',
                                                                 form_class=MyPasswordChangeForm, success_url='/passchangedone/',), name='passwordchange'),
    path('passchangedone/', auth_view.PasswordChangeDoneView.as_view(template_name='app/passchangedone.html'), name='passchangedone'),
    path('pass-reset/', auth_view.PasswordResetView.as_view(template_name='app/password_reset.html', form_class=MyPasswordResetForm), name='reset'),
    path('password-reset/done/', auth_view.PasswordResetDoneView.as_view(template_name='app/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uid64>/<token>/', auth_view.PasswordResetConfirmView.as_view(template_name='app/password_reset_confirm.html', form_class=MyPasswordResetConfirmView), name='password_reset_confirm'),

]
