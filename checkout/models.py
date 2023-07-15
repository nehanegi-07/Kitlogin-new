from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=50)
    price = models.IntegerField(default=0)  # cents

    def __str__(self):
        return self.name
    
    def get_display_price(self):
        return "{0:.2f}".format(self.price / 100)



class Payment(models.Model):
    '''
    This model has a foreign key field named user that refers to the KitUser model from the login app. 
    It also has a product field that stores the name of the product being paid for as a string. 
    Finally, there is a timestamp field that automatically records the time of the payment.
    '''
    user = models.ForeignKey("login.KitUser", on_delete=models.CASCADE)
    # Note that in the choices argument for the product field, we use a list comprehension to generate a list of tuples containing 
    # the name of each available product as both the display value and the underlying value. 
    # This ensures that the product field will only accept valid product names.
    product = models.CharField(max_length=100, choices=[(p.name, p.name) for p in Product.objects.all()])
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} paid for {self.product} on {self.timestamp}"