from django.contrib import admin
from django.conf.urls import include
from rest_framework import routers
from django.urls import path
from levelupapi.views import register_user, login_user, GameTypeView, EventView

router = routers.DefaultRouter(trailing_slash=False) # trailing_slash=False tells
router.register(r'gametypes', GameTypeView, 'gametype')
router.register(r'events', EventView, 'event')

urlpatterns = [
    path('', include(router.urls)),
    # Requests to http://localhost:8000/register will be routed to the register_user function
    path('register', register_user),
    # Requests to http://localhost:8000/login will be routed to the login_user function
    path('login', login_user),
    path('admin/', admin.site.urls),
]
