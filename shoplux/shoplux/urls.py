from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('user_log.urls')),
    path('admin_log/',include('admin_log.urls')),
    path('product_details/',include('product_det.urls')),

]
