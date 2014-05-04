import unittest

from userProfile import *

class UserProfileTests(unittest.TestCase):
    def setUp(self):
      pass

    def tearDown(self):
      pass

    def test_UserProfile_Parse_Google(self):
        json = """{
                 "id": "102535876287081397489",
                 "name": "Tomi Tuhkanen",
                 "given_name": "Tomi",
                 "family_name": "Tuhkanen",
                 "link": "https://plus.google.com/102535876287081397489",
                 "picture": "https://lh3.googleusercontent.com/-JFiYGUyHFYA/AAAAAAAAAAI/AAAAAAAACCo/NcBom9gQ8jM/photo.jpg",
                 "gender": "male",
                 "locale": "en"
                }"""

        user = UserProfile()
        user.parse(json)
        self.assertTrue(user.name == 'Tomi Tuhkanen')
        self.assertTrue(user.id == '102535876287081397489')

        user2 = UserProfile(json)
        self.assertTrue(user2.name == 'Tomi Tuhkanen')
        self.assertTrue(user2.id == '102535876287081397489')

    def test_UserProfile_Parse_Facebook(self):
        json = """{
                "id":"593417762",
                "name":"Tomi Tuhkanen",
                "first_name":"Tomi",
                "last_name":"Tuhkanen",
                "link":"https:\/\/www.facebook.com\/tomi.tuhkanen",
                "location":{
                    "id":"111984632161121",
                    "name":"Espoo, Finland"
                    },
                "gender":"male",
                "timezone":2,
                "locale":"en_US",
                "verified":true,
                "updated_time":"2013-02-14T19:25:33+0000",
                "username":"tomi.tuhkanen"
                }"""

        user = UserProfile()
        user.parse(json)
        self.assertTrue(user.name == 'Tomi Tuhkanen')
        self.assertTrue(user.id == '593417762')

        user2 = UserProfile(json)
        self.assertTrue(user2.name == 'Tomi Tuhkanen')
        self.assertTrue(user2.id == '593417762')