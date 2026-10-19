# Pipeline ETL: Taxa de Desocupação (PNADC/IBGE)

Pipeline de dados que extrai a **taxa de desocupação** de Pernambuco, por sexo, da API de Dados Agregados do IBGE (SIDRA), guarda o dado bruto em um banco documental e publica o dado tratado em bancos relacionais.

Projeto da disciplina **Engenharia de Dados** (CESAR School, 2026.2), construído a partir do material do professor Marco Mialaret.

**Autor:** SEU NOME

## Arquitetura

```
API IBGE ──Load──▶ MongoDB Atlas ──▶ Transform (DataFrame) ──Load──▶ Neon (Postgres)
              (camada Bronze)                              └──────▶ SQLite local
                                                            (camada Silver)
```

| Camada | Destino | Conteúdo |
|---|---|---|
| Bronze | MongoDB Atlas (banco `IBGE`, coleção `PNADC`) | JSON bruto, como veio da API |
| Silver (nuvem) | Neon / PostgreSQL (tabela `pnadc`) | Dado tratado e tipado |
| Silver (local) | SQLite (`data/pnadc.db`, tabela `pnadc`) | Réplica local do dado tratado |

## Fonte dos dados

- API: `https://servicodados.ibge.gov.br/api/v3/agregados/4093/periodos/201201-202601/variaveis/4099`
- Agregado 4093: PNAD Contínua trimestral
- Variável 4099: taxa de desocupação, na semana de referência, de pessoas com 14 anos ou mais
- Filtros: `localidades=N3[26]` (Pernambuco) e `classificacao=2[all]` (Total, Homens e Mulheres)

## Tabela final (`pnadc`)

| Coluna | Tipo | Descrição |
|---|---|---|
| `periodo` | timestamp | Primeiro dia do trimestre (ex.: 2012-01-01) |
| `valor` | double | Taxa de desocupação (%) |
| `ano` | texto | Ano (ex.: 2012) |
| `tri` | inteiro | Trimestre (1 a 4) |
| `sexo` | texto | Total, Homens ou Mulheres |

## Estrutura do projeto

```
.
├── main.py              # orquestra a pipeline
├── src/
│   ├── extract.py       # API do IBGE e leitura do Mongo
│   ├── transform.py     # JSON aninhado -> DataFrame
│   └── load.py          # Mongo, SQLite e Neon
├── Requirements.txt
├── .env.example         # modelo das variáveis de ambiente
└── .gitignore
```

## Como executar

**Requisitos:** Python 3.12 ou superior, uma conta no MongoDB Atlas (cluster gratuito M0) e uma conta no Neon (plano gratuito).

```powershell
# 1. Ambiente virtual
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# 2. Dependências
pip install -r Requirements.txt

# 3. Variáveis de ambiente
Copy-Item .env.example .env
# edite o .env com as suas credenciais

# 4. Executar
python main.py
```

Se o PowerShell bloquear a ativação do ambiente, rode antes `Set-ExecutionPolicy -Scope Process Bypass`.

## Variáveis de ambiente (`.env`)

| Variável | Descrição |
|---|---|
| `SQLITE_PATH` | Caminho do arquivo SQLite (padrão `data/pnadc.db`) |
| `MONGO_URI` | String de conexão do MongoDB Atlas |
| `NEON_URL` | String de conexão do Neon (conexão direta, sem `-pooler`) |

O `.env` nunca deve ser enviado ao repositório (já está no `.gitignore`).

## Saída esperada

```
Dados extraídos da API do IBGE
Dados salvos na camada Bronze!
Extração da camada bronze efetuada com sucesso!
Dados transformados com Sucesso!
Dados salvos na camada Silver Local!
Dados salvos na camada Silver Núvem!
```

A carga substitui os dados a cada execução (`delete_many` no Mongo e `if_exists="replace"` nas tabelas), então rodar a pipeline de novo não duplica registros.

## Problemas conhecidos

- **Erro de SSL ao chamar o IBGE** (`CERTIFICATE_VERIFY_FAILED`): o projeto usa a biblioteca `truststore`, que faz o Python usar os certificados do Windows.
- **Timeout ou `SSL handshake failed` no Mongo Atlas**: o IP da sua rede precisa estar liberado em *Network Access* no Atlas.
- **Windows 11 bloqueando o SQLAlchemy** (Smart App Control bloqueia os arquivos `.pyd`): na raiz do projeto, rode `Get-ChildItem -Recurse .venv\Lib\site-packages\sqlalchemy -Include *.pyd | Remove-Item`.

## Tecnologias

Python, requests, pandas, PyMongo, SQLAlchemy, MongoDB Atlas, Neon (PostgreSQL), SQLite.
