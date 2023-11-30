from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from product_det.models import Category,Brand,Atribute,Atribute_Value,Product,Product_Variant
from .forms import CreateProductForm
from django.views.decorators.cache import cache_control
from django.contrib import messages


# Create your views here.


# --------------------------------------Categary area----------------------------------------------


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def category(request):
    if not request.user.is_superuser:
        return redirect('adminlog:admin_login')
    categories = Category.objects.all()
    content = {
        'categories': categories
    }
    return render(request, 'admin_side/product_categories.html',content)



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def add_category(request):
    if not request.user.is_superuser:
        return redirect('adminlog:admin_login')
    
    if request.method == "POST":
        category_name = request.POST['category_name']
        parent = None if request.POST['parent'] == 'None' else Category.objects.get(category_name=request.POST['parent'])
        description = request.POST['description']

        validate=validate_no_spaces(category_name)
        
        if validate:
            Category.objects.create(
                category_name=category_name,
                parent=parent,
                description=description,
                
            )
        else:
            messages.error(request,"Provide Categary name without space")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        
    return redirect('product_details:category')



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def available(request,category_id):
    if not request.user.is_authenticated:
        return HttpResponse("Unauthorized", status=401)
    if not request.user.is_superuser:
        return redirect('adminlog:admin_login')
    
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


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def delete_category(request,category_id):
    if not request.user.is_authenticated:
        return HttpResponse("Unauthorized", status=401)
    if not request.user.is_superuser:
        return redirect('adminlog:admin_login')
    try:
        category=Category.objects.get(id=category_id)
    except ValueError:
        return redirect('product_details:category')
    category.delete()

    return redirect('product_details:category')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def edit_category(request,category_id):
    if not request.user.is_authenticated:
        return HttpResponse("Unauthorized", status=401)
    if not request.user.is_superuser:
        return redirect('adminlog:admin_login')
    
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

    return render(request,'admin_side/edit_category.html',content)
# ------------------------------------------end categary-----------------------------------------------------------



# ----------------------------------------------Brand-----------------------------------------------------------------



def brand(request):
    if not request.user.is_superuser:
        return redirect('adminlog:admin_login')
    brands = Brand.objects.all()
    content = {
        'brands': brands
    }
    return render(request, 'admin_side/add_brand.html',content)

def add_brand(request):
    if request.method == "POST":
         brand_name = request.POST['brand_name']
    validate=validate_no_spaces(brand_name)
    
    if validate:
        Brand.objects.create(
        brand_name=brand_name,
        )
    else:
        messages.error(request,"Provide Brand name name without space")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    
    return redirect('product_details:brand')
    

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def brand_available(request,brand_id):
    if not request.user.is_authenticated:
        return HttpResponse("Unauthorized", status=401)
    if not request.user.is_superuser:
        return redirect('adminlog:admin_login')
    
    brand = get_object_or_404(Brand, id=brand_id)
    
    if brand.is_active:
        brand.is_active=False
       
    else:
        brand.is_active=True
    brand.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def delete_brand(request,brand_id):
    if not request.user.is_authenticated:
        return HttpResponse("Unauthorized", status=401)
    if not request.user.is_superuser:
        return redirect('adminlog:admin_login')
    try:
        brand=Brand.objects.get(id=brand_id)
    except ValueError:
        return redirect('product_details:brand')
    brand.delete()

    return redirect('product_details:brand')
# -------------------------------------------------------end brand---------------------------------------------------




# -------------------------------------------------------Attribute------------------------------------------------------

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def attribute(request):
    if not request.user.is_superuser:
        return redirect('adminlog:admin_login')
    attributes = Atribute.objects.all()
    content = {
        'attributes': attributes
    }
    return render(request, 'admin_side/add_attribute.html',content)



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def add_attribute(request):
    if not request.user.is_superuser:
        return redirect('adminlog:admin_login')
    if request.method == "POST":
        attribute_name = request.POST['attribute_name']

    validate=validate_no_spaces(attribute_name)
    
    if validate:
        Atribute.objects.create(
        atribute_name=attribute_name,
        )
    else:
        messages.error(request,"Provide Attribute  name without space")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    
    return redirect('product_details:attribute')



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def attribute_available(request,attribute_id):
    if not request.user.is_authenticated:
        return HttpResponse("Unauthorized", status=401)
    if not request.user.is_superuser:
        return redirect('adminlog:admin_login')
    attribute = Atribute.objects.get(id=attribute_id)
    
    if attribute.is_active:
        attribute.is_active=False
       
    else:
        attribute.is_active=True
    attribute.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def delete_attribute(request,attribute_id):
    if not request.user.is_authenticated:
        return HttpResponse("Unauthorized", status=401)
    if not request.user.is_superuser:
        return redirect('adminlog:admin_login')
    try:
        attribute=Atribute.objects.get(id=attribute_id)
    except ValueError:
        return redirect('product_details:attribute')
    attribute.delete()

    return redirect('product_details:attribute')
