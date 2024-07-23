# Django's ORM (Object Relational Mapping) = The ORM handles the translation of Python code into SQL queries
from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.utils.safestring import mark_safe # for handling image sin django panel


# Create your models here.
# default, max_length, max_digits, decimal_places, on_delete, upload_to, auto_now, auto_now_add, choices
class Category(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Product(models.Model):
    # primary ey is set in django by default like in MongoDB
    # if wanted to customize primary_key: """id = models.IntegerField(primary_key = True)"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=5, default=0.00)
    category = models.ForeignKey(Category, on_delete=models.CASCADE) # means that when the referenced object (the one with the foreign key) is deleted, all related objects will also be deleted automatically.
    image = models.ImageField(upload_to="media/")
    # creating a new feature after model making: is_featured
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def image_tag(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))

    # class Meta:
    #     verbose_name_plural = 'Products'
    # Above code is for renaming the class name in teh django admin panel


    def __str__(self):
        return self.name
    # method is used to define a human-readable representation of the model instance
    # if you don't define __str__(), Django will display the object's class name and memory address.
    # whenever you try to print a Product instance or display it in the admin interface, it will show the name of the product.

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rating = models.IntegerField(choices= [(i, str(i)) for i in range(1,6)]) #choices parameter expects a list of tuples where the first element of each tuple is the actual value stored in the database, and the second element is a human-readable representation of that value.
    review = models.TextField()
    created_at = models.DateTimeField(auto_now=True)

    def get_rating(self):
        return self.rating
    # function used to get the rating

    def __str__(self):
        return f"{self.product.name} - {self.user}"
    #Similarly, if you have an Review model representing reviews of items in an order,
    # you might want to represent each item as a combination of the product name and the user who ordered it.

class Order(models.Model): # With multiple products a single transaction
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='OrderItem')
    ordered_at = models.DateTimeField(auto_now_add=True)
    is_ordered = models.BooleanField(default=False)

    def __str__(self):
        return f"Order #{self.pk}"
    # Likewise, if you have an O    rder model and you want to represent each order with a unique identifier,
    # This will display "Order #" followed by the primary key (pk) of the order whenever you print or display an Order instance.

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product.name} - {self.quantity}"

class Whishlist(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)