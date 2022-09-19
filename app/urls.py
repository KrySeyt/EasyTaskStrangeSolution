from django.urls import path, include

from . import views


urlpatterns = [
    path('', views.main, name='main'),
    path('add-array', views.add_array, name='add-array'),
    path('delete-array/<int:array_id>', views.delete_array, name='delete-array'),
    path('process-arrays', views.process_arrays, name='process-arrays'),
    path('save-changes', views.save_changes, name='save-changes'),
]
