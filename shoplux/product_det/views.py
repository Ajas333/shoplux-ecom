from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from product_det.models import Category,Brand,Atribute,Atribute_Value,Product,Product_Variant
from django.forms.formsets import formset_factory

# Create your views here.


# --------------------------------------Categary area----------------------------------------------

def category(request):
    if not request.user.is_superuser:
        return redirect('adminlog:admin_login')
    categories = Category.objects.all()
    content = {
        'categories': categories
    }
    return render(request, 'admin/product_categories.html',content)


def add_category(request):
    category_name = request.POST['category_name']
    parent = None if request.POST['parent'] == 'None' else Category.objects.get(category_name=request.POST['parent'])
    description = request.POST['description']

    Category.objects.create(
        category_name=category_name,
        parent=parent,
        description=description,
        
    )
    return redirect('product_details:category')


def available(request,category_id):
    if not request.user.is_authenticated:
        return HttpResponse("Unauthorized", status=401)
    
    category = get_object_or_404(Category, id=category_id)
    
    if category.is_available:
        category.is_available=False
       
    else:
        category.is_available=True
    category.save()

    
    cat_list=Category.objects.filter(parent_id=category_id)
    for i in cat_list.values():
        print(i)
    
    for category in cat_list:
        if category.is_available:
            category.is_available=False
        else:
            category.is_available=True
        category.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def delete_category(request,category_id):
    if not request.user.is_authenticated:
        return HttpResponse("Unauthorized", status=401)
    try:
        category=Category.objects.get(id=category_id)
    except ValueError:
        return redirect('product_details:category')
    category.delete()

    return redirect('product_details:category')


def edit_category(request,category_id):
    if not request.user.is_authenticated:
        return HttpResponse("Unauthorized", status=401)
    
    category_list=Category.objects.get(id=category_id)
    category_name=category_list.category_name
    category_disc=category_list.description
   
    content={
        'category_name':category_name,
        'category_disc':category_disc
    }
    
    if request.method == "POST":
        cat_name = request.POST['category_name']
        cat_desc = request.POST['description']
        
        category_list.category_name=cat_name
        category_list.description=cat_desc
        category_list.save()

        return redirect('product_details:category')

    return render(request,'admin/edit_category.html',content)
# ------------------------------------------end categary-----------------------------------------------------------



# ----------------------------------------------Brand-----------------------------------------------------------------

def brand(request):
    if not request.user.is_superuser:
        return redirect('adminlog:admin_login')
    brands = Brand.objects.all()
    content = {
        'brands': brands
    }
    return render(request, 'admin/add_brand.html',content)

def add_brand(request):
    brand_name = request.POST['brand_name']
    Brand.objects.create(
        brand_name=brand_name,
    )
    return redirect('product_details:brand')
    
def brand_available(request,brand_id):
    if not request.user.is_authenticated:
        return HttpResponse("Unauthorized", status=401)
    
    brand = get_object_or_404(Brand, id=brand_id)
    
    if brand.is_active:
        brand.is_active=False
       
    else:
        brand.is_active=True
    brand.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def delete_brand(request,brand_id):
    if not request.user.is_authenticated:
        return HttpResponse("Unauthorized", status=401)
    try:
        brand=Brand.objects.get(id=brand_id)
    except ValueError:
        return redirect('product_details:brand')
    brand.delete()

    return redirect('product_details:brand')
# -------------------------------------------------------end brand---------------------------------------------------




# -------------------------------------------------------Attribute------------------------------------------------------
def attribute(request):
    if not request.user.is_superuser:
        return redirect('adminlog:admin_login')
    attributes = Atribute.objects.all()
    content = {
        'attributes': attributes
    }
    return render(request, 'admin/add_attribute.html',content)

def add_attribute(request):
    attribute_name = request.POST['attribute_name']
    Atribute.objects.create(
        atribute_name=attribute_name,
    )
    return redirect('product_details:attribute')

def attribute_available(request,attribute_id):
    if not request.user.is_authenticated:
        return HttpResponse("Unauthorized", status=401)
   
    attribute = Atribute.objects.get(id=attribute_id)
    
    if attribute.is_active:
        attribute.is_active=False
       
    else:
        attribute.is_active=True
    attribute.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def delete_attribute(request,attribute_id):
    if not request.user.is_authenticated:
        return HttpResponse("Unauthorized", status=401)
    try:
        attribute=Atribute.objects.get(id=attribute_id)
    except ValueError:
        return redirect('product_details:attribute')
    attribute.delete()

    return redirect('product_details:attribute')
