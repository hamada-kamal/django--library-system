from django.db import models
from django.utils.text import slugify
from django.urls import reverse

from django.core.validators import MaxValueValidator, MinValueValidator



class Product(models.Model):
    name = models.CharField(max_length=56, verbose_name="اسم المنتج",unique=True)
    price = models.DecimalField(max_digits=7  , decimal_places=2 , verbose_name="السعر")
    wholesale_price = models.DecimalField(max_digits=7  , decimal_places=2 , verbose_name="سعر الجملة")
    available_in_ventory = models.PositiveIntegerField(verbose_name='متوفر')
    discription = models.TextField(max_length=200, blank=True, null=True, verbose_name="الوصف")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الانشاء")
    code = models.CharField(max_length=100, null=True)
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




    

class Client(models.Model):
    phone = models.CharField(max_length=11, unique=True, verbose_name="رقم الهاتف")
    name = models.CharField(max_length=50, unique=True, verbose_name="اسم العميل")
    remaining_money = models.DecimalField(max_digits=7  , decimal_places=2 , default=0, verbose_name="مبلغ متبقى")

    
    def  __str__ (self):
        return self.name
    
class Order(models.Model):
    client = models.ForeignKey(Client,on_delete=models.CASCADE, verbose_name="العميل")
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True)
    remaining_atthattime = models.DecimalField(max_digits=7  , decimal_places=2 , verbose_name="المبلغ المتبقى وقتها")

    paid = models.FloatField(validators=[MinValueValidator(0)],verbose_name="تم دفع")
    ORDslug = models.SlugField(blank=True, null=True, unique=True, allow_unicode=True, max_length=255 , verbose_name="slug")


    class Meta:
        ordering = ["client__name"]

    def save(self , *args  ,**kwargs ):
        self.ORDslug = slugify(self.transaction_id,allow_unicode=True)
        super(Order , self).save( *args , **kwargs)



    @property
    def get_bill_count(self):
        orderitems = self.orderline_set.all()
        count = orderitems.count()
        return count 
    
    @property
    def get_bill_total(self):
        orderitems = self.orderline_set.all()
        total = sum([item.get_total for item in orderitems])
        return total 
    

    def __str__(self):
        return str(self.transaction_id)
 
    
class QuiqOrder(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True)
    paid = models.FloatField(validators=[MinValueValidator(0)],verbose_name="تم دفع")
    ORDslug = models.SlugField(blank=True, null=True, unique=True, allow_unicode=True, max_length=255 , verbose_name="slug")


    def save(self , *args  ,**kwargs ):
        self.ORDslug = slugify(self.transaction_id,allow_unicode=True)
        super(QuiqOrder , self).save( *args , **kwargs)


    @property
    def get_bill_count(self):
        orderitems = self.quiqorderline_set.all()
        count = orderitems.count()
        return count 
    
    @property
    def get_bill_total(self):
        orderitems = self.quiqorderline_set.all()
        total = sum([item.get_total for item in orderitems])
        return total 


    def __str__(self):
        return str(self.transaction_id)
 

    

class OrderLine(models.Model):
    product = models.ForeignKey(Product,null=False, blank=False,on_delete=models.CASCADE, verbose_name="المنتج")
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    qty = models.PositiveIntegerField(default=1, null=False, blank=False, verbose_name="الكميه")
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["product"]
        
    @property
    def get_total(self):
        total = self.product.price * self.qty
        return total
    
    
    def __str__(self):
	    return str(self.product)           
    

class QuiqOrderLine(models.Model):
    product = models.ForeignKey(Product,null=False, blank=False,on_delete=models.CASCADE, verbose_name="المنتج")
    quiqorder = models.ForeignKey(QuiqOrder,on_delete=models.CASCADE)
    qty = models.PositiveIntegerField(default=1, null=False, blank=False, verbose_name="الكميه")
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["product"]
        
    @property
    def get_total(self):
        total = self.product.price * self.qty
        return total
    
    def __str__(self):
	    return str(self.product)           

    
    
 
 
class IncomingOrder(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    transaction_id = models.CharField(max_length=100, null=True)
    seller = models.CharField(max_length=100, null=True,verbose_name="التاجر")
    total = models.FloatField(validators=[MinValueValidator(0)],verbose_name="سعر الفاتوره", default=0)
    remaining_money = models.FloatField(validators=[MinValueValidator(0)],verbose_name="رصيد ما قبله", default=0)
    total2 = models.FloatField(validators=[MinValueValidator(0)],verbose_name="الاجمالى", default=0)
    paid = models.FloatField(validators=[MinValueValidator(0)],verbose_name="تم دفع", default=0)
    still = models.FloatField(validators=[MinValueValidator(0)],verbose_name="مازال", default=0)
    empty_done = models.BooleanField(default=False)
    ORDslug = models.SlugField(blank=True, null=True, unique=True, allow_unicode=True, max_length=255 , verbose_name="slug")


    def save(self , *args  ,**kwargs ):
        self.ORDslug = slugify(self.transaction_id,allow_unicode=True)
        super(IncomingOrder , self).save( *args , **kwargs)


    @property
    def get_bill_count(self):
        orderitems = self.incomingorderline_set.all()
        count = orderitems.count()
        return count 


    def __str__(self):
        return str(self.transaction_id)
    
    
class IncomingOrderLine(models.Model):
    product = models.ForeignKey(Product,null=False, blank=False,on_delete=models.CASCADE, verbose_name="المنتج")
    incomingorder = models.ForeignKey(IncomingOrder,on_delete=models.CASCADE)
    qty = models.PositiveIntegerField(default=1, null=False, blank=False, verbose_name="الكميه")
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["product"]
        
    @property
    def get_total(self):
        total = self.product.price * self.qty
        return total
    
    
    def __str__(self):
	    return str(self.product)           
    
    