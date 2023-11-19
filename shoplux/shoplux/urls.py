from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('user_log.urls')),
    path('user_area/',include('user_area.urls')),
    path('admin_log/',include('admin_log.urls')),
    path('product_details/',include('product_det.urls')),
    path('user_product/',include('user_product_mng.urls')),
    path('admin_dashboard/',include('admin_dashboard.urls')),

]
