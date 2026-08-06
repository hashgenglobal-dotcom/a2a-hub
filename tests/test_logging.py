"""Structured logging verification."""

from __future__ import annotations

import json
import logging

from a2a_hub.logging import JsonFormatter, setup_logging


def test_json_formatter_emits_parseable_line() -> None:
    formatter = JsonFormatter()
    record = logging.LogRecord(
        name="a2a_hub.test",
        level=logging.INFO,
        pathname=__file__,
        lineno=1,
        msg="hello",
        args=(),
        exc_info=None,
    )
    record.fields = {"event": "unit_test"}  # type: ignore[attr-defined]
    payload = json.loads(formatter.format(record))
    assert payload["level"] == "INFO"
    assert payload["logger"] == "a2a_hub.test"
    assert payload["message"] == "hello"
    assert payload["fields"]["event"] == "unit_test"
    assert "timestamp" in payload


def test_setup_logging_configures_root_handler() -> None:
    setup_logging("DEBUG")
    root = logging.getLogger()
    assert root.level == logging.DEBUG
    assert any(isinstance(h.formatter, JsonFormatter) for h in root.handlers)
