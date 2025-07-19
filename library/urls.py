
from django.contrib import admin
from django.urls import path, re_path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf import settings
from django.conf.urls.static import static

schema_view = get_schema_view(
   openapi.Info(
      title="Library API",
      default_version='v1',
      description="Library API",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@library.local"),
      license=openapi.License(name="MIT License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('apps.member.urls')),
    path('api/', include('apps.librarians.urls')),
    path('api/', include('apps.authentication.urls')),
    re_path(r'^auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.jwt')),
    
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    # path('accounts/', include('django.contrib.auth.urls')),  # Uncomment if you want login/logout views
]

# Serve static files in development
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
