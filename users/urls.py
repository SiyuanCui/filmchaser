from django.urls import path, include
from . import views

urlpatterns = [
    # Add page in the background
    path('admin/updt/', views.adminupdt, name="user_updt"),
    path('admin/updtself/', views.adminupdtself, name="user_updtself"),
    # Background list page
    path('admin/list/', views.adminlist, name="user_list"),

    path('add/', views.add, name="useradd"),

    # Data insertion
    path('insert/', views.insert, name="userinsert"),

    # Data insertion
    path('update/', views.update, name="userupdate"),

    # Delete data
    path('delete/', views.delete, name="userdelete"),

]
