from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # The line below routes the root URL to hello_world.urls
    path('', include('hello_world.urls')),
]
