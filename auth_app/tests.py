from django.test import TestCase
from rest_framework.reverse import reverse
from rest_framework import status
from rest_framework.test import APITestCase
import json



class AuthTest(APITestCase):
    def test_auth(self):

        for i in range(0,10):
        #register1
            data = {"username": f"test{i}", "password": f"test{i}"}
            url = reverse('register_user')
            response = self.client.post(url, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            res_data = response.json()
            self.assertIn('data', res_data)

        


        #login
        data = {"username": "test2", "password": "test2"}
        url = reverse('login_user')
        response=self.client.post(url,data,fromat='json')
        res_data = response.json()
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        token=res_data['token']
        print(token)


        #me
        url = reverse('get_mydata')
        print(url)
        response = self.client.get(url, HTTP_AUTHORIZATION='Token ' + token)
        res_data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(res_data)
        
        #search
        search_username = 't'
        offset = 0
        limit = 10
        url = reverse('get_users') + f"?username={search_username}&offset={offset}&limit={limit}"
        print(url)
        response = self.client.get(url, HTTP_AUTHORIZATION='Token ' + token)
        res_data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(res_data)
        
