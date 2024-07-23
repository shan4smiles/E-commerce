# just run this file to update the data model

from main.models import Product

def update_product_field():
    Product.objects.filter(is_featured = False).update(is_featured = True)
    # products = Product.objects.all()
    #
    # for product in products:
    #     # note: we can use try except to handle invalid inputs
    #
    #     # characters input
    #     # product.is_featured = input(f"Enter char field for {product.name}")
    #
    #     # integer input:
    #     # product.is_featured = int(input(f"Enter number field for {product.name}"))
    #
    #     # boolean input:
    #     # user_input = input(f"Enter True or false for {product.name}")
    #     # product.is_featured = user_input.lower() == 'true'
    #
    #     product.save()
if __name__ == "main":
    update_product_field()