from django.urls import path
from admin_dashboard import views


app_name='admin_dashboard'

urlpatterns = [
    path('dashboard',views.dashboard,name='dashboard'),
    path('sales_report',views.sales_report,name='sales_report')
]