# ---------------------------------------------------------end attribute---------------------------------------------------



# ----------------------------------------------------------Attribute value-------------------------------------------------
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def attribute_value(request):
    if not request.user.is_superuser:
        return redirect('adminlog:admin_login')
    attribute_values = Atribute_Value.objects.all()
    attribute_names=Atribute.objects.all()
    content = {
        'attribute_values': attribute_values,
        'attribute_names': attribute_names
    }
    return render(request, 'admin_side/add_attribute_value.html',content)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def add_attribute_value(request):
    if not request.user.is_superuser:
        return redirect('adminlog:admin_login')
    if request.method == 'POST':
        attribute_value_n = request.POST.get('attribute_value_name')

    validate=validate_no_spaces(attribute_value_n)

    if validate:
        attribute = request.POST.get('attribute')
        if attribute_value_n and attribute:
            attribute_id = Atribute.objects.get(atribute_name=attribute)
            Atribute_Value.objects.create(
                atribute_value=attribute_value_n,
                atribute_id=attribute_id.id
            )
    else:
        messages.error(request,"Provide Attribute  name without space")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    
    attribute_values = Atribute_Value.objects.all()
    attribute_names = Atribute.objects.all()
    context = {
        'attribute_values': attribute_values,
        'attribute_names': attribute_names
    }
    
    return render(request, 'admin_side/add_attribute_value.html', context)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def attribute_value_available(request,attribute_value_id):
    if not request.user.is_authenticated:
        return HttpResponse("Unauthorized", status=401)
    if not request.user.is_superuser:
        return redirect('adminlog:admin_login')
   
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
    if not request.user.is_superuser:
        return redirect('adminlog:admin_login')
    try:
        attribute_value=Atribute_Value.objects.get(id=attribute_value_id)
    except ValueError:
        return redirect('product_details:attribute_value')
    attribute_value.delete()

    return redirect('product_details:attribute_value')



# --------------------------------------------end attribute value-------------------------------------------------
       
    




#--------------------------------------------------add product with verient---------------------------------------



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def add_product(request):
    if not request.user.is_authenticated:
        return HttpResponse("Unauthorized", status=401)
    if not request.user.is_superuser:
        return redirect('adminlog:admin_login')
    categories = Category.objects.all()
    brands = Brand.objects.all().exclude(is_active=False)
    

    if request.method == 'POST':
        product_name= request.POST.get('product_name')
        product_sk_id= request.POST.get('sku_id')
        description= request.POST.get('product_desc')
        max_price= request.POST.get('product_max_price')
        sale_price= request.POST.get('product_sale_price')
        category_name= request.POST.get('product_category')
        brand_name=request.POST.get('product_brand')

        validate=validate_no_spaces(product_name)
        if validate:
           validate_max_price=validate_numeric(max_price)
           if validate_max_price:
                validate_sale_price=validate_numeric(sale_price)
                if  validate_sale_price:
                    if sale_price > max_price:
                        messages.error(request,"sale price is greater than max price pleas provide correct value")
                        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
                    else:
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
                            image=request.FILES['image_feild']  
                        )
                        product.save()

                        return redirect('product_details:product_list')
                else:
                    messages.error(request,"provide correct value contain only number")
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
           else:
                messages.error(request,"provide correct value contain only number")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/')) 
        
        else:
            messages.error(request,"Provide Product name without space")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    else:
        form=CreateProductForm()
    content = {
        'categories': categories,
        'brands': brands,   
        'form': form
    }
    return render(request,'admin_side/add_product.html', content)

    



#---------------------------------------------------------end product verient------------------------------------



#-------------------------------------------------------product list----------------------------------------------
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def product_list(request):
    if not request.user.is_superuser:
        return redirect('adminlog:admin_login')
    products=Product.objects.all()
    context={
       "products":products,
   }
    return render(request, 'admin_side/product_list.html',context)




# def product_det(request, product_id):

#     product=get_object_or_404(Product,id=product_id)
#     context={
#         'product':product
#     }

#     return render(request,'admin/product_details.html',context)


