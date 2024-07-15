from django.urls import path, include

app_name = "authentication"

urlpatterns = [
    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.authtoken"))
]
