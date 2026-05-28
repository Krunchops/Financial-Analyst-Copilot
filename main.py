from fastapi import FastAPI
app=FastAPI()
from backend.schemas.research_schema import (CompanyResearchResponse)
from backend.services.market_data import(
    get_company_research
)
from backend.services.ai_analysis import(
    generate_financial_analysis
)
@app.get("/research/{symbol}/{cik}")
async def research(symbol:str,cik:str):
    research_data=await get_company_research(symbol,cik)
    analysis=generate_financial_analysis(research_data)
    return{
        'research_data':research_data,
        'ai_analysis':analysis
    }