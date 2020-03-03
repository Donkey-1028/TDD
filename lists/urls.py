from django.urls import path

from .views import home_page, view_list, new_list

app_name = 'lists'

urlpatterns = [
    path('', home_page, name='home'),
    path('lists/<int:list_id>/', view_list, name='view_list'),
    path('lists/new', new_list, name='new_list'),
]
