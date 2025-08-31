from django.urls import path
from . import views

urlpatterns = [
    path('books/', views.books),
    path('books-http/', views.bookshttp),
    path('books-class/', views.BookList.as_view()),
    path('books-class/<int:key>/', views.BookList.as_view()),
    path('menu-items/', views.MenuItemsView.as_view()),
    path('single-menu/<int:pk>/', views.SingleMenuItem.as_view()),
    path('display-menu/', views.display_menu),
    path('display-single-menu/<int:key>/', views.display_single_menu),
    path('create-single-menu/', views.create_single_menu),
    path('display-form/', views.display_form, name='display_form'),
    path('display-menu-form/', views.display_menu_form),
    path('my-view/', views.my_view),
    path('upload-photo/', views.upload_photo, name='upload_photo')
]