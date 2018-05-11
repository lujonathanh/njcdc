from django.test import TestCase
from calc.models import UserProfile

class UserProfileTestCase(TestCase):
    def setUp(self):
        UserProfile.objects.create(adults = 3, children = 0)
        UserProfile.objects.create(adults = 0, children = 6)
		UserProfile.objects.        

    def test_adults_children(self):
    	adult = UserProfile.objects.get(adults = 3)
    	child = UserProfile.objects.get(children = 6)
    	adult.calculate_net()
    	child.calculate_net()
    	self.assertEqual(adult.net, child.net)
    	self.assertEqual(adult.benefit, child.benefit)
    	self.assertEqual(adult.total_cost, child.total_cost)

    # TODO: test combos of valid and invalid inputs
    def test_blank(self):
    	pass
