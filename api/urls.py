from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from jobs.views import JobViewSet, CategoryViewSet, CategoryJobViewSet, EmployerJobViewSet
from users.views import JobseekerViewSet, EmployerViewSet
from apply_review.views import ApplicationViewSetForJobseeker, ApplicationViewSetForEmployer, ReviewViewSetForEmployer, ReviewViewSetForJobseeker

schema_view = get_schema_view(
   openapi.Info(
      title="WorkWay Projects Backend DRF API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)



router = DefaultRouter()

router.register('jobs', JobViewSet)
router.register('categories', CategoryViewSet)
router.register('jobseekers', JobseekerViewSet, basename='jobseeker')
router.register('employers', EmployerViewSet, basename='employer')

category_router = NestedDefaultRouter(router, 'categories', lookup='category')
category_router.register('jobs', CategoryJobViewSet, basename='category-job')

jobseeker_router = NestedDefaultRouter(router, 'jobseekers', lookup='jobseeker')
jobseeker_router.register('applications', ApplicationViewSetForJobseeker, basename='job-application')
jobseeker_router.register('reviews', ReviewViewSetForJobseeker, basename='jobseeker-reviews')

employer_router = NestedDefaultRouter(router, 'employers', lookup='employer')
employer_router.register('jobs', EmployerJobViewSet, basename='employer-job')
employer_router.register('reviews', ReviewViewSetForEmployer, basename='employer-reivews')

# employer -> jobs -> applications
job_router = NestedDefaultRouter(employer_router, 'jobs', lookup='job')
job_router.register('applications', ApplicationViewSetForEmployer, basename='employer-job-applications')


urlpatterns = [
   path('', include(router.urls)),
   path('', include(category_router.urls)),
   path('', include(jobseeker_router.urls)),
   path('', include(employer_router.urls)),
   path('', include(job_router.urls)),
   path('api-auth/', include('rest_framework.urls')),
   path('auth/', include('djoser.urls')),
   path('auth/', include('djoser.urls.jwt')),
   path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
   path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
