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
from django.utils import timezone
# Create your views here.

class AccountInformation(APIView):

    parser_classes = [JSONParser]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        token = request.headers['Authorization'].split(" ")[1]
        user = Token.objects.filter(key=token)[0]
        
        owner = user.user

        portfolio = Stocks.objects.filter(owner__username=owner.username). \
            order_by("symbol")
        serializer = StocksSerializer(portfolio, many=True)

        response_data = {
            "username": owner.username,
            "email": owner.email,
            "blance": owner.balance,
            "portfolio": serializer.data
        }

        return Response(response_data)


class AccountTransactions(APIView):
    
    parser_classes = [JSONParser]
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        '''
        A user requested to purchase a stock.
        Modify there account if the purchase can be made.
        {
            "symbol": str_symbol,
            "quantity": int_quantity
        }
        '''
        token = request.headers['Authorization'].split(" ")[1]
        user = Token.objects.filter(key=token)[0]
        
        owner = user.user
        symbol = request.data['symbol']
        quantity = request.data['quantity']
        price = 55.0 #query_price(symbol)

        if quantity <= 0:
            response_data = {
                "Invalid request": f"Cannot purchase {quantity} stocks"
            }

        elif price * quantity <= owner.balance:
            try:
                stock_entry = Stocks.objects.filter(owner=owner, symbol=symbol)[0]
                stock_entry.quantity += quantity
                stock_entry.date_last_modified = timezone.now()
                stock_entry.save()
                
                
            except IndexError as ie:
                stock_entry = Stocks(owner=owner, symbol=symbol, quantity=quantity)
                stock_entry.save()
            
            owner.balance -= price * quantity
            owner.save()
            response_data = {
                    "symbol": symbol,
                    "purchase_cost": quantity * price,
                    "num_owned": stock_entry.quantity,
                    "num_purchased": quantity,
                    "current_balance": owner.balance
                }
        else:
            response_data = {"Invalid request": "User does not have sufficient funds for purchase"}

        return Response(response_data)


    def delete(self, request):
        '''
        Sell stocks if the user owns them. Update the user's balance
        with the current market price.
        {
            "symbol": str_symbol,
            "quantity": int_quantity
        }
        '''
        token = request.headers['Authorization'].split(" ")[1]
        user = Token.objects.filter(key=token)[0]
        
        owner = user.user
        symbol = request.data['symbol']
        quantity = request.data['quantity']

        price = 55.0 #query_price(symbol)

        
        if quantity <= 0:
            response_data = {"Invalid request": f"Cannot sell {quantity} stocks"}
        else:
            try:
                stock_entry = Stocks.objects.filter(owner=owner, symbol=symbol)[0]
                
                if stock_entry.quantity - quantity < 0:
                    raise ValueError
                elif stock_entry.quantity - quantity == 0:
                    stock_entry.delete()
                    num_owned = 0
                else:
                    stock_entry.quantity -= quantity
                    num_owned = stock_entry.quantity
                    stock_entry.date_last_modified = timezone.now()
                    stock_entry.save()
                owner.balance += price * quantity
                owner.save()
                response_data = {
                    "symbol": symbol,
                    "sell_price": quantity * price,
                    "num_owned": num_owned,
                    "num_sold": quantity,
                    "current_balance": owner.balance
                }

            except IndexError as ie:
                response_data = {"Invalid request": f"User does not own {symbol}"}
            except ValueError as ve:
                response_data = {"Invalid request": f"User does not have {quantity} {symbol} to sell"}
        
        return Response(response_data)



