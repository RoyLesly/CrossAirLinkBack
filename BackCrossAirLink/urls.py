from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from django.conf import settings
from django.conf.urls.static import static

# from rest_framework_simplejwt import views as simple_jwt_views

schema_view = get_schema_view(
    openapi.Info(
        title="CROSS API",
        default_version='v1.0.1',
        description="CROSS DESCRIPTION",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="nleslynsom@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    # path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('admin/', admin.site.urls),
    path('app/', include('app_control.urls')),
    path('user/', include('user_control.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
