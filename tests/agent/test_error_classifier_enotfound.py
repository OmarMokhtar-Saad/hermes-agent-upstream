"""Node-style DNS failures (ENOTFOUND, "Can't reach the API server") are connection errors."""

from agent.error_classifier import FailoverReason, classify_api_error


def test_cant_reach_the_api_server_enotfound_is_a_connection_error():
    message = "API Error: Can't reach the API server — check your internet or DNS (ENOTFOUND)"
    result = classify_api_error(RuntimeError(message))
    assert result.reason == FailoverReason.timeout, message
    assert result.retryable is True
    assert result.should_compress is False
