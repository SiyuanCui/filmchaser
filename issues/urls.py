from django.urls import path, include
from . import views

urlpatterns = [
    # Background list page
    path('admin/list/', views.adminlist, name="issues_list"),
    # backend author
    path('admin/author/', views.author, name="issues_author"),

    path('add/', views.add, name="issuesadd"),

    # Data insertion
    path('insert/', views.insert, name="issuesinsert"),

    # Data insertion
    path('update/', views.update, name="issuesupdate"),
    path('adminupdt/', views.adminupdt, name="adminupdt"),

    # Delete data
    path('delete/', views.delete, name="issuesdelete"),

]
