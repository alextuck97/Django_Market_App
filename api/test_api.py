from django.contrib.auth.models import User
from .models import PortfolioHistory, Stocks
from django.test import Client, TestCase
from .views import RESTAccountPortfolio
from rest_auth.urls import LoginView
import json


class StockTransactionTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="test_user", password="testing123")
        
        s1 = Stocks(owner=self.user, symbol="AAPL", quantity=4)
        s2 = Stocks(owner=self.user, symbol="SFWY", quantity=6)
        s1.save()
        s2.save()

        data = {
            "username": "test_user",
            "password": "testing123"
        }
        response = self.client.post("/api/rest-auth/login/", data=data, content_type="application/json")
        
        self.token = "Token " + json.loads(response.content)['key']
        

    def test_buy(self):
        
        # Expected usage of buying
        data = {
            "symbol": "MSFT",
            "quantity": 3
        }

        response = self.client.post("/api/userportfolio/", data=data, \
            content_type="application/json", HTTP_AUTHORIZATION=self.token)
        content = json.loads(response.content)
       
        self.assertEqual(response.status_code, 200)
        self.assertEqual(content['num_purchased'], 3)
        self.assertEqual(content['symbol'], 'MSFT')

        # Buying 0 entries
        data = {
            "symbol": "MSFT",
            "quantity": 0
        }

        response = self.client.post("/api/userportfolio/", data=data, \
            content_type="application/json", HTTP_AUTHORIZATION=self.token)
        content = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertTrue("Invalid request" in content)
    
    def test_sell(self):
        # Selling things you dont own
        data = {
            "symbol": "MSFT",
            "quantity": 3
        }

        response = self.client.delete("/api/userportfolio/", data=data,\
            content_type="application/json", HTTP_AUTHORIZATION=self.token)
        content = json.loads(response.content)
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue("Invalid request" in content)

        # Selling negative things 
        data = {
            "symbol": "SFWY",
            "quantity": -3
        }

        response = self.client.delete("/api/userportfolio/", data=data,\
            content_type="application/json", HTTP_AUTHORIZATION=self.token)
        content = json.loads(response.content)
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue("Invalid request" in content)

        # Expected selling
        data = {
            "symbol": "AAPL",
            "quantity": 3
        }

        response = self.client.delete("/api/userportfolio/", data=data,\
            content_type="application/json", HTTP_AUTHORIZATION=self.token)
        content = json.loads(response.content)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(content['num_sold'], 3)
        self.assertEqual(content['num_owned'], 1)