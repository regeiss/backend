# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Alojamento(models.Model):
    nome = models.CharField(unique=True, max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'alojamento'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class CepAtingido(models.Model):
    cep = models.CharField(primary_key=True, max_length=8)
    logradouro = models.CharField(max_length=200)
    num_inicial = models.BigIntegerField(blank=True, null=True)
    num_final = models.BigIntegerField(blank=True, null=True)
    municipio = models.CharField(max_length=150)
    uf = models.CharField(max_length=2)
    bairro = models.CharField(max_length=150, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cep_atingido'


class DemandaAmbiente(models.Model):
    cpf = models.OneToOneField('Responsavel', models.DO_NOTHING, db_column='cpf', primary_key=True)
    quantidade = models.IntegerField(blank=True, null=True)
    especie = models.TextField(blank=True, null=True)  # This field type is a guess.
    acompanha_tutor = models.TextField()  # This field type is a guess.
    vacinado = models.TextField(blank=True, null=True)  # This field type is a guess.
    vac_raiva = models.TextField(blank=True, null=True)  # This field type is a guess.
    vac_v8v10 = models.TextField(blank=True, null=True)  # This field type is a guess.
    nec_racao = models.TextField(blank=True, null=True)  # This field type is a guess.
    castrado = models.TextField(blank=True, null=True)  # This field type is a guess.
    porte = models.TextField(blank=True, null=True)  # This field type is a guess.
    evolucao = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'demanda_ambiente'


class DemandaEducacao(models.Model):
    cpf_responsavel = models.CharField(max_length=11)
    nome = models.CharField(max_length=150)
    genero = models.CharField(max_length=10, blank=True, null=True)
    alojamento = models.IntegerField(blank=True, null=True)
    data_nasc = models.DateField(blank=True, null=True)
    unidade_ensino = models.IntegerField(blank=True, null=True)
    turno = models.CharField(max_length=10, blank=True, null=True)
    demanda = models.CharField(max_length=300, blank=True, null=True)
    evolucao = models.CharField(max_length=500, blank=True, null=True)
    cpf = models.CharField(primary_key=True, max_length=11)

    class Meta:
        managed = False
        db_table = 'demanda_educacao'


class DemandaHabitacao(models.Model):
    cpf = models.CharField(primary_key=True, max_length=11)
    latitude = models.DecimalField(max_digits=11, decimal_places=8, blank=True, null=True)
    longitude = models.DecimalField(max_digits=11, decimal_places=8, blank=True, null=True)
    area_verde = models.CharField(max_length=1, blank=True, null=True)
    ocupacao = models.CharField(max_length=1, blank=True, null=True)
    material = models.CharField(max_length=50, blank=True, null=True)
    relacao_imovel = models.CharField(max_length=50, blank=True, null=True)
    uso_imovel = models.CharField(max_length=50, blank=True, null=True)
    cod_rge = models.BigIntegerField(blank=True, null=True)
    evolucao = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'demanda_habitacao'


class DemandaInterna(models.Model):
    cpf = models.CharField(primary_key=True, max_length=11)
    demanda = models.CharField(max_length=150)
    data = models.DateField()
    status = models.CharField(max_length=100, blank=True, null=True)
    evolucao = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'demanda_interna'


class DemandaSaude(models.Model):
    cpf = models.CharField(primary_key=True, max_length=11)
    genero = models.CharField(max_length=20, blank=True, null=True)
    saude_cid = models.CharField(max_length=40, blank=True, null=True)
    data_nasc = models.DateField(blank=True, null=True)
    gest_puer_nutriz = models.CharField(max_length=1)
    mob_reduzida = models.CharField(max_length=1)
    cuida_outrem = models.CharField(max_length=1)
    pcd_ou_mental = models.CharField(max_length=1)
    alergia_intol = models.CharField(max_length=100, blank=True, null=True)
    subs_psicoativas = models.CharField(max_length=100, blank=True, null=True)
    med_controlada = models.CharField(max_length=100, blank=True, null=True)
    local_ref = models.CharField(max_length=100, blank=True, null=True)
    evoluções = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'demanda_saude'


class Desaparecido(models.Model):
    cpf = models.CharField(max_length=11)
    data_desaparecimento = models.DateField()
    vinculo = models.CharField(max_length=30)
    tel_contato = models.CharField(max_length=20, blank=True, null=True)
    nome_desaparecido = models.CharField(max_length=150)

    class Meta:
        managed = False
        db_table = 'desaparecido'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Membro(models.Model):
    cpf = models.CharField(primary_key=True, max_length=11)
    nome = models.CharField(max_length=150)
    cpf_responsavel = models.ForeignKey('Responsavel', models.DO_NOTHING, db_column='cpf_responsavel')
    timestamp = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'membro'


class Responsavel(models.Model):
    cpf = models.CharField(primary_key=True, max_length=11)
    nome = models.CharField(max_length=150)
    cep = models.CharField(max_length=8)
    numero = models.BigIntegerField()
    complemento = models.CharField(max_length=300, blank=True, null=True)
    telefone = models.BigIntegerField(blank=True, null=True)
    bairro = models.CharField(max_length=100, blank=True, null=True)
    logradouro = models.CharField(max_length=100, blank=True, null=True)
    nome_mae = models.CharField(max_length=100, blank=True, null=True)
    data_nasc = models.DateField(blank=True, null=True)
    timestamp = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=1, blank=True, null=True)
    cod_rge = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'responsavel'
