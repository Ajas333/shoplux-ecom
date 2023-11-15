from django.shortcuts import render,redirect
from product_det.models import Product,Category
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control

# Create your views here.

@login_required(login_url='adminlog:admin_login')  # Use the named URL pattern
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('adminlog:admin_login')

    product_count=Product.objects.count()
    category_count=Category.objects.count()
    
    context={
        'product_count':product_count,
        'category_count':category_count
    }

    return render(request, 'admin/admin_index.html', context)