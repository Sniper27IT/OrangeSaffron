from django.shortcuts import render, redirect, get_object_or_404
from .models import Recipe, Favorite, Category, UserProfile, Comment, Yummy, Photo
from .forms import RecipeForm, UserProfileForm, PhotoForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


def home(request):
    return render(request, 'home.html')


def create_recipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()

            photos = request.FILES.getlist('photos')
            for photo in photos:
                Photo.objects.create(recipe=recipe, image=photo)

            profile = request.user.userprofile
            profile.recipes_created += 1
            profile.save()

            return redirect('recipe_detail', recipe_id=recipe.pk)
    else:
        form = RecipeForm()

    return render(request, 'create_recipe.html', {'form': form})


@login_required
def update_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)

    if request.user != recipe.author:
        return redirect('recipe_detail', recipe_id=recipe.pk)

    photos = Photo.objects.filter(recipe=recipe)

    if request.method == 'POST':
        recipe_form = RecipeForm(request.POST, instance=recipe)
        photo_form = PhotoForm(request.POST, request.FILES)

        if recipe_form.is_valid():
            recipe = recipe_form.save()

            Photo.objects.filter(recipe=recipe).delete()

            if 'photos' in request.FILES:
                photos = request.FILES.getlist('photos')[:5]
                for photo in photos:
                    Photo.objects.create(recipe=recipe, image=photo)

            return redirect('recipe_detail', recipe_id=recipe.pk)
    else:
        recipe_form = RecipeForm(instance=recipe)
        photo_form = PhotoForm()

    return render(request, 'update_recipe.html', {'recipe_form': recipe_form, 'photo_form': photo_form, 'photos': photos})


@login_required
def delete_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    if request.user == recipe.author:
        if request.method == 'POST':
            recipe.delete()
            profile = request.user.userprofile
            profile.recipes_created -= 1
            profile.save()
            return redirect('home')
    else:
        return redirect('home', recipe_id=recipe_id)


def recipe_detail(request, recipe_id):
    recipe = Recipe.objects.get(pk=recipe_id)
    is_favorite = False
    if request.user.is_authenticated:
        is_favorite = Favorite.objects.filter(user=request.user, recipe=recipe).exists()

    if request.method == 'POST':
        if request.user.is_authenticated:
            comment_content = request.POST.get('comment', '')
            if comment_content.strip():
                Comment.objects.create(recipe=recipe, user=request.user, content=comment_content)

    yummy_count = Yummy.objects.filter(recipe=recipe).count()

    is_liked = False
    if request.user.is_authenticated:
        is_liked = Yummy.objects.filter(user=request.user, recipe=recipe).exists()

    if request.method == 'POST' and request.user.is_authenticated:
        if is_liked:
            Yummy.objects.filter(user=request.user, recipe=recipe).delete()
        else:
            Yummy.objects.create(user=request.user, recipe=recipe)

        yummy_count = Yummy.objects.filter(recipe=recipe).count()

    comments = Comment.objects.filter(recipe=recipe).order_by('-created_at')
    photos = Photo.objects.filter(recipe=recipe)

    return render(request, 'recipe_detail.html', {
        'recipe': recipe,
        'is_favorite': is_favorite,
        'is_liked': is_liked,
        'comments': comments,
        'yummy_count': yummy_count,
        'photos': photos,
    })


def recipe_search(request):
    query = request.GET.get('query')
    category_id = request.GET.get('category')
    author_id = request.GET.get('author')

    recipes = Recipe.objects.all()

    if query:
        recipes = Recipe.objects.filter(title__icontains=query)
    if category_id:
        recipes = Recipe.objects.filter(category_id=category_id)
    if author_id:
        recipes = Recipe.objects.filter(author_id=author_id)

    categories = Category.objects.all()

    return render(request, 'recipe_search.html', {'recipes': recipes, 'query': query, 'categories': categories})


def my_favorites(request):
    favorites = Favorite.objects.filter(user=request.user)
    return render(request, 'my_favorites.html', {'favorites': favorites})


def register(request):
    if request.method == 'POST':
        user_form = UserCreationForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            login(request, user)
            return redirect('home')
    else:
        user_form = UserCreationForm()
        profile_form = UserProfileForm()
    return render(request, 'register.html', {'user_form': user_form, 'profile_form': profile_form})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('home')


def profile_view(request, user_id):
    user_profile = get_object_or_404(UserProfile, user__id=user_id)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
    else:
        form = UserProfileForm(instance=user_profile)

    return render(request, 'profile.html', {'user_profile': user_profile, 'form': form})


def add_to_favorites(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    favorite, created = Favorite.objects.get_or_create(user=request.user, recipe=recipe)
    print(f"Recipe {recipe_id} added to favorites for user {request.user.username}")
    return redirect('recipe_detail', recipe_id=recipe.id)


def remove_from_favorites(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    favorite = Favorite.objects.filter(user=request.user, recipe=recipe)
    favorite.delete()
    return redirect('recipe_detail', recipe_id=recipe.id)


@login_required
def follow_user(request, user_id):
    user_to_follow = get_object_or_404(User, id=user_id)
    user_profile = user_to_follow.userprofile
    user_profile.followers.add(request.user)
    return redirect('profile', user_id=user_id)


@login_required
def unfollow_user(request, user_id):
    user_to_unfollow = get_object_or_404(User, id=user_id)
    user_profile = user_to_unfollow.userprofile
    user_profile.followers.remove(request.user)
    return redirect('profile', user_id=user_id)


@login_required
def followed_users(request):
    user_profile = request.user.userprofile
    following_users = User.objects.filter(userprofile__followers=request.user)
    return render(request, 'followed_users.html', {'following_users': following_users})


def delete_photo(request, photo_id):
    photo = get_object_or_404(Photo, pk=photo_id)
    recipe_id = photo.recipe.pk
    photo.delete()
    return redirect('update_recipe', recipe_id=recipe_id)




