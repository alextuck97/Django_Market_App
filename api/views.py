from django.shortcuts import render
from .models import Stocks
from .serializers import StocksSerializer, UserSerializer, UserSerializerWithToken
from django.contrib.auth.models import User
from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

#from rest_framework.authtoken.models import Token
from django.utils import timezone
import base64
import json
# Create your views here.

class CurrentUser(APIView):

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class CreateUser(APIView):

    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = UserSerializerWithToken(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AccountInformation(APIView):

    parser_classes = [JSONParser]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        token = request.headers['Authorization'].split(" ")[1]
        payload = get_payload(token)
        username = payload["username"]
        user = User.objects.filter(username=username)[0]
        
        portfolio = Stocks.objects.filter(owner=user). \
            order_by("symbol")
        serializer = StocksSerializer(portfolio, many=True)

        response_data = {
            "username": user.username,
            "portfolio": serializer.data
        }

        return Response(response_data)


class ModifyWatchList(APIView):
    
    parser_classes = [JSONParser]
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        '''
        A user requested to purchase a stock.
        Modify there account if the purchase can be made.
        {
            "symbol": str_symbol
        }
        '''
        token_header = request.headers['Authorization'].split(" ")[1]
        payload = get_payload(token_header)
        user = User.objects.filter(username=payload['username'])[0]
        
        symbol = request.data['symbol']

        # If an index error is raised then the user is not watching the stock.
        # Yea I know its convoluted.
        try:
            stock_entry = Stocks.objects.filter(owner=user, symbol=symbol)[0]
            response_data = {
                "symbol" : symbol,
                "alert" : "failure",
                "message" : "Already watching symbol"
            }
            
        except IndexError as ie:
            stock = Stocks(owner=user, symbol=symbol)    
            stock.save()
            response_data = {
                "symbol" : symbol,
                "alert" : "success",
                "message" : "Added to watch list"
            }
                
        return Response(response_data)


    def delete(self, request):
        '''
        Sell stocks if the user owns them. Update the user's balance
        with the current market price.
        {
            "symbol": str_symbol
        }
        '''
        token = request.headers['Authorization'].split(" ")[1]
        
        payload = get_payload(token)
        username = payload["username"]
        user = User.objects.filter(username=username)[0]
        symbol = request.data['symbol']
        
        # If the user is not watching the stock raise an IndexError.
        # Else remove the stock.
        try:
            stock_entry = Stocks.objects.filter(owner=user, symbol=symbol)[0]

            stock_entry.delete()            
            response_data = {
                "symbol": symbol,
                "alert": "success",
                "message": "Symbol removed from watch list"   
            }
        except IndexError as ie:
            response_data = {
                "symbol": symbol,
                "alert": "failure",
                "message": "User was not watching symbol"  
            }
           
        
        return Response(response_data)



def get_payload(token):
    """
    Extract the payload from a JWT token
    """
    payload = token.split(".")[1]

    if len(payload) % 4:
        payload += "=" * (4 - len(payload) % 4)
    
    payload = base64.b64decode(payload)
    payload = json.loads(payload)
    return payload