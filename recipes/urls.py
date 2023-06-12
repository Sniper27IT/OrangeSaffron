from django.urls import path
from . import views
from .views import profile_view


urlpatterns = [
    path('', views.home, name='home'),
    path('create/', views.create_recipe, name='create_recipe'),
    path('recipe/<int:recipe_id>/', views.recipe_detail, name='recipe_detail'),
    path('search/', views.recipe_search, name='recipe_search'),
    path('myfavorites/', views.my_favorites, name='my_favorites'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/<int:user_id>/', profile_view, name='profile'),
    path('recipe/add_favorite/<int:recipe_id>/', views.add_to_favorites, name='add_to_favorites'),
    path('recipe/remove_favorite/<int:recipe_id>/', views.remove_from_favorites, name='remove_from_favorites'),
    path('follow/<int:user_id>/', views.follow_user, name='follow_user'),
    path('unfollow/<int:user_id>/', views.unfollow_user, name='unfollow_user'),
    path('followed-users/', views.followed_users, name='followed_users'),
    path('recipes/<int:recipe_id>/update/', views.update_recipe, name='update_recipe'),
    path('delete-photo/<int:photo_id>/', views.delete_photo, name='delete_photo'),
    path('recipe/delete/<int:recipe_id>/', views.delete_recipe, name='delete_recipe'),
]

