from .models import Stocks, User
from django.test import Client, TestCase
from rest_auth.urls import LoginView
from .industry_lists import industry_defaults
import json


class WatchModificationTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="test_user", password="testing123")
        
        s1 = Stocks(owner=self.user, symbol="AAPL")
        s2 = Stocks(owner=self.user, symbol="SFWY")
        s1.save()
        s2.save()

        data = {
            "username": "test_user",
            "password": "testing123"
        }
        response = self.client.post("/api/token-auth/", data=data, content_type="application/json")
        
        self.token = "JWT " + json.loads(response.content)['token']
        

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


    def test_watch(self):
        
        # Expected usage of watching
        url = "/api/watch/"
       
        data = {
            "symbol": "MSFT"
        }

        response = self.client.post(url, data=data, \
            content_type="application/json", HTTP_AUTHORIZATION=self.token)
        content = json.loads(response.content)
       
        self.assertEqual(response.status_code, 200)
        self.assertEqual(content['symbol'], 'MSFT')
        self.assertEqual(content['alert'], 'success')

        # Watch a watched stock
        data = {
            "symbol": "MSFT"
        }

        response = self.client.post(url, data=data, \
            content_type="application/json", HTTP_AUTHORIZATION=self.token)
        content = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(content["alert"], 'failure')


    def test_unwatch(self):
        # Unwatching things you dont watch
        url = "/api/watch/"
        
        data = {
            "symbol": "MSFT"
        }

        response = self.client.delete(url, data=data,\
            content_type="application/json", HTTP_AUTHORIZATION=self.token)
        content = json.loads(response.content)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(content["alert"], 'failure')

        # Expected use 
        data = {
            "symbol": "AAPL"
        }

        response = self.client.delete(url, data=data,\
            content_type="application/json", HTTP_AUTHORIZATION=self.token)
        content = json.loads(response.content)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(content["alert"], 'success')


class RequestIndustryTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="test_user", password="testing123")
        
        data = {
            "username": "test_user",
            "password": "testing123"
        }
        response = self.client.post("/api/token-auth/", data=data, content_type="application/json")
        
        self.token = "JWT " + json.loads(response.content)['token']

    def test_get_industry(self):

        url = "/api/request-industry/"

        # Expected usage
        response = self.client.get(url + "real_estate/",\
            content_type="application/json", HTTP_AUTHORIZATION=self.token)
        content = json.loads(response.content)

        self.assertListEqual(content["defaults"], industry_defaults["real_estate"])

        # Bad key
        response = self.client.get(url+ "nor_good/",\
            content_type="application/json", HTTP_AUTHORIZATION=self.token)
        content = json.loads(response.content)

        self.assertListEqual(content["defaults"], industry_defaults["technology"])


