import os

CODESPACE_NAME = os.environ.get("CODESPACE_NAME")


def endpoint_checker():
    if CODESPACE_NAME is not None:
        return f"https://{CODESPACE_NAME}-4566.app.github.dev"
    else:
        return "http://host.docker.internal:4566"