from django.shortcuts import render, redirect


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def update_product(request, product_id):
    if not request.user.is_superuser:
        return redirect('adminlog:admin_login')
   
    if not request.user.is_authenticated:
        return redirect('adminlog:admin_login')

    try:
        product = Product.objects.get(id=product_id)
        product_variants=Product_Variant.objects.filter(product=product)
    except Product.DoesNotExist:
        return HttpResponse("Product not found", status=404)

    for product_variant in product_variants:
        if product_variant.stock == 0:
            product_variant.is_active = False
            product_variant.save()
        else:
            product_variant.is_active =True
            product_variant.save()
    try:
        for products in product_variants:
            if products.stock == 0:
                products.is_active = False
            else:
                product.is_active = True
    except:
        pass

    if request.method == 'POST':
        form = CreateProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_details:product_list')
        else:
            print(form.errors)
            context = {
                'form': form,
                'product': product,
                'product_variants': product_variants,
            }
            return render(request, 'admin_side/product_details.html', context)

    else:
        form = CreateProductForm(instance=product)
        # print(form)
    context = {
        'form': form,
        'product': product,
        'product_variants': product_variants,
    }
    return render(request, 'admin_side/product_details.html', context)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def delete_product(request,product_id):
    if not request.user.is_authenticated:
        return redirect('adminlog:admin_login')
    if not request.user.is_superuser:
        return redirect('adminlog:admin_login')
    try:
        product = Product.objects.get(id=product_id)
        product.delete()
        return redirect('product_details:product_list')
    except Product.DoesNotExist:
        return HttpResponse("Product not found", status=404)
    
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def add_veriants(request,product_id):
    if not request.user.is_authenticated:
        return redirect('adminlog:admin_login')
    if not request.user.is_superuser:
        return redirect('adminlog:admin_login')
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return HttpResponse("Product not found", status=404)
    attributes = Atribute.objects.prefetch_related('atribute_value_set').filter(is_active=True)

    attribute_dict = {}
    for attribute in attributes:
        attribute_values = attribute.atribute_value_set.filter(is_active=True)
        attribute_dict[attribute.atribute_name] = attribute_values
    #to show how many atribute in fronend
    attribute_values_count = attributes.count() 

    if request.method=='POST':
        stock=request.POST.get('stock')
        attribute_ids=[]
        for i in range(1,attribute_values_count+1):
            req_atri = request.POST.get('atributes_'+str(i))
            if req_atri != 'None':
                attribute_ids.append(int(req_atri))
    
        verient=Product_Variant(
            product=product,
            stock=stock,
            thumbnail_image=request.FILES['thumbnail']
        )    
        verient.save()
        verient.atributes.set(attribute_ids)
        

    context ={
        "product":product,
        'attribute_dict':attribute_dict
    }
    return render(request, 'admin_side/add_verients.html',context)
    

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def edit_varient(request,product_variant_id):
    print(product_variant_id)
    if not request.user.is_authenticated:
        return redirect('adminlog:admin_login')
    if not request.user.is_superuser:
        return redirect('adminlog:admin_login')
   
    
    product_variant=get_object_or_404(Product_Variant, id=product_variant_id)
    atribute_values = product_variant.atributes.all()

    for atribute_value in atribute_values:
        print(atribute_value.atribute_value)

    attributes = Atribute.objects.prefetch_related('atribute_value_set').filter(is_active=True)

    attribute_dict = {}
    for attribute in attributes:
        attribute_values = attribute.atribute_value_set.filter(is_active=True)
        attribute_dict[attribute.atribute_name] = attribute_values
    #to show how many atribute in fronend
    attribute_values_count = attributes.count() 
    
    context={
        'product_variant':product_variant,
        'attribute_dict': attribute_dict
    }
    if request.method=='POST':
        stock=request.POST.get('stock')
        attribute_ids=[]
        for i in range(1, attribute_values_count + 1):
            req_atri = request.POST.get('atributes_' + str(i))
            if req_atri is not None and req_atri != 'None':
                attribute_ids.append(int(req_atri))
        product_variant.stock=stock
        product_variant.save()
        product_variant.atributes.set(attribute_ids)

        # return redirect('product_details:update_product')
        return redirect('product_details:update_product', product_id=product_variant.product.id)


    return render(request,'admin_side/edit_variant.html',context)



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def delete_variant(request,product_variant_id):
    if not request.user.is_authenticated:
        return redirect('adminlog:admin_login')
    if not request.user.is_superuser:
        return redirect('adminlog:admin_login')
    try:
        product_variant = Product_Variant.objects.get(id=product_variant_id)
        product_variant.delete()
        return redirect('product_details:update_product', product_id=product_variant.product.id)
    except Product.DoesNotExist:
        return HttpResponse("Product not found", status=404)
    



# validation

def validate_no_spaces(value):
   
    if value.strip() != value:
        
        return False
    return True

def validate_numeric(value):
    if value.isdigit():
        return True
    return False