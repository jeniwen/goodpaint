from django.test import TestCase
from django.test import Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from .models import Listing
from .models import ListingEdit
from .forms import ListingPostForm
from .forms import ListingPostFormEdit
from django.core.files import File
import os
from django.core.files.uploadedfile import SimpleUploadedFile
import mock
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
from decimal import *


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

thislisting = None
thislistingid = 1

# Create your tests here.
class ListingTests(TestCase):
    

    def setUp(self):
        self.client = Client()
        user = User.objects.create(username='testuser')
        user.set_password('1234')
        self.user = user
        user.save()
        self.client.force_login(self.user, backend=None)


    def test_no_listings(self):
        response = self.client.get(reverse('listing:mylistings'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['my_listings'], [])

    def test_add_listings(self):
        self.thislisting = create_listing({
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
        self.thislistingid = self.thislisting.id
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['my_listings'], ['<Listing: testuser Unity of Unit Tests>'])

    def test_delete_listings(self):
        self.test_add_listings()
        response = self.client.get(reverse('listing:listing_delete', kwargs={'pk': self.thislistingid }))
        self.assertEqual(response.status_code, 302) #redirect
        self.test_no_listings()
    
    def test_edit_listing(self):
        #First adds a listing
        self.test_add_listings()

        #Fills out new edit form
        edit_form_data1 = {
            'title': 'Unity Part 2',
            'descrip': 'You really are a test!',
            'stock': 2,
            'price': 101.01
        }
        edit_form = ListingPostFormEdit(data=edit_form_data1)
        self.assertTrue(edit_form.is_valid())

        #Post form
        response = self.client.post(
            reverse('listing:listing_edit', kwargs={'pk': self.thislistingid }),
            edit_form_data1
        )
        response = self.client.get(reverse('listing:mylistings'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['my_listings'], ['<Listing: testuser Unity Part 2>'])

        response = self.client.get('/browse/' + str(self.thislisting.id) + '/details/')
        self.assertEqual(response.context['listing'].stock, 68) #Should increase by 2
        self.assertEqual(response.context['listing'].descrip, 'You really are a test!') 
        self.assertAlmostEqual(response.context['listing'].price, Decimal(101.01))  #Almost because of Decimal


        



        