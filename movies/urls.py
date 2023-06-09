from django.urls import path, include
from . import views

urlpatterns = [

    path('admin/updt/', views.adminupdt, name="movies_updt"),

    # Background details page
    path('admin/detail/', views.admindetail, name="movies_detail"),
    # Front list page
    path('', views.index, name="moviesindex"),
    # Front desk details page
    path('detail/', views.detail, name="moviesdetail"),

    # Data insertion
    path('insert/', views.insert, name="moviesinsert"),

    # Data insertion
    path('update/', views.update, name="moviesupdate"),

    # Delete data
    path('delete/', views.delete, name="moviesdelete"),

]
