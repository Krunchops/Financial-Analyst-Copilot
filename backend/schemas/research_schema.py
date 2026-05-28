from pydantic import BaseModel

class QuoteResponse(BaseModel):
    symbol:str
    currency:str
    company_name:str

class ProfileResponse(BaseModel):
    Exchange: str
    cik: float

class CompanyResearchResponse(BaseModel):
    quote:QuoteResponse
    profile:ProfileResponse