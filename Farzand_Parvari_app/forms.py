from django import forms

class loginForm(forms.Form):
    username = forms.CharField(label='نام کاربری ',max_length=100 , error_messages={'خطا' :'نام کاربری را صحیح وارد نمایید'} , )
    password   = forms.CharField(widget=forms.PasswordInput , label='رمز عبور' )
