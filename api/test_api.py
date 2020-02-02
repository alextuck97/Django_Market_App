from .models import PortfolioHistory, Stocks, User
from django.test import Client, TestCase
from rest_auth.urls import LoginView
import json


class PortfolioModificationTest(TestCase):
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
        

    def test_get_portfolio(self):
        '''
        What happens with no users? How would this situation happen where a client
        has their key but the account no longer exists?
        '''
        url = "/api/account-summary/"
        response = self.client.get(url, content_type="application/json", HTTP_AUTHORIZATION=self.token)
        content = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(content['username'], "test_user")
        self.assertEqual(len(content['portfolio']), 2)


    def test_buy(self):
        # All stocks are assumed to cost $55. Why? Cause thats how it is.
        # Expected usage of buying
        url = "/api/transaction/"
       
        data = {
            "symbol": "MSFT",
            "quantity": 3
        }

        response = self.client.post(url, data=data, \
            content_type="application/json", HTTP_AUTHORIZATION=self.token)
        content = json.loads(response.content)
       
        self.assertEqual(response.status_code, 200)
        self.assertEqual(content['num_purchased'], 3)
        self.assertEqual(content['symbol'], 'MSFT')
        self.assertEqual(content['current_balance'], 10000 - 55 * 3)

        # Buying 0 entries
        data = {
            "symbol": "MSFT",
            "quantity": 0
        }

        response = self.client.post(url, data=data, \
            content_type="application/json", HTTP_AUTHORIZATION=self.token)
        content = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertTrue("Invalid request" in content)

        # Buying too much
        data = {
            "symbol": "MSFT",
            "quantity": 10000
        }

        response = self.client.post(url, data=data, \
            content_type="application/json", HTTP_AUTHORIZATION=self.token)
        content = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertTrue("Invalid request" in content)

    def test_sell(self):
        # Selling things you dont own
        url = "/api/transaction/"
        
        data = {
            "symbol": "MSFT",
            "quantity": 3
        }

        response = self.client.delete(url, data=data,\
            content_type="application/json", HTTP_AUTHORIZATION=self.token)
        content = json.loads(response.content)
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue("Invalid request" in content)

        # Selling negative things 
        data = {
            "symbol": "SFWY",
            "quantity": -3
        }

        response = self.client.delete(url, data=data,\
            content_type="application/json", HTTP_AUTHORIZATION=self.token)
        content = json.loads(response.content)
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue("Invalid request" in content)

        # Expected selling
        data = {
            "symbol": "AAPL",
            "quantity": 3
        }

        response = self.client.delete(url, data=data,\
            content_type="application/json", HTTP_AUTHORIZATION=self.token)
        content = json.loads(response.content)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(content['num_sold'], 3)
        self.assertEqual(content['num_owned'], 1)
        self.assertEqual(content['current_balance'], 10000 + 55 * 3)


