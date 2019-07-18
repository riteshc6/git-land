
from django.urls import path, include
from . import views
from mysite import settings
from django.conf.urls.static import static

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('accounts/', include('django.contrib.auth.urls'), name='login'),
    path('<username>/repo_form', views.repo_form, name='repo_form'),
    path('<username>/dir/<path:filepath>', views.repos, name='repos'),
    path('<username>/file/<path:filepath>', views.repo_file, name='repo_file'),
    path('<username>', views.repos_home, name='repos_home'),
    path('', views.landing_page, name='landing_page'),
    path('welcome', views.home, name='home')
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
