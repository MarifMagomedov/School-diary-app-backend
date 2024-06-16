from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

from utils.dependencies import get_auth_service


class CurrentUserMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        endpoint = request.url.path

        if endpoint == '/auth/register' or endpoint == '/auth/login' or request.method == 'OPTIONS':
            return await call_next(request)

        auth_service = await get_auth_service()
        await auth_service.verify_token(request.headers.get('token'))
        response = await call_next(request)

        return response
