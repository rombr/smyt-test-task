from datetime import date

from django.test import TestCase
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse

from utils import (
    get_models_config,
    NoConfigFileError,
    InvalidConfigFileFormatError,
    ConfigFileParseError,
)
from models import Users, Rooms


class LoadConfigTestCase(TestCase):
    def test_no_config_file(self):
        self.assertRaises(NoConfigFileError, get_models_config, "some_file.yaml")

    def test_invalid_config_file_format(self):
        self.assertRaises(
            InvalidConfigFileFormatError, get_models_config, "test_configs/models.json"
        )

    def test_invalid_config_structure(self):
        self.assertRaises(
            ConfigFileParseError, get_models_config, "test_configs/models_invalid.yaml"
        )


class ModelsTestCase(TestCase):
    def setUp(self):
        Users.objects.create(
            name="Tom Backs", paycheck=100500, date_joined="2013-12-21"
        )
        Rooms.objects.create(department="IT", spots=7)

    def test_valid_date_while_user_create(self):
        user = Users.objects.get(name="Tom Backs")
        self.assertEqual(user.date_joined, date(2013, 12, 21))

    def test_invalid_date(self):
        self.assertRaises(
            ValidationError,
            Users.objects.create,
            name="Tom Backs",
            paycheck=100500,
            date_joined="2013-12-21-",
        )

    def test_invalid_int(self):
        self.assertRaises(ValueError, Rooms.objects.create, department="IT", spots="7d")


class OperationsTestCase(TestCase):
    def setUp(self):
        Users.objects.create(
            name="Tom Backs", paycheck=100500, date_joined="2013-12-21"
        )
        Rooms.objects.create(department="IT", spots=7)

    def test_index_page(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "#users")
        self.assertContains(response, "#rooms")

    def test_api_get_objects(self):
        response = self.client.get(reverse("api", args=["rooms"]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "IT")

    def test_api_create_new_object(self):
        response = self.client.post(
            reverse("api", args=["rooms"]),
            {
                "department": "Sales",
                "spots": 15,
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Sales")

    def test_api_create_new_object_with_bad_param(self):
        response = self.client.post(
            reverse("api", args=["rooms"]),
            {
                "department": "Sales",
                "spots": "15d",
            },
        )
        self.assertEqual(response.status_code, 400)

    def test_api_get_object_details(self):
        response = self.client.get(reverse("api_details", args=["users", 1]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Tom Backs")

    def test_api_get_not_existing_object_details(self):
        response = self.client.get(reverse("api_details", args=["users", 2]))
        self.assertEqual(response.status_code, 404)

    def test_api_update_object_details(self):
        response = self.client.post(
            reverse("api_details", args=["users", 1]),
            {
                "name": "Mark Grace",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Mark Grace")

    def test_api_update_object_details_with_invalid_param(self):
        response = self.client.post(
            reverse("api_details", args=["users", 1]),
            {
                "date_joined": "2013-12-21@",
            },
        )
        self.assertEqual(response.status_code, 400)
