from rest_framework.authtoken.views import obtain_auth_token
from django.urls import path,include
from file_upload_app.api import views

urlpatterns = [
    path('register/',views.register_view,name='register'),
    path('logout/',views.logout_view,name='logout'),

    path('files/',views.AllFileView.as_view(),name='all-files'),
    path('files/my-files/',views.AllFileByUserView.as_view(),name='all-user-files'),
    path('files/<int:pk>/',views.FileDetailView.as_view(),name='file-detail'),
    path('files/create-file/',views.FileCreateView.as_view(),name='file-create'),


]