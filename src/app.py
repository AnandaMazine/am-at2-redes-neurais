from contextlib import asynccontextmanager
from pathlib import Path

import joblib
import pandas as pd
from fastapi import FastAPI

from src.schemas import ReservaInput, ReservaOutput

# Localiza o arquivo na pasta models
CAMINHO_MODELO = (Path(__file__).resolve().parent.parent / "models" / "modelo_mlp.joblib")

#lifespan = carrega o pipeline quando o servidor inicia
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Carrega o modelo de machine learning
    app.state.modelo = joblib.load(CAMINHO_MODELO)
    yield
    # Libera recursos do modelo, se necessário
    del app.state.modelo
    
app = FastAPI(
    title="API de Cancelamento de Reservas",
    description="Previsões com uma rede neural para prever o cancelamento de reservas de hotel",
    version="1.0.0",
    lifespan=lifespan
)

@app.get("/info")
def info():
    return {
        "status": "ativo",
        "framework": "FastAPI",
        "modelo": "MLPClassifier"
    }
    
@app.post("/predict", response_model=ReservaOutput)
def prever(reserva: ReservaInput):
    modelo = app.state.modelo
    
    # Transforma a entrada validade em uma tabela com uma reserva
    dados = pd.DataFrame([reserva.model_dump()])
    
    # Obtém a classe prevista e as probalidades
    classe = int(modelo.predict(dados)[0])
    probabilidades = modelo.predict_proba(dados)[0]
    
    # Localiza a probabilidade da classe prevista
    indice_classe = list(modelo.classes_).index(classe)
    probabilidade = float(probabilidades[indice_classe])
    
    return ReservaOutput(classe_predita=classe, probabilidade=probabilidade)
    
    
    
