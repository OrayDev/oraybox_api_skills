"""Unit tests for oraybox_http_api.py client."""

import json
import unittest
from unittest.mock import MagicMock, patch

import sys
sys.path.insert(0, "oraybox-http-api/scripts")

from oraybox_http_api import OrayboxHttpAPI, OrayboxHttpAPIError


class TestOrayboxHttpAPI(unittest.TestCase):

    def setUp(self):
        self.client = OrayboxHttpAPI(host="192.168.1.1", password="admin")

    def test_base_url(self):
        self.assertEqual(self.client.base_url, "http://192.168.1.1/cgi-bin/oraybox")

    def test_base_url_https(self):
        client = OrayboxHttpAPI(host="192.168.1.1", password="admin", scheme="https")
        self.assertEqual(client.base_url, "https://192.168.1.1/cgi-bin/oraybox")

    def test_prepare_params_serializes_dict(self):
        form = self.client._prepare_params("wifi_get", {"dev": "2.4G", "info": {"mod": "dhcp"}})
        self.assertEqual(form["_api"], "wifi_get")
        self.assertEqual(form["_pwd"], "admin")
        self.assertEqual(form["dev"], "2.4G")
        self.assertEqual(form["info"], '{"mod":"dhcp"}')

    def test_prepare_params_serializes_list(self):
        form = self.client._prepare_params("test", {"items": [1, 2, 3]})
        self.assertEqual(form["items"], "[1,2,3]")

    @patch("oraybox_http_api.requests.Session.post")
    def test_call_success(self, mock_post):
        mock_response = MagicMock()
        mock_response.json.return_value = {"code": 0, "data": {"sn": "12345"}}
        mock_response.text = json.dumps({"code": 0, "data": {"sn": "12345"}})
        mock_post.return_value = mock_response

        result = self.client.call("sys_base_info")
        self.assertEqual(result["code"], 0)
        self.assertEqual(result["data"]["sn"], "12345")

        # Verify form data
        args, kwargs = mock_post.call_args
        self.assertEqual(kwargs["data"]["_api"], "sys_base_info")
        self.assertEqual(kwargs["data"]["_pwd"], "admin")

    @patch("oraybox_http_api.requests.Session.post")
    def test_call_error_code(self, mock_post):
        mock_response = MagicMock()
        mock_response.json.return_value = {"code": 4, "msg": "Wrong password"}
        mock_response.text = json.dumps({"code": 4, "msg": "Wrong password"})
        mock_post.return_value = mock_response

        with self.assertRaises(OrayboxHttpAPIError) as ctx:
            self.client.call("sys_base_info")
        self.assertIn("Wrong password", str(ctx.exception))
        self.assertEqual(ctx.exception.api_name, "sys_base_info")

    @patch("oraybox_http_api.requests.Session.post")
    def test_call_http_error(self, mock_post):
        from requests.exceptions import ConnectionError
        mock_post.side_effect = ConnectionError("Connection refused")

        with self.assertRaises(OrayboxHttpAPIError) as ctx:
            self.client.call("sys_base_info")
        self.assertIn("Connection refused", str(ctx.exception))

    @patch("oraybox_http_api.requests.Session.post")
    def test_call_json_decode_error(self, mock_post):
        mock_response = MagicMock()
        mock_response.json.side_effect = json.JSONDecodeError("test", "", 0)
        mock_response.text = "not json"
        mock_post.return_value = mock_response

        with self.assertRaises(OrayboxHttpAPIError) as ctx:
            self.client.call("sys_base_info")
        self.assertEqual(ctx.exception.raw_response, "not json")

    @patch("oraybox_http_api.requests.Session.post")
    def test_call_batch(self, mock_post):
        responses = [
            {"code": 0, "data": {"sn": "123"}},
            {"code": 0, "data": {"cpu": "10%"}},
        ]
        mock_response = MagicMock()
        mock_response.json.side_effect = responses
        mock_response.text = "{}"
        mock_post.return_value = mock_response

        results = self.client.call_batch([
            {"api": "sys_base_info"},
            {"api": "cpu_mem_get"},
        ])
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0]["data"]["sn"], "123")
        self.assertEqual(results[1]["data"]["cpu"], "10%")

    def test_call_batch_missing_api(self):
        with self.assertRaises(OrayboxHttpAPIError) as ctx:
            self.client.call_batch([{"params": "x"}])
        self.assertIn("Missing 'api' key", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
