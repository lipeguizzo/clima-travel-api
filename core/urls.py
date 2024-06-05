from django.contrib import admin
from django.urls import path
from climate.views import ClimateView

urlpatterns = [
    path('admin', admin.site.urls),
    path('climate', ClimateView.as_view(), name='climate' ),
]
