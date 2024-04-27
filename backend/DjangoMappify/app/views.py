from .models import *
from .serializers import *
from rest_framework.viewsets import ModelViewSet
from .models import Employee
from rest_framework import permissions as perm
from .serializers import EmployeeSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action

# Create your views here.

class EmployeeView(ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


    # @action(detail=False,methods=['GET'],permission_classes=[perm.AllowAny])
    # def get_one_user(self, request):
    #     id = request.GET.get('id')
    #     if not id:
    #         return Response('Bed Request no id ', status=status.HTTP_400_BAD_REQUEST)
    #     employee = Employee.objects.get(id:id)

    #     return Response(employee, status=status.HTTP_200_OK)


    



