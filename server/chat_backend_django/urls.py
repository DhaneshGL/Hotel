
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('chat_app.urls')),
    path('api/admin/', include('chat_app.admin_urls')),
]
