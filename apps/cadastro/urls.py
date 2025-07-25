# ✅ NOVA VERSÃO CORRIGIDA
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    AlojamentoViewSet, CepAtingidoViewSet, DemandaAmbienteViewSet,
    DemandaEducacaoViewSet, DemandaHabitacaoViewSet, DemandaInternaViewSet,
    DemandaSaudeViewSet, DesaparecidoViewSet, MembroViewSet, ResponsavelViewSet
)

# Configuração do router
router = DefaultRouter()
router.register(r'alojamentos', AlojamentoViewSet)
router.register(r'ceps-atingidos', CepAtingidoViewSet)
router.register(r'responsaveis', ResponsavelViewSet)
router.register(r'membros', MembroViewSet)
router.register(r'demandas-ambiente', DemandaAmbienteViewSet)
router.register(r'demandas-educacao', DemandaEducacaoViewSet)
router.register(r'demandas-habitacao', DemandaHabitacaoViewSet)
router.register(r'demandas-internas', DemandaInternaViewSet)
router.register(r'demandas-saude', DemandaSaudeViewSet)
router.register(r'desaparecidos', DesaparecidoViewSet)

app_name = 'cadastro'

urlpatterns = [
    # Router URLs direto (sem prefixo adicional)
    path('', include(router.urls)),
]
