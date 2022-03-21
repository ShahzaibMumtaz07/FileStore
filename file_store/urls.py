"""file_store URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf.urls import url

open_info = openapi.Info(
      title="Spekit-Challenge",
      default_version='v1',
      description="Spekit Home Task Challenge",
      terms_of_service="#",
      contact=openapi.Contact(email="shahzaib.mumtaz.20195@gmail.com"),
      license=openapi.License(name="MIT"),
   )
schema_view = get_schema_view(
   open_info,
   public=True,
   permission_classes=(permissions.AllowAny,),
)



urlpatterns = [
    path('api-token-auth/', obtain_jwt_token, name='obtain_jwt_token'),
    # url(r'', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

    path('api/', include('api.urls'))
]


if settings.DEBUG:
  urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

