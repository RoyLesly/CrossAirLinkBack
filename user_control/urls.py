from django.urls import path, include
from rest_framework import routers
from user_control.models import UserActivities
from user_control.views import (
    CrudUserView, LoginView, LogoutView, CreatePasswordView, MeView,
    UserActivitiesView, UsersView, UserActivitiesView, UsersView, GroupView, 
    PermissionView, AssignGroupsToUserView, UserProfilesView,
    AssignPermissionsGroupView, CompanyProfileView
)

app_name = "user_control"

router = routers.DefaultRouter(trailing_slash=False)
router.register("crud-user", CrudUserView, "crud-user")
router.register("assign-group-to-user", AssignGroupsToUserView, "assign-group-to-user")
router.register("assign-permissions-to-group", AssignPermissionsGroupView, "assign-permissions-to-group")
router.register("login", LoginView, "login")
router.register("logout", LogoutView, "logout")
router.register("create-password", CreatePasswordView, "create-password")
router.register("me", MeView, "me")
router.register("activities-log", UserActivitiesView, "activities log")
router.register("users", UsersView, "users")
router.register("user-profiles", UserProfilesView, "user-profiles")

router.register('groups',  GroupView, "groups" ),
router.register('permissions',  PermissionView, "permissions" ),
router.register('crud-company-profile',  CompanyProfileView, 'company-profile' ),


urlpatterns = [
    path('', include(router.urls)),
]
