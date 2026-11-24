
import secrets
from fastapi import Request, Response, HTTPException


def generate_xsrf_token():
    """Generate a cryptographically secure XSRF token."""
    return secrets.token_urlsafe(32)


def set_xsrf_cookie(response: Response, token: str):
    """Store the XSRF token in a cookie accessible to JavaScript."""
    response.set_cookie(
        key="xsrf_token",
        value=token,
        httponly=False,
        secure=False,  # True when deployed over HTTPS
        samesite="lax",
        max_age=3600,
        path="/"
    )


def verify_xsrf_token(request: Request):
    """Verify that the request's header matches its XSRF cookie."""
    cookie_token = request.cookies.get("xsrf_token")
    header_token = request.headers.get("X-XSRF-Token")

    if not cookie_token or not header_token:
        raise HTTPException(
            status_code=403,
            detail="Missing XSRF token"
        )

    if not secrets.compare_digest(cookie_token, header_token):
        raise HTTPException(
            status_code=403,
            detail="Invalid XSRF token"
        )
