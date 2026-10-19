"""
Smoke-test a running PlantAssist deployment over HTTP. Exits non-zero on the first failure.
"""

import json
import os
import sys
import urllib.error
import urllib.request
from typing import Any

BASE_URL = os.environ.get("BASE_URL", "http://127.0.0.1:8000")
EXPECTED_SHA = os.environ.get("EXPECTED_SHA")


def request(method: str, path: str, body: dict[str, Any] | None = None) -> tuple[int, Any]:
    """
    Send one JSON request and return (status code, parsed JSON body).
    """
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(  # noqa: S310  (URL from our own config)
        f"{BASE_URL}{path}",
        data=data,
        method=method,
        headers={"Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as response:  # noqa: S310  (URL from our own config)
            return response.status, json.loads(response.read() or b"null")
    except urllib.error.HTTPError as error:
        return error.code, json.loads(error.read() or b"null")


def check(passed: bool, description: str) -> None:
    """
    Print the result of one check, and stop with exit code 1 if it failed.
    """
    if not passed:
        print(f"FAIL  {description}")
        sys.exit(1)
    print(f"ok    {description}")


def main() -> None:
    status, body = request("GET", "/health/ready")
    check(status == 200, f"/health/ready returns 200 (got {status}: {body})")

    status, body = request("GET", "/version")
    check(status == 200, "/version returns 200")
    if EXPECTED_SHA:
        check(
            body["gitSha"] == EXPECTED_SHA,
            f"/version reports commit {EXPECTED_SHA} (got {body['gitSha']})",
        )

    status, created = request(
        "POST",
        "/api/v1/incidents",
        {"machineId": "SMOKE-01", "title": "Smoke test", "symptoms": "Created by the smoke test"},
    )
    check(status == 201, f"creating an incident returns 201 (got {status}: {created})")
    incident_id = created["id"]

    status, fetched = request("GET", f"/api/v1/incidents/{incident_id}")
    check(status == 200 and fetched["id"] == incident_id, "the new incident can be fetched")

    status, resolved = request(
        "PATCH",
        f"/api/v1/incidents/{incident_id}/resolution",
        {"resolution": "Resolved by the smoke test"},
    )
    check(status == 200 and resolved["status"] == "RESOLVED", "the incident can be resolved")

    status, error = request("GET", "/api/v1/incidents/00000000-0000-0000-0000-000000000000")
    check(
        status == 404 and error["code"] == "INCIDENT_NOT_FOUND",
        "an unknown incident returns the standard 404 error",
    )

    print("Smoke test passed.")


if __name__ == "__main__":
    main()
