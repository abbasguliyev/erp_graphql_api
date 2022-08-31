from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path, re_path
from django.views.static import serve

from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView

from api.api import schema
from graphql_playground.views import GraphQLPlaygroundView

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r"^media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT}),
    re_path(r"^static/(?P<path>.*)$", serve, {"document_root": settings.STATIC_ROOT}),
    
    path("graphql", csrf_exempt(GraphQLView.as_view(graphiql=True, schema=schema))),
    path('playground/', GraphQLPlaygroundView.as_view(endpoint="https://do.kodaze.com/graphql")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
