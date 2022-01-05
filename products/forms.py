from django import forms
from .models import *
from django.forms.models import inlineformset_factory



class AddProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'price', 'wholesale_price', 'available_in_ventory','discription')


        
class CreateOrderForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ('name','phone')
        


# AuthorBooksFormset = inlineformset_factory(Order, OrderItem, fields=('product','quantity',),extra=1)



# htmx


class LineForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ('product','quantity',)