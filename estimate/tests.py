from estimate.models import Estimate
from rest_framework import status
from rest_framework.test import APITestCase
from unittest.mock import patch
from user.models import User


# ==========================
#         UNIT TESTS
# ==========================
class EstimateCreateViewTestCase(APITestCase):
    def setUp(self):
        self.user: User = User.objects.create_user(email='alireza.ghanimati78@gmail.com')
        self.url = '/estimate/'

    @patch('estimate.views.EstimateSerializer')
    def test_create_estimate_success(self, MockEstimateSerializer):
        # Set up the mock serializer to return a valid instance
        mock_serializer_instance = MockEstimateSerializer.return_value
        mock_serializer_instance.is_valid.return_value = True
        mock_serializer_instance.save.return_value = Estimate(note='Test note')

        data = {
            'note': 'Test note',
            'created_by': self.user.id,
        }
        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Estimate.objects.count(), 1)
        self.assertEqual(Estimate.objects.first().note, 'Test note')

    @patch('estimate.views.EstimateSerializer')
    def test_create_estimate_invalid_data(self, MockEstimateSerializer):
        mock_serializer_instance = MockEstimateSerializer.return_value
        mock_serializer_instance.is_valid.return_value = False
        mock_serializer_instance.errors = {'created_by': ['This field is required.']}

        data = {
            'note': 'test note',
        }
        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Estimate.objects.count(), 0)


class EstimateDetailViewTestCase(APITestCase):
    def setUp(self):
        self.user: User = User.objects.create(email="alireza.ghnaimati78@gmail.com")
        self.estimate: Estimate = Estimate.objects.create(note='Test note', created_by=self.user)
        self.url = f'/estimate/{self.estimate.id}/'

    @patch('estimate.views.EstimateSerializer')
    def test_retrieve_estimate(self, MockEstimateSerializer):
        response = self.client.get(self.url)
        print(response)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['note'], self.estimate.note)

    @patch('estimate.views.EstimateSerializer')
    def test_update_estimate(self, MockEstimateSerializer):
        data = {'note': 'Updated note'}
        mock_serializer_instance = MockEstimateSerializer.return_value
        mock_serializer_instance.is_valid.return_value = True
        mock_serializer_instance.save.return_value = None  # No return value for save

        response = self.client.patch(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.estimate.refresh_from_db()
        self.assertEqual(self.estimate.note, 'Updated note')

    def test_delete_estimate(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Estimate.objects.count(), 0)

    def test_retrieve_non_existent_estimate(self):
        response = self.client.get('/estimate/999/')  # Assuming 999 does not exist
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_non_existent_estimate(self):
        data = {'note': 'Updated note'}
        response = self.client.put('/estimate/999/', data, format='json')  # Assuming 999 does not exist
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_non_existent_estimate(self):
        response = self.client.delete('/estimate/999/')  # Assuming 999 does not exist
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


# ==========================
#     INTEGRATION TESTS
# ==========================
class EstimateCreationTestCase(APITestCase):
    def setUp(self):
        self.user: User = User.objects.create(email='alireza.ghnaimati78@gmail.com')
        self.url = '/estimate/'
        self.client.force_authenticate(user=self.user)

    def test_estimate_creation(self):
        data = {
            'note': 'this is test estimate',
            'created_by': self.user.id,
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Estimate.objects.count(), 1)
        self.assertEqual(response.data['note'], data['note'])
        self.assertEqual(response.data['created_by'], data['created_by'])


class EstimateDetailTestCase(APITestCase):
    def setUp(self):
        self.user: User = User.objects.create(email='alireza.ghnaimati78@gmail.com')
        self.estimate: Estimate = Estimate.objects.create(note='Initial note', created_by=self.user)
        self.url = f'/estimate/{self.estimate.id}/'
        self.client.force_authenticate(user=self.user)

    def test_retrieve_estimate(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['note'], self.estimate.note)
        self.assertEqual(response.data['created_by'], self.estimate.created_by)

    def test_update_estimate(self):
        data = {'note': 'Updated note'}
        response = self.client.patch(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.estimate.refresh_from_db()
        self.assertEqual(self.estimate.note, 'Updated note')

    def test_delete_estimate(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Estimate.objects.count(), 0)
