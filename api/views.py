from django.shortcuts import render
from .models import Stocks, PortfolioHistory
from .serializers import HistorySerializer, StocksSerializer
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.http.request import HttpRequest
from rest_framework.authtoken.models import Token
# Create your views here.


class RESTAccountPortfolio(APIView):
    
    parser_classes = [JSONParser]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):                   
        '''
        Return a user's portfolio.
        Authentication token required.
        '''
        portfolio = Stocks.objects.filter(owner__username=request.data['owner']). \
            order_by("symbol")
        serializer = StocksSerializer(portfolio, many=True)
        return Response(serializer.data)

    def post(self, request):
        '''
        A user requested to purchase a stock.
        Modify there account if the purchase can be made.
        '''
        token = request.headers['Authorization'].split(" ")[1]
        owner = Token.objects.filter(key=token)[0].user
        
        symbol = request.data['symbol']
        quantity = request.data['quantity']
        return Response({"owner": owner})


    def delete(self, request):
        pass





