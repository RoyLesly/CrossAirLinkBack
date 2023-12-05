from rest_framework.viewsets import ModelViewSet
from django.contrib.auth.models import Group, Permission
from rest_framework.permissions import IsAuthenticated
from .models import check_permission, CompanyProfile
from .serializers import (
    UserCreateSerializer, UserUpdateSerializer, CustomUser, UserProfile, CustomUserSerializer, LogoutSerialiser,
    LoginSerialiser, CreatePasswordUserSerializer, UserActivities, UserActivitiesSerializer, GetUserSerializer,
    GroupSerializer, PermissionSerializer, AssignGroupsToUserSerializer, CompanyProfileSerializer,
    AssignPermissionsToGroupSerializer, UserProfileSerializer,
)
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from datetime import date, datetime
from BackCrossAirLink.utils import get_access_token, get_query, CustomPagination
from BackCrossAirLink.custom_methods import IsAuthenticatedCustom


def add_user_activity(user, action):
    UserActivities.objects.create(
        # user_id=user.id,
        username=user.username,
        action=action
    )


class GroupView(ModelViewSet):
    http_method_names = [ "post", "get", "put"]
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    pagination_class = CustomPagination       # This limits to 100
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def get_queryset(self):
        perm_check = "view_group"
        if self.request.method.lower() != "get":
            return self.queryset
        data = self.request.query_params.dict()
        data.pop("page", None)
        keyword = data.pop("keyword", None)
        results = self.queryset

        if keyword:
            search_fields = ("")
            query = get_query(keyword, search_fields)
            results = results.filter(query)
        return results
    
    def create(self, request, *args, **kwargs):
        perm_check = "auth.add_group"
        check_permission(request.data["payload"]["created_by_id"], perm_check)
            
        if (request.data["payload"]["created_by_id"] == 0):
            raise Exception("User Not Loggin") 
        serializer = self.serializer_class(data=request.data["payload"])

        if serializer.is_valid():
            serializer.save()
            return Response({"success": serializer.data }) 
        raise Exception(serializer.errors)
        return Response({"errors": serializer.errors })  

    def update(self, request, *args, **kwargs):
        perm_check = "auth.change_group"
        check_permission(request.data["payload"]["updated_by_id"], perm_check)
        if (request.data["payload"]["updated_by_id"] < 1):
            raise Exception("User Not Loggin")  
        object = self.get_object()
        serializer = self.serializer_class(data=request.data["payload"], instance=object)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": serializer.data })            
        return Response({"errors": serializer.errors })   
    
    def destroy(self, request, *args, **kwargs):
        perm_check = "auth.delete_group"
        check_permission(request.data["payload"]["created_by_id"], perm_check)

        if (request.data["payload"]["deleted_by_id"] < 1):
            raise Exception("User Not Loggin") 
        object = self.get_object()
        try:
            object.delete()  
            return Response({"success": "DELETED" })     
        except:
            return Response({"errors": "NOT DELETED"}) 
       

class PermissionView(ModelViewSet):
    http_method_names = [ "post", "get", "put"]
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    pagination_class = CustomPagination       # This limits to 100
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def get_queryset(self):
        if self.request.method.lower() != "get":
            return self.queryset
        data = self.request.query_params.dict()
        data.pop("page", None)
        keyword = data.pop("keyword", None)
        results = self.queryset

        if keyword:
            search_fields = ("")
            query = get_query(keyword, search_fields)
            results = results.filter(query)
        return results
    
    def create(self, request, *args, **kwargs):
        perm_check = "auth.add_permission"
        check_permission(request.data["payload"]["created_by_id"], perm_check)        
        if (request.data["payload"]["created_by_id"] == 0):
            raise Exception("User Not Loggin")                     
        serializer = self.serializer_class(data=request.data["payload"])
        if serializer.is_valid():
            raise Exception(serializer.data)
            serializer.save()
            return Response({"success": serializer.data }) 
        return Response({"errors": serializer.errors })  

    def update(self, request, *args, **kwargs):
        if (request.data["payload"]["updated_by_id"] < 1):
            raise Exception("User Not Loggin")
        perm_check = "auth.change_permission"
        check_permission(request.data["payload"]["created_by_id"], perm_check)  
        object = self.get_object()
        serializer = self.serializer_class(data=request.data["payload"], instance=object)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": serializer.data })            
        return Response({"errors": serializer.errors })   
    
    def destroy(self, request, *args, **kwargs):
        if (request.data["payload"]["deleted_by_id"] < 1):
            raise Exception("User Not Loggin") 
        object = self.get_object()
        perm_check = "auth.delete_permission"
        check_permission(request.data["payload"]["created_by_id"], perm_check)
        try:
            object.delete()  
            return Response({"success": "DELETED" })     
        except:
            return Response({"errors": "NOT DELETED"}) 


