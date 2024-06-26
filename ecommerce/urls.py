from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('' , include('core.urls')),
    path('items/', include('item.urls', namespace='item')),
    path('payment/', include('payment.urls', namespace='payment')),
    path('admin/', admin.site.urls),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
