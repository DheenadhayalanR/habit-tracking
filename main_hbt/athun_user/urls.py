from django.urls import path,include
from rest_framework.routers import DefaultRouter
from . import views

# router=DefaultRouter()

# router.register('reg',Registerviwe,basename='register_post_method_only')
# router.register('log',Loginview,basename='login_post_method_only')                #'not_mention_the_methods'

urlpatterns = [
    
    path('signup/',views.Registerviwe.as_view(),name='Registerviwe'),
    path('signin/',views.Loginview.as_view(),name='Loginviwe'),
    path('refershaccesstoken/',views.RefershAccessToken.as_view(),name='Refersh Access Token'),
    path('profile/',include('profile_app.urls')),

]