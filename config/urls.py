from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('campaigns.urls')),
    path('api/v1/dashboard/', include('dashboard.urls')),
    path('api/v1/ai/', include('ai_tools.urls')),
]
