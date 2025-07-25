# backend/apps/cadastro/serializers.py
from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field
from .models import (
    Alojamento, CepAtingido, DemandaAmbiente, DemandaEducacao,
    DemandaHabitacao, DemandaInterna, DemandaSaude, Desaparecido,
    Membro, Responsavel
)


class AlojamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alojamento
        fields = '__all__'


class CepAtingidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CepAtingido
        fields = '__all__'


class ResponsavelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Responsavel
        fields = '__all__'
        
    def validate_cpf(self, value):
        """Validação básica de CPF"""
        if len(value) != 11:
            raise serializers.ValidationError("CPF deve ter 11 dígitos")
        if not value.isdigit():
            raise serializers.ValidationError("CPF deve conter apenas números")
        return value


class MembroSerializer(serializers.ModelSerializer):
    cpf_responsavel_nome = serializers.CharField(source='cpf_responsavel.nome', read_only=True)
    
    class Meta:
        model = Membro
        fields = '__all__'
        
    def validate_cpf(self, value):
        """Validação básica de CPF"""
        if len(value) != 11:
            raise serializers.ValidationError("CPF deve ter 11 dígitos")
        if not value.isdigit():
            raise serializers.ValidationError("CPF deve conter apenas números")
        return value


class DemandaAmbienteSerializer(serializers.ModelSerializer):
    cpf_nome = serializers.CharField(source='cpf.nome', read_only=True)
    
    class Meta:
        model = DemandaAmbiente
        fields = '__all__'


class DemandaEducacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = DemandaEducacao
        fields = '__all__'
        
    def validate_cpf(self, value):
        """Validação básica de CPF"""
        if len(value) != 11:
            raise serializers.ValidationError("CPF deve ter 11 dígitos")
        if not value.isdigit():
            raise serializers.ValidationError("CPF deve conter apenas números")
        return value


class DemandaHabitacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = DemandaHabitacao
        fields = '__all__'
        
    def validate_cpf(self, value):
        """Validação básica de CPF"""
        if len(value) != 11:
            raise serializers.ValidationError("CPF deve ter 11 dígitos")
        if not value.isdigit():
            raise serializers.ValidationError("CPF deve conter apenas números")
        return value


class DemandaInternaSerializer(serializers.ModelSerializer):
    class Meta:
        model = DemandaInterna
        fields = '__all__'
        
    def validate_cpf(self, value):
        """Validação básica de CPF"""
        if len(value) != 11:
            raise serializers.ValidationError("CPF deve ter 11 dígitos")
        if not value.isdigit():
            raise serializers.ValidationError("CPF deve conter apenas números")
        return value


class DemandaSaudeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DemandaSaude
        fields = '__all__'
        
    def validate_cpf(self, value):
        """Validação básica de CPF"""
        if len(value) != 11:
            raise serializers.ValidationError("CPF deve ter 11 dígitos")
        if not value.isdigit():
            raise serializers.ValidationError("CPF deve conter apenas números")
        return value


class DesaparecidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Desaparecido
        fields = '__all__'
        
    def validate_cpf(self, value):
        """Validação básica de CPF"""
        if len(value) != 11:
            raise serializers.ValidationError("CPF deve ter 11 dígitos")
        if not value.isdigit():
            raise serializers.ValidationError("CPF deve conter apenas números")
        return value


# Serializers com relacionamentos detalhados
class ResponsavelComMembrosSerializer(serializers.ModelSerializer):
    membros = MembroSerializer(source='membro_set', many=True, read_only=True)
    total_membros = serializers.SerializerMethodField()
    
    class Meta:
        model = Responsavel
        fields = '__all__'
        
    @extend_schema_field(serializers.IntegerField)
    def get_total_membros(self, obj) -> int:
        """Retorna o total de membros associados ao responsável"""
        return obj.membro_set.count()


class ResponsavelComDemandasSerializer(serializers.ModelSerializer):
    demanda_ambiente = DemandaAmbienteSerializer(read_only=True)
    demandas_educacao = DemandaEducacaoSerializer(source='demandaeducacao_set', many=True, read_only=True)
    demanda_habitacao = DemandaHabitacaoSerializer(read_only=True)
    demandas_internas = DemandaInternaSerializer(source='demandainterna_set', many=True, read_only=True)
    demanda_saude = DemandaSaudeSerializer(read_only=True)
    
    class Meta:
        model = Responsavel
        fields = '__all__'
