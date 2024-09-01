
from django.contrib import admin
from django.urls import path , include
from my_api import views
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

router = DefaultRouter()
router.register('guests', views.viewsets_guest)
router.register('Movie', views.Viewsets_Movie)
router.register('Reservation', views.Viewsets_Reservation)

urlpatterns = [
    path('admin/', admin.site.urls),
    # 1 
    path('Django/json_response_no_model', views.no_rest_no_model),
    #2
    path('Djangi/json_response_with_model_no_rest', views.no_rest_with_model),
    #3.1 => FBV  GET POST

    path('rest/FBV_list',views.FBV_list ),

    #3.2 => FBV PUT GET DELETE

    path('rest/FBV_list/<int:pk>',views.FBV_pk ),

    # 4.1 List and Create == GET and POST

    path('rest/CBV_list',views.CBV_List.as_view(), name='cbv_list'),

    #4.2 GET PUT DELETE

    path('rest/CBV_list/<int:pk>',views.CBV_pk.as_view(), name='cbv_list'),

    # 5.1 mixins list

    path('rest/mixins/',views.mixins_list.as_view(), name='mixins_list'),

    # 5.2  mixins get put delete

    path('rest/mixins/<int:pk>',views.mixins_pk.as_view(), name='mixins_list'),

    # 6.1 generics list

    path('rest/generics/',views.generics_list.as_view(), name='generics_list'),

    # 6.2 generics get put delete 

    path('rest/generics/<int:pk>',views.generics_pk.as_view(), name='generics_pk'),

    # 7 ViewSets

    path('rest/viewsets/', include(router.urls)),

    # 8 find movie 

    path('fbv/findmovie', views.find_movie),

    # 9 new reservation 

    path('fbv/newreservation', views.new_reservation),

    # 10 rest auth url

    path('api-auth', include('rest_framework.urls')),

    # 11 token auth

    path('api-token-auth', obtain_auth_token),

    # 12 Post pk generics Post_pk
    #path('Post/generics/',views.Post_List.as_view()),
    path('Post/generics/<int:pk>',views.Post_pk.as_view()),






]
