import logging
from django.shortcuts import render

logger = logging.getLogger('accounts')


class AccessLogMiddleware:
    """Log attempts to access protected paths.

    It inspects path prefixes defined in `PROTECTED_PATHS` and logs unauthenticated access attempts.
    """

    PROTECTED_PATHS = ['/profile']

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check before view
        path = request.path
        if any(path.startswith(p) for p in self.PROTECTED_PATHS):
            if not request.session.get('user_id'):
                logger.info(
                    f'Unauthorized access attempt to {path} from {request.META.get("REMOTE_ADDR")}')
        response = self.get_response(request)
        return response


class ErrorHandlingMiddleware:
    """Convert 404/500 responses into rendered templates and log them."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            response = self.get_response(request)
        except Exception as exc:
            logger.exception('Server error: %s', exc)
            return render(request, '500.html', status=500)

        # post-process responses
        if getattr(response, 'status_code', None) == 404:
            logger.info(f'Page not found: {request.path}')
            return render(request, '404.html', status=404)
        return response
