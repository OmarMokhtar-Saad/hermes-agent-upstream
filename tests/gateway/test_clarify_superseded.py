"""A message sent while a question is open releases it as *superseded*, not as a timeout.

The owner typed a message a second after a choice card posted; the gateway released the clarify so
the message could route, and the agent was told "[user did not respond within 60m]". It must be
told the user wrote instead.
"""

from unittest.mock import MagicMock

import pytest

from gateway.run_turn_runner_clarify_delivery import _clarify_send_then_wait
from tools import clarify_gateway as cm


@pytest.fixture(autouse=True)
def _clean_clarify():
    with cm._lock:
        cm._entries.clear()
        cm._session_index.clear()
    yield


def test_a_message_instead_of_an_answer_is_not_reported_as_silence():
    cm.register("cid1", "sk", "Which?", ["alpha", "beta"])
    sent = MagicMock()
    sent.result.return_value = MagicMock(success=True)

    assert cm.supersede("cid1")
    response, answered = _clarify_send_then_wait(sent, clarify_id="cid1", session_key="sk", clarify_mod=cm)

    assert (response, answered) == (cm.SUPERSEDED_NOTICE, False)
    assert not cm.supersede("cid1")  # already released: a late tap finds nothing to answer
