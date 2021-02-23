from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):

    # TODO -- write tests for every view function / feature!

    def test_initial_load(self):
        with app.get_client() as client:
            res = client.get('/')
            self.assertEqual(res.status_code, 200)
