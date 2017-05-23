"""manosBackend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

#Por ver
from rest_framework import routers 
from apps.apiREST.views import *
router = routers.DefaultRouter()
router.register(r'^userDOC',UserViewSet)
router.register(r'^workerDOC',WorkerViewSet)
router.register(r'^addressDOC',AddressViewSet)
router.register(r'^commentDOC',CommentViewSet)
router.register(r'^categoryDOC',CategoryViewSet)
router.register(r'^subcategoryDOC',SubcategoryViewSet)
router.register(r'^jobrequestDOC',JobRequestViewSet)
router.register(r'^photoDOC',PhotoViewSet)
router.register(r'^jobapplicationDOC',JobApplicationViewSet)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('apps.apiREST.urls')),
	url(r'^',include(router.urls)),
]






