#!/usr/bin/env python3
"""
Oraybox HTTP API Client

A Python client for calling Oray router management APIs via HTTP POST.
The router exposes APIs at /cgi-bin/oraybox with form data.

Required form fields:
    _api  - API name to call
    _pwd  - Router admin password

Additional parameters depend on the specific API.

Pure standard library — no external dependencies.
"""

import json
import ssl
import urllib.error
import urllib.parse
import urllib.request
from typing import Any, Dict, List, Optional, Union

DEFAULT_TIMEOUT = 30
DEFAULT_SCHEME = "http"


class OrayboxHttpAPIError(Exception):
    """Base exception for Oraybox HTTP API errors."""

    def __init__(self, message, api_name=None, raw_response=None):
        # type: (str, Optional[str], Optional[str]) -> None
        super(OrayboxHttpAPIError, self).__init__(message)
        self.api_name = api_name
        self.raw_response = raw_response


class OrayboxHttpAPI(object):
    """HTTP client for Oray router management APIs.

    Args:
        host: Router IP address or hostname (e.g., "192.168.1.1").
        password: Router admin panel password.
        timeout: HTTP request timeout in seconds (default: 30).
        scheme: URL scheme, "http" or "https" (default: "http").
        verify_ssl: Whether to verify SSL certificates (default: False).
        use_proxy: Whether to use the system HTTP/HTTPS proxy. Default is
            False because routers are typically on the local network and
            should not go through an external proxy.
    """

    def __init__(
        self,
        host=None,  # type: Optional[str]
        password=None,  # type: Optional[str]
        timeout=DEFAULT_TIMEOUT,  # type: int
        scheme=DEFAULT_SCHEME,  # type: str
        verify_ssl=False,  # type: bool
        use_proxy=False,  # type: bool
    ):
        # type: (...) -> None
        import os
        resolved_host = host or os.environ.get("ORAYBOX_HOST")
        if not resolved_host:
            raise OrayboxHttpAPIError(
                "Router host is required. Pass host= or set ORAYBOX_HOST environment variable."
            )
        self.host = resolved_host.rstrip("/")
        self.password = password or os.environ.get("ORAYBOX_PASSWORD")
        self.timeout = timeout
        self.scheme = scheme
        self.verify_ssl = verify_ssl
        self.use_proxy = use_proxy
        self._ssl_context = ssl.create_default_context()
        if not verify_ssl:
            self._ssl_context.check_hostname = False
            self._ssl_context.verify_mode = ssl.CERT_NONE
        handlers = [urllib.request.HTTPSHandler(context=self._ssl_context)]  # type: List[urllib.request.BaseHandler]
        if not use_proxy:
            handlers.insert(0, urllib.request.ProxyHandler({}))
        self._opener = urllib.request.build_opener(*handlers)

    @property
    def base_url(self):
        # type: () -> str
        """Return the full base URL for API calls."""
        return "{}://{}/cgi-bin/oraybox".format(self.scheme, self.host)

    def _prepare_params(self, api_name, params):
        # type: (str, Dict[str, Any]) -> Dict[str, str]
        """Build the form data dict with _api, _pwd and serialized params."""
        form = {"_api": api_name}  # type: Dict[str, str]
        if self.password is not None:
            form["_pwd"] = self.password
        for key, value in params.items():
            if isinstance(value, (dict, list)):
                form[key] = json.dumps(value, ensure_ascii=False, separators=(",", ":"))
            elif value is not None:
                form[key] = str(value)
        return form

    def call(self, api_name, **params):
        # type: (str, **Any) -> Dict[str, Any]
        """Call a single Oraybox API via HTTP POST.

        Args:
            api_name: The API name (e.g., "sys_base_info", "wifi_get").
            **params: Additional API-specific parameters.

        Returns:
            Parsed JSON response as a dict.

        Raises:
            OrayboxHttpAPIError: On HTTP errors, JSON decode errors,
                or when the router returns an error code.
        """
        form = self._prepare_params(api_name, params)
        data = urllib.parse.urlencode(form).encode("utf-8")
        req = urllib.request.Request(
            self.base_url,
            data=data,
            method="POST",
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )

        try:
            with self._opener.open(
                req, timeout=self.timeout
            ) as response:
                raw_body = response.read().decode("utf-8")
        except urllib.error.HTTPError as exc:
            raise OrayboxHttpAPIError(
                f"HTTP error {exc.code}: {exc.reason}", api_name=api_name
            ) from exc
        except urllib.error.URLError as exc:
            raise OrayboxHttpAPIError(
                f"Connection failed: {exc.reason}", api_name=api_name
            ) from exc
        except TimeoutError as exc:
            raise OrayboxHttpAPIError(
                f"Request timed out after {self.timeout}s", api_name=api_name
            ) from exc

        try:
            result = json.loads(raw_body)
        except json.JSONDecodeError as exc:
            raise OrayboxHttpAPIError(
                f"Failed to decode JSON response: {exc}",
                api_name=api_name,
                raw_response=raw_body,
            ) from exc

        code = result.get("code")
        if code is not None and code != 0:
            msg = result.get("msg", "API returned error code {}".format(code))
            raise OrayboxHttpAPIError(
                "API error: {} (code={})".format(msg, code),
                api_name=api_name,
                raw_response=raw_body,
            )

        return result

    def call_batch(self, calls):
        # type: (List[Dict[str, Any]]) -> List[Dict[str, Any]]
        """Execute a sequence of API calls.

        Args:
            calls: List of call specifications. Each dict must contain
                an ``api`` key with the API name; remaining keys are
                passed as parameters.

        Returns:
            List of parsed JSON responses, in the same order as *calls*.

        Example::

            results = client.call_batch([
                {"api": "sys_base_info"},
                {"api": "cpu_mem_get"},
            ])
        """
        results = []  # type: List[Dict[str, Any]]
        for call_spec in calls:
            if "api" not in call_spec:
                raise OrayboxHttpAPIError("Missing 'api' key in batch call spec")
            api_name = call_spec.pop("api")
            result = self.call(api_name, **call_spec)
            results.append(result)
        return results

    def set_wifi_password(
        self,
        band,  # type: str
        password,  # type: str
        encryption=None,  # type: Optional[str]
    ):
        # type: (...) -> Dict[str, Any]
        """Set WiFi password for the given band (2.4G or 5G).

        Automatically detects firmware version and uses the correct
        encryption parameter (`encryption` for new firmware, `encrypt`
        for older firmware without `feature` field).

        Args:
            band: WiFi band — "2.4G" or "5G".
            password: New WiFi password (8-63 characters).
            encryption: Encryption type. If None, auto-detected from
                `wifi_get` response (`feature.encryptions`). Falls back
                to "psk2+ccmp" if detection fails.

        Returns:
            Parsed JSON response from `wifi_set`.

        Raises:
            OrayboxHttpAPIError: On API errors.
        """
        if band not in ("2.4G", "5G"):
            raise ValueError("band must be '2.4G' or '5G'")

        current = self.call("wifi_get", dev=band, tag=1)
        cfg = current.get(band) if band in current else current

        if not cfg or not isinstance(cfg, dict):
            raise OrayboxHttpAPIError(
                f"No WiFi config found for {band}", api_name="wifi_get"
            )

        if encryption is None:
            feature = cfg.get("feature", {})
            wdevs = feature.get("wdevs", [])
            if wdevs and "encryptions" in wdevs[0]:
                encryptions = wdevs[0]["encryptions"]
                for enc in ("psk2+ccmp", "psk2", "psk-mixed+ccmp", "psk+ccmp"):
                    if enc in encryptions:
                        encryption = enc
                        break
                if encryption is None:
                    encryption = encryptions[-1] if encryptions else "psk2+ccmp"
            else:
                encryption = "psk2+ccmp"

        has_feature = "feature" in cfg
        enc_key = "encryption" if has_feature else "encrypt"

        raw_ssid_list = cfg.get("ssid_list", [])
        ssid_list = []  # type: List[Dict[str, Any]]
        for item in raw_ssid_list:
            if not isinstance(item, dict) or not item.get("ssid"):
                continue
            ssid_item = {
                "ssid": item.get("ssid", ""),
                "pwd": password,
                enc_key: encryption,
                "hidden": int(item.get("hidden", "0")),
                "isolation": int(item.get("isolation", "0")),
                "sta_isolation": int(item.get("sta_isolation", "0")),
                "switch": int(item.get("switch", "1")),
            }  # type: Dict[str, Any]
            for opt in ("maxassoc", "ft", "vlanid", "shaping_switch", "upload", "download"):
                if opt in item and item[opt] not in (None, "", 0, "0"):
                    ssid_item[opt] = item[opt]
            ssid_list.append(ssid_item)

        if not ssid_list:
            raise OrayboxHttpAPIError(
                f"No valid SSID config found for {band}", api_name="wifi_get"
            )

        return self.call(
            "wifi_set",
            dev=band,
            switch=int(cfg.get("switch", 1)),
            htmode=cfg.get("htmode", "HT40" if band == "2.4G" else "VHT80"),
            channel=0 if cfg.get("channel") == "auto" else int(cfg.get("channel", 0)),
            level=int(cfg.get("level", 3)),
            pattern=int(cfg.get("pattern", 0)),
            country=cfg.get("country", "CN"),
            ssid_list=ssid_list,
        )

    def __enter__(self):
        # type: () -> OrayboxHttpAPI
        return self

    def __exit__(self, *args):
        # type: (*Any) -> None
        pass


