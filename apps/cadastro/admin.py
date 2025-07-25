from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Alojamento, CepAtingido, DemandaAmbiente, DemandaEducacao,
    DemandaHabitacao, DemandaInterna, DemandaSaude, Desaparecido,
    Membro, Responsavel
)


@admin.register(Alojamento)
class AlojamentoAdmin(admin.ModelAdmin):
    list_display = ['id', 'nome']
    search_fields = ['nome']
    list_filter = ['nome']
    ordering = ['nome']


@admin.register(CepAtingido)
class CepAtingidoAdmin(admin.ModelAdmin):
    list_display = ['cep', 'logradouro', 'municipio', 'uf', 'bairro']
    search_fields = ['cep', 'logradouro', 'municipio', 'bairro']
    list_filter = ['uf', 'municipio']
    ordering = ['cep']
    readonly_fields = []
    
    def has_add_permission(self, request):
        return True
    
    def has_delete_permission(self, request, obj=None):
        return True 


@admin.register(Responsavel)
class ResponsavelAdmin(admin.ModelAdmin):
    list_display = ['cpf', 'nome', 'telefone', 'cep', 'bairro', 'status_display', 'timestamp']
    search_fields = ['cpf', 'nome', 'nome_mae', 'cep', 'bairro']
    list_filter = ['status', 'bairro', 'timestamp']
    ordering = ['-timestamp']
    readonly_fields = ['timestamp']
    
    fieldsets = (
        ('Informações Pessoais', {
            'fields': ('cpf', 'nome', 'nome_mae', 'data_nasc')
        }),
        ('Contato', {
            'fields': ('telefone', 'cep', 'logradouro', 'numero', 'complemento', 'bairro')
        }),
        ('Sistema', {
            'fields': ('status', 'cod_rge', 'timestamp'),
            'classes': ('collapse',)
        })
    )
    
    def status_display(self, obj):
        if obj.status == 'A':
            return format_html('<span style="color: green;">●</span> Ativo')
        elif obj.status == 'I':
            return format_html('<span style="color: red;">●</span> Inativo')
        return obj.status
    status_display.short_description = 'Status'
    
    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Membro)
class MembroAdmin(admin.ModelAdmin):
    list_display = ['cpf', 'nome', 'cpf_responsavel', 'status_display', 'timestamp']
    search_fields = ['cpf', 'nome', 'cpf_responsavel__nome']
    list_filter = ['status', 'timestamp']
    ordering = ['-timestamp']
    readonly_fields = ['timestamp']
    autocomplete_fields = ['cpf_responsavel']
    
    def status_display(self, obj):
        if obj.status == 'A':
            return format_html('<span style="color: green;">●</span> Ativo')
        elif obj.status == 'I':
            return format_html('<span style="color: red;">●</span> Inativo')
        return obj.status
    status_display.short_description = 'Status'
    
    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(DemandaAmbiente)
class DemandaAmbienteAdmin(admin.ModelAdmin):
    list_display = ['cpf', 'get_nome', 'quantidade', 'especie', 'vacinado', 'castrado']
    search_fields = ['cpf__cpf', 'cpf__nome']
    list_filter = ['especie', 'vacinado', 'castrado', 'porte']
    readonly_fields = ['cpf']
    
    fieldsets = (
        ('Responsável', {
            'fields': ('cpf',)
        }),
        ('Informações do Animal', {
            'fields': ('quantidade', 'especie', 'porte', 'acompanha_tutor')
        }),
        ('Saúde', {
            'fields': ('vacinado', 'vac_raiva', 'vac_v8v10', 'castrado')
        }),
        ('Necessidades', {
            'fields': ('nec_racao',)
        }),
        ('Observações', {
            'fields': ('evolucao',)
        })
    )
    
    def get_nome(self, obj):
        return obj.cpf.nome if obj.cpf else '-'
    get_nome.short_description = 'Nome do Responsável'
    
    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(DemandaEducacao)
