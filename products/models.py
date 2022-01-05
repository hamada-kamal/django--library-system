from typing_extensions import Required
from django.db import models
from django.utils.text import slugify
from django.urls import reverse
# Create your models here.




class Product(models.Model):
    name = models.CharField(max_length=56, verbose_name="اسم المنتج",unique=True)
    price = models.DecimalField(max_digits=7  , decimal_places=2 , verbose_name="السعر")
    wholesale_price = models.DecimalField(max_digits=7  , decimal_places=2 , verbose_name="سعر الجملة")
    available_in_ventory = models.PositiveIntegerField(verbose_name='متوفر')
    discription = models.TextField(max_length=200, blank=True, null=True, verbose_name="الوصف")
    count_sold = models.IntegerField(default=0, verbose_name='تم بيع')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الانشاء")
    PROslug = models.SlugField(blank=True, null=True, unique=True, allow_unicode=True, max_length=255 , verbose_name="slug")

    class Meta:
        ordering = ["name"]

    def save(self , *args  ,**kwargs ):
        self.PROslug = slugify(self.name,allow_unicode=True)
        super(Product , self).save( *args , **kwargs)
        
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("products:product_details", kwargs={"slug": self.PROslug})



class Customer(models.Model):
    phone = models.CharField(max_length=11)
    customer = models.CharField(max_length=50)
    
    def  __str__ (self):
        return self.customer


class Client(models.Model):
    phone = models.CharField(max_length=11, verbose_name="رقم الهاتف")
    name = models.CharField(max_length=50, verbose_name="اسم العميل")
    def  __str__ (self):
        return self.name
    
class Order(models.Model):
    client = models.ForeignKey(Client,on_delete=models.CASCADE, verbose_name="العميل")
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True)
    ORDslug = models.SlugField(blank=True, null=True, unique=True, allow_unicode=True, max_length=255 , verbose_name="slug")

    def save(self , *args  ,**kwargs ):
        self.ORDslug = slugify(self.transaction_id,allow_unicode=True)
        super(Order , self).save( *args , **kwargs)

    # @property
    # def shipping(self):
    #     shipping = False
    #     orderitems = self.orderitem_set.all()
    #     for i in orderitems:
    # 	    if i.product.digital == False:
    #          shipping = True
    #     return shipping



    # @property
    # def get_cart_total(self):
    #     orderitems = self.orderitem_set.all()
    #     total = sum([item.get_total for item in orderitems])
    #     return total 

    # @property
    # def get_bill_items(self):
    #     orderitems = self.orderitem_set.all()
    #     total = sum([item.quantity for item in orderitems])
    #     return total 
    def __str__(self):
        return str(self.transaction_id)
 
    def get_absolute_url(self):
        return reverse("products:bill_details", kwargs={"slug": self.ORDslug})
    
    

        
    
    
class OrderItem(models.Model):
    product = models.ForeignKey(Product,null=False, blank=False,on_delete=models.CASCADE, verbose_name="المنتج")
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1, null=False, blank=False, verbose_name="الكميه")
    date_added = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ["product"]
    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total
    
    def __str__(self):
	    return str(self.product)