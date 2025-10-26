# Copyright (c) 2025 Mikheil Tabidze
import sys
from urllib import error as urlerror
from urllib import request


def healthcheck() -> None:
    """
    CLI entrypoint for the healthcheck.

    Reads the healthcheck URL from ``argv[1]``, performs a GET request,
    and exits with:
    - 0: success — container is healthy and ready for use
    - 1: unhealthy — container isn't working correctly
    - 2: reserved — should not be used

    Success messages are printed to stdout;
    failure messages are printed to stderr.
    """
    if len(sys.argv) > 1 and sys.argv[1]:
        url = sys.argv[1]
    else:
        print(  # noqa: T201
            "Healthcheck error: No healthcheck URL provided as argument.",
            file=sys.stderr,
        )
        sys.exit(1)
    try:
        req = request.Request(url=url, method="GET")  # noqa: S310
        with request.urlopen(req) as resp:  # noqa: S310
            status_code = getattr(resp, "status", None) or resp.getcode()
            if 200 <= status_code < 300:  # noqa: PLR2004
                print(f"Healthy: {status_code}")  # noqa: T201
                sys.exit(0)
            print(f"Unhealthy: {status_code}", file=sys.stderr)  # noqa: T201
            sys.exit(1)
    except urlerror.HTTPError as e:
        print(f"Unhealthy: {e.code}", file=sys.stderr)  # noqa: T201
        sys.exit(1)
    except urlerror.URLError as e:
        print(f"Healthcheck error: {e.reason}", file=sys.stderr)  # noqa: T201
        sys.exit(1)
    except ValueError as e:
        print(f"Healthcheck error: {e}", file=sys.stderr)  # noqa: T201
        sys.exit(1)


if __name__ == "__main__":
    healthcheck()
