from django.shortcuts import render
from django.db.models import Q

from rest_framework import generics ,status
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, ValidationError

from .models import Book
from .serializers import BookSerializer ,BookQuerySerializer
from core.utils import PrepareFilters
from .utils import codeMapping, translate2isbn, sanitizedParams

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# Create your views here.
class BookListCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    @swagger_auto_schema(
        operation_id='create',
        operation_summary="Create brand new book",
        operation_description="Add brand new book into DB",
        tags=["Books"]
    )
    def post(self, request, *args, **kwargs):
        is_many = isinstance(request.data,list)
        if is_many:
            success = 0
            fail = 0
            errors = []
            for i,v in enumerate(request.data):
                serializer = self.get_serializer(data=v)
                if serializer.is_valid():
                    serializer.save()
                    success+=1
                else:
                    fail+=1
                    errors.append({
                        'index':i,
                        'error_details':serializer.errors
                    })
            
            #Define result_code
            result_code = codeMapping(success,fail,len(request.data))
            return Response(
                {
                    'result':result_code,
                    'is_many':is_many,
                    'request_total':len(request.data),
                    'request_success':success,
                    'request_fail':fail,     
                    'errors':errors            
                },
                status=status.HTTP_200_OK
            )
        else:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'result':'success'}, status=status.HTTP_201_CREATED)
            return Response({'result':'failure','errors':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
            
    
class BookRetrieveView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    @swagger_auto_schema(
        operation_id='get_one',
        operation_summary="Get book",
        operation_description="Get one single record from the DB based on the book ISBN number",
        tags=["Books"]
    )
    def get(self, request, *args, **kwargs):
        object = translate2isbn(self.kwargs)
        data_serializable = self.serializer_class(object).data
        return Response({'result':True,'Book':data_serializable})

class BookListView(generics.ListAPIView):
    serializer_class = BookQuerySerializer
    
    def get_queryset(self):
        queryset = Book.objects.filter(status=1)
        queryParams = self.request.query_params
        serializer = self.get_serializer_class()
        newQueryParams = sanitizedParams(queryParams,serializer)
        
        #No set coincidence
        if not newQueryParams:
            return queryset
        
        #Use sanitized query parameters to init serilizer
        serialize_data = serializer(data=newQueryParams)
        if serialize_data.is_valid(raise_exception=True):
            filters_dict = {
                'isbn':'exact',
                'title':'icontains',
                'author':'icontains',
                'genre':'exact'
            }
            query_filters = PrepareFilters(serialize_data.validated_data,filters_dict)
            queryset = Book.objects.filter(query_filters)
        
        #Return query set 
        return queryset
            
    @swagger_auto_schema(
        operation_id='list',
        operation_summary='Get all instances.',
        operation_description=(
            'Return all the enable instances that match with the filters. '
            'You can filter by `ISBN`, `title`, `author`, or `genre` using query parameters.'
        ),
        tags=['Books'],
        manual_parameters=[
            openapi.Parameter(
                'isbn', openapi.IN_QUERY, 
                description="Filter books by ISBN number (exact match).", 
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'title', openapi.IN_QUERY, 
                description="Filter books by title (case insensitive).", 
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'author', openapi.IN_QUERY, 
                description="Filter books by author (case insensitive).", 
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'genre', openapi.IN_QUERY, 
                description= f'Filter books by genre (exact match) - Posibble options: {Book.BookGenres.choices}.', 
                type=openapi.TYPE_INTEGER
            ),
        ],
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    
class BookUpdateView(generics.UpdateAPIView):
    queryset = Book.objects.filter(status=1)
    serializer_class = BookSerializer
    
    def get_object(self):
        return translate2isbn(self.kwargs)

    @swagger_auto_schema(
        operation_id='entire_update',
        operation_summary="Book full update",
        operation_description="Required the entire body request to update",
        tags=["Books"]
    )
    def put(self, request, *args, **kwargs):
        object2update = self.get_object()
        params2update = self.request.data
        serializer = self.get_serializer_class()
        paramsSanitized = sanitizedParams(params2update,serializer)
        
        #No set coincidence
        if not paramsSanitized:
            return Response({'result':False,'details':'Not valid parameters has been found on your request.'})
        
        serialize_data = serializer(object2update,data=paramsSanitized)
        if serialize_data.is_valid():
            serialize_data.save()
            return Response({'result':True,'body':serialize_data.data}, status=status.HTTP_200_OK)
        return Response({'result':False,'errors':serialize_data.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(
        operation_id='partial_update',
        operation_summary="Book partial update",
        operation_description="Requiere at least one attribute from the model to update.",
        tags=["Books"]
    )
    def patch(self, request, *args, **kwargs):
        object2update = self.get_object()
        params2update = self.request.data
        
        serializer = self.get_serializer_class()
        paramsSanitized = sanitizedParams(params2update,serializer)
        
        #No set coincidence
        if not paramsSanitized:
            return Response({'result':False,'details':'Not valid parameters has been found on your request.'})
        
        #Use sanitized query parameters to init serilizer
        serialize_data = serializer(object2update,data=paramsSanitized,partial=True)
        if serialize_data.is_valid():
            serialize_data.save()
            return Response({'result':True,'body':serialize_data.data}, status=status.HTTP_200_OK)
        return Response({'result':False,'errors':serialize_data.errors}, status=status.HTTP_400_BAD_REQUEST)
    
class BookDeleteView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    def get_object(self):
        return translate2isbn(self.kwargs)
    
    @swagger_auto_schema(
        operation_id='delete',
        operation_summary='Book delete',
        operation_description='Delete disabled books only.',
        tags=['Books']
    ) 
    def delete(self, request, *args, **kwargs):
        object2delete = self.get_object()
        if object2delete.status == 0:
            object2delete.delete()
            return Response({'result':True},status=status.HTTP_200_OK)
        return Response({'result':False,'errors':{'status':'Only disable records can be delete it.'}}, status=status.HTTP_400_BAD_REQUEST)

