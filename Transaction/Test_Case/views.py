from decimal import Decimal
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from account.models import User
from Transaction.models import Add_Transaction, Category, Payment, Type


class TypeTests(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(
            email='admin@example.com',
            first_name='M',
            last_name='shahzad',
            gender='M',
            phone_number="09876543211",
            password='admin'
        )
        self.user = User.objects.create_user(email='shahzad@gmail.com',
                                             first_name='M',
                                             last_name='shahzad',
                                             gender='M',
                                             phone_number='09876543211',
                                             password='testpass',
                                             confirm_password='Shahzad123.')
        self.client_admin = APIClient()
        self.client_admin.force_authenticate(user=self.admin)
        self.client_user = APIClient()
        self.client_user.force_authenticate(user=self.user)
        self.type1 = Type.objects.create(add_type='Type 1')
        self.type2 = Type.objects.create(add_type='Type 2')

    def test_admin_get_type_list(self):
        response = self.client_admin.get(reverse('type-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        last_obj = Type.objects.last()
        self.assertEqual('Type 2', last_obj.add_type)

    def test_user_get_type_list(self):
        response = self.client_user.get(reverse('type-list'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_create_new_type(self):
        data = {'add_type': 'Type 3'}
        response = self.client_admin.post(reverse('type-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Type.objects.count(), 3)

    def test_user_create_new_type(self):
        data = {'add_type': 'Type 3'}
        response = self.client_user.post(reverse('type-list'), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Type.objects.count(), 2)

    def test_admin_update_type(self):
        data = {'add_type': 'Updated Type'}
        response = self.client_admin.put(
            reverse('type-detail', args=[self.type1.pk]), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Type.objects.get(pk=self.type1.pk)
                         .add_type, 'Updated Type')

    def test_user_update_type(self):
        data = {'add_type': 'Updated Type'}
        response = self.client_user.put(
            reverse('type-detail', args=[self.type1.pk]), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Type.objects.get(pk=self.type1.pk).add_type, 'Type 1')

    def test_admin_delete_type(self):
        response = self.client_admin.delete(
            reverse('type-detail', args=[self.type1.pk]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Type.objects.count(), 1)

    def test_user_delete_type(self):
        response = self.client_user.delete(
            reverse('type-detail', args=[self.type1.pk]))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Type.objects.count(), 2)


class CategoryTests(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(
            email='admin@example.com',
            first_name='M',
            last_name='shahzad',
            gender='M',
            phone_number="09876543211",
            password='admin'
        )
        self.user = User.objects.create_user(email='shahzad@gmail.com',
                                             first_name='M',
                                             last_name='shahzad',
                                             gender='M',
                                             phone_number='09876543211',
                                             password='testpass',
                                             confirm_password='Shahzad123.')
        self.client_admin = APIClient()
        self.client_admin.force_authenticate(user=self.admin)
        self.client_user = APIClient()
        self.client_user.force_authenticate(user=self.user)
        self.category1 = Category.objects.create(
            new_category='Food',
            icons='/home/shahzad/Documents/clone_Api/media/1674243678808.jpeg',
            color='#FFFFFFFF')
        self.category2 = Category.objects.create(
            new_category='Food',
            icons='/home/shahzad/Documents/clone_Api/media/1674243678808.jpeg',
            color='#FFFFFFFF')

    def test_admin_get_category_list(self):
        response = self.client_admin.get(reverse('category-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_user_get_category_list(self):
        response = self.client_user.get(reverse('category-list'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_create_new_category(self):
        data = {'new_category': 'category 3', 'color': '#FFFFFFFF'}
        response = self.client_admin.post(reverse('category-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.count(), 3)

    def test_user_create_new_category(self):
        data = {'new_category': 'category 3', 'color': '#FFFFFFFF'}
        response = self.client_user.post(reverse('category-list'), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Category.objects.count(), 2)

    def test_admin_update_category(self):
        data = {'new_category': 'Updated Type'}
        response = self.client_admin.put(
            reverse('category-detail', args=[self.category1.pk]), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Category.objects.get(pk=self.category1.pk)
                         .new_category, 'Updated Type')

    def test_user_update_category(self):
        data = {'new_category': 'Updated Type'}
        response = self.client_user.put(
            reverse('category-detail', args=[self.category1.pk]), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_delete_category(self):
        response = self.client_admin.delete(
            reverse('category-detail', args=[self.category1.pk]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Category.objects.count(), 1)

    def test_user_delete_category(self):
        response = self.client_user.delete(
            reverse('category-detail', args=[self.category1.pk]))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Category.objects.count(), 2)


class PaymentTests(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(
            email='admin@example.com',
            first_name='M',
            last_name='shahzad',
            gender='M',
            phone_number="09876543211",
            password='admin'
        )
        self.user = User.objects.create_user(email='shahzad@gmail.com',
                                             first_name='M',
                                             last_name='shahzad',
                                             gender='M',
                                             phone_number='09876543211',
                                             password='testpass',
                                             confirm_password='Shahzad123.')
        self.client_admin = APIClient()
        self.client_admin.force_authenticate(user=self.admin)
        self.client_user = APIClient()
        self.client_user.force_authenticate(user=self.user)
        self.payment1 = Payment.objects.create(payment_method='Payment 1')
        self.payment2 = Payment.objects.create(payment_method='Payment 2')

    def test_admin_get_payment_list(self):
        response = self.client_admin.get(reverse('payments-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_user_get_payment_list(self):
        response = self.client_user.get(reverse('payments-list'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_create_new_payment(self):
        data = {'payment_method': 'Payment 3'}
        response = self.client_admin.post(reverse('payments-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Payment.objects.count(), 3)

    def test_user_create_new_payment(self):
        data = {'payment_method': 'Payment 3'}
        response = self.client_user.post(reverse('payments-list'), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Payment.objects.count(), 2)

    def test_admin_update_payment(self):
        data = {'payment_method': 'Updated Type'}
        response = self.client_admin.put(
            reverse('payments-detail', args=[self.payment1.pk]), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Payment.objects.get(pk=self.payment1.pk)
                         .payment_method, 'Updated Type')

    def test_user_update_payment(self):
        data = {'payment_method': 'Updated Type'}
        response = self.client_user.put(
            reverse('payments-detail', args=[self.payment1.pk]), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_delete_payment(self):
        response = self.client_admin.delete(
            reverse('payments-detail', args=[self.payment1.pk]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Payment.objects.count(), 1)

    def test_user_delete_payment(self):
        response = self.client_user.delete(
            reverse('payments-detail', args=[self.payment1.pk]))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Payment.objects.count(), 2)


class TransactionViewTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='shahzad@gmail.com',
                                             first_name='M',
                                             last_name='shahzad',
                                             gender='M',
                                             phone_number='09876543211',
                                             password='testpass',
                                             confirm_password='Shahzad123.')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.type = Type.objects.create(add_type='Income')
        self.payment_method = Payment.objects.create(payment_method='Paypal')
        self.category = Category.objects.create(new_category='Food',
                                                color='#FFFFFFFF')
        self.transaction = Add_Transaction.objects.create(
            user=self.user,
            type=self.type,
            payment_method=self.payment_method,
            description='Test transaction',
            category=self.category,
            amount=Decimal('10.50'),
            frequency=Add_Transaction.NON_RECURRING
        )

    def test_get_transaction_list(self):
        response = self.client.get(reverse('transaction-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)
        response_data = response.data['results']
        self.assertEqual(response_data[0]['id'], self.user.id)
        self.assertEqual(response_data[0]['type'], self.type.id)
        self.assertEqual(response_data[0]['payment_method'],
                         self.payment_method.id)
        self.assertEqual(response_data[0]['description'], 'Test transaction')
        self.assertEqual(response_data[0]['category'], self.category.id)
        self.assertEqual(response_data[0]['amount'], '10.50')
        self.assertEqual(response_data[0]['frequency'],
                         Add_Transaction.NON_RECURRING)

    def test_create_transaction(self):
        data = {
            'type': self.type.id,
            'payment_method': self.payment_method.id,
            'description': 'New transaction',
            'category': self.category.id,
            'amount': '25.00',
            'frequency': Add_Transaction.MONTHLY
        }
        response = self.client.post(reverse('transaction-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Add_Transaction.objects.count(), 2)
        transaction = Add_Transaction.objects.last()
        self.assertEqual(transaction.user, self.user)
        self.assertEqual(transaction.type, self.type)
        self.assertEqual(transaction.payment_method, self.payment_method)
        self.assertEqual(transaction.description, 'New transaction')
        self.assertEqual(transaction.category, self.category)
        self.assertEqual(transaction.amount, Decimal('25.00'))
        self.assertEqual(transaction.frequency, Add_Transaction.MONTHLY)

    def test_update_transaction(self):
        url = reverse('transaction-detail', kwargs={'pk': self.transaction.pk})
        data = {
            'type': self.type.id,
            'payment_method': self.payment_method.id,
            'description': 'Updated transaction',
            'category': self.category.id,
            'amount': '15.00',
            'frequency': Add_Transaction.WEEKLY
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.transaction.refresh_from_db()
        self.assertEqual(self.transaction.description, 'Updated transaction')
        self.assertEqual(self.transaction.amount, Decimal('15.00'))
        self.assertEqual(self.transaction.frequency, Add_Transaction.WEEKLY)

    def test_delete_transaction(self):
        url = reverse('transaction-detail', kwargs={'pk': self.transaction.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Add_Transaction.objects.count(), 0)