import os
import django
from faker import Faker
import random

# Configurando o Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from capacita.models import Ficha, Atividade

fake = Faker('pt_BR')

def gerar_ficha():
    atividade = random.choice(Atividade.objects.all())
    return Ficha(
        nis=''.join(random.choices('0123456789', k=11)),
        nome_completo=fake.name().upper(),
        cpf=''.join(filter(str.isdigit, fake.cpf()))[:11],  # Garantindo que o CPF tenha no máximo 11 caracteres
        genero=random.choice(['M', 'F']),
        data_nascimento=fake.date_of_birth(minimum_age=18, maximum_age=70),
        escolaridade=random.choice(['FUNDAMENTAL', 'MEDIO', 'GRADUACAO', 'POS_GRADUACAO']),
        atividade=atividade,
        endereco=fake.street_address().upper(),
        complemento=fake.street_suffix().upper() if fake.boolean() else None,  # Usando street_suffix para gerar complemento ou None
        bairro=fake.bairro().upper(),
        cep=''.join(filter(str.isdigit, fake.postcode()))[:8],  # Garantindo que o CEP tenha no máximo 8 caracteres
        uf=random.choice(['AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI', 'RJ', 'RN', 'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO']),
        celular=''.join(filter(str.isdigit, fake.cellphone_number()))[:11],  # Garantindo que o celular tenha no máximo 11 caracteres
        fixo=''.join(filter(str.isdigit, fake.phone_number()))[:10] if fake.boolean() else None,  # Garantindo que o fixo tenha no máximo 10 caracteres ou None
        email=fake.email().lower(),
        interesse_ter_negocio=random.choice(['S', 'N']),
        preferencia_aula=random.choice(['ONLINE', 'PRESENCIAL']),
        meio_comunicacao_aula=random.choice(['WHATSAPP', 'EMAIL']),
        assistir_online=random.choice(['S', 'N']),
        if_true_assistir_casa=random.choice(['COMPUTADOR', 'CELULAR', 'TABLET', 'OUTRO']) if fake.boolean() else None,
        nome_fantasia=fake.company().upper() if fake.boolean() else None,
        cnpj=''.join(filter(str.isdigit, fake.cnpj()))[:14] if fake.boolean() else None,  # Garantindo que o CNPJ tenha no máximo 14 caracteres ou None
        situacao_empresa=random.choice(['ATIVA', 'N_ATIVA']) if fake.boolean() else None,
        porte_empresa=random.choice(['MEI', 'ME']) if fake.boolean() else None,
        data_abertura=fake.date_this_century() if fake.boolean() else None,
        cnae_principal=''.join(random.choices('0123456789', k=7)) if fake.boolean() else None,  # Gerando cnae_principal com exatamente 7 dígitos ou None
        setor=random.choice(['COMERCIO', 'SERVICO', 'AGRONEGOCIOS', 'INDUSTRIA']) if fake.boolean() else None,
        tipo_vinculo=random.choice(['REPRESENTANTE', 'RESPONSAVEL']) if fake.boolean() else None,
        modulo_marketing=fake.boolean(),
        modulo_financeiro=fake.boolean(),
        modulo_planejamento=fake.boolean(),
        modulo_outros=fake.boolean(),
        responsabilizacao=fake.boolean(),
        manejo_dados=fake.boolean(),
        armazenamento_dados=fake.boolean(),
        autorizacao=fake.boolean(),
        comunicacao=random.choice(['S', 'N']),
    )

# Gerando 150 fichas
fichas = [gerar_ficha() for _ in range(150)]

# Salvando as fichas no banco de dados
Ficha.objects.bulk_create(fichas)

print("150 fichas geradas com sucesso!")
