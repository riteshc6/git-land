
from django.urls import path, include
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('<username>/<path:filepath>', views.repos, name='repos'),
    path('', views.home, name='home')
]
