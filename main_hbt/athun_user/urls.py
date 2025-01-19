from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import Registerviwe,Loginview

router=DefaultRouter()

router.register('reg',Registerviwe,basename='register_post_method_only')
router.register('log',Loginview,basename='not_mention_the_methods')

urlpatterns = [
    # path('signup/',Registerviwe.as_view(),name='Registerviwe'),
    # path('signup/<int:pk>/',Registerviwe.as_view(),name='Registerviwe')
]+router.urls