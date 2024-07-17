from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from core.models import Tweet, User
from django.contrib.auth import get_user_model

class TwitterCloneAPITestCase(TestCase):
    
    def setUp(self):
        self.client = APIClient()
        self.User = get_user_model()
        self.user1 = self.User.objects.create_user(username='user1', password='testpassword')
        self.user2 = self.User.objects.create_user(username='user2', password='testpassword')
        self.client.force_authenticate(user=self.user1) # Força a autenticação

    def test_listagem_de_tweets(self):
        Tweet.objects.create(user=self.user1, content='Tweet de teste 1')
        
        url = reverse('tweets')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Verifica se apenas um tweet foi retornado
        
    def test_criacao_de_tweet(self):
        url = reverse('tweets')
        data = {'content': 'Novo tweet de teste'}
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Tweet.objects.count(), 1)

    def test_login_de_usuario(self):
        url = reverse('token_obtain_pair')
        data = {'username': 'user1', 'password': 'testpassword'}
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_seguir_e_deixar_de_seguir_usuarios(self):
        # Seguir o usuário user2
        url_seguir = reverse('follow_unfollow', kwargs={'pk': self.user2.pk})
        response_seguir = self.client.post(url_seguir)
        
        self.assertEqual(response_seguir.status_code, status.HTTP_200_OK)
        self.assertIn(self.user2, self.user1.following.all())

        # Deixar de seguir o usuário user2
        url_deixar_de_seguir = reverse('follow_unfollow', kwargs={'pk': self.user2.pk})
        response_deixar_de_seguir = self.client.post(url_deixar_de_seguir)
        
        self.assertEqual(response_deixar_de_seguir.status_code, status.HTTP_200_OK)
        self.assertNotIn(self.user2, self.user1.following.all())
