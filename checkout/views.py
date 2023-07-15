import json
import stripe
from django.core.mail import send_mail
from django.conf import settings
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from django.views import View
from checkout.models import Product


stripe.api_key = settings.STRIPE_SECRET_KEY


class SuccessView(TemplateView):
    template_name = "success.html"


class CancelView(TemplateView):
    template_name = "cancel.html"


class ProductLandingPageView(TemplateView):
    '''
    This Django view renders the landing page for a given product ID.
    It passes the product object and the Stripe publishable key to the template.
    '''
    template_name = "landing.html"

    def get_context_data(self, **kwargs):
        '''
        This method gets the product object and the Stripe publishable key.
        '''
        product = Product.objects.get(name="DPA")
        context = super(ProductLandingPageView, self).get_context_data(**kwargs)
        context.update({
            "product": product,
            "stripe_publishable_key": settings.STRIPE_PUBLIC_KEY
        })
        print("context=", context)
        return context



class CreateCheckoutSessionView(View):
    '''
    This Django view creates a Stripe Checkout session for a given product ID.
    It sets the session mode to 'payment' and specifies success and cancel URLs.
    It returns the ID of the created session.
    '''
    def post(self, request, *args, **kwargs):
        product_id = self.kwargs["pk"]
        product = Product.objects.get(id=product_id)
        YOUR_DOMAIN = "http://127.0.0.1:8000"
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'usd',
                        'unit_amount': product.price,
                        'product_data': {
                            'name': product.name,
                            # 'images': ['https://i.imgur.com/EHyR2nP.png'],
                        },
                    },
                    'quantity': 1,
                },
            ],
            metadata={
                "product_id": product.id
            },
            mode='payment',
            success_url=YOUR_DOMAIN + '/success/',
            cancel_url=YOUR_DOMAIN + '/cancel/',
        )
        return JsonResponse({
            'id': checkout_session.id
        })

# to test this webhook, you can use the Stripe CLI 
# run command stripe listen --forward-to localhost:8000/checkout/webhooks/stripe/

@csrf_exempt
def stripe_webhook(request):
    '''
    This Django view creates a Stripe Checkout session for a given product ID. 
    It sets the session mode to 'payment' and specifies success and cancel URLs. 
    It returns the ID of the created session.
    '''
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None
    print("stripe_webhook payload=", payload)

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        print("checkout.session.completed=", session)

        customer_email = session["customer_details"]["email"]
        product_id = session["metadata"]["product_id"]

        product = Product.objects.get(id=product_id)

        send_mail(
            subject="Here is your product",
            message=f"Thanks for your purchase. Here is the product you ordered. The URL is {product.url}",
            recipient_list=[customer_email],
            from_email="matt@test.com"
        )

        # TODO - decide whether you want to send the file or the URL
    
    elif event["type"] == "payment_intent.succeeded":
        intent = event['data']['object']
        print("payment_intent.succeeded", intent)

        stripe_customer_id = intent["customer"]
        stripe_customer = stripe.Customer.retrieve(stripe_customer_id)

        customer_email = stripe_customer['email']
        product_id = intent["metadata"]["product_id"]

        product = Product.objects.get(id=product_id)

        send_mail(
            subject="Here is your product",
            message=f"Thanks for your purchase. Here is the product you ordered. The URL is {product.url}",
            recipient_list=[customer_email],
            from_email="matt@test.com"
        )

    return HttpResponse(status=200)


@csrf_exempt
def intent_post(request):
    '''
    This Django view handles Stripe webhook events. It parses the payload and verifies the signature. 
    It handles checkout.session.completed and payment_intent.succeeded events, sends an email to the 
    customer with the product URL, and returns an HTTP response.
    '''
    try:
        req_json = json.loads(request.body)
        customer = stripe.Customer.create(email=req_json['email'])
        product_id = 1
        product = Product.objects.get(id=product_id)
        intent = stripe.PaymentIntent.create(
            amount=product.price,
            currency='usd',
            customer=customer['id'],
            metadata={
                "product_id": product.id
            }
        )
        print("secreet=",intent['client_secret'])
        return JsonResponse({
            'client_secret': intent['client_secret']
        })
    except Exception as e:
        return JsonResponse({ 'error': str(e) })
        

