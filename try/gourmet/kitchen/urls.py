from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.loginview, name='loginview'),
    path('signup', views.signup, name='signup'),
    path('profile/<str:usernameLink>', views.profile, name='profile'),
    path('logout',views.logout_view,name='logout'),
    path('dpChange',views.dpChange,name='dpChange'),
    path('coverChange',views.coverChange,name='coverChange'),
    path('detailsChange',views.detailsChange,name='detailsChange'),
    path('new',views.newRecipe, name="newRecipe"),
    path('acceptNewRec',views.acceptNewRec, name="acceptNewRec"),
    path('category/<str:categoryName>', views.category, name="category"),
    path('result',views.result,name="result"),
    path('team',views.team,name="team")

]
