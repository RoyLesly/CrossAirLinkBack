from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from BackCrossAirLink.utils import get_query, CustomPagination
from .serializers import (
    BundleSerializer, TransactionsSerializer, CustomerSerializer,
    Bundle, Transactions, Customer
)
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from user_control.models import check_permission
from django.core.exceptions import ValidationError
from django.db import IntegrityError


class CustomerCRUDView(ModelViewSet):
    http_method_names = ["get", "post", "put", "delete"]
    queryset = Customer.objects.all().order_by("-created_by")
    serializer_class = CustomerSerializer
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
    
    def create(self, request, *args, **kwargs):
        print("HERE")
        data = request.data["payload"]
        if (data["created_by_id"] < 1):
            raise Exception("User Not Login")
        print(data)
        perm_check = "billing.add_customer"
        check_permission(request.data["payload"]["created_by_id"], perm_check)
        serializer = self.serializer_class(data=data) 
        print("here")
        if serializer.is_valid():
            print(request.data["payload"])
            serializer.save()
            return Response({"success": serializer.data })  
        print(serializer.errors)
        return Response({"error": serializer.errors })  
    
    def update(self, request, *args, **kwargs):
        perm_check = "billing.change_customer"
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
        perm_check = "billing.delete_customer"
        check_permission(request.data["payload"]["deleted_by_id"], perm_check)
        if (request.data["payload"]["deleted_by_id"] < 1):
            raise Exception("User Not Loggin")  
        object = self.get_object()
        try:
            object.delete()
            return Response({"success": "Deleted" })            
        except:
            return Response({"errors": "Error" }) 
        
    
class BundleView(ModelViewSet):
    http_method_names = ["get", "post", "put", "delete"]
    queryset = Bundle.objects.all().order_by("bundle_name")
    serializer_class = BundleSerializer
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
    
    def create(self, request, *args, **kwargs):
        
        data = request.data["payload"]
        if (data["created_by_id"] < 0):
            raise Exception("User Not Login") 
        perm_check = "billing.add_bundle"
        check_permission(request.data["payload"]["created_by_id"], perm_check)
        serializer = self.serializer_class(data=data) 
        if serializer.is_valid():
            try:
                serializer.save()
                return Response({"success": serializer.data })  
            except Exception as e:
                return Response({"error": str(e) })  
        return Response({"error": serializer.errors })  
    
    def update(self, request, *args, **kwargs):
        perm_check = "billing.change_bundle"
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
        perm_check = "billing.delete_bundle"
        check_permission(request.data["payload"]["deleted_by_id"], perm_check)
        if (request.data["payload"]["deleted_by_id"] < 1):
            raise Exception("User Not Loggin")  
        object = self.get_object()
        try:
            object.delete()
            return Response({"success": "Deleted" })            
        except:
            return Response({"errors": "Error" }) 


class CRUDTransactions(ModelViewSet):
    http_method_names = ["get", "post", "put", "delete"]
    queryset = Transactions.objects.all().order_by("-created_at")
    serializer_class = TransactionsSerializer
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
    
    def create(self, request, *args, **kwargs):
        data = request.data["payload"]
        if (data["created_by_id"] == 0):
            return Response({"login": "Not Logged IN ..." })  
        perm_check = "billing.add_transactions"
        check_permission(request.data["payload"]["created_by_id"], perm_check)
        serializer = self.serializer_class(data=data) 
        if serializer.is_valid():
            serializer.save()
            return Response({"success": "SUCCESS" })  
        return Response({"error": serializer.errors })  
    
    def update(self, request, *args, **kwargs):
        perm_check = "billing.change_transactions"
        check_permission(request.data["payload"]["updated_by_id"], perm_check)
        if (request.data["payload"]["updated_by_id"] < 1):
            raise Exception("User Not Loggin")  
        object = self.get_object()
        serializer = self.serializer_class(data=request.data["payload"], instance=object)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": serializer.data })  
        return Response({"error": serializer.errors })      

    def destroy(self, request, *args, **kwargs):
        perm_check = "billing.delete_transactions"
        check_permission(request.data["payload"]["deleted_by_id"], perm_check)
        if (request.data["payload"]["deleted_by_id"] < 1):
            raise Exception("User Not Loggin")  
        object = self.get_object()
        try:
            object.delete()
            return Response({"success": "Deleted" })            
        except:
            return Response({"errors": "Error" })  