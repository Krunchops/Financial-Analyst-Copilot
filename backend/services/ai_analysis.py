from langchain_groq import ChatGroq
from dotenv import load_dotenv
from langchain_core.messages import(
    SystemMessage,HumanMessage,AIMessage
)
from pydantic import BaseModel,Field
from typing import TypedDict
load_dotenv()
llm=ChatGroq(
    model="llama-3.1-8b-instant"
)
from langgraph.graph import StateGraph,END
class CheckValidityOutput(BaseModel):
    validity_score:int= Field(gt=0 , lt=10)
validity_llm=llm.with_structured_output(CheckValidityOutput)
class AnalysisState(TypedDict):
    research_data:dict
    formatted_context:str
    messages:list
    analysis:str
    retry_count:int
    invalid:bool

def format_context_node(state:AnalysisState):
    research_data=state['research_data']
    quote=research_data['quote']
    profile=research_data['profile']
    formatted_context = f"""

    COMPANY RESEARCH DATA

    Symbol:
    {quote.get('symbol')}

    Company Name:
    {quote.get('company_name')}

    Currency:
    {quote.get('currency')}

    Exchange:
    {profile.get('exchange')}

    CIK:
    {profile.get('cik')}
    """
    return {
        "formatted_context":formatted_context
    }

def build_prompt_node(state:AnalysisState):
    formatted_context=state['formatted_context']
    messages = [

        SystemMessage(
            content=(

                """
                You are an expert financial analyst.

                Analyze the provided company research data.

                Rules:

                - Do not hallucinate.
                - Only use provided context.
                - Keep analysis concise.
                - Mention risks if possible.
                - Use structured sections.

                Output format:

                Summary:
                Risks:
                Market Position:
                """
            )
        ),

        HumanMessage(
            content=formatted_context
        )
    ]

    return {

        "messages": messages
    }
def llm_node(
        state:AnalysisState
):
    messages=state['messages']
    response=llm.invoke(messages)
    return{
        'analysis':response.content
    }
def validator_node(state:AnalysisState):
    analysis=state['analysis']
    retry_count=state.get('retry_count',0)
    invalid=False
    check_validity_Score_prompt=[SystemMessage(content="You are to give a score based on the depth and clarity of analysis given. Return a score between 1 and 9"),HumanMessage(content=f"Analysis:{analysis}")]
    response_of_validity=validity_llm.invoke(check_validity_Score_prompt)
    if response_of_validity.validity_score<3:
        invalid=True
    return{
        'retry_count':retry_count,
        'invalid':invalid
    }

def route_after_validation(state:AnalysisState):
    invalid=state['invalid']
    retry_count=state['retry_count']
    if invalid and retry_count<2:
        return 'retry'
    return 'finish'


def retry_node(state:AnalysisState):
    retry_count=state['retry_count']
    return{
        'retry_count':retry_count+1
    }

graph=StateGraph(
    AnalysisState
)
graph.add_node(
    "formatter",
    format_context_node
)

graph.add_node(
    "prompt_builder",
    build_prompt_node
)

graph.add_node(
    "llm_node",
    llm_node
)

graph.add_node(
    "validator",
    validator_node
)

graph.add_node(
    "retry_node",
    retry_node
)

graph.set_entry_point(
    "formatter"
)

graph.add_edge(
    "formatter",
    "prompt_builder"
)

graph.add_edge(
    "prompt_builder",
    "llm_node"
)

graph.add_edge(
    "llm_node",
    "validator"
)
graph.add_conditional_edges(
    'validator',
    route_after_validation,
    {
        'retry':'retry_node',
        'finish':END
    }
)
graph.add_edge(
    'retry_node','llm_node'
)
workflow=graph.compile()
def generate_financial_analysis(
    research_data
):

    result = workflow.invoke(

        {

            "research_data":
            research_data,

            "retry_count":
            0
        }
    )

    return result[
        "analysis"
    ]