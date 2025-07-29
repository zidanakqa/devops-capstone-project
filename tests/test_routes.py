"""
Account API Service Test Suite

Test cases can be run with the following:
  nosetests -v --with-spec --spec-color
  coverage report -m
"""
import os
import logging
from unittest import TestCase
from tests.factories import AccountFactory
from service.common import status  # HTTP Status Codes
from service.models import db, Account, init_db
from service.routes import app
from service import talisman
from flask_cors import CORS

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql://postgres:postgres@localhost:5432/postgres"
)

BASE_URL = "/accounts"


######################################################################
#  T E S T   C A S E S
######################################################################
class TestAccountService(TestCase):
    """Account Service Tests"""

    @classmethod
    def setUpClass(cls):
        """Run once before all tests"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        init_db(app)
        talisman.force_https = False  


    @classmethod
    def tearDownClass(cls):
        """Runs once before test suite"""

    def setUp(self):
        """Runs before each test"""
        db.session.query(Account).delete()  # clean up the last tests
        db.session.commit()

        self.client = app.test_client()

    def tearDown(self):
        """Runs once after each test case"""
        db.session.remove()

    ######################################################################
    #  H E L P E R   M E T H O D S
    ######################################################################

    def _create_accounts(self, count):
        """Factory method to create accounts in bulk"""
        accounts = []
        for _ in range(count):
            account = AccountFactory()
            response = self.client.post(BASE_URL, json=account.serialize())
            self.assertEqual(
                response.status_code,
                status.HTTP_201_CREATED,
                "Could not create test Account",
            )
            new_account = response.get_json()
            account.id = new_account["id"]
            accounts.append(account)
        return accounts

    ######################################################################
    #  A C C O U N T   T E S T   C A S E S
    ######################################################################

    def test_index(self):
        """It should get 200_OK from the Home Page"""
        response = self.client.get("/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_health(self):
        """It should be healthy"""
        resp = self.client.get("/health")
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertEqual(data["status"], "OK")

    def test_create_account(self):
        """It should Create a new Account"""
        account = AccountFactory()
        response = self.client.post(
            BASE_URL,
            json=account.serialize(),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Make sure location header is set
        location = response.headers.get("Location", None)
        self.assertIsNotNone(location)

        # Check the data is correct
        new_account = response.get_json()
        self.assertEqual(new_account["name"], account.name)
        self.assertEqual(new_account["email"], account.email)
        self.assertEqual(new_account["address"], account.address)
        self.assertEqual(new_account["phone_number"], account.phone_number)
        self.assertEqual(new_account["date_joined"], str(account.date_joined))

    def test_bad_request(self):
        """It should not Create an Account when sending the wrong data"""
        response = self.client.post(BASE_URL, json={"name": "not enough data"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unsupported_media_type(self):
        """It should not Create an Account when sending the wrong media type"""
        account = AccountFactory()
        response = self.client.post(
            BASE_URL,
            json=account.serialize(),
            content_type="test/html"
        )
        self.assertEqual(response.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

    # ADD YOUR TEST CASES HERE ...
    # ADD YOUR TEST CASES HERE ...  # 4 spaces

    def test_get_account(self):  # 4 spaces
        """It should Read a single Account"""  # 8 spaces
        account = self._create_accounts(1)[0]  # 8 spaces
        resp = self.client.get(  # 8 spaces
            f"{BASE_URL}/{account.id}", content_type="application/json"  # 12 spaces
        )  # 8 spaces
        self.assertEqual(resp.status_code, status.HTTP_200_OK)  # 8 spaces
        data = resp.get_json()  # 8 spaces
        self.assertEqual(data["name"], account.name)  # 8 spaces

    def test_get_account_not_found(self):  # 4 spaces
        """It should not Read an Account that is not found"""  # 8 spaces
        resp = self.client.get(f"{BASE_URL}/0")  # 8 spaces
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)  # 8 spaces

    def test_get_account_list(self):  # 4 spaces
        """It should Get a list of Accounts"""  # 8 spaces
        self._create_accounts(5)  # 8 spaces
        resp = self.client.get(BASE_URL)  # 8 spaces
        self.assertEqual(resp.status_code, status.HTTP_200_OK)  # 8 spaces
        data = resp.get_json()  # 8 spaces
        self.assertEqual(len(data), 5)  # 8 spaces

    def test_update_account(self):  # 4 spaces
        """It should Update an existing Account"""  # 8 spaces
        # create an Account to update  # 8 spaces
        test_account = AccountFactory()  # 8 spaces
        resp = self.client.post(BASE_URL, json=test_account.serialize())  # 8 spaces
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)  # 8 spaces

        # update the account  # 8 spaces
        new_account = resp.get_json()  # 8 spaces
        new_account["name"] = "Updated Name"  # 8 spaces
        resp = self.client.put(  # 8 spaces
            f"{BASE_URL}/{new_account['id']}",  # 12 spaces
            json=new_account,  # 12 spaces
            content_type="application/json",  # 12 spaces
        )  # 8 spaces
        self.assertEqual(resp.status_code, status.HTTP_200_OK)  # 8 spaces
        updated_account = resp.get_json()  # 8 spaces
        self.assertEqual(updated_account["name"], "Updated Name")  # 8 spaces

    def test_update_account_not_found(self):  # 4 spaces
        """It should not Update an Account that is not found"""  # 8 spaces
        test_account = AccountFactory()  # 8 spaces
        resp = self.client.put(  # 8 spaces
            f"{BASE_URL}/0",  # 12 spaces
            json=test_account.serialize(),  # 12 spaces
            content_type="application/json",  # 12 spaces
        )  # 8 spaces
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)  # 8 spaces

    def test_delete_account(self):  # 4 spaces
        """It should Delete an Account"""  # 8 spaces
        account = self._create_accounts(1)[0]  # 8 spaces
        resp = self.client.delete(f"{BASE_URL}/{account.id}")  # 8 spaces
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)  # 8 spaces
        # make sure they are deleted  # 8 spaces
        resp = self.client.get(f"{BASE_URL}/{account.id}")  # 8 spaces
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)  # 8 spaces

    def test_method_not_allowed(self):  # 4 spaces
        """It should not allow an illegal method call"""  # 8 spaces
        resp = self.client.delete(BASE_URL)  # 8 spaces
        self.assertEqual(resp.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)  # 8 spaces

        

    def test_cors_security(self):
        """It should return a CORS header"""
        response = self.client.get('/', environ_overrides=HTTPS_ENVIRON)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check for the CORS header
        self.assertEqual(response.headers.get('Access-Control-Allow-Origin'), '*')    
