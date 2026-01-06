from rest_framework import serializers
from .models import Product,Collection
from decimal import Decimal


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id','title','products_count']
    products_count = serializers.IntegerField(read_only = True)

# class CollectionSerializer(serializers.Serializer):
#     id = serializers.IntegerField()
#     title = serializers.CharField(max_length = 255)


# Model Serializer: (modenWorld use this )
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields =['id','title','slug','description','unit_price','inventory','price_with_tax','collection']

    # collection = serializers.HyperlinkedRelatedField(
    #     queryset=Collection.objects.all(),
    #     view_name = 'collection-detail'
    # )
    price_with_tax = serializers.SerializerMethodField(method_name='calculate_tax')
    def calculate_tax(self,product : Product):
        return product.unit_price * Decimal(1.1)
    

    # WithOut modelSerializer:(not recommended.)

# class ProductSerializer(serializers.Serializer):
#     id = serializers.IntegerField()
#     title = serializers.CharField(max_length= 255)
#     price = serializers.DecimalField(max_digits=6,decimal_places=2,source='unit_price')
#             # Add a computed field called price_with_tax to the API response, whose value is calculated by a custom method.”
#     price_with_tax = serializers.SerializerMethodField(method_name='calculate_tax')

#     def calculate_tax(self,product : Product):
#         return product.unit_price * Decimal(1.1)
    
#         # Represent the collection relationship using only the primary key (ID) 
#     # collection = serializers.PrimaryKeyRelatedField(
#     #     queryset = Collection.objects.all()
#     # )

#         # “Serialize the related object using its str() method.”
#     # collection = serializers.StringRelatedField()

#         # “Serialize the related Collection object inline using CollectionSerializer.”
#     # collection = CollectionSerializer()

#         # This line defines a relationship field in a DRF serializer that represents a related object using a URL instead of an ID.
#     collection = serializers.HyperlinkedRelatedField(
#         queryset=Collection.objects.all(),
#         view_name = 'collection-detail'
#     )
        
