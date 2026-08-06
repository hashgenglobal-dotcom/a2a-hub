"""Fetcher unit tests — mocked HTTP only (no external network)."""

from __future__ import annotations

import asyncio
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock

import aiohttp
import pytest

from a2a_hub.crawler.fetcher import Fetcher, fetch_all
from a2a_hub.crawler.models import USER_AGENT


@pytest.mark.asyncio
async def test_fetch_success_with_mocked_http() -> None:
    response = AsyncMock()
    response.status = 200
    response.headers = {"Content-Type": "application/json"}
    response.text = AsyncMock(return_value='{"name":"Agent X","url":"https://x.example/a2a"}')
    response.__aenter__ = AsyncMock(return_value=response)
    response.__aexit__ = AsyncMock(return_value=None)

    session = MagicMock(spec=aiohttp.ClientSession)
    session.get = MagicMock(return_value=response)

    async with Fetcher(session=session) as fetcher:
        result = await fetcher.fetch("https://example.com/.well-known/agent.json")

    assert result.error is None
    assert result.status_code == 200
    assert result.response_body is not None
    assert '"name":"Agent X"' in result.response_body
    assert result.content_type == "application/json"
    assert result.duration_ms is not None
    session.get.assert_called_once()
    # User-Agent is set on real sessions; injected session is caller-owned


@pytest.mark.asyncio
async def test_fetch_timeout() -> None:
    session = MagicMock(spec=aiohttp.ClientSession)

    def _raise_timeout(*_args: object, **_kwargs: object) -> object:
        raise TimeoutError

    session.get = MagicMock(side_effect=_raise_timeout)

    async with Fetcher(session=session, timeout_seconds=0.1) as fetcher:
        result = await fetcher.fetch("https://example.com/.well-known/agent.json")

    assert result.status_code is None
    assert result.error == "timeout"
    assert result.response_body is None


@pytest.mark.asyncio
async def test_fetch_connection_failure() -> None:
    session = MagicMock(spec=aiohttp.ClientSession)

    def _raise_conn(*_args: object, **_kwargs: object) -> object:
        raise aiohttp.ClientConnectionError("connection refused")

    session.get = MagicMock(side_effect=_raise_conn)

    async with Fetcher(session=session) as fetcher:
        result = await fetcher.fetch("https://example.com/.well-known/agent.json")

    assert result.error is not None
    assert result.error.startswith("connection_error:")
    assert result.response_body is None


@pytest.mark.asyncio
async def test_fetch_non_200() -> None:
    response = AsyncMock()
    response.status = 404
    response.headers = {"Content-Type": "application/json"}
    response.text = AsyncMock(return_value='{"error":"missing"}')
    response.__aenter__ = AsyncMock(return_value=response)
    response.__aexit__ = AsyncMock(return_value=None)

    session = MagicMock(spec=aiohttp.ClientSession)
    session.get = MagicMock(return_value=response)

    async with Fetcher(session=session) as fetcher:
        result = await fetcher.fetch("https://example.com/.well-known/agent.json")

    assert result.status_code == 404
    assert result.error == "http_error: status 404"
    assert result.response_body == '{"error":"missing"}'


@pytest.mark.asyncio
async def test_fetch_invalid_content_type_preserves_body() -> None:
    response = AsyncMock()
    response.status = 200
    response.headers = {"Content-Type": "text/html"}
    response.text = AsyncMock(return_value="<html>nope</html>")
    response.__aenter__ = AsyncMock(return_value=response)
    response.__aexit__ = AsyncMock(return_value=None)

    session = MagicMock(spec=aiohttp.ClientSession)
    session.get = MagicMock(return_value=response)

    async with Fetcher(session=session) as fetcher:
        result = await fetcher.fetch("https://example.com/.well-known/agent.json")

    assert result.error is not None
    assert "invalid_content_type" in result.error
    assert result.response_body == "<html>nope</html>"


@pytest.mark.asyncio
async def test_fetch_local_file_seed(tmp_path: Path) -> None:
    card = tmp_path / "agent.json"
    card.write_text('{"name":"Local Agent","url":"https://local/a2a"}', encoding="utf-8")

    async with Fetcher() as fetcher:
        result = await fetcher.fetch(card.as_uri())

    assert result.error is None
    assert result.status_code == 200
    assert result.response_body is not None
    assert "Local Agent" in result.response_body


def test_user_agent_constant() -> None:
    assert USER_AGENT == "A2A-Hub-Crawler/0.1"
