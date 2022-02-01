from django import forms
from .models import *
from django.forms.models import inlineformset_factory



class AddProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'price', 'wholesale_price', 'available_in_ventory','discription')


        
class BillUserForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ('name','phone','remaining_money')
        

class LineForm(forms.ModelForm):
    class Meta:
        model = OrderLine
        fields = ('product','qty',)
        

class QuiqLineForm(forms.ModelForm):
    class Meta:
        model = QuiqOrderLine
        fields = ('product','qty',)

class PaidForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('paid',)