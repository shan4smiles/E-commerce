from django.shortcuts import render, redirect

# Create your views here.
def home(request):
    products = Product.objects.filter(is_featured = True)
    return render(request, 'home.html', {'data': products})

from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    return render(request, 'index.html')

from django.contrib.auth import logout
@login_required
def logout_user(request):
    logout(request)
    return redirect('main:home')

print("----------------------------------------------------------------------------------------------------------------------")
# Forms usage
from .forms import UserRegistrationForm
def register_user(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('main:index')
    else:
        form = UserRegistrationForm()
    return render(request, 'register_user.html', {'form': form})

from .forms import AuthenticationForm
from django.contrib.auth import login,authenticate
def authenticate_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username_from_form = form.cleaned_data['username']
            password_from_form = form.cleaned_data['password']
            user = authenticate(request,username = username_from_form,password= password_from_form)
            if user is not None:
                login(request, user)
                return redirect('main:index')
            else:
                return render(request, 'login.html', {'error_message': 'Invalid username or password'})
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

from .forms import ProductRegistrationForm
@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductRegistrationForm(request.POST, request.FILES) # request.FILES because even image ta is being passed
        if form.is_valid():
            form.save()
            return redirect('main:index')
    else:
        form = ProductRegistrationForm()
    return render(request, 'add_product.html', {'form': form})

print("----------------------------------------------------------------------------------------------------------------------")
# For filtering, searching

from django.db.models import Q
from .models import Product, Category
@login_required
def product_list(request):
    # Get all products
    products = Product.objects.all()
    categories = Category.objects.all() # to display in HTML options
    # Get from HTML
    name = request.GET.get('name')
    price_min = request.GET.get('price_min')
    price_max = request.GET.get('price_max')
    category = request.GET.get('category')
    is_featured = request.GET.get('is_featured')
    # Filter it from database
    if name:
        products = products.filter(Q(name__icontains=name) | Q(description__icontains=name))
    if price_min:
        products = products.filter(price__gte=price_min)
    if price_max:
        products = products.filter(price__lte=price_max)
    if category:
        products = products.filter(category__name=category)
    if is_featured:
        products = products.filter(is_featured=is_featured)

    # Return data
    return render(request, 'product_list.html', {'data': products, 'categories': categories},)

print("----------------------------------------------------------------------------------------------------------------------")
# getting from a post form via HTML

from django.shortcuts import get_object_or_404
from .models import Product, Review
from .forms import ReviewForm
from django.contrib import messages # to handle error messages: messages.error(request, "Msg here")
@login_required
def product_details(request, pk):
    product = Product.objects.filter(pk = pk).first() # first() is used bcz, filter generally returns alist of objects, or use below
    # product = get_object_or_404(Product, pk= pk)

    # to display reviews
    reviews = Review.objects.filter(product=product)

    # to make review add section disappear
    user = request.user
    review_submitted = False # for disabling the review section
    existing_review = Review.objects.filter(user=user, product=product)
    if existing_review:
        messages.error(request, 'You have already submitted a review for this product.')
        review_submitted = True  # Set flag to indicate review submission

    # to add review without form
    if request.method == 'POST':
        user = user
        product = product
        rating = request.POST.get('rating')
        review = request.POST.get('review')
        review_section = Review(user=user, product= product, rating=rating, review=review)
        review_section.save()
        return redirect('main:product_detail', pk=pk)

    return render(request, 'product_details.html',{'data': product, 'reviews': reviews, 'review_submitted': review_submitted})

    # # to add review via forms
    # if request.method=='POST':
    #     form = ReviewForm(request.POST)
    #     if form.is_valid():
    #         if existing_review:
    #             messages.error(request, 'You have already submitted a review for this product.')
    #             review_submitted = True  # Set flag to indicate review submission
    #         else:
    #             review = form.save(commit=False)
    #             # we set commit as False and save it in another form before commiting it to database bcz the "user" and "product" field need to be filled
    #             review.product = product
    #             review.user = request.user # the current logged user
    #             review.save() # by default commit = True
    #             return redirect('main:product_detail', pk=pk)
    # else:
    #     if existing_review:
    #         messages.error(request, 'You have already submitted a review for this product.')
    #         review_submitted = True  # Set flag to indicate review submission
    #     form = ReviewForm()
    # return render(request, 'product_details.html', {'data': product, 'reviews': reviews, 'form': form, 'review_submitted': review_submitted})
