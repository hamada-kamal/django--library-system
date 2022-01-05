from . import  views

from django.urls import path

app_name = 'products'

urlpatterns = [

    path('products/line-form/', views.create_line_form, name="line-form"),
    path('products/line-detail/<pk>/', views.detail_line, name="detail-line"),
    path('products/bill/line/<pk>/delete/', views.delete_line , name="delete-line"),
    path('products/bill/line/<pk>/update/', views.update_line_form , name="update-line"),
    path('products/bill/<pk>/', views.create_line, name="create-line"),
    path('add-new-bill/', views.add_bill, name="add-bill"),
    
]
