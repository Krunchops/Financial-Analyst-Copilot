import asyncio
import aiohttp
import os
from dotenv import load_dotenv
load_dotenv()
api_key=os.getenv("FMP_API_KEY")
BASE_URL=("https://financialmodelingprep.com/stable") #domains remain the same, endpoints change

async def fetch_stock_quote(symbol):
    url=(f"{BASE_URL}/search-symbol")
    params={
    "query":symbol,
    "apikey":api_key
}
    async with aiohttp.ClientSession() as session:
        async with session.get(url,params=params) as response:
            data=await response.json()
            if not data:
                return{
                    "symbol":symbol,
                    "price":"No Data Found"
                }
            stock_data=data[0]
            normalized_data={
                "symbol":stock_data.get("symbol"),
                "currency":stock_data.get("currency"),
                "company_name":stock_data.get("name")
            }
            return normalized_data

async def fetch_company_profile(cik:str):
    url=(f"{BASE_URL}/search-cik")
    params={
        "cik":cik,
        "apikey":api_key
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url,params=params) as response:
            data=await response.json()
            if not data:
                return{
                    "error_message":"DATA NOT FOUND"
                }
            stock_data=data[0]
            normalized_data={
                "cik":stock_data.get("cik"),
                "Exchange":stock_data.get("exchangeFullName"),

            }
            return normalized_data


async def get_company_research(symbol,cik):
    quote_data,profile_data=await asyncio.gather(fetch_stock_quote(symbol),
        fetch_company_profile(cik),
        # fetch_stock_quote("TSLA"),

        # fetch_stock_quote("NVDA"),

        return_exceptions=True)
    research_data={
        'quote':quote_data,
        'profile':profile_data
    }
    return research_data
