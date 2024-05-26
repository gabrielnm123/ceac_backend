from django.db import models
from django.core.exceptions import ValidationError

class Atividade(models.Model):
    atividade = models.CharField(max_length=100, verbose_name='ATIVIDADES DISPONÍVEIS:')
    disponivel = models.BooleanField(default=True, verbose_name='ESSA ATIVIDADE ESTÁ DIPONÍVEL')
    
    def __str__(self) -> str:
        return self.atividade
    
    def save(self, *args, **kwargs) -> None:
        self.atividade = self.atividade.strip()
        return super().save(*args, **kwargs)

class Ficha(models.Model):
    # FICHA DE INSCRIÇÃO DE CAPACITAÇÃO
    nome_completo = models.CharField(max_length=100, verbose_name='NOME COMPLETO:')
    cpf = models.CharField(max_length=11, verbose_name='CADASTRO DE PESSOA FÍSICA (CPF):')
    genero = models.CharField(max_length=20, choices=(('M', 'Masculino'), ('F', 'Feminino')), verbose_name='GÊNERO:')
    data_nascimento = models.DateField(verbose_name='DATA DE NASCIMENTO:')
    escolaridade = models.CharField(max_length=50, choices=(
        ('fundamental', 'Ensino Fundamental'),
        ('medio', 'Ensino Médio'),
        ('graduacao', 'Graduação'),
        ('pos_graduacao', 'Pós-Graduação')
    ), verbose_name='ESCOLARIDADE:')
    atividade = models.ForeignKey(Atividade, on_delete=models.PROTECT, verbose_name='ATIVIDADE QUE ATUA OU DESEJA ATUAR:')
    endereco = models.CharField(max_length=100, verbose_name='ENDEREÇO RESIDENCIAL:')
    complemento = models.CharField(max_length=100, blank=True, null=True, verbose_name='COMPLEMENTO:')
    bairro = models.CharField(max_length=100, verbose_name='BAIRRO:')
    cep = models.CharField(max_length=8, verbose_name='CEP:')
    uf = models.CharField(max_length=2, choices=(
        ('AC', 'Acre'),
        ('AL', 'Alagoas'),
        ('AP', 'Amapá'),
        ('AM', 'Amazonas'),
        ('BA', 'Bahia'),
        ('CE', 'Ceará'),
        ('DF', 'Distrito Federal'),
        ('ES', 'Espírito Santo'),
        ('GO', 'Goiás'),
        ('MA', 'Maranhão'),
        ('MT', 'Mato Grosso'),
        ('MS', 'Mato Grosso do Sul'),
        ('MG', 'Minas Gerais'),
        ('PA', 'Pará'),
        ('PB', 'Paraíba'),
        ('PR', 'Paraná'),
        ('PE', 'Pernambuco'),
        ('PI', 'Piauí'),
        ('RJ', 'Rio de Janeiro'),
        ('RN', 'Rio Grande do Norte'),
        ('RS', 'Rio Grande do Sul'),
        ('RO', 'Rondônia'),
        ('RR', 'Roraima'),
        ('SC', 'Santa Catarina'),
        ('SP', 'São Paulo'),
        ('SE', 'Sergipe'),
        ('TO', 'Tocantins'),
    ), verbose_name=' UF:')
    contato = models.CharField(max_length=11, verbose_name='CONTATO:')
    email = models.EmailField(max_length=254, verbose_name='E-MAIL:')
    interesse_ter_negocio = models.CharField(max_length=1, choices=(
        ('s', 'SIM'), ('n', 'NÃO')
    ), verbose_name='O INTERESSADO TEM INTERESSE EM POSSUIR UM NEGÓCIO?')

    preferencia_aula = models.CharField(max_length=20, choices=(('online', 'Online'), ('presencial', 'Presencial')), verbose_name='VOCÊ PREFERE ASSISTIR AULAS ONLINE OU PRESENCIAIS?')
    meio_comunicacao_aula = models.CharField(max_length=20, choices=(('whatsapp', 'WhatsApp'), ('email', 'Email')), verbose_name='VOCÊ GOSTARIA QUE ENVIÁSSEMOS O LINK PARA AS AULAS POR?')
    assistir_online = models.CharField(max_length=1, choices=(
        ('s', 'SIM'), ('n', 'NÃO')), verbose_name='TEM CONDIÇÕES DE ASSISTIR AULAS ONLINE?')
    if_true_assistir_casa = models.CharField(max_length=10, blank=True, null=True, choices=(
        ('computador', 'Computador'),
        ('celular', 'Celular'),
        ('tablet', 'Tablet'),
        ('outro', 'Outro')
    ), verbose_name='SE VOCÊ RESPONDEU “SIM” À PERGUNTA ANTERIOR, POR ONDE VOCÊ ASSISTIRIA ÀS AULAS ONLINE?')

    # DADOS PESSOA JURÍDICA
    nome_fantasia = models.CharField(max_length=100, blank=True, null=True, verbose_name='NOME FANTASIA')
    cnpj = models.CharField(max_length=14, blank=True, null=True, verbose_name='CNPJ:')
    situacao_empresa = models.CharField(max_length=50, blank=True, null=True, choices=(
        ('ativa', 'Ativa'),
        ('n_ativa', 'Não Ativa')
    ), verbose_name='SITUAÇÃO DA EMPRESA:')
    porte_empresa = models.CharField(max_length=50, blank=True, null=True, choices=(
        ('MEI', 'Microempreendedor individual (MEI)'),
        ('ME', 'Microempresa (ME)')
    ), verbose_name='PORTE:')
    data_abertura = models.DateField(blank=True, null=True, verbose_name='DATA ABERTURA:')
    cnae_principal = models.CharField(max_length=7, blank=True, null=True, verbose_name='CNAE PRINCIPAL (Classificação Nacional de Atividades  Econômicas):')
    setor = models.CharField(max_length=50, blank=True, null=True, choices=(
        ('comercio', 'Comércio'),
        ('servico', 'Serviço'),
        ('agronegocios', 'Agronegócios'),
        ('industria', 'Indústria')
    ), verbose_name='SETOR:')
    tipo_vinculo = models.CharField(max_length=50, blank=True, null=True, choices=(
        ('representante', 'Representante'),
        ('responsavel', 'Responsável')
    ), verbose_name='TIPO DE VÍNCULO')

    # Extra

    # Módulos de Capacitação
    modulo_marketing = models.BooleanField(default=False, verbose_name='Marketing (Como dominar o mercado digital)')
    modulo_financeiro = models.BooleanField(default=False, verbose_name='Financeiro (Domine o fluxo de caixa de sua empresa)')
    modulo_planejamento = models.BooleanField(default=False, verbose_name='Planejamento (Modelo de negócio que funciona, aprenda a fazer o seu)')
    modulo_outros = models.BooleanField(default=False, verbose_name='Outros')

    # Declaração de ciência e autorização
    responsabilizacao = models.BooleanField(default=False, verbose_name='Declaro estar CIENTE de que sou plenamente responsável pela veracidade das informações aqui prestadas, vez que serão comprovadas no início da capacitação, e de que a falsidade das informações acima implicará sanções cabíveis de natureza civil, administrativa e criminal.')
    manejo_dados = models.BooleanField(default=False, verbose_name='Declaro estar CIENTE de que, em razão da parceria com o SEBRAE, a responsabilidade pelo manejo dos dados supra solicitados é compartilhada entre o SEBRAE e a Coordenadoria de Empreendedorismo e Sustentabilidade de Negócios (COESNE), na Secretaria Municipal do Desenvolvimento Econômico (SDE), caso seja verificada a necessidade de alterações.')
    armazenamento_dados = models.BooleanField(default=False, verbose_name='DECLARO estar CIENTE quanto ao armazenamento dos meus dados no banco de cadastro da COESNE e pelo SEBRAE, para a formulação futura de políticas públicas com foco em públicos específicos, e para que EU seja informado(a) sobre a execução de novos projetos pela COESNE, respeitada a confidencialidade dos dados, que somente serão tratados por colaboradores formalmente autorizados no âmbito da SDE.')
    autorizacao = models.BooleanField(default=False, verbose_name='AUTORIZO ao SEBRAE o armazenamento e a utilização dos meus dados com a finalidade de oferecer produtos e serviços do seu interesse, realizar pesquisas relacionadas ao seu atendimento, realizar comunicações oficiais pelo SEBRAE ou por nossos prestadores de serviços por meio de diversos canais de comunicação e enriquecer o seu cadastro a partir de base de dados controladas pelo SEBRAE.')
    comunicacao = models.CharField(max_length=1, choices=(
        ('s', 'Sim, eu concordo.'), ('n', 'Não, eu não concordo.')
    ), verbose_name='Você autoriza que as comunicações sejam realizadas por meio de ligação, mensagem instantânea e e-mail?')

    # Data de criação da ficha
    data_criacao = models.DateTimeField(auto_now_add=True, verbose_name='Data de criação da ficha')

    def __str__(self) -> str:
        return self.nome_completo
    
    def clean_list(self, fields: list) -> None:
        for field in fields:
            if getattr(self, field) and not str(getattr(self, field)).isnumeric():
                raise ValidationError({field: 'Deve conter somente números!'})

    def clean(self):
        self.clean_list(
            ('cpf', 'cep', 'cnpj', 'cnae_principal')
        )

    def save(self, *args, **kwargs) -> None:
        self.nome_completo = self.nome_completo.upper()
        super().save(*args, **kwargs)
