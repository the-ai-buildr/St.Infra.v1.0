import time
from typing import Iterator


def stream_agent_response(prompt: str, history: list) -> Iterator[str]:
    """Stub generator for agent responses."""
    stub_response = "This is a stub response from the agent service."
    for token in stub_response.split():
        yield token + " "
        time.sleep(0.05)
