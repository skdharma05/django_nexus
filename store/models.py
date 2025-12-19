from django.db import models
# 'Many To Many' RelationShip

class Promotion(models.Model):
    description = models.CharField(max_length=255)
    discount = models.FloatField()

# 'One To One'  and 'One To Many' RelationShip
class Collection(models.Model):
    title = models.CharField(max_length=255)
    featured_product = models.ForeignKey('Product',on_delete=models.SET_NULL, null=True,related_name='+')

class Product(models.Model): #  database
    title = models.CharField(max_length=255) # this will create a table called Product and colum called title = varchar(255)
    slug = models.SlugField()
    description = models.TextField() # why we choose Textfield insted of charfield because textField doesnt need max length.
    #9999.99
    unit_price = models.DecimalField(max_digits=6,decimal_places=2)
    inventory = models.IntegerField()
    last_update = models.DateField(auto_now=True)
    collection = models.ForeignKey(Collection,on_delete=models.PROTECT) # One To Many RelationShip
    promotions = models.ManyToManyField(Promotion) # Many To Many RelationShip


class Customer(models.Model):
    MEMBERSHIP_BRONZE ='B'
    MEMBERSHIP_SILVER ='S'
    MEMBERSHIP_GOLD ='G'
    
    MEMBERSHIP_CHOICES=[
        (MEMBERSHIP_BRONZE,'Bronze'),
        (MEMBERSHIP_SILVER,'Silver'),
        (MEMBERSHIP_GOLD,'Gold')
    ]

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email =models.EmailField(unique=True)
    phone = models.CharField(max_length=20,blank=True,null=True)
    birth_date =models.DateField(blank=True,null=True)
    membership = models.CharField(max_length=1,choices=MEMBERSHIP_CHOICES , default=MEMBERSHIP_BRONZE)


        
class Order(models.Model):

    STATUS_PENDING ='P'
    STATUS_COMPLETE ='C'
    STATUS_FAILED ='F'

    PAYMENT_STATUS = [
        (STATUS_PENDING,'Pending'),
        (STATUS_COMPLETE,'Completed'),
        (STATUS_FAILED,'Failed'),
    ]
    placed_at= models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=1,choices=PAYMENT_STATUS,default=STATUS_PENDING)
    customer = models.ForeignKey(Customer,on_delete=models.PROTECT) # One To Many RelationShip


class Address(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE) # One To Many RelationShip
    zip = models.CharField(max_length=15)


class OrderItem(models.Model):
    order = models.ForeignKey(Order,on_delete=models.PROTECT) # One To Many RelationShip
    product = models.ForeignKey(Product,on_delete=models.PROTECT) # One To Many RelationShip
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=6,decimal_places=2)

class Cart(models.Model):
    created_at = models.DateTimeField(auto_now_add=True) 

class CartItem(models.Model):
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE) # One To Many RelationShip
    product = models.ForeignKey(Product,on_delete=models.CASCADE) # One To Many RelationShip
    quantity = models.PositiveIntegerField()