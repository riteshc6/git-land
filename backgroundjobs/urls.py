
from django.urls import path, include
from . import views

urlpatterns = [
    # path('ci/<path:repo_path>/<int:commit_id>',views.call_celery,name='call_celery'),
    # path('check_status/<task_id>',views.check_status,name='check_status'),
    # path('user/notifications',views.display_messages,name='notifications'),
    path('<username>/<repo_name>',views.display_all_messages,name='test_result'),
    path('<username>/<repo_name>/<int:test_id>',views.test_log,name='test_log'),
    path('display_message',views.display_message,name='display_message'),
    # path('test/click',views.test,name='test'),
]
