from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Meal, Review
from .forms import ReviewForm
from cart.forms import CartAddMealForm  # Correct form import


# Meal detail + review creation
def meal_detail(request, category_slug, meal_slug):
    category = get_object_or_404(Category, slug=category_slug)
    meal = get_object_or_404(
        Meal,
        category_id=category.id,
        slug=meal_slug
    )

    # Handle review submission
    if request.method == 'POST':
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            cf = review_form.cleaned_data
            author_name = "Anonymous"  # Default author
            if request.user.is_authenticated and request.user.first_name != '':
                author_name = request.user.first_name

            # Create the review
            Review.objects.create(
                meal=meal,
                author=author_name,
                rating=cf['rating'],
                text=cf['text']
            )

            return redirect(
                'listings:meal_detail',
                category_slug=category_slug,
                meal_slug=meal_slug
            )
    else:
        review_form = ReviewForm()

    # Cart form for adding a meal to the cart
    cart_meal_form = CartAddMealForm()

    return render(
        request,
        'meal/detail.html',
        {
            'meal': meal,
            'review_form': review_form,
            'cart_meal_form': cart_meal_form
        }
    )


# List all meals (homepage) or meals by category
def meal_list(request, category_slug=None):
    category = None
    meals = Meal.objects.all()
    categories = Category.objects.all()

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        meals = meals.filter(category=category)

    context = {
        'category': category,
        'categories': categories,
        'meals': meals,
    }

    return render(request, 'meal/list.html', context)