class DemandaEducacaoAdmin(admin.ModelAdmin):
    list_display = ['cpf', 'nome', 'data_nasc', 'alojamento', 'turno', 'unidade_ensino']
    search_fields = ['cpf', 'nome', 'cpf_responsavel']
    list_filter = ['genero', 'turno', 'alojamento', 'unidade_ensino']
    
    fieldsets = (
        ('Identificação', {
            'fields': ('cpf', 'nome', 'cpf_responsavel', 'genero', 'data_nasc')
        }),
        ('Localização', {
            'fields': ('alojamento',)
        }),
        ('Educação', {
            'fields': ('unidade_ensino', 'turno', 'demanda')
        }),
        ('Evolução', {
            'fields': ('evolucao',)
        })
    )
    
    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(DemandaHabitacao)
class DemandaHabitacaoAdmin(admin.ModelAdmin):
    list_display = ['cpf', 'material', 'relacao_imovel', 'uso_imovel', 'area_verde']
    search_fields = ['cpf']
    list_filter = ['material', 'relacao_imovel', 'uso_imovel', 'area_verde', 'ocupacao']
    
    fieldsets = (
        ('Identificação', {
            'fields': ('cpf',)
        }),
        ('Localização', {
            'fields': ('latitude', 'longitude', 'cod_rge')
        }),
        ('Características do Imóvel', {
            'fields': ('material', 'relacao_imovel', 'uso_imovel', 'area_verde', 'ocupacao')
        }),
        ('Evolução', {
            'fields': ('evolucao',)
        })
    )
    
    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(DemandaInterna)
class DemandaInternaAdmin(admin.ModelAdmin):
    list_display = ['cpf', 'demanda', 'data', 'status']
    search_fields = ['cpf', 'demanda']
    list_filter = ['status', 'data']
    ordering = ['-data']
    
    fieldsets = (
        ('Identificação', {
            'fields': ('cpf', 'data')
        }),
        ('Demanda', {
            'fields': ('demanda', 'status')
        }),
        ('Evolução', {
            'fields': ('evolucao',)
        })
    )
    
    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(DemandaSaude)
class DemandaSaudeAdmin(admin.ModelAdmin):
    list_display = ['cpf', 'genero', 'data_nasc', 'saude_cid', 'pcd_ou_mental']
    search_fields = ['cpf', 'saude_cid']
    list_filter = ['genero', 'gest_puer_nutriz', 'mob_reduzida', 
                  'cuida_outrem', 'pcd_ou_mental']
    
    fieldsets = (
        ('Identificação', {
            'fields': ('cpf', 'genero', 'data_nasc')
        }),
        ('Condições de Saúde', {
            'fields': ('saude_cid', 'pcd_ou_mental', 'mob_reduzida')
        }),
        ('Situação Especial', {
            'fields': ('gest_puer_nutriz', 'cuida_outrem')
        }),
        ('Medicamentos e Alergias', {
            'fields': ('alergia_intol', 'med_controlada', 'subs_psicoativas')
        }),
        ('Referência', {
            'fields': ('local_ref',)
        }),
        ('Evolução', {
            'fields': ('evolucao',)
        })
    )
    
    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Desaparecido)
class DesaparecidoAdmin(admin.ModelAdmin):
    list_display = ['nome_desaparecido', 'cpf', 'data_desaparecimento', 'vinculo', 'tel_contato']
    search_fields = ['nome_desaparecido', 'cpf', 'tel_contato']
    list_filter = ['vinculo', 'data_desaparecimento']
    ordering = ['-data_desaparecimento']
    
    fieldsets = (
        ('Pessoa Desaparecida', {
            'fields': ('nome_desaparecido', 'data_desaparecimento')
        }),
        ('Informações do Comunicante', {
            'fields': ('cpf', 'vinculo', 'tel_contato')
        })
    )
    
    def has_delete_permission(self, request, obj=None):
        return False


# Configurações gerais do admin
admin.site.site_header = "Administração - Sistema de Cadastro"
admin.site.site_title = "Admin Cadastro"
admin.site.index_title = "Painel Administrativo"
