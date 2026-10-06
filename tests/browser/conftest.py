import functools
import http.server
import threading

import pytest


@pytest.fixture(scope="session")
def served(site):
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(site))
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    yield f"http://127.0.0.1:{server.server_address[1]}"
    server.shutdown()


def pytest_collection_modifyitems(items):
    for item in items:
        if "/browser/" in str(item.fspath):
            item.add_marker(pytest.mark.browser)
