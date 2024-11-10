from django.urls import path,include,re_path
from . import views


app_name = 'home'




bucket_urls = [
	 path('', views.upload_photo, name='upload_photo'),
    re_path(r'^download/(?P<photo_name>.+)/$', views.download_photo, name='download_photo'),
    re_path(r'^delete/(?P<photo_name>.+)/$', views.delete_photo, name='delete_photo'),  # Update this line
]

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('category/<slug:category_slug>/', views.HomeView.as_view(), name='category_filter'),
    path('bucket/',include(bucket_urls)),
    path('product/<slug:slug>', views.DetailView.as_view(), name='detail'),

]
