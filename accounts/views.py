from django.shortcuts import render, redirect
from .forms import Userform
from .models import User, UserProfile
from django.contrib import messages, auth
from vendor.forms import VendorForm
from .utils import detectUser
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
# Create your views here.

#restrict accessing the customer pase
def check_role_vendor(user):
    if user.roll == 1:
        return True
    else:
        raise PermissionDenied
#restrict accessing the vendor page
def check_role_customer(user):
    if user.roll == 2:
        return True
    else:
        raise PermissionDenied
    
    
def registerUser(request):
    if request.method == 'POST':
        form = Userform(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            user = form.save(commit=False)
            user.set_password(password)
            user.roll = User.CUSTOMER
            user.save()
            messages.success(request, 'Your account has been register successfully')
            return redirect('registerUser')
        else:
            print(form.errors)
    else:
        form = Userform()
    context = {
        'form':form
    }
    
    
    return render(request, 'accounts/registerUser.html', context)



def registerVendor(request):
    if request.method=='POST':
        form = Userform(request.POST)
        v_form = VendorForm(request.POST, request.FILES)
        
        
        if form.is_valid() and v_form.is_valid():
            password = form.cleaned_data['password']
            user = form.save(commit=False)
            user.set_password(password)
            user.roll = User.VENDOR
            user.save()
            
            vendor = v_form.save(commit=False)
            vendor.user = user
            user_profile = UserProfile.objects.get(user = user)
            vendor.user_profile = user_profile
            vendor.save()
            
            messages.success(request, 'Your Resturent has been register successfully')
            return redirect('registerVendor')
        else:
            
            print(form.errors)
    else:
        form = Userform()
        v_form = VendorForm()
   
   
    
    context = {
        'form': form,
        'v_form':  v_form
    }
    return render (request, 'accounts/registerVendor.html', context)


def login(request):
    
    if request.user.is_authenticated:
        messages.warning(request, 'you are already logged in')
        return redirect('myAccount')
    
    elif request.method=='POST':
        email =request.POST['email']
        password =request.POST['password']
        
        user = auth.authenticate(email=email, password=password)
        
        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You are logged in.')
            return redirect('myAccount')
        
        else:
            messages.error(request, 'Invalid login!')
            return redirect('login')
    
    return render(request, 'accounts/login.html')

def logout(request):
    auth.logout(request)
    messages.info(request, 'you are logged out')
    return redirect('login')


@login_required(login_url = 'login')
def myAccount(request):
    user = request.user
    redirectUrl = detectUser(user)
    return redirect(redirectUrl)

@login_required(login_url = 'login')
@user_passes_test(check_role_customer)
def custDashboard(request):
    return render(request, 'accounts/custDashboard.html')

@login_required(login_url = 'login')
@user_passes_test(check_role_vendor)
def vendorDashboard(request):
    return render(request, 'accounts/vendorDashboard.html')