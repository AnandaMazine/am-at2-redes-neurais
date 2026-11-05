# AT2 — Redes Neurais MLP

Projeto da disciplina de Aprendizado de Máquina desenvolvido por Ananda Mazine.

## Objetivo

Treinar uma rede neural MLP para prever o cancelamento de reservas de hotel e disponibilizar as previsões por meio de uma API com FastAPI.

## Dataset

Foi utilizado o dataset **Hotel Booking Demand**, disponível no Kaggle:

https://www.kaggle.com/datasets/jessemostipak/hotel-booking-demand

A base original contém 119.390 registros e 32 colunas. O arquivo está em `data/dataset.csv`.

### Variáveis utilizadas

| Coluna | Descrição |
|---|---|
| lead_time | Dias entre a reserva e a chegada prevista |
| stays_in_weekend_nights | Quantidade de noites reservadas de fim de semana |
| stays_in_week_nights | Quantidade de noites reservadas durante a semana |
| adults | Quantidade de adultos |
| hotel | Tipo de hotel |
| market_segment | Segmento de mercado da reserva |

A variável alvo é `is_canceled`: **0 para não cancelada** e **1 para cancelada**.

As seis variáveis de entrada selecionadas não possuem valores ausentes.

## Tecnologias

- Python e UV
- Pandas e Matplotlib
- Scikit-learn
- Joblib
- FastAPI e Pydantic
- Jupyter Notebook

## Treinamento e avaliação

Os dados foram separados em 75% para treinamento e 25% para teste, utilizando `random_state=42` e estratificação pela variável alvo.

O Pipeline reúne:

- `StandardScaler` para padronizar as variáveis numéricas.
- `OneHotEncoder` para codificar as variáveis categóricas.
- `MLPClassifier` com duas camadas ocultas de 32 e 16 neurônios, ativação ReLU, otimizador Adam, taxa de aprendizado inicial de 0,001 e limite de 500 épocas.

### Resultados no conjunto de teste

**Acurácia: 71,90%.**

| Classe | Precision | Recall | F1-score | Quantidade |
|---|---:|---:|---:|---:|
| Não cancelada | 0,73 | 0,88 | 0,80 | 18.792 |
| Cancelada | 0,69 | 0,44 | 0,54 | 11.056 |

O modelo reconheceu melhor as reservas não canceladas. Identificou aproximadamente 44% dos cancelamentos reais, o que representa uma limitação na detecção dessa classe.

A análise exploratória, o treinamento e a matriz de confusão estão no notebook `notebooks/analise_treinamento.ipynb`.

O Pipeline completo foi salvo em `models/modelo_mlp.joblib`.

## Como executar

É necessário ter Git e UV instalados.

### 1. Clonar o repositório

```bash
git clone https://github.com/AnandaMazine/am-at2-redes-neurais.git
cd am-at2-redes-neurais
```

### 2. Instalar as dependências

```bash
uv sync --locked
```

### 3. Iniciar a API

Na raiz do projeto, execute:

```bash
uv run fastapi dev src/app.py
```

O Pipeline é carregado uma única vez durante a inicialização da aplicação, por meio do Lifespan, e armazenado em `app.state.modelo`.

### 4. Acessar a documentação

Com o servidor em execução, abra:

http://127.0.0.1:8000/docs

## Endpoints

### GET /info

Retorna informações sobre o serviço:

```json
{
  "status": "ativo",
  "framework": "FastAPI",
  "modelo": "MLPClassifier"
}
```

### POST /predict

Recebe os dados de uma reserva:

```json
{
  "lead_time": 30,
  "stays_in_weekend_nights": 2,
  "stays_in_week_nights": 3,
  "adults": 2,
  "hotel": "Resort Hotel",
  "market_segment": "Online TA"
}
```

Exemplo de resposta:

```json
{
  "classe_predita": 0,
  "probabilidade": 0.6563052397546172
}
```

- `classe_predita`: 0 para não cancelada e 1 para cancelada.
- `probabilidade`: probabilidade estimada da classe prevista, entre 0 e 1. Não representa garantia do resultado.

Entradas que não atendem às regras do schema, como antecedência negativa, retornam HTTP 422.

## Testes HTTP

Com a API em execução, abra `requisicoes.http` no VS Code e utilize a extensão REST Client para clicar em **Send Request** em cada bloco.

O arquivo contém:

1. Consulta às informações do serviço.
2. Predição válida para o Perfil A.
3. Predição válida para o Perfil B.
4. Entrada inválida com antecedência negativa.

Todas as requisições incluem o cabeçalho:

```http
User-Agent: Client-Avaliativo
```

Os perfis A e B retornaram classes distintas nos testes realizados. As requisições válidas retornam HTTP 200, e a entrada inválida deve retornar HTTP 422.

## Como reproduzir o treinamento

Na raiz do projeto, execute:

```bash
uv run jupyter notebook
```

Abra `notebooks/analise_treinamento.ipynb` e execute as células em ordem, do início ao fim.

A última etapa salva novamente o Pipeline em `models/modelo_mlp.joblib`. Não é necessário repetir o treinamento para executar a API com o modelo já incluído no repositório.