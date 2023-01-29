from django import forms
from .models import Category, FoodItem
from accounts.validators import allow_only_images_validator
class Category_form(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['category_name', 'description']
        
        
class Food_form(forms.ModelForm):
    image = forms.FileField(widget=forms.FileInput(attrs = {'class':'btn btn-info w-100'}),validators = [allow_only_images_validator])
    
    class Meta:
        model = FoodItem
        fields = ['category', 'food_title', 'description', 'price', 'image', 'is_available']
        