from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from web import views, forms

app_name = 'web'

urlpatterns = [
    path('', views.start_page, name='start_page'),
    path('advert/<int:advert_id>', views.advert, name='advert'),
    path('category/<slug:category>', views.all_in_category, name='all_in_category'),
    path('create_advert', views.create_advert, name='create_advert'),
    path('edit_profile', views.edit_profile, name='edit_profile'),

    path('login/', LoginView.as_view(template_name='login.html', authentication_form=forms.UserLoginForm), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),
]