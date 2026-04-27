#!/usr/bin/env python3
"""
Oraybox HTTP API Client

A Python client for calling Oray router management APIs via HTTP POST.
The router exposes APIs at /cgi-bin/oraybox with form data.

Required form fields:
    _api  - API name to call
    _pwd  - Router admin password

Additional parameters depend on the specific API.
"""

import json
from typing import Any

import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

DEFAULT_TIMEOUT = 30
DEFAULT_SCHEME = "http"


class OrayboxHttpAPIError(Exception):
    """Base exception for Oraybox HTTP API errors."""

    def __init__(self, message: str, api_name: str | None = None, raw_response: str | None = None):
        super().__init__(message)
        self.api_name = api_name
        self.raw_response = raw_response


class OrayboxHttpAPI:
    """HTTP client for Oray router management APIs.

    Args:
        host: Router IP address or hostname (e.g., "192.168.1.1").
        password: Router admin panel password.
        timeout: HTTP request timeout in seconds (default: 30).
        scheme: URL scheme, "http" or "https" (default: "http").
        verify_ssl: Whether to verify SSL certificates (default: False).
    """

    def __init__(
        self,
        host: str,
        password: str,
        timeout: int = DEFAULT_TIMEOUT,
        scheme: str = DEFAULT_SCHEME,
        verify_ssl: bool = False,
    ):
        self.host = host.rstrip("/")
        self.password = password
        self.timeout = timeout
        self.scheme = scheme
        self.verify_ssl = verify_ssl
        self._session = requests.Session()
        self._session.verify = verify_ssl

    @property
    def base_url(self) -> str:
        """Return the full base URL for API calls."""
        return f"{self.scheme}://{self.host}/cgi-bin/oraybox"

    def _prepare_params(self, api_name: str, params: dict[str, Any]) -> dict[str, str]:
        """Build the form data dict with _api, _pwd and serialized params."""
        form: dict[str, str] = {
            "_api": api_name,
            "_pwd": self.password,
        }
        for key, value in params.items():
            if isinstance(value, (dict, list)):
                form[key] = json.dumps(value, ensure_ascii=False, separators=(",", ":"))
            elif value is not None:
                form[key] = str(value)
        return form

    def call(self, api_name: str, **params: Any) -> dict[str, Any]:
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
        try:
            response = self._session.post(
                self.base_url,
                data=form,
                timeout=self.timeout,
            )
            response.raise_for_status()
        except requests.exceptions.RequestException as exc:
            raise OrayboxHttpAPIError(
                f"HTTP request failed: {exc}", api_name=api_name
            ) from exc

        try:
            result = response.json()
        except json.JSONDecodeError as exc:
            raise OrayboxHttpAPIError(
                f"Failed to decode JSON response: {exc}",
                api_name=api_name,
                raw_response=response.text,
            ) from exc

        code = result.get("code")
        if code is not None and code != 0:
            msg = result.get("msg", f"API returned error code {code}")
            raise OrayboxHttpAPIError(
                f"API error: {msg} (code={code})",
                api_name=api_name,
                raw_response=response.text,
            )

        return result

    def call_batch(self, calls: list[dict[str, Any]]) -> list[dict[str, Any]]:
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
        results: list[dict[str, Any]] = []
        for call_spec in calls:
            if "api" not in call_spec:
                raise OrayboxHttpAPIError("Missing 'api' key in batch call spec")
            api_name = call_spec.pop("api")
            result = self.call(api_name, **call_spec)
            results.append(result)
        return results

    def set_wifi_password(
        self,
        band: str,
        password: str,
        encryption: str | None = None,
    ) -> dict[str, Any]:
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

        # Fetch current config
        # Note: when dev is specified, wifi_get returns the band config directly.
        # When dev is omitted, it wraps configs under "2.4G" / "5G" keys.
        current = self.call("wifi_get", dev=band, tag=1)
        cfg = current.get(band) if band in current else current

        if not cfg or not isinstance(cfg, dict):
            raise OrayboxHttpAPIError(
                f"No WiFi config found for {band}", api_name="wifi_get"
            )

        # Detect encryption type
        if encryption is None:
            feature = cfg.get("feature", {})
            wdevs = feature.get("wdevs", [])
            if wdevs and "encryptions" in wdevs[0]:
                encryptions = wdevs[0]["encryptions"]
                # Prefer psk2+ccmp if available
                for enc in ("psk2+ccmp", "psk2", "psk-mixed+ccmp", "psk+ccmp"):
                    if enc in encryptions:
                        encryption = enc
                        break
                if encryption is None:
                    encryption = encryptions[-1] if encryptions else "psk2+ccmp"
            else:
                encryption = "psk2+ccmp"

        # Determine whether to use `encryption` or deprecated `encrypt`
        has_feature = "feature" in cfg
        enc_key = "encryption" if has_feature else "encrypt"

        # Build ssid_list from current config
        raw_ssid_list = cfg.get("ssid_list", [])
        ssid_list: list[dict[str, Any]] = []
        for item in raw_ssid_list:
            if not isinstance(item, dict) or not item.get("ssid"):
                continue
            ssid_item: dict[str, Any] = {
                "ssid": item.get("ssid", ""),
                "pwd": password,
                enc_key: encryption,
                "hidden": int(item.get("hidden", "0")),
                "isolation": int(item.get("isolation", "0")),
                "sta_isolation": int(item.get("sta_isolation", "0")),
                "switch": int(item.get("switch", "1")),
            }
            # Preserve optional fields if present
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

    def __enter__(self) -> "OrayboxHttpAPI":
        return self

    def __exit__(self, *args: Any) -> None:
        self._session.close()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Call Oraybox router API via HTTP")
    parser.add_argument("--host", required=True, help="Router IP or hostname")
    parser.add_argument("--password", required=True, help="Admin password")
    parser.add_argument("--api", required=True, help="API name to call")
    parser.add_argument("--param", action="append", default=[], help="Extra param as key=value (can repeat)")
    parser.add_argument("--timeout", type=int, default=30, help="HTTP timeout")
    parser.add_argument("--https", action="store_true", help="Use HTTPS")
    args = parser.parse_args()

    params = {}
    for p in args.param:
        if "=" not in p:
            parser.error(f"Invalid param format: {p}")
        k, v = p.split("=", 1)
        params[k] = v

    client = OrayboxHttpAPI(
        host=args.host,
        password=args.password,
        timeout=args.timeout,
        scheme="https" if args.https else "http",
    )
    try:
        result = client.call(args.api, **params)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    except OrayboxHttpAPIError as exc:
        print(f"Error: {exc}", file=__import__("sys").stderr)
        raise SystemExit(1)
