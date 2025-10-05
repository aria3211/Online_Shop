from api.models import Order, User,Product,Category
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.db.models import Count

class ProductAPITestCase(APITestCase):
    def setUp(self):
        self.admin_user = User.objects.create_superuser(username='admin',password='admin')
        self.normal_user = User.objects.create_user(username='user2',password='1234')

        self.product = Product.objects.create(
            name='new product',
            description="Test Description",
            price=9.99,
            stock=10
        )
        self.url = reverse('product_detail',kwargs={'product_id':self.product.pk})


    def test_get_product(self):
        responce = self.client.get(self.url)
        self.assertEqual(responce.status_code,status.HTTP_200_OK)
        self.assertEqual(responce.data['stock'],self.product.stock)

    def test_unauthroized_update_product(self):
        data = {'name':'mobile'}
        responce = self.client.put(self.url,data)
        self.assertEqual(responce.status_code,status.HTTP_401_UNAUTHORIZED)

    def test_unauthroized_delete_product(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)

    def test_only_admin_can_delete_product(self):
        # test for normal users can not delete 
        self.client.login(username='user2',password='1234')
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)
        # check product wouildn't delete
        self.assertTrue(Product.objects.filter(pk=self.product.pk).exists())



        # test for admin user can delete
        self.client.login(username='admin',password='admin')
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code,status.HTTP_204_NO_CONTENT)
        self.assertFalse(Product.objects.filter(pk=self.product.pk).exists())



class CategoryTestCase(APITestCase):
    def setup(self):
        self.admin_user = User.objects.create_superuser(username='admin',password='admin')
        self.normal_user = User.objects.create_user(username='user2',password='1234')

        self.category = Category.objects.create(
            name = 'test',
            description = 'test description'
        )
        self.product = Product.objects.create(
            name='new product',
            description="Test Description",
            price=9.99,
            stock=10
        )

        self.url = reverse('categories')

    def test_all_users_seen(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code,status.HTTP_200_OK)
    
    def test_count_product_for_each_category(self):
        self.category = Category.objects.annotate(self.product)

        

