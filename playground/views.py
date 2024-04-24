from django.shortcuts import render
from django.db import transaction
from django.contrib.contenttypes.models import ContentType
from store.models import Product,Collection,Order,OrderItem
from tags.models import TaggedItem


def say_hello(request):
    # #custom manager
    # query_set = TaggedItem.objects.get_tags_for(Product, 500)
    
    # #creating objects
    # collection = Collection()
    # collection.title = 'Games'
    # collection.featured_product = None
    # collection.save()
    
    ## update 
    # Collection.objects.filter(pk=6).update(featured_product=None)


    ## deleting objects
    # collection = Collection(pk=7)
    # collection.delete()

    ## using transaction
    # with transaction.atomic():
    #     order = Order()
    #     order.customer_id = 1
    #     order.save()

    #     item = OrderItem()
    #     item.order = order
    #     item.product_id = -1
    #     item.quantity = 1
    #     item.unit_price = 10
    #     item.save()



    return render(request, 'hello.html', { 'name': 'peter'})