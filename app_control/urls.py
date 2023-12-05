from django.urls import path, include

app_name = "app_control"

urlpatterns = [
    # path('', include(router.urls)),
    path('billing/', include('app_control.billing.urls')),
]