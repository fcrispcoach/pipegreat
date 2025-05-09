Este projeto implementa uma pipeline completa de validação de dados utilizando:
- **Apache Airflow** para orquestração
- **Great Expectations** para validação de qualidade de dados
- **Python** para transformações ETL

## Pré-requisitos

- Python 3.8+
- Airflow 2.5+
- Great Expectations 0.15+
- Docker (opcional para ambiente containerizado)

## Instalação

1. Clone o repositório:
git clone https://github.com/fcrispcoach/pipegreat.git
cd pipegreat

2. python -m venv venv
source venv/bin/activate  # Linux/Mac

3. Instale as dependências
pip install -r requirements.txt

4. Inicialize o Great Expectations:
great_expectations init

## Configuração

1. Configure as conexões no Airflow:
airflow connections add 'ge_storage' --type fs --extra '{"path": "/path/to/ge_data"}'

2. Edite o arquivo config/config.yml com seus caminhos locais

## Estrutura do Projeto

pipegreat/
├── dags/               # DAGs do Airflow
├── great_expectations/ # Configuração do GE
├── scripts/            # Scripts de ETL e validação
├── data/               # Dados de exemplo
├── config/             # Arquivos de configuração
└── tests/              # Testes automatizados

## Execução

1. Inicie o Airflow:
airflow standalone
