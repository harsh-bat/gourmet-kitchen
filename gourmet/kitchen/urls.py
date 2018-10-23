from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.loginview, name='loginview'),
    path('signup', views.signup, name='signup'),
    path('profile/<str:usernameLink>', views.profile, name='profile'),
    path('edit/<int:recNoLink>', views.editRec, name='editRec'),
    path('recipe/<int:recNoLink>', views.recipe, name='recipe'),
    path('logout',views.logout_view,name='logout'),
    path('dpChange',views.dpChange,name='dpChange'),
    path('coverChange',views.coverChange,name='coverChange'),
    path('detailsChange',views.detailsChange,name='detailsChange'),
    path('new',views.newRecipe, name="newRecipe"),
    path('acceptNewRec',views.acceptNewRec, name="acceptNewRec"),
    path('acceptEditRec',views.acceptEditRec, name="acceptEditRec"),
    path('search', views.search, name="search"),
    path('category/<str:urlCategory>', views.category, name="category"),
    path('saveTarget', views.saveTarget, name="saveTarget"),
    path('starTarget', views.starTarget, name="starTarget"),
    path('meet', views.meet, name="meet"),
]
