from django.test import TestCase
from django.test import Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from .models import Listing
from django.core.files import File
import os
from django.core.files.uploadedfile import SimpleUploadedFile
import mock
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def create_listing(dict, user, image):
    l = Listing.objects.create(
        owner = user,
        title = dict['title'],
        medium = dict['medium'],
        dimensions1 = dict['dim1'],
        dimensions2 = dict['dim2'],
        unit = dict['unit'],
        image = SimpleUploadedFile(name='test_image.jpg', content=open(os.path.join(BASE_DIR, "static/common_static/logo.png"), 'rb').read(), content_type='image/jpeg'),
        descrip = dict['descrip'],
        stock = dict['stock'],
        price = 99.99
    )
    return l



# Create your tests here.
class ListingTests(TestCase):
    thislisting = None
    def setUp(self):
        self.client = Client()
        self.l = None
        user = User.objects.create(username='testuser')
        user.set_password('1234')
        self.user = user
        user.save()
        self.client.force_login(self.user, backend=None)


    def test_no_listings(self):
        print(reverse('listing:mylistings'))
        response = self.client.get(reverse('listing:mylistings'))
        print(response)
        print(response.context)
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['my_listings'], [])

    def test_add_listings(self):
        # upload_file = File(open(os.path.join(BASE_DIR, "static/common_static/logo.png"), "rb"))
        thislisting = create_listing({
            'username': 'jen888',
            'title': 'Unity of Unit Tests',
            'medium': 'Watercolour',
            'dim1': 888,
            'dim2': 420,
            'unit': 'cm',
            'descrip': 'Are you a test because you are really testing me',
            'stock': 66,
            'price': 99.99
        }, self.user, None )
        response = self.client.get(reverse('listing:mylistings'))
        print(response.context)
        # self.listing_added = self.l.id
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['my_listings'], ['<Listing: testuser Unity of Unit Tests>'])

    def test_delete_listings(self):
        response = self.client.get(reverse('listing:listing_delete', kwargs={'pk': 1}))
        print(response)
        print(response.context)
        