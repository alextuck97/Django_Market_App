from rest_framework import serializers
from .models import Stocks, PortfolioHistory

'''
Set of model serializers for the api
'''

class StocksSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Stocks
        fields = ['owner', "symbol", "quantity", "date_last_modified"]#"__all__"


class HistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PortfolioHistory
        fields = ['owner', 'stock_assets', 'cash_assets', 'date']