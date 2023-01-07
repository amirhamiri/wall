from django.urls import path
from . import views


app_name = 'ads'
urlpatterns = [
    path('all', views.AdListView.as_view(), name='ad_list'),
    path('add', views.AdCreateView.as_view(), name='ad_create'),
    path('<int:pk>', views.AdDetailView.as_view(), name='ad_detail')
]
