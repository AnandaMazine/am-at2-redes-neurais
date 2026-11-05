from typing import Literal
from pydantic import BaseModel, Field

class ReservaInput(BaseModel):
    lead_time: int = Field(ge=0, description="Dias entre a reserva e a chegada prevista", examples=[30])
    stays_in_weekend_nights: int = Field(ge=0, description="Qutidade de noites de fim de semana", examples=[3])
    stays_in_week_nights: int = Field(ge=0, description="Qutidade de noites durante a semana", examples=[3])
    adults: int = Field(ge=0, description="Qutidade de adultos", examples=[2])
    hotel: Literal["City Hotel", "Resort Hotel"] = Field(description="Tipo de hotel", examples=["Resort Hotel"])
    market_segment: Literal["Direct", "Corporate", "Online TA", "Offline TA/TO", "Complementary", "Groups", "Undefined", "Aviation"] = Field(description="Segmento de mercado da reserva", examples=["Online TA"])
    
class ReservaOutput(BaseModel):
    classe_predita: int = Field(description="0 para não cancelada e 1 para cancelada")
    probabilidade: float = Field(ge=0.0, le=1.0, description="Probabilidade estimada da classe predita")