# ---------------------------------------------------------end attribute---------------------------------------------------



# ----------------------------------------------------------Attribute value-------------------------------------------------
def attribute_value(request):
    if not request.user.is_superuser:
        return redirect('adminlog:admin_login')
    attribute_values = Atribute_Value.objects.all()
    attribute_names=Atribute.objects.all()
    content = {
        'attribute_values': attribute_values,
        'attribute_names': attribute_names
    }
    return render(request, 'admin/add_attribute_value.html',content)


def add_attribute_value(request):
    if request.method == 'POST':
        attribute_value_n = request.POST.get('attribute_value_name')
        attribute = request.POST.get('attribute')
        if attribute_value_n and attribute:
            attribute_id = Atribute.objects.get(atribute_name=attribute)
            Atribute_Value.objects.create(
                atribute_value=attribute_value_n,
                atribute_id=attribute_id.id
            )
    
    attribute_values = Atribute_Value.objects.all()
    attribute_names = Atribute.objects.all()
    context = {
        'attribute_values': attribute_values,
        'attribute_names': attribute_names
    }
    
    return render(request, 'admin/add_attribute_value.html', context)


def attribute_value_available(request,attribute_value_id):
    if not request.user.is_authenticated:
        return HttpResponse("Unauthorized", status=401)
   
    attribute_value = Atribute_Value.objects.get(id=attribute_value_id)
    
    if attribute_value.is_active:
        attribute_value.is_active=False
       
    else:
        attribute_value.is_active=True
    attribute_value.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def delete_attribute_value(request,attribute_value_id):
    if not request.user.is_authenticated:
        return HttpResponse("Unauthorized", status=401)
    try:
        attribute_value=Atribute_Value.objects.get(id=attribute_value_id)
    except ValueError:
        return redirect('product_details:attribute_value')
    attribute_value.delete()

    return redirect('product_details:attribute_value')



# --------------------------------------------end attribute value-------------------------------------------------
       
    




#--------------------------------------------------add product with verient---------------------------------------




def add_product(request):
    if not request.user.is_authenticated:
        return HttpResponse("Unauthorized", status=401)
    categories = Category.objects.all()
    brands = Brand.objects.all().exclude(is_active=False)
    # attribute=Atribute_Value.objects.prefetch_related('atribute_id').all()
    
     
    content = {
        'categories': categories,
        'brands': brands,        
    }
    if request.method == 'POST':
        product_name= request.POST.get('product_name')
        product_sk_id= request.POST.get('sku_id')
        description= request.POST.get('product_desc')
        max_price= request.POST.get('product_max_price')
        sale_price= request.POST.get('product_sale_price')
        category_name= request.POST.get('product_category')
        brand_name=request.POST.get('product_brand')

       

        category = get_object_or_404(Category, category_name=category_name)
        brand = get_object_or_404(Brand, brand_name=brand_name)

        product = Product(
            product_name=product_name,
            sku_id=product_sk_id,
            product_catg=category,
            product_brand=brand,
            product_description=description,
            max_price=max_price,
            sale_price=sale_price,
            image=request.FILES['image_feild']  # Make sure your file input field is named 'product_image'
        )
        product.save()
   
       

        return redirect('product_details:add_product')
   
    return render(request,'admin/add_product.html', content)

    



#---------------------------------------------------------end product verient------------------------------------



#-------------------------------------------------------product list----------------------------------------------

def product_list(request):

    products=Product.objects.all()
    context={
       "products":products,
   }
    return render(request, 'admin/product_list.html',context)




def product_det(request, product_id):

    product=get_object_or_404(Product,id=product_id)
    context={
        'product':product
    }

    return render(request,'admin/product_details.html',context)

def update_product(request,product_id):
     
     product=Product.objects.get(id=product_id)

     if request.method=='POST':
         product_name=request.POST.get('product_name')
         sku_id=request.POST.get('sku_id')
         desc=request.POSt.get('product_desc')
         max_price=request.POST.get('max_price')
         sale_price=request.POST.get('sale_price') 
         print(product_name)
         product.product_name=product_name
         product.sku_id=sku_id
         product.product_description=desc 
         product.max_price=max_price  
         product.sale_price=sale_price

         if 'image_field' in request.FILES:
            product.image = request.FILES['image_field']
         product.save() 

         return redirect('product_details:product_list')     

     return redirect('product_details:product_list') 