from django.db import models
from django.core.exceptions import ValidationError

class Atividade(models.Model):
    atividade = models.CharField(max_length=100, verbose_name='ATIVIDADES DISPONÍVEIS:')
    disponivel = models.BooleanField(default=True, verbose_name='ESSA ATIVIDADE ESTÁ DISPONÍVEL')
    
    def __str__(self) -> str:
        return self.atividade
    
    def save(self, *args, **kwargs) -> None:
        self.atividade = self.atividade.strip().upper()
        return super().save(*args, **kwargs)

# FICHA DE INSCRIÇÃO DE CAPACITAÇÃO
class Ficha(models.Model):
    nis = models.CharField(max_length=11, verbose_name='NIS (Número de Identificação Social)')
    nome_completo = models.CharField(max_length=100, verbose_name='NOME COMPLETO:')
    cpf = models.CharField(max_length=11, verbose_name='CADASTRO DE PESSOA FÍSICA (CPF):')
    genero = models.CharField(max_length=20, choices=(('M', 'MASCULINO'), ('F', 'FEMININO')), verbose_name='GÊNERO:')
    data_nascimento = models.DateField(verbose_name='DATA DE NASCIMENTO:')
    escolaridade = models.CharField(max_length=50, choices=(
        ('FUNDAMENTAL', 'ENSINO FUNDAMENTAL'),
        ('MEDIO', 'ENSINO MÉDIO'),
        ('GRADUACAO', 'GRADUAÇÃO'),
        ('POS_GRADUACAO', 'PÓS-GRADUAÇÃO')
    ), verbose_name='ESCOLARIDADE:')
    atividade = models.ForeignKey(Atividade, on_delete=models.PROTECT, verbose_name='ATIVIDADE QUE ATUA OU DESEJA ATUAR:')
    endereco = models.CharField(max_length=100, verbose_name='ENDEREÇO RESIDENCIAL:')
    complemento = models.CharField(max_length=100, blank=True, null=True, verbose_name='COMPLEMENTO:')
    bairro = models.CharField(max_length=100, verbose_name='BAIRRO:')
    cep = models.CharField(max_length=8, verbose_name='CEP:')
    uf = models.CharField(max_length=2, choices=(
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
    fixo = models.CharField(max_length=10, verbose_name='FIXO:', blank=True, null=True)
    email = models.EmailField(max_length=254, verbose_name='E-MAIL:')
    interesse_ter_negocio = models.CharField(max_length=1, choices=(
        ('S', 'SIM'), ('N', 'NÃO')
    ), verbose_name='O INTERESSADO TEM INTERESSE EM POSSUIR UM NEGÓCIO?')

    preferencia_aula = models.CharField(max_length=20, choices=(('ONLINE', 'ONLINE'), ('PRESENCIAL', 'PRESENCIAL')), verbose_name='VOCÊ PREFERE ASSISTIR AULAS ONLINE OU PRESENCIAIS?')
    meio_comunicacao_aula = models.CharField(max_length=20, choices=(('WHATSAPP', 'WHATSAPP'), ('EMAIL', 'EMAIL')), verbose_name='VOCÊ GOSTARIA QUE ENVIÁSSEMOS O LINK PARA AS AULAS POR?')
    assistir_online = models.CharField(max_length=1, choices=(
        ('S', 'SIM'), ('N', 'NÃO')), verbose_name='TEM CONDIÇÕES DE ASSISTIR AULAS ONLINE?')
    if_true_assistir_casa = models.CharField(max_length=10, blank=True, null=True, choices=(
        ('COMPUTADOR', 'COMPUTADOR'),
        ('CELULAR', 'CELULAR'),
        ('TABLET', 'TABLET'),
        ('OUTRO', 'OUTRO')
    ), verbose_name='SE VOCÊ RESPONDEU “SIM” À PERGUNTA ANTERIOR, POR ONDE VOCÊ ASSISTIRIA ÀS AULAS ONLINE?')

    # DADOS PESSOA JURÍDICA
    nome_fantasia = models.CharField(max_length=100, blank=True, null=True, verbose_name='NOME FANTASIA')
    cnpj = models.CharField(max_length=14, blank=True, null=True, verbose_name='CNPJ:')
    situacao_empresa = models.CharField(max_length=50, blank=True, null=True, choices=(
        ('ATIVA', 'ATIVA'),
        ('N_ATIVA', 'NÃO ATIVA')
    ), verbose_name='SITUAÇÃO DA EMPRESA:')
    porte_empresa = models.CharField(max_length=50, blank=True, null=True, choices=(
        ('MEI', 'MICROEMPREENDEDOR INDIVIDUAL (MEI)'),
        ('ME', 'MICROEMPRESA (ME)')
    ), verbose_name='PORTE:')
    data_abertura = models.DateField(blank=True, null=True, verbose_name='DATA ABERTURA:')
    cnae_principal = models.CharField(max_length=7, blank=True, null=True, verbose_name='CNAE PRINCIPAL (CLASSIFICAÇÃO NACIONAL DE ATIVIDADES ECONÔMICAS):')
    setor = models.CharField(max_length=50, blank=True, null=True, choices=(
        ('COMERCIO', 'COMÉRCIO'),
        ('SERVICO', 'SERVIÇO'),
        ('AGRONEGOCIOS', 'AGRONEGÓCIOS'),
        ('INDUSTRIA', 'INDÚSTRIA')
    ), verbose_name='SETOR:')
    tipo_vinculo = models.CharField(max_length=50, blank=True, null=True, choices=(
        ('REPRESENTANTE', 'REPRESENTANTE'),
        ('RESPONSAVEL', 'RESPONSÁVEL')
    ), verbose_name='TIPO DE VÍNCULO')

    # Extra

    # Módulos de Capacitação
    modulo_marketing = models.BooleanField(default=False, verbose_name='MARKETING (COMO DOMINAR O MERCADO DIGITAL)')
    modulo_financeiro = models.BooleanField(default=False, verbose_name='FINANCEIRO (DOMINE O FLUXO DE CAIXA DE SUA EMPRESA)')
    modulo_planejamento = models.BooleanField(default=False, verbose_name='PLANEJAMENTO (MODELO DE NEGÓCIO QUE FUNCIONA, APRENDA A FAZER O SEU)')
    modulo_outros = models.BooleanField(default=False, verbose_name='OUTROS')

    # Declaração de ciência e autorização
    responsabilizacao = models.BooleanField(default=False, verbose_name='DECLARO ESTAR CIENTE DE QUE SOU PLENAMENTE RESPONSÁVEL PELA VERACIDADE DAS INFORMAÇÕES AQUI PRESTADAS, VEZ QUE SERÃO COMPROVADAS NO INÍCIO DA CAPACITAÇÃO, E DE QUE A FALSIDADE DAS INFORMAÇÕES ACIMA IMPLICARÁ SANÇÕES CABÍVEIS DE NATUREZA CIVIL, ADMINISTRATIVA E CRIMINAL.')
    manejo_dados = models.BooleanField(default=False, verbose_name='DECLARO ESTAR CIENTE DE QUE, EM RAZÃO DA PARCERIA COM O SEBRAE, A RESPONSABILIDADE PELO MANEJO DOS DADOS SUPRA SOLICITADOS É COMPARTILHADA ENTRE O SEBRAE E A COORDENADORIA DE EMPREENDEDORISMO E SUSTENTABILIDADE DE NEGÓCIOS (COESNE), NA SECRETARIA MUNICIPAL DO DESENVOLVIMENTO ECONÔMICO (SDE), CASO SEJA VERIFICADA A NECESSIDADE DE ALTERAÇÕES.')
    armazenamento_dados = models.BooleanField(default=False, verbose_name='DECLARO ESTAR CIENTE QUANTO AO ARMAZENAMENTO DOS MEUS DADOS NO BANCO DE CADASTRO DA COESNE E PELO SEBRAE, PARA A FORMULAÇÃO FUTURA DE POLÍTICAS PÚBLICAS COM FOCO EM PÚBLICOS ESPECÍFICOS, E PARA QUE EU SEJA INFORMADO(A) SOBRE A EXECUÇÃO DE NOVOS PROJETOS PELA COESNE, RESPEITADA A CONFIDENCIALIDADE DOS DADOS, QUE SOMENTE SERÃO TRATADOS POR COLABORADORES FORMALMENTE AUTORIZADOS NO ÂMBITO DA SDE.')
    autorizacao = models.BooleanField(default=False, verbose_name='AUTORIZO AO SEBRAE O ARMAZENAMENTO E A UTILIZAÇÃO DOS MEUS DADOS COM A FINALIDADE DE OFERECER PRODUTOS E SERVIÇOS DO SEU INTERESSE, REALIZAR PESQUISAS RELACIONADAS AO SEU ATENDIMENTO, REALIZAR COMUNICAÇÕES OFICIAIS PELO SEBRAE OU POR NOSSOS PRESTADORES DE SERVIÇOS POR MEIO DE DIVERSOS CANAIS DE COMUNICAÇÃO E ENRIQUECER O SEU CADASTRO A PARTIR DE BASE DE DADOS CONTROLADAS PELO SEBRAE.')
    comunicacao = models.CharField(max_length=1, choices=(
        ('S', 'SIM, EU CONCORDO.'),
        ('N', 'NÃO, EU NÃO CONCORDO.')
    ), verbose_name='VOCÊ AUTORIZA QUE AS COMUNICAÇÕES SEJAM REALIZADAS POR MEIO DE LIGAÇÃO, MENSAGEM INSTANTÂNEA E E-MAIL?')

    # Data de criação da ficha
    data_criacao = models.DateTimeField(auto_now_add=True, verbose_name='DATA DE CRIAÇÃO DA FICHA')

    def __str__(self) -> str:
        return self.nome_completo

    def clean_list(self, fields: list) -> None:
        for field in fields:
            if getattr(self, field) and not str(getattr(self, field)).isnumeric():
                raise ValidationError({field: 'Deve conter somente números!'})

    def clean(self):
        self.clean_list(
            ('cpf', 'cep', 'cnpj', 'cnae_principal', 'celular', 'fixo', 'nis')
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