if __name__ == "__main__":
    import sys

    # Force UTF-8 for stdout/stderr to prevent mojibake on Windows and
    # other environments where the default encoding is not UTF-8.
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")

    import argparse

    parser = argparse.ArgumentParser(description="Call Oraybox router API via HTTP")
    parser.add_argument("--host", default=None, help="Router IP or hostname (default: $ORAYBOX_HOST)")
    parser.add_argument("--password", default=None, help="Admin password (default: $ORAYBOX_PASSWORD)")
    parser.add_argument("--api", required=True, help="API name to call")
    parser.add_argument("--param", action="append", default=[], help="Extra param as key=value (can repeat)")
    parser.add_argument("--timeout", type=int, default=30, help="HTTP timeout")
    parser.add_argument("--https", action="store_true", help="Use HTTPS")
    parser.add_argument("--use-proxy", action="store_true", help="Use system HTTP/HTTPS proxy (default: disabled)")
    args = parser.parse_args()

    host = args.host
    password = args.password

    params = {}
    for p in args.param:
        if "=" not in p:
            parser.error("Invalid param format: {}".format(p))
        k, v = p.split("=", 1)
        params[k] = v

    client = OrayboxHttpAPI(
        host=host,
        password=password,
        timeout=args.timeout,
        scheme="https" if args.https else "http",
        use_proxy=args.use_proxy,
    )
    try:
        result = client.call(args.api, **params)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    except OrayboxHttpAPIError as exc:
        import sys as _sys
        _sys.stderr.write("Error: {}\n".format(exc))
        raise SystemExit(1)
