from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from company import views
from jewelapp import settings

schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)
urlpatterns = [
                  url(r'^api/swagger(?P<format>\.json|\.yaml)$', schema_view.with_ui(cache_timeout=0),
                      name='schema-json'),
                  url(r'^api/swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
                  url(r'^api/redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
                  url(r'^admin/', admin.site.urls),
                  url(r'^api/', include('user.urls')),
                  url(r'^api/agent/', include('agent.urls')),
                  url(r'^api/customer/', include('customer.urls')),
                  url(r'^api/', include('questions.urls')),
                  url(r'^api/masters/area/$', views.AreaList.as_view())
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) \
              + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
