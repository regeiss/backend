from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from django.db.models import Q
from .models import (
    Alojamento, CepAtingido, DemandaAmbiente, DemandaEducacao,
    DemandaHabitacao, DemandaInterna, DemandaSaude, Desaparecido,
    Membro, Responsavel
)
from .serializers import (
    AlojamentoSerializer, CepAtingidoSerializer, DemandaAmbienteSerializer,
    DemandaEducacaoSerializer, DemandaHabitacaoSerializer, DemandaInternaSerializer,
    DemandaSaudeSerializer, DesaparecidoSerializer, MembroSerializer,
    ResponsavelSerializer, ResponsavelComMembrosSerializer, ResponsavelComDemandasSerializer
)

class AlojamentoViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet somente leitura para Alojamentos
    """
    queryset = Alojamento.objects.all()
    serializer_class = AlojamentoSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['nome']
    filterset_fields = ['nome']


class CepAtingidoViewSet(viewsets.ModelViewSet):
    """
    ViewSet somente leitura para CEPs atingidos
    """
    queryset = CepAtingido.objects.all()
    serializer_class = CepAtingidoSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['cep', 'logradouro', 'municipio', 'bairro']
    filterset_fields = ['uf', 'municipio']


class ResponsavelViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciamento de Responsáveis
    """
    queryset = Responsavel.objects.all()
    serializer_class = ResponsavelSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['cpf', 'nome', 'nome_mae', 'cep', 'bairro']
    filterset_fields = ['status', 'bairro', 'cep']
    ordering_fields = ['nome', 'timestamp']
    ordering = ['-timestamp']

    def get_serializer_class(self):
        if self.action == 'com_membros':
            return ResponsavelComMembrosSerializer
        elif self.action == 'com_demandas':
            return ResponsavelComDemandasSerializer
        return self.serializer_class

    @action(detail=True, methods=['get'])
    def com_membros(self, request, pk=None):
        """
        Retorna responsável com lista de membros
        """
        responsavel = self.get_object()
        serializer = ResponsavelComMembrosSerializer(responsavel)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def com_demandas(self, request, pk=None):
        """
        Retorna responsável com todas as demandas associadas
        """
        responsavel = self.get_object()
        serializer = ResponsavelComDemandasSerializer(responsavel)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def buscar_por_cpf(self, request):
        """
        Busca responsável por CPF
        """
        cpf = request.query_params.get('cpf', None)
        if cpf:
            try:
                responsavel = Responsavel.objects.get(cpf=cpf)
                serializer = self.get_serializer(responsavel)
                return Response(serializer.data)
            except Responsavel.DoesNotExist:
                return Response({'detail': 'Responsável não encontrado'}, 
                              status=status.HTTP_404_NOT_FOUND)
        return Response({'detail': 'CPF é obrigatório'}, 
                       status=status.HTTP_400_BAD_REQUEST)


class MembroViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciamento de Membros
    """
    queryset = Membro.objects.all()
    serializer_class = MembroSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['cpf', 'nome', 'cpf_responsavel__nome']
    filterset_fields = ['status', 'cpf_responsavel']
    ordering_fields = ['nome', 'timestamp']
    ordering = ['-timestamp']

    @action(detail=False, methods=['get'])
    def por_responsavel(self, request):
        """
        Lista membros por CPF do responsável
        """
        cpf_responsavel = request.query_params.get('cpf_responsavel', None)
        if cpf_responsavel:
            membros = self.queryset.filter(cpf_responsavel=cpf_responsavel)
            serializer = self.get_serializer(membros, many=True)
            return Response(serializer.data)
        return Response({'detail': 'CPF do responsável é obrigatório'}, 
                       status=status.HTTP_400_BAD_REQUEST)


class DemandaAmbienteViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciamento de Demandas de Ambiente
    """
    queryset = DemandaAmbiente.objects.all()
    serializer_class = DemandaAmbienteSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['cpf__cpf', 'cpf__nome']
    filterset_fields = ['especie', 'vacinado', 'castrado', 'porte']


class DemandaEducacaoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciamento de Demandas de Educação
    """
    queryset = DemandaEducacao.objects.all()
    serializer_class = DemandaEducacaoSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['cpf', 'nome', 'cpf_responsavel']
    filterset_fields = ['genero', 'turno', 'alojamento', 'unidade_ensino']


class DemandaHabitacaoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciamento de Demandas de Habitação
    """
    queryset = DemandaHabitacao.objects.all()
    serializer_class = DemandaHabitacaoSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['cpf']
    filterset_fields = ['material', 'relacao_imovel', 'uso_imovel', 'area_verde', 'ocupacao']


class DemandaInternaViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciamento de Demandas Internas
    """
    queryset = DemandaInterna.objects.all()
    serializer_class = DemandaInternaSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['cpf', 'demanda']
    filterset_fields = ['status']
    ordering_fields = ['data']
    ordering = ['-data']

    @action(detail=False, methods=['get'])
    def por_status(self, request):
        """
        Lista demandas por status
        """
        status_demanda = request.query_params.get('status', None)
        if status_demanda:
            demandas = self.queryset.filter(status=status_demanda)
            serializer = self.get_serializer(demandas, many=True)
            return Response(serializer.data)
        return Response({'detail': 'Status é obrigatório'}, 
                       status=status.HTTP_400_BAD_REQUEST)


class DemandaSaudeViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciamento de Demandas de Saúde
    """
    queryset = DemandaSaude.objects.all()
    serializer_class = DemandaSaudeSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['cpf', 'saude_cid']
    filterset_fields = ['genero', 'gest_puer_nutriz', 'mob_reduzida', 
                       'cuida_outrem', 'pcd_ou_mental']

    @action(detail=False, methods=['get'])
    def grupos_prioritarios(self, request):
        """
        Lista pessoas em grupos prioritários
        """
        prioritarios = self.queryset.filter(
            Q(gest_puer_nutriz='S') | 
            Q(mob_reduzida='S') | 
            Q(pcd_ou_mental='S')
        )
        serializer = self.get_serializer(prioritarios, many=True)
        return Response(serializer.data)


class DesaparecidoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciamento de Desaparecidos
    """
    queryset = Desaparecido.objects.all()
    serializer_class = DesaparecidoSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nome_desaparecido', 'cpf', 'tel_contato']
    filterset_fields = ['vinculo']
    ordering_fields = ['data_desaparecimento']
    ordering = ['-data_desaparecimento']

    @action(detail=False, methods=['get'])
    def recentes(self, request):
        """
        Lista desaparecimentos dos últimos 30 dias
        """
        from datetime import datetime, timedelta
        data_limite = datetime.now().date() - timedelta(days=30)
        recentes = self.queryset.filter(data_desaparecimento__gte=data_limite)
        serializer = self.get_serializer(recentes, many=True)
        return Response(serializer.data)
    
    
