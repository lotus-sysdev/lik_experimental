import json
from django.utils.deprecation import MiddlewareMixin
from .models import UserActionLog
import logging
import threading

_thread_locals = threading.local()

def get_current_user():
    return getattr(_thread_locals, 'user', None)

class CurrentUserMiddleware(MiddlewareMixin):
    def process_request(self, request):
        _thread_locals.user = getattr(request, 'user', None)

logger = logging.getLogger(__name__)

class UserActionMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.user.is_authenticated and request.method == 'POST':
            action = f'{request.method} - {request.path}'
            payload_data = dict(request.POST)
            csrf_token = payload_data.pop('csrfmiddlewaretoken', None)  # Remove 'csrfmiddlewaretoken' key
            payload = json.dumps(payload_data)
            UserActionLog.objects.create(user=request.user, action=action, payload=payload)
            logger.info(f'User: {request.user.username} - Action: {action} - Payload: {payload}')
