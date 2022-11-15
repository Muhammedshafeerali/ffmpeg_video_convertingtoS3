from django.urls import include, path
# from django.views.decorators.csrf import csrf_exempt
from .views import *

urlpatterns = [
    path(
        '',
        homeView.as_view(),
        name="homeView"
    ),
    path(
        'api/sendfile/',
        UploadAwsFile.as_view(),
        name="sendfile"
    ),
]