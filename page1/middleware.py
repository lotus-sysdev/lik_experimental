import json
from django.utils.deprecation import MiddlewareMixin
from .models import UserActionLog
import logging

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
