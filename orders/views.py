from django.shortcuts import render, redirect, HttpResponse
from marketplace.models import Cart
from marketplace.context_processors import get_cart_amounts
from .models import Order, OrderedFood, Payment
import simplejson as json
from .forms import OrderForm
from .utils import generate_order_number
from accounts.utils import send_notification_customer
from django.contrib.auth.decorators import login_required

# Create your views here.
def place_order(request):
    
    cart_items = Cart.objects.filter(user=request.user).order_by('created_at')
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('marketplace')
    
    subtotal = get_cart_amounts(request)['subtotal']
    total_tax = get_cart_amounts(request)['tax']
    grand_total = get_cart_amounts(request)['grand_total']
    total_data = {}
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = Order()
            order.first_name = form.cleaned_data['first_name']
            order.last_name = form.cleaned_data['last_name']
            order.phone = form.cleaned_data['phone']
            order.email = form.cleaned_data['email']
            order.address = form.cleaned_data['address']
            order.country = form.cleaned_data['country']
            order.state = form.cleaned_data['state']
            order.city = form.cleaned_data['city']
            order.pin_code = form.cleaned_data['pin_code']
            order.user = request.user
            order.total = grand_total
            order.total_data = json.dumps(total_data)
            order.total_tax = total_tax
            order.payment_method = request.POST['payment_method']
            
            order.save()# order id/ pk is generated
            order.order_number = generate_order_number(order.id)
            order.save() 
            context = {
                'order':order,
                'cart_items':cart_items,
            }
            return render(request, 'orders/place_order.html', context)
            
            
        else:
            print(form.errors)
    return render(request, 'orders/place_order.html')


def payments(request):
    # check idf the the request is ajax or not
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method == 'POST':
        # store the payment details in the payment model
        order_number = request.POST.get('order_number')
        transaction_id = request.POST.get('transaction_id')
        payment_method = request.POST.get('payment_method')
        status = request.POST.get('status')
        
        order = Order.objects.get(user=request.user, order_number=order_number)
        payment = Payment(
            user = request.user,
            transaction_id = transaction_id,
            payment_method = payment_method,
            amount = order.total,
            status = status
        )
        payment.save()
        
        # update the order model
        order.payment = payment
        order.is_ordered = True
        order.save()
        
        # move the cart items in ordered food model
        
        cart_items = Cart.objects.filter(user=request.user)
        for item in cart_items:
            ordered_food = OrderedFood()
            ordered_food.order = order
            ordered_food.payment = payment
            ordered_food.user = request.user
            ordered_food.fooditem = item.fooditem
            ordered_food.quantity = item.quantity
            ordered_food.price = item.fooditem.price
            ordered_food.amount = item.fooditem.price * item.quantity # total amount
            ordered_food.save()
            
            # send order confirmation to the customer
        mail_subject = 'Thank you for ordering us.'
        mail_template = 'orders/order_confirmation_email.html'
        context = {
            'user': request.user,
            'order': order,
            'to_email': order.email,
        }
        send_notification_customer(mail_subject, mail_template, context)
        return HttpResponse('send email')
  
    return HttpResponse('payments view')