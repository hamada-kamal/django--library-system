from .models import Product
def calc_empty_products(request):
    products = Product.objects.filter(available_in_ventory=0)
    emptyNum = products.count() 
    return {"emptyNum":emptyNum}