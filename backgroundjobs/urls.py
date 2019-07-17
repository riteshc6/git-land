
from django.urls import path, include
from . import views

urlpatterns = [
    # path('ci/<path:repo_path>/<int:commit_id>',views.call_celery,name='call_celery'),
    # path('check_status/<task_id>',views.check_status,name='check_status'),
    # path('user/notifications',views.display_messages,name='notifications'),
    path('test_result/<username>/<int:repo_id>',views.display_all_messages,name='test_result'),
    # path('test/click',views.test,name='test'),
]
