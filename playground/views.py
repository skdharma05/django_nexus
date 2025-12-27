from django.shortcuts import render
from store.models import Product ,OrderItem ,Customer,Order ,Collection
from django.db.models import Q # 'Q' is a query expression object in Django.It lets you construct complex database queries using logical operators like: OR, AND, NOT.
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import F # An F object lets the database compare fields to fields, or update a field based on its current value, without pulling data into Python.
from django.db.models import Prefetch
from django.db.models.aggregates import Min,Max,Avg,Count,Sum
from django.db.models import Value , Func ,ExpressionWrapper , DecimalField
from django.db.models.functions import Concat
from django.db import models
from django.contrib.contenttypes.models import ContentType
from tags.models import TaggedItem



# Create your views here.
def say_hello(request):

    # Filtering:
    """
    exists = Product.objects.filter(pk=0).exists() #if product doesnt exists it return None thats why we use exists()
    queryset = Product.objects.filter(unit_price__range=(20, 30)) #we dont use < or >= like sign in inside this django methodes so we use '__' double underscore continue to ls = lessthan gt = graterthan gte = graterthanequal etc...
    queryset = Product.objects.filter(title__icontains ='coffee') # contains is case sentitive so we use i before contains. we also have startwith and endwith implementation.
    queryset = Product.objects.filter(last_update__year =2021)
    queryset = Product.objects.filter(description__isnull = True)

    """
        
    # complex Lookups using Q objects.(Multiple filter):
    """
    # we want to Products: inventory <10 AND price <20
    queryset = Product.objects.filter(inventory__lt=10 , unit_price__lt=20)
    # Another way to multiplle filter :
    queryset = Product.objects.filter(inventory__lt=10).filter(unit_price__lt=20)

    """

    # Q object:
    """
    # we want to Products: inventory <10 OR price <20
    queryset = Product.objects.filter(Q(inventory__lt=10) | Q(unit_price__lt=20))  # Uing OR ("|")
    queryset = Product.objects.filter(Q(inventory__lt=10) & Q(unit_price__lt=20))  # Uing AND ("&")
    queryset = Product.objects.filter(Q(inventory__lt=10) & ~Q(unit_price__lt=20))  # Uing NOT ("~")

    """
    # F Object:
    """
    queryset = Product.objects.filter(inventory=F('unit_price'))  # Compare 2 tables  ("F")
    queryset = Product.objects.filter(unit_price=F('unit_price') * 1.10)  # Increase unit_price by 10% using F object

    """

    # Sorting:
    """
    # queryset = Product.objects.order_by('-title') # Desc order ('-')
    queryset = Product.objects.order_by('unit_price','-title')
    queryset = Product.objects.earliest('unit_price') # it give only one value  its minmun value
    queryset = Product.objects.latest('unit_price') # tjis give only one value its maximum.
    
    """

    # Limiting Result (using to how many we product in our first page and next , etc.. )
    """
    queryset = Product.objects.all()[:5]# this will show first 5 obj in the array using slice method 
    queryset = Product.objects.all()[5:10]# this will show  6 to 10  obj in the array using slice method 
    
    """
    # Selecting Field to Query:Only selected columns are fetched from the database. Eg "SELECT id, title FROM product;"
    """
    # queryset = Product.objects.values('id','title') # SELECT id, title FROM product; this what this line doing.
    # queryset = Product.objects.values('id','title','collection__title')  # Selects titles from related Collection table using a JOIN

    """
    

    # What this does:
    # 1. Gets all product_id values from the OrderItem table
    # 2.Filters Product objects whose id is in that list
    # 3.Orders the result by title

    # Conceptual SQL:
    # SELECT *
    # FROM product
    # WHERE id IN (
    #     SELECT product_id FROM order_item
    # )
    # ORDER BY title;

    """
    queryset = Product.objects.filter(id__in = OrderItem.objects.values('product_id')).order_by('title')

    """

    # Defering Fields:
    """
    queryset = Product.objects.only('id','title') # Loads only the specified fields initially. Other fields are deferred.
    queryset = Product.objects.defer('description') # Loads all fields except the ones you specify.Deferred fields are fetched only if accessed later.
    
    """

    # Selecting Related Object.
    """
    queryset = Product.objects.select_related('collection').all()
    queryset = Product.objects.prefetch_related('promotions').all()
    queryset = Product.objects.prefetch_related('promotions').select_related('collection').all()
    queryset = Product.objects.select_related('customer').prefetch_related[5:]
    
    """ 
    """
    queryset = Order.objects.select_related('customer').prefetch_related('orderitem_set__product').order_by('-placed_at')[:5]
                    # OR
    queryset = Order.objects.select_related('customer').prefetch_related(Prefetch('orderitem_set', queryset = OrderItem.objects.select_related('product'))).order_by('-placed_at')[:5]

    return render(request,'hello.html',{'name':'Dharma','orders':list(queryset)})

    """
    # Aggregating Objects:
    """
    result = Product.objects.aggregate(count = Count('id'),min_price=Min('unit_price'))

    return render(request,'hello.html',{'name':'Dharma','result':result})

    """

    # Annotating Objects:
        # What is annotate() in Django ORM?
        #     annotate() is used to add extra calculated fields to each object in a QuerySet.
        #     Think of it like adding a new column in SQL that is computed using aggregation or expressions.
    """
    result = Product.objects.annotate(is_new=Value(True))
    result = Product.objects.annotate(new_id=F("id"))

    return render(request,'hello.html',{'name':'Dharma','result':list(result)})

    """

    # Calling Database Function:
    """
    result = Customer.objects.annotate(
        #CONCAT
        full_name =Func(F('first_name'),Value(' '),F('last_name'),function='CONCAT')
    )
                # OR (Short Method with Same Result.)
                
    result = Customer.objects.annotate(full_name =Concat('first_name',Value(' '),'last_name'))
    
    return render(request,'hello.html',{'name':'Dharma','result':list(result)})

    """

    # Grouping Data:
    """
    result = Customer.objects.annotate(order_count = Count('order'))
    
    return render(request,'hello.html',{'name':'Dharma','result':list(result)})

    """

    # Working with Expression Wrappers :

        # ExpressionWrapper is used when Django needs help determining the output type of an expression.

        # It wraps expressions like:

        # Multiplication of fields
        # Arithmetic
        # Functions
        # Mixed types (F expressions + constants)

        # 📌 Without it, Django may raise:
        # FieldError: Expression contains mixed types

    """

    discount_price = ExpressionWrapper(F('unit_price')*0.8, output_field = DecimalField())

    result = Product.objects.annotate( discounted_price = discount_price)
    
    return render(request,'hello.html',{'name':'Dharma','result':list(result)})

    """

    # Quering Generic Relationship:
    """
    content_type = ContentType.objects.get_for_model(Product)
    result = TaggedItem.objects \
        .select_related('tag') \
        .filter(
            content_type=content_type,
            object_id = 1
        )

    return render(request,'hello.html',{'name':'Dharma','result':list(result)})

    """

    # Custom Manager:

    """
    result =TaggedItem.objects.get_tags_for(Product,1)

    return render(request,'hello.html',{'name':'Dharma','result':list(result)})
    
    """
    # Understanding QuerySet Cache:

    """
    result = Product.objects.all()
    list(result)
    result[0]

    return render(request,'hello.html',{'name':'Dharma','result':list(result)})

    """
    # Creating Objects:
        # To inssert a new data to database.
        
    """    
    collection = Collection()
    collection.title = 'Video Game'
    collection.featured_product =  Product(pk=1)
    collection.save()

    return render(request,'hello.html',{'name':'Dharma'})

    """
    # Updating Objects:

    """

    # collection = Collection(pk = 10) // even we didnt update title django will automatically update like "" empty so   
    # collection.featured_product = None
    # collection.save()

    # collection=Collection.objects.get(pk=11)
    # collection.featured_product=None
    # collection.save() 
        # OR
    Collection.objects.filter(pk = 11).update(featured_product=None)


    return render(request,'hello.html',{'name':'Dharma'})

    """

    # Deleting Objects:

    """
    collection = Collection(pk=11) # delete single object
    collection.delete()

    Collection.objects.filter(id__gt=10).delete() # Delete multiple object.


    return render(request,'hello.html',{'name':'Dharma'})

    """
    # Transactions:
    """
    from django.db import transaction

    with transaction.atomic():
        order = Order()
        order.customer_id = 1
        order.save()

        item = OrderItem()
        item.order=order
        item.product_id = -1
        item.quantity =1
        item.unit_price = 10
        item.save()

    return render(request,'hello.html',{'name':'Dharma'})

    """

    # Executing Raw SQL Queries:

    """
    result = Product.objects.raw('SELECT * FROM store_product')

    from django.db import connection

    cursor = connection.cursor()
    cursor.execute('SELECT * FROM store_product')
    cursor.close()

    with connection.cursor() as cursor: # prefered we dont need to close it it automaticlly done it.
        cursor.execute("  ")

    return render(request,'hello.html',{'name':'Dharma','result':list(result)})

    """

    return render(request,'hello.html',{'name':'Dharma'})












