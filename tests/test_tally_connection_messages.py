import sys
from pathlib import Path
import socket

import requests
import pytest

# Ensure the application module is importable during tests
ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

# Prevent heavy optional imports during testing
sys.modules.setdefault("sentence_transformers", None)

import app


def test_connection_error_message_includes_timeout_guidance():
    message = app.get_tally_connection_error_message(
        host="103.109.7.224",
        port=9000,
        host_candidates=["103.109.7.224"],
        error_detail="Connection to 103.109.7.224 timed out.",
    )

    assert "timed out" in message
    assert "curl -v --connect-timeout 5" in message


def test_connection_error_message_includes_refused_guidance():
    message = app.get_tally_connection_error_message(
        host="localhost",
        port=9000,
        host_candidates=["localhost", "127.0.0.1"],
        error_detail="Failed to establish a new connection: [Errno 111] Connection refused",
    )

    assert "Tried hosts: localhost, 127.0.0.1." in message
    assert "actively refused the connection" in message


def test_post_to_tally_with_fallback_uses_short_connect_timeout(monkeypatch):
    captured_timeouts = []

    def fake_getaddrinfo(host, port):
        return [(None, None, None, None, None)]

    def fake_post(url, data, headers, timeout):
        captured_timeouts.append(timeout)
        raise requests.exceptions.ConnectionError("simulated connection error")

    monkeypatch.setattr(app, "get_tally_host_candidates", lambda host: ["127.0.0.1"])
    monkeypatch.setattr(app.socket, "getaddrinfo", fake_getaddrinfo)
    monkeypatch.setattr(app.requests, "post", fake_post)

    try:
        app.post_to_tally_with_fallback("localhost", 9000, "<xml />", timeout=30)
    except requests.exceptions.ConnectionError:
        pass

    assert captured_timeouts == [(5.0, 30.0)]


def test_post_to_tally_with_fallback_skips_unresolvable_hosts(monkeypatch):
    called_hosts = []

    def fake_getaddrinfo(host, port):
        if host == "bad.host":
            raise socket.gaierror("not known")
        return [(None, None, None, None, None)]

    def fake_post(url, data, headers, timeout):
        called_hosts.append(url)
        raise requests.exceptions.ConnectionError("simulated connection error")

    monkeypatch.setattr(app, "get_tally_host_candidates", lambda host: ["bad.host", "127.0.0.1"])
    monkeypatch.setattr(app.socket, "getaddrinfo", fake_getaddrinfo)
    monkeypatch.setattr(app.requests, "post", fake_post)

    with pytest.raises(requests.exceptions.ConnectionError) as exc:
        app.post_to_tally_with_fallback("localhost", 9000, "<xml />", timeout=10)

    assert called_hosts == ["http://127.0.0.1:9000"]
    assert "bad.host: Name resolution failed" in str(exc.value)
