from unittest.mock import MagicMock
from falcon import testing
from api.api_manager import get_api


class ApiTestCase(testing.TestCase):
    def setUp(self):
        super(ApiTestCase, self).setUp()
        db = MagicMock()
        self.app = get_api(db)
