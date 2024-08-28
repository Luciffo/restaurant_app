from django.contrib import admin
from django.urls import path, include
from restaurant import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('restaurant.urls')),
    # path('accounts/', include('django.contrib.auth.urls')),  # URL-ы для аутентификации
    path('register/', views.register, name='register'),
]   + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)