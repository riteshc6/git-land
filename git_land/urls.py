
from django.urls import path, include
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('<username>/<path:filepath>', views.repos, name='repos'),
    path('<username>', views.repos_home, name='repos_home'),
    path('', views.home, name='home')
]
