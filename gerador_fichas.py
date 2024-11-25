import os
import django
from faker import Faker
import random

# Configurando o Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from capacita.models import Ficha, ModulosCapacita

fake = Faker('pt_BR')

def criar_modulos_capacita():
    modulos = [
        {
            'nome': 'MARKETING',
            'descricao': 'Como dominar o mercado digital.'
        },
        {
            'nome': 'FINANCEIRO',
            'descricao': 'Domine o fluxo de caixa de sua empresa.'
        },
        {
            'nome': 'PLANEJAMENTO',
            'descricao': 'Modelo de negócio que funciona, aprenda a fazer o seu.'
        },
        {
            'nome': 'GESTÃO DE PESSOAS',
            'descricao': 'Motive e lidere sua equipe.'
        },
        {
            'nome': 'TECNOLOGIA DA INFORMAÇÃO',
            'descricao': 'Inovações tecnológicas para o seu negócio.'
        },
        {
            'nome': 'LOGÍSTICA',
            'descricao': 'Otimize a distribuição e entrega de seus produtos.'
        },
        {
            'nome': 'VENDAS',
            'descricao': 'Técnicas de vendas eficazes para aumentar seus resultados.'
        },
        {
            'nome': 'CONTROLE DE QUALIDADE',
            'descricao': 'Garantia de qualidade nos processos produtivos.'
        }
    ]

    for modulo in modulos:
        ModulosCapacita.objects.create(
            nome=modulo['nome'],
            descricao=modulo['descricao']
        )

def gerar_ficha():
    # Gerando dados pessoais obrigatórios
    ficha = Ficha(
        nome_completo=fake.name().upper(),
        cpf=''.join(filter(str.isdigit, fake.cpf()))[:11],
        genero=random.choice(['M', 'F']),
        data_nascimento=fake.date_of_birth(minimum_age=18, maximum_age=70),
        escolaridade=random.choice(['FUNDAMENTAL', 'MEDIO', 'GRADUACAO', 'POS_GRADUACAO']),
        atividade=random.choice(['ARTESANATO', 'AGRICULTURA_URBANA', 'COMERCIO', 'ESTETICA_E_BELEZA', 'GASTRONOMIA', 'INDUSTRIA', 'SERVICO']),
        cep=''.join(filter(str.isdigit, fake.postcode()))[:8],
        endereco=fake.street_address().upper(),
        complemento=fake.street_suffix().upper() if fake.boolean() else None,
        bairro=fake.bairro().upper(),
        uf=random.choice(['AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI', 'RJ', 'RN', 'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO']),
        celular=''.join(filter(str.isdigit, fake.cellphone_number()))[:11],
        fixo=''.join(filter(str.isdigit, fake.phone_number()))[:10] if fake.boolean() else None,
        email=fake.email().lower(),
        interesse_ter_negocio=random.choice(['S', 'N']),
        preferencia_aula=random.choice(['ONLINE', 'PRESENCIAL']),
        meio_comunicacao_aula=random.choice(['WHATSAPP', 'EMAIL']),
        assistir_online='S' if random.choice([True, False]) else 'N',
        modulo_capacita=random.choice(ModulosCapacita.objects.all()),
        data_criacao=fake.date_this_year()
    )

    if ficha.assistir_online == 'S':
        ficha.if_true_assistir_casa = random.choice(['COMPUTADOR', 'CELULAR', 'TABLET', 'OUTRO'])

    # Se for preencher os dados jurídicos, todos os campos devem ser preenchidos
    preencher_dados_juridicos = random.choice([True, False])
    if preencher_dados_juridicos:
        ficha.nome_fantasia = fake.company().upper()
        ficha.cnpj = ''.join(filter(str.isdigit, fake.cnpj()))[:14]
        ficha.situacao_empresa = random.choice(['ATIVA', 'N_ATIVA'])
        ficha.porte_empresa = random.choice(['MEI', 'ME'])
        ficha.data_abertura = fake.date_this_century()
        ficha.cnae_principal = ''.join(random.choices('0123456789', k=7))
        ficha.setor = random.choice(['COMERCIO', 'SERVICO', 'AGRONEGOCIOS', 'INDUSTRIA'])
        ficha.tipo_vinculo = random.choice(['REPRESENTANTE', 'RESPONSAVEL'])

    ficha.save()
    return ficha

# Criando os módulos de aprendizagem se não existirem
criar_modulos_capacita()

# Gerando 150 fichas
for _ in range(150):
    gerar_ficha()

print('150 fichas geradas com sucesso!')
