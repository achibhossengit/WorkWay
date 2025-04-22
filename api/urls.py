from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter
from jobs.views import JobViewSet, CategoryViewSet, NestedJobViewSet

router = DefaultRouter()

router.register('jobs', JobViewSet)
router.register('categories', CategoryViewSet)

category_router = NestedDefaultRouter(router, 'categories', lookup='category')
category_router.register('jobs', NestedJobViewSet, basename='category-job')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(category_router.urls)),
]
