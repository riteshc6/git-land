
from django.urls import path, include
from . import views

urlpatterns = [
    path('/ci',views.call_celery,name='call_celery'),
    path('/check_status/<int:task_id>',views.check_status,name='check_status'),
    path('/user/notifications',views.display_messages,name='notifications'),
    path('/<username>/<int:repo_id>/test_results',views.display_messages,name='test_result'),
]
