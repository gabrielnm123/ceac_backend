import os
import django
from faker import Faker
import random

# Configurando o Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from capacita.models import Ficha, ModulosAprendizagem, FichaModulo

fake = Faker('pt_BR')

def criar_modulos_aprendizagem():
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
        ModulosAprendizagem.objects.get_or_create(
            nome=modulo['nome'],
            defaults={'descricao': modulo['descricao']}
        )

def gerar_ficha():
    ficha = Ficha(
        nome_completo=fake.name().upper(),
        cpf=''.join(filter(str.isdigit, fake.cpf()))[:11],
        genero=random.choice(['M', 'F']),
        data_nascimento=fake.date_of_birth(minimum_age=18, maximum_age=70),
        escolaridade=random.choice(['FUNDAMENTAL', 'MEDIO', 'GRADUACAO', 'POS_GRADUACAO']),
        atividade=random.choice(['ARTESANATO', 'AGRICULTURA URBANA', 'COMÉRCIO', 'ESTÉTICA E BELEZA', 'GASTRONOMIA', 'INDÚSTRIA', 'SERVIÇO']),
        endereco=fake.street_address().upper(),
        complemento=fake.street_suffix().upper() if fake.boolean() else None,
        bairro=fake.bairro().upper(),
        cep=''.join(filter(str.isdigit, fake.postcode()))[:8],
        uf=random.choice(['AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI', 'RJ', 'RN', 'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO']),
        celular=''.join(filter(str.isdigit, fake.cellphone_number()))[:11],
        fixo=''.join(filter(str.isdigit, fake.phone_number()))[:10] if fake.boolean() else None,
        email=fake.email().lower(),
        interesse_ter_negocio=random.choice(['S', 'N']),
        preferencia_aula=random.choice(['ONLINE', 'PRESENCIAL']),
        meio_comunicacao_aula=random.choice(['WHATSAPP', 'EMAIL']),
        assistir_online=random.choice(['S', 'N']),
        if_true_assistir_casa=random.choice(['COMPUTADOR', 'CELULAR', 'TABLET', 'OUTRO']) if fake.boolean() else None,
        nome_fantasia=fake.company().upper() if fake.boolean() else None,
        cnpj=''.join(filter(str.isdigit, fake.cnpj()))[:14] if fake.boolean() else None,
        situacao_empresa=random.choice(['ATIVA', 'N_ATIVA']) if fake.boolean() else None,
        porte_empresa=random.choice(['MEI', 'ME']) if fake.boolean() else None,
        data_abertura=fake.date_this_century() if fake.boolean() else None,
        cnae_principal=''.join(random.choices('0123456789', k=7)) if fake.boolean() else None,
        setor=random.choice(['COMERCIO', 'SERVICO', 'AGRONEGOCIOS', 'INDUSTRIA']) if fake.boolean() else None,
        tipo_vinculo=random.choice(['REPRESENTANTE', 'RESPONSAVEL']) if fake.boolean() else None,
    )
    ficha.save()

    # Associando os módulos de aprendizagem
    modulos = ModulosAprendizagem.objects.filter(disponivel=True)
    for modulo in random.sample(list(modulos), k=random.randint(0, len(modulos))):
        FichaModulo.objects.create(ficha=ficha, modulo=modulo)

    return ficha

# Criando os módulos de aprendizagem se não existirem
criar_modulos_aprendizagem()

# Gerando 150 fichas
for _ in range(150):
    gerar_ficha()

print("150 fichas geradas com sucesso!")
