from django.contrib import admin ,messages
from . import models
from django.db.models import Count
from django.utils.html import format_html , urlencode
from django.urls import reverse
from django.db.models import QuerySet
# from django.contrib.contenttypes.admin import GenericTabularInline
# from tags.models import TaggedItem

# Register your models here.
# admin.site.register(models.Collection)
# admin.site.register(models.Product)


# Custom Filter:(Adding Filtering to the List Page)
class InventoryFilter(admin.SimpleListFilter):
    title = 'inventory'
    parameter_name = 'inventory'

    def lookups(self, request, model_admin):
        return [
            ('<10','Low')
        ]
    def queryset(self, request, queryset: QuerySet):
        if self.value()=='<10':
           return queryset.filter(inventory__lt = 10)
        
# class TagInline(GenericTabularInline):
#     model = TaggedItem
#     autocomplete_fields =['tag']



@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin): # to Know more use Django ModelAdmin (docs).
    
    # inlines = [TagInline]

    actions=['clear_inventory']
    list_display = ['title','unit_price','inventory_status','collection_title']
    ordering = ['title']
    list_editable=['unit_price']
    list_filter=['collection','last_update','title',InventoryFilter]
    list_per_page = 10
    list_select_related=['collection']
    
    # Adding Data Validation
    autocomplete_fields =['collection']
    search_fields =['title']
    exclude=['promotions']
    prepopulated_fields = {
        'slug' : ['title']
    }

    def collection_title(self,product):
        return product.collection.title

    @admin.display(ordering='inventory')
    def inventory_status(self,product):
        if product.inventory<10:
            return 'LOW'
        return "OK"
   
    # Creating Custom Actions:
    @admin.action(description='Clear inventory')
    def clear_inventory(self,request,queryset:QuerySet):
        update_count = queryset.update(inventory=0)
        self.message_user(
            request,
            f'{update_count} products were successfully updated.',messages.ERROR
        ) 



@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display=['first_name','last_name','membership','orders']
    list_editable = ['membership']
    list_per_page = 10
    ordering = ['first_name','last_name']

    # Search field to search specific data.
    search_fields=['first_name__istartswith','last_name__istartswith']

    @admin.display(ordering='orders')
    def orders(self, customer):
        url = (
            reverse('admin:store_order_changelist')
            + '?'
            + urlencode({
                'customer__id': str(customer.id)
            })
        )
        return format_html('<a href="{}">{}</a>', url, customer.orders)


    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            orders = Count('order')
        )

@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title','product_count']
    ordering = ['title']
    search_fields=['title']

    # Providing link to other page:  
    @admin.display(ordering='product_count')
    def product_count(self,collection):
        url = (reverse('admin:store_product_changelist')
               +'?'
               +urlencode({
                   'collection__id' : str(collection.id)
               })
             )
        return format_html('<a href="{}">{}</a>',url ,collection.product_count)
         
    
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            product_count=Count('products')
        )

# Editing Children Using Inlines:
class OrderItemInline(admin.StackedInline):
    autocomplete_fields =['product']
    model = models.OrderItem
    min_num =1
    max_num = 10
    extra =0


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    autocomplete_fields =['customer']
    inlines = [OrderItemInline]
    list_display = ['id','customer','placed_at']

    
