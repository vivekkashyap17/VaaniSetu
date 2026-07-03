"""API-key verification (regression guard for the undefined-API_KEY bug)."""

import asyncio

import pytest
from fastapi import HTTPException

from app.core.security.api_key import verify_api_key
from app.core.config.settings import get_settings

VALID_KEY = get_settings().API_KEY


def test_valid_key_passes():
    # Should not raise, and returns None implicitly.
    assert asyncio.run(verify_api_key(VALID_KEY)) is None


def test_wrong_key_rejected_with_401():
    with pytest.raises(HTTPException) as exc_info:
        asyncio.run(verify_api_key("definitely-wrong-key"))
    assert exc_info.value.status_code == 401


def test_missing_key_rejected_with_401():
    with pytest.raises(HTTPException) as exc_info:
        asyncio.run(verify_api_key(None))
    assert exc_info.value.status_code == 401
