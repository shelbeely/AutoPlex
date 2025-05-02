from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from datetime import datetime

# Media Schemas
class MovieBase(BaseModel):
    title: str
    original_title: Optional[str] = None
    summary: Optional[str] = None
    genres: List[str] = []
    keywords: List[str] = []
    release_year: Optional[int] = None
    release_date: Optional[datetime] = None
    content_rating: Optional[str] = None
    external_ids: Dict[str, str] = {}
    file_path: Optional[str] = None
    file_size: Optional[int] = None
    rating: Optional[float] = None
    user_rating: Optional[float] = None
    play_count: Optional[int] = None
    last_played: Optional[datetime] = None
    runtime_minutes: Optional[int] = None
    aspect_ratio: Optional[str] = None
    studio: Optional[str] = None
    directors: List[str] = []
    writers: List[str] = []
    producers: List[str] = []
    cast: List[str] = []
    voice_actors: List[str] = []
    audio_languages: List[str] = []
    subtitle_languages: List[str] = []
    resolution: Optional[str] = None
    format: Optional[str] = None
    codec: Optional[str] = None

class MovieCreate(MovieBase):
    title: str
    release_year: int

class MovieUpdate(MovieBase):
    pass

class MovieOut(MovieBase):
    id: int
    added_date: datetime
    updated_date: datetime

    class Config:
        from_attributes = True

# TV Show Schemas
class TVShowBase(BaseModel):
    title: str
    original_title: Optional[str] = None
    summary: Optional[str] = None
    genres: List[str] = []
    keywords: List[str] = []
    release_year: Optional[int] = None
    release_date: Optional[datetime] = None
    content_rating: Optional[str] = None
    external_ids: Dict[str, str] = {}
    file_path: Optional[str] = None
    file_size: Optional[int] = None
    rating: Optional[float] = None
    user_rating: Optional[float] = None
    play_count: Optional[int] = None
    last_played: Optional[datetime] = None
    first_air_date: Optional[datetime] = None
    last_air_date: Optional[datetime] = None
    seasons_count: Optional[int] = None
    episodes_count: Optional[int] = None
    status: Optional[str] = None
    runtime_per_episode: Optional[int] = None
    networks: List[str] = []
    production_companies: List[str] = []
    creators: List[str] = []
    showrunners: List[str] = []
    producers: List[str] = []
    cast: List[str] = []
    guest_stars: List[str] = []

class TVShowCreate(TVShowBase):
    title: str
    release_year: int

class TVShowUpdate(TVShowBase):
    pass

class TVShowOut(TVShowBase):
    id: int
    added_date: datetime
    updated_date: datetime

    class Config:
        from_attributes = True

# Music Schemas
class MusicBase(BaseModel):
    title: str
    original_title: Optional[str] = None
    summary: Optional[str] = None
    genres: List[str] = []
    keywords: List[str] = []
    release_year: Optional[int] = None
    release_date: Optional[datetime] = None
    content_rating: Optional[str] = None
    external_ids: Dict[str, str] = {}
    file_path: Optional[str] = None
    file_size: Optional[int] = None
    rating: Optional[float] = None
    user_rating: Optional[float] = None
    play_count: Optional[int] = None
    last_played: Optional[datetime] = None
    album: Optional[str] = None
    artist: Optional[str] = None
    album_artist: Optional[str] = None
    track_number: Optional[int] = None
    disc_number: Optional[int] = None
    duration_seconds: Optional[int] = None
    composers: List[str] = []
    producers: List[str] = []
    featured_artists: List[str] = []
    audio_codec: Optional[str] = None
    bitrate: Optional[int] = None
    sample_rate: Optional[int] = None
    channels: Optional[int] = None
    album_art_url: Optional[str] = None

class MusicCreate(MusicBase):
    title: str
    artist: str
    release_year: int

class MusicUpdate(MusicBase):
    pass

class MusicOut(MusicBase):
    id: int
    added_date: datetime
    updated_date: datetime

    class Config:
        from_attributes = True

# Query Schemas
class QueryRequest(BaseModel):
    query: str
    media_type: Optional[str] = None
    filters: Dict[str, Any] = {}

class QueryResponse(BaseModel):
    results: List[Dict[str, Any]]
    count: int
    query_time: float

# Recommendation Schemas
class RecommendRequest(BaseModel):
    user_id: str
    history: List[str] = []
    preferences: Dict[str, Any] = {}

class RecommendResponse(BaseModel):
    recommendations: List[Dict[str, Any]]
    explanation: str
    media_type: str

# Request Schemas
class RequestMedia(BaseModel):
    title: str
    media_type: str
    year: Optional[int] = None
    external_id: Optional[str] = None

class RequestResponse(BaseModel):
    success: bool
    message: str
    request_id: Optional[str] = None

# General Response Schemas
class SuccessResponse(BaseModel):
    success: bool
    message: str

class ErrorDetails(BaseModel):
    error: str
    detail: Optional[str] = None

class StandardResponse(BaseModel):
    response: SuccessResponse
    data: Optional[Any] = None
    error: Optional[ErrorDetails] = None

# Beginner's Tip: These Pydantic models are like the skeleton of our API - they help us make sure all our data is dressed properly before it goes out in public! 👗✨

# Fun Fact: Pydantic was named after the ancient Greek sculptor Pydantic, who was known for his attention to detail - just like our data validation! 🎨
