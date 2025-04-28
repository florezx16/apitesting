from django.shortcuts import HttpResponse
from django.http import JsonResponse
from .models import DamagedSystem
from .utils import createRequestLog, getCodeByLog, specific_volume_liquid, specific_volume_vapor

from rest_framework.views import APIView
from rest_framework import generics ,status
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

import random

# Create your views here.
class GetStatus(generics.RetrieveAPIView):
    queryset = DamagedSystem.objects.all()
    serializer_class = None
    
    def get_object(self):
        query_set = self.get_queryset()
        random_system = random.choice(query_set)
        return random_system
    
    @swagger_auto_schema(
        operation_id='get',
        operation_summary='Get random damaged  system.',
        operation_description=('Will return a random damaged system, also return an ID if you want to get your specific result.'),
        tags=['AltScore'],
    )
    def get(self, request, *args, **kwargs):
        systemInstance = self.get_object() #Instance from model
        log = createRequestLog(systemInstance)
        return JsonResponse(
            {
                'damaged_system':systemInstance.name,
                'log_id':str(log.id)
            }
        )
    
class GetRepairBay(APIView):    
    @swagger_auto_schema(
        operation_id='get',
        operation_summary='HTML page.',
        operation_description=('Return HTML page based on the damaged system, you can also add your log_id to get your specific result'),
        tags=['AltScore'],
        manual_parameters=[
            openapi.Parameter(
                'log_id', openapi.IN_QUERY, 
                description="Get your specific record(exact match).", 
                type=openapi.TYPE_STRING
            )
        ],
    )
    
    def get(self, request):
        query_params = self.request.query_params
        code = getCodeByLog(query_params.get('log_id',None))
        html_response = f'''
        <!DOCTYPE html>
        <html>
            <head>
                <title>Repair</title>
            </head>
            <body>
                <div class="anchor-point">{code}</div>
            </body>
        </html>
        '''
        return HttpResponse(html_response)
    
class SendTeapot(APIView):
    @swagger_auto_schema(
        operation_id="I'm TEAPOT",
        operation_summary='HTTP status code response.',
        operation_description=('Return HTTP status code(418)'),
        tags=['AltScore']
    )
    def post(self, request):
        return Response(status=status.HTTP_418_IM_A_TEAPOT)  
    
class PhaseChange_diagram(APIView):
    @swagger_auto_schema(
        operation_id="phase-change-diagram",
        operation_summary='Returns liquid & vapor based on different formulas.',
        operation_description=('Return specific values based on formulas and values that only work for the specific situation and diagram found.'),
        tags=['AltScore'],
        manual_parameters=[
            openapi.Parameter(
                'pressure', openapi.IN_QUERY, 
                description="Based pressure to use in calculations.", 
                type=openapi.TYPE_INTEGER
            )
        ]
    )
    def get(self, request):
        query_params = self.request.query_params
        pressure = float(query_params.get('pressure',0))
        liquid = specific_volume_liquid(pressure)
        vapor = specific_volume_vapor(pressure)
        return Response(
            data={
                'specific_volume_liquid':liquid,
                'specific_volume_vapor':vapor
            },
            status=status.HTTP_200_OK
        )