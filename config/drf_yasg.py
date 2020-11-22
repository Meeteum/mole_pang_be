from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Mole Pang Backend API",
        default_version="v1",
        description="How to use Mole Pang Backend API",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(name="An WonSeok", email="codeengraver@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    permission_classes=(permissions.AllowAny,),
    public=True,
)