class CrudUserView(ModelViewSet):
    http_method_names = ["get", "post", "put", "delete"]
    queryset = CustomUser.objects.all()
    serializer_class = GetUserSerializer
    serializer_class_create = UserCreateSerializer
    serializer_class_update = UserUpdateSerializer
    pagination_class = CustomPagination       # This limits to 100
    
    def get_queryset(self):
        if self.request.method.lower() != "get":
            return self.queryset
        data = self.request.query_params.dict()
        data.pop("page", None)
        keyword = data.pop("keyword", None)
        results = self.queryset#.filter(**data)

        if keyword:
            search_fields = ("")
            query = get_query(keyword, search_fields)
            results = results.filter(query)
        return results

    def create(self, request):
        perm_check = "user_control.add_customuser"
        check_permission(request.data["payload"]["created_by_id"], perm_check)
        valid_request = self.serializer_class_create(data=request.data["payload"])

        try:
            if valid_request.is_valid():
                print("valid")
                print(request.data)
                if CustomUser.objects.filter(username=request.data["payload"]["username"]):
                    return Response(
                        {"error": "UserName Exist Already"},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                print("HHfffHH")
                valid_request.save()
                print("HHHH")
                return Response({ "success": "SUCCESS" })
            else:
                return Response({ "error": valid_request.errors })
        except:
            ser = self.serializer_class(data=request.data["payload"])
            if ser.is_valid():
                pass
                # raise Exception("HERE")
            return Response({"errors": ser.errors})


        try:
            CustomUser.objects.create(**valid_request.validated_data)
        except:
            return Response(
                {"error": "Server Error"},
                status=status.HTTP_400_BAD_REQUEST
            )

        add_user_activity(request.user, "added new user")

        return Response(
            {"success": "User Created Successfully"},
            status=status.HTTP_201_CREATED
        )

    def update(self, request, *args, **kwargs):
        perm_check = "user_control.change_customuser"
        check_permission(request.data["payload"]["updated_by_id"], perm_check)
        if (request.data["payload"]["updated_by_id"] < 1):
            raise Exception("User Not Loggin")  
        object = self.get_object()
        serializer = self.serializer_class(data=request.data["payload"], instance=object)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": serializer.data })            
        return Response({"errors": serializer.errors }) 
     
    def destroy(self, request, *args, **kwargs):
        perm_check = "user_control.change_customuser"
        check_permission(request.data["payload"]["deleted_by_id"], perm_check)
        if (request.data["payload"]["deleted_by_id"] < 1):
            raise Exception("User Not Loggin")  
        object = self.get_object()
        if object.is_superuser:
            raise Exception("Cannot Delete This User")
        try:
            object.delete()
            return Response({"success": "Deleted" })            
        except:
            return Response({"errors": "Error" })  
    

class LoginView(ModelViewSet):
    http_method_names = ["post"]
    queryset = CustomUser.objects.all()
    serializer_class = LoginSerialiser

    def create(self, request):
        valid_request = self.serializer_class(data=request.data["payload"])
        valid_request.is_valid(raise_exception=True)

        new_user = valid_request.validated_data["is_new_user"]
        if new_user:
            user = CustomUser.objects.filter(username=valid_request.validated_data["username"])
            if user:
                user = user[0]
                if not user.password:
                    return Response({"user": user})
                else:
                    raise Exception("User has Password Already")
            else:
                raise Exception("User With Username not Found")
        if (valid_request.validated_data.get("password", None) == None):
            user = CustomUser.objects.filter(username=valid_request.validated_data["username"])
            if not user:
                return Response({"errors": {"User": "With Username not Found !!!"}})
            if not user.first().password:
                return Response({"success": {"Info": "Exist in Database !!!", "user": {
                         "username": user.first().username, "role": user.first().role, "id": user.first().id, "is_active": user.first().is_active, 
                         "created_at": user.first().created_at, "last_login": user.first().last_login
                        }
                    }})
            if user.first().password:
                return Response({"success": {"Info": "Exist in Database !!!" }})
            
        user = authenticate(
            username=valid_request.validated_data["username"],
            password=valid_request.validated_data.get("password", None)
        )

        if not user:
            return Response( {"error": "Invalid Username or Password"}, )
        access = get_access_token({"user_id": user.id}, 1)
        user.last_login = datetime.now()
        user.save()

        response = Response()
        response.set_cookie(key="jwt", value=access, httponly=True)
        response.data = {"success": 
                         {"jwt": access, 
                         "username": user.username, 
                         "role": user.role, 
                         "id": user.id, 
                         "is_active": user.is_active,
                         "created_at": user.created_at,
                         "last_login": user.last_login}
                         }
        add_user_activity(user, "logged in")
        return response
    

class LogoutView(ModelViewSet):
    http_method_names = ["post"]
    serializer_class = LogoutSerialiser

    def create(self, request):
        valid_request = self.serializer_class(data=request.data)
        if not valid_request.is_valid():
            raise Exception(valid_request.errors)
        response = Response()
        response.delete_cookie('jwt')
        response.data = { "message": "success" }
        try:
            user = CustomUser.objects.get(id = valid_request.validated_data["user_id"]),
            return response
        except:
            raise Exception("User ID Not Found")


class CreatePasswordView(ModelViewSet):
    serializer_class = CreatePasswordUserSerializer
    http_method_names = ["post"]
    queryset = CustomUser.objects.all()

    def create(self, request):
        valid_request = self.serializer_class(data=request.data["payload"])
        if not valid_request.is_valid():
            raise Exception(valid_request.errors)

        user = CustomUser.objects.filter(
            id=valid_request.validated_data["user_id"])

        if not user:
            raise Exception("User with Id not Found")

        user = user[0]

        user.set_password(valid_request.validated_data["password"])
        user.save()

        add_user_activity(user, "updated password")

        return Response({"success": "User Password Updated"})


class MeView(ModelViewSet):
    serializer_class = CustomUserSerializer
    http_method_names = ["get"]
    queryset = CustomUser.objects.all()
    permission_classes = (IsAuthenticatedCustom, )

    def list(self, request):
        data1 = CustomUser.objects.get(id=request.user.id)
        user = {
            "id": data1.id,
            "username": data1.username,
            "last_login": data1.last_login,
            "created_at": data1.created_at,
            "role": data1.role,
            "email": data1.email,
        }
        return Response(user)


class UserActivitiesView(ModelViewSet):
    serializer_class = UserActivitiesSerializer
    http_method_names = ["get"]
    queryset = UserActivities.objects.all()
    permission_classes = (IsAuthenticatedCustom, )
    pagination_class = CustomPagination

    class Meta:
        ordering = ("-created_at", )          
    

class UsersView(ModelViewSet):
    serializer_class = GetUserSerializer
    http_method_names = ["get"]
    pagination_class = CustomPagination       # This limits to 100
    queryset = CustomUser.objects.all()


class UserProfilesView(ModelViewSet):
    http_method_names = ["get", "post", "put", "delete"]
    queryset = UserProfile.objects.all().order_by("-created_at")
    serializer_class = UserProfileSerializer
    pagination_class = CustomPagination       # This limits to 100
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def get_queryset(self):
        if self.request.method.lower() != "get":
            return self.queryset
        data = self.request.query_params.dict()
        data.pop("page", None)
        keyword = data.pop("keyword", None)
        results = self.queryset#.filter(**data)

        if keyword:
            search_fields = ("")
            query = get_query(keyword, search_fields)
            results = results.filter(query)
        return results        
    
    def update(self, request, *args, **kwargs):
        perm_check = "user_control.change_userprofile"        
        check_permission(request.data["payload"]["updated_by_id"], perm_check)
        data = request.data["payload"]
        object = self.get_object()
        serializer = self.serializer_class(data=data, instance=object)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": serializer.data}) 
        raise Exception(serializer.errors)
    
    def destroy(self, request, *args, **kwargs):
        perm_check = "user_control.delete_userprofile"
        check_permission(request.data["payload"]["deleted_by_id"], perm_check)
        if (request.data["payload"]["deleted_by_id"] < 1):
            raise Exception("User Not Loggin")  
        object = self.get_object()
        try:
            object.delete()
            return Response({"success": "Deleted" })            
        except:
            return Response({"errors": "Error" }) 


class AssignGroupsToUserView(ModelViewSet):
    http_method_names = ["put"]
    queryset = CustomUser.objects.all()
    serializer_class = AssignGroupsToUserSerializer

    def update(self, request, pk=None):
        data = request.data["payload"]
        object = self.get_object()
        perm_check = "auth.change_group"
        check_permission(request.data["payload"]["created_by_id"], perm_check)
        serializer = self.serializer_class(data=data, instance=object)
        # raise Exception(data)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": serializer.data}) 
        raise Exception(serializer.errors)
        return Response({"errors": serializer.errors }) 
    

class AssignPermissionsGroupView(ModelViewSet):
    http_method_names = ["put"]
    queryset = Group.objects.all()
    serializer_class = AssignPermissionsToGroupSerializer

    def update(self, request, pk=None):
        perm_check = "auth.change_permission"        
        check_permission(request.data["payload"]["created_by_id"], perm_check)
        data = request.data["payload"]
        object = self.get_object()
        serializer = self.serializer_class(data=data, instance=object)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": serializer.data}) 
        raise Exception(serializer.errors)
        return Response({"errors": serializer.errors }) 
    

class CompanyProfileView(ModelViewSet):
    http_method_names = ["get", "post", "put", "delete"]
    queryset = CompanyProfile.objects.all().order_by("-created_at")
    serializer_class = CompanyProfileSerializer
    pagination_class = CustomPagination       # This limits to 100
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def get_queryset(self):
        if self.request.method.lower() != "get":
            return self.queryset
        data = self.request.query_params.dict()
        data.pop("page", None)
        keyword = data.pop("keyword", None)
        results = self.queryset#.filter(**data)

        if keyword:
            search_fields = ("")
            query = get_query(keyword, search_fields)
            results = results.filter(query)
        return results       

    def create(self, request):
        perm_check = "user_control.add_companyprofile"
        check_permission(request.data["payload"]["created_by_id"], perm_check)
        serializer = self.serializer_class(data=request.data["payload"]) 
        if serializer.is_valid():
            serializer.save()
            return Response({"success": serializer.data}) 
        raise Exception(serializer.errors)
    
    def update(self, request, *args, **kwargs):
        perm_check = "user_control.change_companyprofile"        
        check_permission(request.data["payload"]["updated_by_id"], perm_check)
        data = request.data["payload"]
        object = self.get_object()
        serializer = self.serializer_class(data=data, instance=object)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": serializer.data}) 
        raise Exception(serializer.errors)
    
    def destroy(self, request, *args, **kwargs):
        perm_check = "user_control.delete_userprofile"
        check_permission(request.data["payload"]["deleted_by_id"], perm_check)
        if (request.data["payload"]["deleted_by_id"] < 1):
            raise Exception("User Not Loggin")  
        object = self.get_object()
        try:
            object.delete()
            return Response({"success": "Deleted" })            
        except:
            return Response({"errors": "Error" }) 
