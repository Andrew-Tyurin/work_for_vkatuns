from django.urls import path, include

from user import views


urlpatterns = [
    path('mycompany/', include('user_company.urls')),
    path('login/', views.LoginUserView.as_view(), name='login'),
    path('register/', views.RegisterUserView.as_view(), name='register'),
    path('logout/', views.LogoutUserView.as_view(), name='logout'),
]