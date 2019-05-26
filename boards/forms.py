from django import forms
from django.utils.safestring import mark_safe
# from uploads.core.models import Document

class LoginForm(forms.Form):
	username=forms.CharField()
	password=forms.CharField(widget=forms.PasswordInput)
class RegisterForm(forms.Form):
	cc = (
		('__','-----'),
        ('In', '+91'),
        ('US','+22'),
        )
	username=forms.CharField()
	email=forms.EmailField()
	country_code=forms.ChoiceField(choices=cc)
	mobile_no=forms.IntegerField(min_value=1111111111,max_value=9999999999)
	password=forms.CharField(widget=forms.PasswordInput)
	password1=forms.CharField(label='confirm Password',widget=forms.PasswordInput)
	
	def clean(self):
		data=self.cleaned_data
		password=self.cleaned_data.get('password')
		password1=self.cleaned_data.get('password1')
		if password != password1:
			raise forms.ValidationError("Password doesn't Match")
		return data

class Forgotp(forms.Form):
	mail=forms.EmailField()
	otp=forms.DecimalField(max_digits=4,required=False)
class PasswordUpdate(forms.Form):
	password=forms.CharField(widget=forms.PasswordInput)
	password1=forms.CharField(label='confirm Password',widget=forms.PasswordInput)
	# if password != password1:
	# 	raise forms.ValidationError("Password Mismatch")

class AddProduct(forms.Form):
	productname=forms.CharField()
	productprice=forms.DecimalField(max_digits=2)
	productdescription=forms.CharField(widget=forms.Textarea)
# class DocumentForm(forms.ModelForm):
#     class Meta:
#         model = Document
#         fields = ('description', 'document', )