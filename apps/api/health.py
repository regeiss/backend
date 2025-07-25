from django.db import connection
from django.core.cache import cache
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
import redis
from django.conf import settings

@api_view(['GET'])
@permission_classes([AllowAny])
def health_check_detailed(request):
    """Health check detalhado com verificações de dependências"""
    health_status = {
        'status': 'healthy',
        'checks': {}
    }
    
    # Verificar database
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        health_status['checks']['database'] = 'healthy'
    except Exception as e:
        health_status['checks']['database'] = f'unhealthy: {str(e)}'
        health_status['status'] = 'unhealthy'
    
    # Verificar Redis
    try:
        cache.set('health_check', 'ok', 30)
        cache.get('health_check')
        health_status['checks']['redis'] = 'healthy'
    except Exception as e:
        health_status['checks']['redis'] = f'unhealthy: {str(e)}'
        health_status['status'] = 'unhealthy'
    
    return Response(health_status)
