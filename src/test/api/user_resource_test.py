import os
import unittest
import uuid
from unittest import mock
from src.test.api.api_test_case import ApiTestCase

app_version = str(uuid.uuid4())


class TestMyApp(ApiTestCase):
    @mock.patch.dict(os.environ, {'APP_VERSION': app_version})
    def test_get_message(self):
        resp = {'name': 'together', 'version': app_version}
        result = self.simulate_get('/statz')
        self.assertEqual(result.json, resp)


if __name__ == '__main__':
    unittest.main()
