from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf.urls.static import static
# from django.conf.urls import url
# from django.views.static import serve

schema_view = get_schema_view(
    openapi.Info(
        title="MINIMO PROJECT API",
        default_version="v1",
        description="MINIMO 프로젝트 제작을 위한 API 문",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(name="mhm", email="minhmin219@gmail.com"),
        license=openapi.License(name="Test License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('dj_rest_auth.urls')),
    path('users/', include('dj_rest_auth.registration.urls')),
    path('users/', include('allauth.urls')),
    path('minimo/', include('apps.posts.urls')),
    # path('prj/', include('apps.projects.urls')),
    # path('project/', include('apps.projects.urls')),
    # path('social/', include('apps.social.urls'))
    # path('users/', include('users.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    urlpatterns += [
        re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name="schema-json"),
        re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
        re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),]

