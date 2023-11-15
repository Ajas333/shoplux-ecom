from django.urls import path
from admin_dashboard import views


app_name='admin_dashboard'

urlpatterns = [
    path('dashboard',views.dashboard,name='dashboard')
]
