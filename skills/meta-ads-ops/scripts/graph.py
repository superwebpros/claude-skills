"""Tiny stdlib Graph API client shared by the meta-ads-ops scripts.

META_GRAPH_BASE  default https://graph.facebook.com/v21.0 (point it at a relay in a sandbox)
META_TOKEN       optional; when unset no token is sent (a relay injects it)
"""
import json
import os
import urllib.error
import urllib.parse
import urllib.request

BASE = os.environ.get("META_GRAPH_BASE", "https://graph.facebook.com/v21.0").rstrip("/")


class GraphError(RuntimeError):
    pass


def _auth(params: dict) -> dict:
    token = os.environ.get("META_TOKEN")
    return {**params, "access_token": token} if token else dict(params)


def _encode(params: dict) -> dict:
    return {k: v if isinstance(v, str) else json.dumps(v) for k, v in params.items()}


def _send(req) -> dict:
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as exc:
        body = exc.read().decode(errors="replace")
        try:
            err = json.loads(body).get("error", {})
            msg = err.get("error_user_msg") or err.get("message") or body
        except ValueError:
            msg = body
        raise GraphError(f"HTTP {exc.code}: {msg}") from None


def get(path: str, **params) -> dict:
    qs = urllib.parse.urlencode(_encode(_auth(params)))
    return _send(urllib.request.Request(f"{BASE}/{path.lstrip('/')}?{qs}"))


def get_all(path: str, **params) -> list:
    """Follow paging.next; returns the concatenated `data` lists."""
    page = get(path, **params)
    rows = list(page.get("data", []))
    while page.get("paging", {}).get("next"):
        page = _send(urllib.request.Request(page["paging"]["next"]))
        rows.extend(page.get("data", []))
    return rows


def post(path: str, **params) -> dict:
    data = urllib.parse.urlencode(_encode(_auth(params))).encode()
    return _send(urllib.request.Request(f"{BASE}/{path.lstrip('/')}", data=data, method="POST"))
