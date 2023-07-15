from django.contrib import admin
from django.urls import path
from sca.views import ScaView, get_csrf_token





from sca.views import (
    ScaView,

)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('get_csrf_token/', get_csrf_token, name='get_csrf_token'),
    path('contract/', ScaView.as_view(), name='sca_request'),
   
]
