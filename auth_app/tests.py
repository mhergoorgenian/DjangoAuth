from django.test import TestCase
from rest_framework.reverse import reverse
from rest_framework import status
from rest_framework.test import APITestCase
import json



class AuthTest(APITestCase):
    def test_auth(self):

        #register
        data = {"username": "test1", "password": "test1"}
        url = reverse('register_user')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        res_data = response.json()
        self.assertIn('data', res_data)


        #login
        data = {"username": "test1", "password": "test1"}
        url = reverse('login_user')
        response=self.client.post(url,data,fromat='json')
        res_data = response.json()
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        token=res_data['token']
        print(token)


        #checkUser
        url = reverse('get_users')
        response = self.client.get(url, HTTP_AUTHORIZATION='Token '+token)
        print(response)
        res_data = json.loads(response.content)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        print(res_data)

