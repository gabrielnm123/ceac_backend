from django.db import models
from django.core.exceptions import ValidationError

class ModulosAprendizagem(models.Model):
    nome = models.CharField(unique=True, verbose_name="Nome do Módulo")
    descricao = models.TextField(unique=True, verbose_name="Descrição", blank=True, null=True)
    disponivel = models.BooleanField(default=True, verbose_name="Disponível para Seleção")

    def __str__(self):
        return self.nome
    
    def save(self, *args, **kwargs) -> None:
        self.nome = self.nome.upper().strip()
        self.descricao = self.descricao.upper().strip()
        super().save(*args, **kwargs)

# Modelo intermediário para ligar Ficha com ModulosAprendizagem
class FichaModulo(models.Model):
    ficha = models.ForeignKey('Ficha', on_delete=models.CASCADE)
    modulo = models.ForeignKey(ModulosAprendizagem, on_delete=models.CASCADE)

    def __str__(self):
        return self.ficha.nome_completo

# FICHA DE INSCRIÇÃO DE CAPACITAÇÃO
class Ficha(models.Model):
    nome_completo = models.CharField(verbose_name='NOME COMPLETO:')
    cpf = models.CharField(max_length=11, unique=True, verbose_name='CADASTRO DE PESSOA FÍSICA (CPF):')
    genero = models.CharField(choices=(('M', 'MASCULINO'), ('F', 'FEMININO')), verbose_name='GÊNERO:')
    data_nascimento = models.DateField(verbose_name='DATA DE NASCIMENTO:')
    escolaridade = models.CharField(choices=(
        ('FUNDAMENTAL', 'ENSINO FUNDAMENTAL'),
        ('MEDIO', 'ENSINO MÉDIO'),
        ('GRADUACAO', 'GRADUAÇÃO'),
        ('POS_GRADUACAO', 'PÓS-GRADUAÇÃO')
    ), verbose_name='ESCOLARIDADE:')
    atividade = models.CharField(
    choices=(
        ('ARTESANATO', 'ARTESANATO'),
        ('AGRICULTURA_URBANA', 'AGRICULTURA URBANA'),
        ('COMERCIO', 'COMÉRCIO'),
        ('ESTETICA_E_BELEZA', 'ESTÉTICA E BELEZA'),
        ('GASTRONOMIA', 'GASTRONOMIA'),
        ('INDUSTRIA', 'INDÚSTRIA'),
        ('SERVICO', 'SERVIÇO'),
    ),
    verbose_name='ATIVIDADE QUE ATUA OU DESEJA ATUAR:'
)
    endereco = models.CharField(verbose_name='ENDEREÇO RESIDENCIAL:')
    complemento = models.CharField(blank=True, null=True, verbose_name='COMPLEMENTO:')
    bairro = models.CharField(verbose_name='BAIRRO:')
    cep = models.CharField(max_length=8, verbose_name='CEP:')
    uf = models.CharField(choices=(
        ('AC', 'ACRE'),
        ('AL', 'ALAGOAS'),
        ('AP', 'AMAPÁ'),
        ('AM', 'AMAZONAS'),
        ('BA', 'BAHIA'),
        ('CE', 'CEARÁ'),
        ('DF', 'DISTRITO FEDERAL'),
        ('ES', 'ESPÍRITO SANTO'),
        ('GO', 'GOIÁS'),
        ('MA', 'MARANHÃO'),
        ('MT', 'MATO GROSSO'),
        ('MS', 'MATO GROSSO DO SUL'),
        ('MG', 'MINAS GERAIS'),
        ('PA', 'PARÁ'),
        ('PB', 'PARAÍBA'),
        ('PR', 'PARANÁ'),
        ('PE', 'PERNAMBUCO'),
        ('PI', 'PIAUÍ'),
        ('RJ', 'RIO DE JANEIRO'),
        ('RN', 'RIO GRANDE DO NORTE'),
        ('RS', 'RIO GRANDE DO SUL'),
        ('RO', 'RONDÔNIA'),
        ('RR', 'RORAIMA'),
        ('SC', 'SANTA CATARINA'),
        ('SP', 'SÃO PAULO'),
        ('SE', 'SERGIPE'),
        ('TO', 'TOCANTINS'),
    ), verbose_name='UF:')
    celular = models.CharField(max_length=11, verbose_name='CELULAR:')
    fixo = models.CharField(max_length=10, blank=True, null=True, verbose_name='FIXO:')
    email = models.EmailField(unique=True, verbose_name='E-MAIL:')
    interesse_ter_negocio = models.CharField(choices=(
        ('S', 'SIM'), ('N', 'NÃO')
    ), verbose_name='O INTERESSADO TEM INTERESSE EM POSSUIR UM NEGÓCIO?')

    preferencia_aula = models.CharField(choices=(('ONLINE', 'ONLINE'), ('PRESENCIAL', 'PRESENCIAL')), verbose_name='VOCÊ PREFERE ASSISTIR AULAS ONLINE OU PRESENCIAIS?')
    meio_comunicacao_aula = models.CharField(choices=(('WHATSAPP', 'WHATSAPP'), ('EMAIL', 'EMAIL')), verbose_name='VOCÊ GOSTARIA QUE ENVIÁSSEMOS O LINK PARA AS AULAS POR?')
    assistir_online = models.CharField(choices=(('S', 'SIM'), ('N', 'NÃO')), verbose_name='TEM CONDIÇÕES DE ASSISTIR AULAS ONLINE?')
    if_true_assistir_casa = models.CharField(blank=True, null=True, choices=(
        ('COMPUTADOR', 'COMPUTADOR'),
        ('CELULAR', 'CELULAR'),
        ('TABLET', 'TABLET'),
        ('OUTRO', 'OUTRO')
    ), verbose_name='SE VOCÊ RESPONDEU “SIM” À PERGUNTA ANTERIOR, POR ONDE VOCÊ ASSISTIRIA ÀS AULAS ONLINE?')

    # DADOS PESSOA JURÍDICA
    nome_fantasia = models.CharField(blank=True, null=True, verbose_name='NOME FANTASIA')
    cnpj = models.CharField(max_length=14, blank=True, null=True, unique=True, verbose_name='CNPJ:')
    situacao_empresa = models.CharField(blank=True, null=True, choices=(
        ('ATIVA', 'ATIVA'),
        ('N_ATIVA', 'NÃO ATIVA')
    ), verbose_name='SITUAÇÃO DA EMPRESA:')
    porte_empresa = models.CharField(blank=True, null=True, choices=(
        ('MEI', 'MICROEMPREENDEDOR INDIVIDUAL (MEI)'),
        ('ME', 'MICROEMPRESA (ME)')
    ), verbose_name='PORTE:')
    data_abertura = models.DateField(blank=True, null=True, verbose_name='DATA ABERTURA:')
    cnae_principal = models.CharField(max_length=7, blank=True, null=True, verbose_name='CNAE PRINCIPAL (CLASSIFICAÇÃO NACIONAL DE ATIVIDADES ECONÔMICAS):')
    setor = models.CharField(blank=True, null=True, choices=(
        ('COMERCIO', 'COMÉRCIO'),
        ('SERVICO', 'SERVIÇO'),
        ('AGRONEGOCIOS', 'AGRONEGÓCIOS'),
        ('INDUSTRIA', 'INDÚSTRIA')
    ), verbose_name='SETOR:')
    tipo_vinculo = models.CharField(blank=True, null=True, choices=(
        ('REPRESENTANTE', 'REPRESENTANTE'),
        ('RESPONSAVEL', 'RESPONSÁVEL')
    ), verbose_name='TIPO DE VÍNCULO')

    # Módulos de Capacitação com modelo intermediário
    modulos_aprendizagem = models.ManyToManyField(ModulosAprendizagem, through='FichaModulo', blank=True, verbose_name='MÓDULOS DE CAPACITAÇÃO') # esse campo não deveria aparecer quando for criar a ficha do admin?

    def __str__(self) -> str:
        return self.nome_completo

    def clean_list(self, fields: list) -> None:
        for field in fields:
            if getattr(self, field) and not str(getattr(self, field)).isnumeric():
                raise ValidationError({field: 'Deve conter somente números!'})

    def clean(self):
        self.clean_list(
            ('cpf', 'cep', 'cnpj', 'cnae_principal', 'celular', 'fixo')
        )

    def save(self, *args, **kwargs) -> None:
        self.nome_completo = self.nome_completo.upper().strip()
        self.endereco = self.endereco.upper().strip()   
        if self.complemento:
            self.complemento = self.complemento.upper().strip()
        self.bairro = self.bairro.upper().strip()
        if self.nome_fantasia:
            self.nome_fantasia = self.nome_fantasia.upper().strip()
        self.email = self.email.lower().strip()
        super().save(*args, **kwargs)

    class Meta:
        permissions = [
            ("capacita_buscarFicha", "Capacita/Buscar Ficha"),
            ("capacita_criarFicha", "Capacita/Criar Ficha"),
        ]
