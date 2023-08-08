from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import CustomSignupForm
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth import authenticate, login
from .models import Customer, SubscriptionDetails
import stripe
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse
from django.utils.timezone import make_aware
from datetime import datetime
from django.contrib.auth.models import User

stripe.api_key = "sk_test_51MiYppSGNFKxiTC6ebqKwWr3gMCqDrkR8SSQ2R7pwf9VucxVtrcCv8fwVVhPZubqrlNolQ757MgislDdCNss7xHo00IaC4fD4E"


def home(request):
    return render(request, 'core/home.html')


@login_required
def settings(request):
    return render(request, 'core/settings.html')


def join(request):
    return render(request, 'core/join.html')

@login_required
def settings(request):
    membership = False
    cancel_at_period_end = False
    if request.method == 'POST':
        subscription = stripe.Subscription.retrieve(request.user.customer.stripe_subscription_id)
        subscription.cancel_at_period_end = True
        request.user.customer.cancel_at_period_end = True
        cancel_at_period_end = True
        subscription.save()
        request.user.customer.save()
    else:
        try:
            if request.user.customer.membership:
                membership = True
            if request.user.customer.cancel_at_period_end:
                cancel_at_period_end = True
        except Customer.DoesNotExist:
            membership = False
    return render(request, 'core/settings.html', {'membership':membership,
    'cancel_at_period_end':cancel_at_period_end})


@login_required
def checkout(request):

    try:
        if request.user.customer.membership:
            return redirect('settings')
    except Customer.DoesNotExist:
        pass

    if request.method == 'POST':
        pass
    else:
        membership = 'monthly'
        final_dollar = 100
        membership_id = 'price_1MiYs3SGNFKxiTC6UpxYaxCq'
        if request.method == 'GET' and 'membership' in request.GET:
            if request.GET['membership'] == 'yearly':
                membership = 'yearly'
                membership_id = 'price_1MiYs3SGNFKxiTC6EKIBL70x'
                final_dollar = 1200

        # Create Strip Checkout
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            customer_email = request.user.email,
            line_items=[{
                'price': membership_id,
                'quantity': 1,
            }],
            mode='subscription',
            allow_promotion_codes=True,
            success_url='http://127.0.0.1:8000/success?session_id={CHECKOUT_SESSION_ID}',
            cancel_url='http://127.0.0.1:8000/cancel',
        )

        return render(request, 'core/checkout.html', {'final_dollar': final_dollar, 'session_id': session.id})

def success(request):
    if request.method == 'GET' and 'session_id' in request.GET:
        session = stripe.checkout.Session.retrieve(request.GET['session_id'],)
        customer = Customer()
        customer.user = request.user
        customer.stripeid = session.customer
        customer.membership = True
        customer.cancel_at_period_end = False
        customer.stripe_subscription_id = session.subscription
        customer.save()
        subscription_details = stripe.Subscription.retrieve(session.subscription)
        # base_plan_product_details = stripe.Product.retrieve(settings.STRIPE_BASE_PLAN_PRODUCT_ID)
        if subscription_details.status == 'active':
            subscription_start_date = subscription_details.current_period_start
            subscription_date = make_aware(datetime.fromtimestamp(subscription_start_date))
            subscription_date_start = subscription_date.strftime("%Y-%m-%d %H:%M")
            subscription_end_date = subscription_details.current_period_end
            subscription_end = make_aware(datetime.fromtimestamp(subscription_end_date))
            subscription_date_end = subscription_end.strftime("%Y-%m-%d %H:%M")
            base_plan_list_details = SubscriptionDetails.objects.create(
                                    user=customer,
                                    product_id=subscription_details.plan['product'],
                                    subscription_status=subscription_details.status,
                                    subscription_amount=subscription_details.plan['amount']/100,
                                    # subscription_name=subscription_details.name,
                                    subscription_period=subscription_details.plan['interval'],
                                    subscription_start_date=subscription_date_start,
                                    subscription_end_date=subscription_date_end    
                                )
            base_plan_list_details .save()
    return render(request, 'core/success.html')


def cancel(request):
    return render(request, 'core/cancel.html')



class SignUp(generic.CreateView):
    form_class = CustomSignupForm
    success_url = reverse_lazy('home')
    template_name = 'registration/signup.html'

    def form_valid(self, form):
        valid = super(SignUp, self).form_valid(form)
        username, password = form.cleaned_data.get('username'), form.cleaned_data.get('password1')
        new_user = authenticate(username=username, password=password)
        login(self.request, new_user)
        return valid
    

@user_passes_test(lambda u: u.is_superuser)
def updateaccounts(request):
    customers = Customer.objects.all()
    for customer in customers:
        subscription = stripe.Subscription.retrieve(customer.stripe_subscription_id)
        if subscription.status != 'active':
            customer.membership = False
        else:
            customer.membership = True
        customer.cancel_at_period_end = subscription.cancel_at_period_end
        customer.save()
    return HttpResponse('completed')