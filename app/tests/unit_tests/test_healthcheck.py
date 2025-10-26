# Copyright (c) 2025 Mikheil Tabidze
import sys
from urllib import error as urlerror

import healthcheck as hc
import pytest


class _FakeResponse:
    def __init__(self, status: int | None = None, code: int | None = None):
        self.status = status
        self._code = code

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def getcode(self):
        return self._code


def _set_argv(url: str | None):
    argv = ["healthcheck"]
    if url is not None:
        argv.append(url)
    sys.argv = argv


def test_no_argument_exits_1_and_prints_error(capsys, monkeypatch):
    _set_argv(None)
    with pytest.raises(SystemExit) as exc:
        hc.healthcheck()
    assert exc.value.code == 1
    out, err = capsys.readouterr()
    assert out == ""
    assert "No healthcheck URL provided" in err


def test_success_2xx_status_uses_status_attr_and_exits_0(capsys, monkeypatch):
    _set_argv("http://example.com/health")

    def fake_urlopen(req):
        return _FakeResponse(status=200)

    monkeypatch.setattr(hc.request, "urlopen", fake_urlopen)

    with pytest.raises(SystemExit) as exc:
        hc.healthcheck()
    assert exc.value.code == 0
    out, err = capsys.readouterr()
    assert "Healthy: 200" in out
    assert err == ""


def test_success_2xx_status_uses_getcode_when_no_status_attr(capsys, monkeypatch):
    _set_argv("http://example.com/health")

    def fake_urlopen(req):
        return _FakeResponse(status=None, code=204)

    monkeypatch.setattr(hc.request, "urlopen", fake_urlopen)

    with pytest.raises(SystemExit) as exc:
        hc.healthcheck()
    assert exc.value.code == 0
    out, err = capsys.readouterr()
    assert "Healthy: 204" in out
    assert err == ""


def test_non_2xx_status_prints_unhealthy_and_exits_1(capsys, monkeypatch):
    _set_argv("http://example.com/health")

    def fake_urlopen(req):
        return _FakeResponse(status=503)

    monkeypatch.setattr(hc.request, "urlopen", fake_urlopen)

    with pytest.raises(SystemExit) as exc:
        hc.healthcheck()
    assert exc.value.code == 1
    out, err = capsys.readouterr()
    assert out == ""
    assert "Unhealthy: 503" in err


def test_http_error_prints_unhealthy_code_and_exits_1(capsys, monkeypatch):
    _set_argv("http://example.com/health")

    def fake_urlopen(req):
        raise urlerror.HTTPError(req.full_url, 404, "Not Found", None, None)

    monkeypatch.setattr(hc.request, "urlopen", fake_urlopen)

    with pytest.raises(SystemExit) as exc:
        hc.healthcheck()
    assert exc.value.code == 1
    out, err = capsys.readouterr()
    assert out == ""
    assert "Unhealthy: 404" in err


def test_url_error_prints_reason_and_exits_1(capsys, monkeypatch):
    _set_argv("http://example.com/health")

    def fake_urlopen(req):
        raise urlerror.URLError("Connection refused")

    monkeypatch.setattr(hc.request, "urlopen", fake_urlopen)

    with pytest.raises(SystemExit) as exc:
        hc.healthcheck()
    assert exc.value.code == 1
    out, err = capsys.readouterr()
    assert out == ""
    assert "Healthcheck error: Connection refused" in err


def test_value_error_prints_message_and_exits_1(capsys, monkeypatch):
    _set_argv("htp://bad-url")

    def fake_urlopen(req):
        raise ValueError("unknown url type: htp")

    monkeypatch.setattr(hc.request, "urlopen", fake_urlopen)

    with pytest.raises(SystemExit) as exc:
        hc.healthcheck()
    assert exc.value.code == 1
    out, err = capsys.readouterr()
    assert out == ""
    assert "Healthcheck error: unknown url type: htp" in err
