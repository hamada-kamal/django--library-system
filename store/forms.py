from django import forms
from .models import *



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
        

class IncomingLineForm(forms.ModelForm):
    class Meta:
        model = IncomingOrderLine
        fields = ('product','qty',)

class PaidForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('paid',)
        
        
class IncomInfoForm(forms.ModelForm):
    class Meta:
        model = IncomingOrder
        fields = ('seller','total','remaining_money','total2','paid','still')