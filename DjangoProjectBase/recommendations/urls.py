from django.urls import path
from . import views

urlpatterns = [
    path('', views.recommend_movie, name='recommend_movie'),  # Cambiado para que la URL raíz apunte a recommend_movie
]
