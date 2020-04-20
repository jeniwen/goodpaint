from django.test import TestCase
from django.test import Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from listing.models import Listing
from django.core.files import File
import os
from django.core.files.uploadedfile import SimpleUploadedFile
import mock
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Create your tests here.
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

#Borrows from tests written in listing.test
class CartTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.l = None
        user = User.objects.create(username='testuser')
        user.set_password('1234')
        self.user = user
        user.save()
        self.client.force_login(self.user, backend=None)
        print("Setup completed.")
        self.listing = create_listing({
            'username': 'jen888',
            'title': 'Unity of Unit Tests',
            'medium': 'Watercolour',
            'dim1': 888,
            'dim2': 420,
            'unit': 'cm',
            'descrip': 'Are you a test because you are really testing me',
            'stock': 2,
            'price': 99.99
        }, self.user, None )
        response = self.client.get(reverse('listing:mylistings'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['my_listings'], ['<Listing: testuser Unity of Unit Tests>'])
        print("Setup complete.")

    def test_add_to_cart(self):
        response = self.client.get(reverse('shopping_cart:addtocart', kwargs={'pk':self.listing.id} ))
        self.assertEqual(response.status_code, 302) #redirects to shopping cart

        # Getting shopping cart order items
        response = self.client.get(reverse('shopping_cart:mycart'))
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.context['user_order'])
        self.assertIsNotNone(response.context['order_num'])
        self.assertQuerysetEqual(response.context['user_order'], ['<OrderItem: Unity of Unit Tests>'])

        #Making sure stock is decreased
        response = self.client.get('/browse/' + str(self.listing.id) + '/details/')
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.context['listing'])
        self.assertEqual(response.context['listing'].stock, 1) #2 in stock in first place, should be one left after adding to card

        #One more time
        response = self.client.get(reverse('shopping_cart:addtocart', kwargs={'pk':self.listing.id} ))
        response = self.client.get(reverse('shopping_cart:mycart'))
        print(response.context['user_order'])
        self.assertQuerysetEqual(response.context['user_order'],['<OrderItem: Unity of Unit Tests>','<OrderItem: Unity of Unit Tests>'], ordered=False)
        response = self.client.get('/browse/' + str(self.listing.id) + '/details/')
        self.assertEqual(response.context['listing'].stock, 0) #Should be none left.

        #Adding to cart item with 0 left in stock should redirect to browse
        response = self.client.get(reverse('shopping_cart:addtocart', kwargs={'pk':self.listing.id} ))
        response = self.client.get('/browse/' + str(self.listing.id) + '/details/')
        self.assertEqual(response.context['listing'].stock, 0) #Should still be 0 left! Not -1!

        #Deleting from cart
        response = self.client.get(reverse('shopping_cart:deletefromcart', kwargs={'pk':self.listing.id} ))
        response = self.client.get('/browse/' + str(self.listing.id) + '/details/')
        self.assertEqual(response.context['listing'].stock, 1) #Should go back to 1
        response = self.client.get(reverse('shopping_cart:mycart'))
        self.assertQuerysetEqual(response.context['user_order'], ['<OrderItem: Unity of Unit Tests>'])

  
