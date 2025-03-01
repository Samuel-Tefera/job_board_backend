"""URL mapping for the user API"""

from django.urls import path

from user import views

app_name = 'user'

urlpatterns = [
     path('create/', views.CreateUserView.as_view(), name='create'),
     path('login/', views.UserLoginView.as_view(), name='get_token'),
     path('logout/', views.UserLogoutView.as_view(), name='delete_token'),
     path('me/', views.ManageUserView.as_view(), name='me'),
     path('<int:id>/', views.UserDetailView.as_view(), name='user')
]
