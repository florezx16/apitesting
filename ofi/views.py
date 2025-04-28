from .models import Client
from .serializer import ClientMainSerializer
from rest_framework import generics
from rest_framework.response import Response

from drf_yasg.utils import swagger_auto_schema

# Create your views here.
class ClientRetrieveView(generics.RetrieveAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientMainSerializer
    
    @swagger_auto_schema(
        operation_id='get_one',
        operation_summary="Get client",
        operation_description="Get one record",
        tags=["Ofi"]
    )
    def get(self, request, *args, **kwargs):
        data_serializable = self.serializer_class(object).data
        return Response({'result':True,'Clients':data_serializable})
    
class ClientCheck(generics.CreateAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientMainSerializer
    
    @swagger_auto_schema(
        operation_id='create',
        operation_summary="Client background check",
        operation_description="Run all",
        tags=["Ofi"]
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'result':'success'}, status=status.HTTP_201_CREATED)
        return Response({'result':'failure','errors':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
