"""djangoProject1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app01 import views
from app01.views import PredictVisitorsView

# url和函数的对应关系
urlpatterns = [
    path('admin/', admin.site.urls),

    path('getRelics/', views.getRelics),
    path('getCategory/', views.getCategory),
    path('updateCategory/', views.updateCategory),
    path('updateRelics/', views.updateRelics),
    path('uploadFile/', views.uploadFile),
    path('getPercent/', views.getPercent),
    path('getRelicsInfo/', views.getRelicsInfo),
    path('getCircleInfo/', views.getCircleInfo),
    path('getColumChartInfo/', views.getColumChartInfo),
    path('deleteRelics/', views.deleteRelics),
    path('insertRelics/', views.insertRelics),
    path('deleteCategory/<int:id>/', views.deleteCategory),
    path('getAllUsers/', views.getAllUsers),
    path('predict/', PredictVisitorsView.as_view(), name='predict_visitors'),
    path('getWordCloudData/', views.get_word_cloud_data),

]
