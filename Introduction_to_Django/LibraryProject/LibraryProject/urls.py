from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('relationships/', include('LibraryProject.relationship_app.urls')), #adjust if your app is not in a folder.
]