from fastapi import APIRouter, HTTPException
from src.api.schemas import RecommendRequest, RecommendResponse
from src.db.repositories import MediaRepository
from src.utils.logging import get_logger
from typing import Any
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_openrouter import ChatOpenRouter
import os
import json

# Initialize router and logger
router = APIRouter()
log = get_logger(__name__)

# Initialize repository
media_repo = MediaRepository()

# Initialize LLM for recommendations
llm = ChatOpenRouter(
    model_name="qwen/qwen3-235b-a22b:free",
    openrouter_api_key=os.getenv("OPENROUTER_API_KEY")
)

# Prompt template for recommendation generation
recommend_prompt = PromptTemplate(
    input_variables=["user_id", "history", "preferences"],
    template="""
    You are a media recommendation assistant for AutoPlex. Generate personalized media recommendations based on user history and preferences.
    
    User ID: {user_id}
    Watch/Listen History: {history}
    Preferences: {preferences}
    
    Return a JSON object with:
    - recommendations: List of media items with title, reason, media_type, and year
    - explanation: Overall explanation of the recommendation strategy
    
    Example:
    {{
      "recommendations": [
        {{
          "title": "Tenet",
          "reason": "You liked Inception's cerebral themes and visuals.",
          "media_type": "movie",
          "year": 2020
        }}
      ],
      "explanation": "Based on your history of watching cerebral sci-fi movies, I've recommended similar titles with complex narratives."
    }}
    
    Only return the JSON object without any additional text.
    """
)

recommend_chain = LLMChain(llm=llm, prompt=recommend_prompt)

@router.post("/", response_model=RecommendResponse)
async def get_recommendations(recommend_request: RecommendRequest):
    """
    Generate personalized media recommendations based on user history and preferences.
    
    Uses LLM to analyze user history and generate explainable recommendations.
    """
    log.info(f"Generating recommendations for user: {recommend_request.user_id}")
    
    try:
        # Get user history and preferences
        user_history = recommend_request.history or media_repo.get_user_history(recommend_request.user_id)
        user_preferences = recommend_request.preferences or media_repo.get_user_preferences(recommend_request.user_id)
        
        # Generate recommendations using LLM
        llm_response = await recommend_chain.acall({
            "user_id": recommend_request.user_id,
            "history": user_history,
            "preferences": user_preferences
        })
        
        # Parse LLM response
        recommendations = llm_response.get("recommendations", [])
        explanation = llm_response.get("explanation", "No explanation provided")
        
        # Format response
        return RecommendResponse(
            recommendations=recommendations,
            explanation=explanation,
            media_type=recommendations[0].get("media_type", "movie") if recommendations else "movie"
        )
        
    except Exception as e:
        log.error(f"Error generating recommendations: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/rationale")
async def get_recommendation_rationale(media_type: str, filters: dict = None):
    """
    Get the rationale behind recommendations for a specific media type and filters.
    
    Returns: Explanation of how recommendations would be generated based on the provided criteria
    """
    log.info(f"Generating recommendation rationale for {media_type} with filters: {filters}")
    
    try:
        # Get explanation template
        explanation = media_repo.get_recommendation_explanation(media_type, filters)
        return {"explanation": explanation}
    except Exception as e:
        log.error(f"Error fetching recommendation rationale: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

# Beginner's Tip: This route implements the recommendation system that makes AutoPlex truly intelligent. 
# It combines user history with LLM-powered analysis to provide personalized suggestions! 🎯🧠

# Fun Fact: The first movie recommendation system was developed in 1997 by MIT researchers and was called "Movie Critic"!
