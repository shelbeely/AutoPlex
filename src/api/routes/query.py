from fastapi import APIRouter, HTTPException
from src.api.schemas import QueryRequest, QueryResponse
from src.db.repositories import MediaRepository
from src.utils.logging import get_logger
from typing import Any
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_openrouter import ChatOpenRouter

# Initialize router and logger
router = APIRouter()
log = get_logger(__name__)

# Initialize repository
media_repo = MediaRepository()

# Initialize LLM for query translation
llm = ChatOpenRouter(
    model_name="qwen/qwen3-235b-a22b:free",
    openrouter_api_key=os.getenv("OPENROUTER_API_KEY")
)

# Prompt template for natural language to SQL translation
query_prompt = PromptTemplate(
    input_variables=["query", "media_type"],
    template="""
    You are a media query assistant for AutoPlex. Convert the natural language query to SQL filters.
    
    Query: {query}
    Media Type: {media_type}
    
    Return a JSON object with:
    - sql_filters: SQL WHERE clause conditions
    - parameters: Dictionary of parameter values
    
    Example:
    For "Find me 80s sci-fi movies under 2 hours", return:
    {{
      "sql_filters": "release_year BETWEEN 1980 AND 1989 AND genres LIKE '%sci-fi%' AND runtime_minutes < 120",
      "parameters": {{}}
    }}
    
    Only return the JSON object without any additional text.
    """
)

query_chain = LLMChain(llm=llm, prompt=query_prompt)

@router.post("/natural", response_model=QueryResponse)
async def natural_query(query_request: QueryRequest):
    """
    Process a natural language query and return relevant media results.
    
    Converts natural language to SQL filters using LLM and executes against the database.
    """
    log.info(f"Processing natural language query: {query_request.query}")
    
    try:
        # Get SQL filters from LLM
        llm_response = await query_chain.acall({
            "query": query_request.query,
            "media_type": query_request.media_type or "all"
        })
        
        # Parse LLM response
        sql_filters = llm_response.get("sql_filters", "")
        parameters = llm_response.get("parameters", {})
        
        # Execute query
        results = media_repo.advanced_search(
            media_type=query_request.media_type,
            filters=sql_filters,
            params=parameters,
            skip=query_request.filters.get("skip", 0),
            limit=query_request.filters.get("limit", 100)
        )
        
        # Format response
        return QueryResponse(
            results=results,
            count=len(results),
            query_time=0.0  # Would be populated with actual timing
        )
        
    except Exception as e:
        log.error(f"Error processing query: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/filters")
async def get_filter_options(media_type: str):
    """
    Get available filter options for a specific media type.
    
    Returns: Dictionary of filter categories and available options
    """
    log.info(f"Fetching filter options for {media_type}")
    
    try:
        filters = media_repo.get_filter_options(media_type)
        return {"filters": filters}
    except Exception as e:
        log.error(f"Error fetching filter options: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

# Beginner's Tip: This route shows how we combine natural language processing with structured database queries.
# The LLM acts as a translator between human language and SQL, making the system accessible to non-technical users! 🤖💬

# Fun Fact: The first chatbot ELIZA was created in 1966 and could simulate a conversation by simply rephrasing user inputs!
