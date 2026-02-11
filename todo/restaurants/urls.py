from rest_framework import routers

from restaurants import views

router = routers.DefaultRouter()
router.register(r'restaurants', views.RestaurantViewSet)

app_name = 'restaurants'

urlpatterns = [

]
