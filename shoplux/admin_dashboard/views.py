from django.shortcuts import render,redirect
from product_det.models import Product,Category
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from order_mng.models import Order
from datetime import timedelta, datetime
from django.db.models import Count
from user_log.models import Account
from django.db.models.functions import TruncDate,TruncMonth, TruncYear
from django.db.models import Sum, Q


# Create your views here.

@login_required(login_url='adminlog:admin_login')  # Use the named URL pattern
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def dashboard(request):
    if not request.user.is_superuser:
        return redirect('adminlog:admin_login')
 
    product_count=Product.objects.count()
    category_count=Category.objects.count()
    orders=Order.objects.all()
    last_orders= Order.objects.order_by('-created_at')[:5]
    orders_count=orders.count()
    total_users_count = Account.objects.count()
    total = 0
    for order in orders:
        if order.status == 'Delivered':
            total += order.order_total
        if (order.payment and order.payment.payment_method == 'razorpay') or (order.payment and order.payment.payment_method == 'Wallet'):
            total += order.order_total
    revenue=int(total)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=7)

    daily_order_counts = (
            Order.objects
            .filter(created_at__range=(start_date, end_date), is_ordered=True)
            .values('created_at')
            .annotate(order_count=Count('id'))
            .order_by('created_at')
        )
    
    dates = [entry['created_at'].strftime('%Y-%m-%d') for entry in daily_order_counts]
    counts = [entry['order_count'] for entry in daily_order_counts]
   
    
    monthly_order_counts = (
        Order.objects
        .filter(created_at__year=datetime.now().year)  # Filter by current year
        .annotate(month=TruncMonth('created_at'))
        .values('month')
        .annotate(order_count=Count('id'))
        .order_by('month')
    )
    monthlyDates = [entry['month'].strftime('%Y-%m') for entry in monthly_order_counts]
    monthlyCounts = [entry['order_count'] for entry in monthly_order_counts]

    # Fetch yearly order counts and their respective dates
    yearly_order_counts = (
        Order.objects
        .annotate(year=TruncYear('created_at'))
        .values('year')
        .annotate(order_count=Count('id'))
        .order_by('year')
    )
    yearlyDates = [entry['year'].strftime('%Y') for entry in yearly_order_counts]
    yearlyCounts = [entry['order_count'] for entry in yearly_order_counts]

    statuses = ['Delivered', 'New', 'Conformed', 'Cancelled', 'Return','Shipped']
    order_counts = [Order.objects.filter(status=status).count() for status in statuses]

    print(order_counts)
    context={
        'product_count':product_count,
        'category_count':category_count,
        'orders_count':orders_count,
        'dates': dates,
        'counts': counts,
        'monthlyDates':monthlyDates,
        'monthlyCounts':monthlyCounts,
        'yearlyDates':yearlyDates,
        'yearlyCounts':yearlyCounts,
        'last_orders': last_orders,
        'revenue':revenue,
        'total_users_count': total_users_count,
        'statuses': statuses,
        'order_counts': order_counts,
    }

   

    return render(request, 'admin_side/admin_index.html', context)



def sales_report(request):
    if not request.user.is_superuser:
        return redirect('adminlog:admin_login')
    start_date_value = ""
    end_date_value = ""
    try:

        orders=Order.objects.filter(is_ordered = True).order_by('-created_at')
    
    except:
        pass
    if request.method == 'POST':
       
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        start_date_value = start_date
        end_date_value = end_date
        if start_date and end_date:
          
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
            end_date = datetime.strptime(end_date, '%Y-%m-%d')

           
            orders = orders.filter(created_at__range=(start_date, end_date))
   
    context={
        'orders':orders,
        'start_date_value':start_date_value,
        'end_date_value':end_date_value
    }

    return render(request,'admin_side/sales_report.html',context)