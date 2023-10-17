"""
URL configuration for wxxcx project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from wxxcx_app01.views import LoginAPI, RegisterAPI, TaskListCreate, TaskCreateAPI, CourierCreateAPI
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/login/', LoginAPI.as_view(), name='api-login'),
    path('api/register/', RegisterAPI.as_view(), name='api-register'),
    path('api/tasks/', TaskListCreate.as_view(), name='task-list-create'),
    path('api/create_task/', TaskCreateAPI.as_view(), name='create_task'),
    path('api/courier_create/', CourierCreateAPI.as_view(), name='courier_create'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)