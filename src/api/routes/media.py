from fastapi import APIRouter, HTTPException
from typing import List
from src.db.repositories import MediaRepository
from src.api.schemas import MovieOut, TVShowOut, MusicOut
from src.utils.logging import get_logger

# Initialize router and logger
router = APIRouter()
log = get_logger(__name__)

# Initialize media repository
media_repo = MediaRepository()  # In a real app, this would be initialized with a DB session

@router.get("/movies", response_model=List[MovieOut])
async def get_movies(skip: int = 0, limit: int = 100):
    """
    Retrieve a list of movies from the database.
    
    Parameters:
    - skip: Number of records to skip (for pagination)
    - limit: Maximum number of records to return
    
    Returns:
    - List of movies in the specified range
    """
    log.info(f"Fetching movies: skip={skip}, limit={limit}")
    try:
        movies = media_repo.get_movies(skip=skip, limit=limit)
        return movies
    except Exception as e:
        log.error(f"Error fetching movies: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/movies/{movie_id}", response_model=MovieOut)
async def get_movie(movie_id: int):
    """
    Retrieve a specific movie by its ID.
    
    Parameters:
    - movie_id: Unique identifier of the movie
    
    Returns:
    - The movie with the specified ID, or 404 if not found
    """
    log.info(f"Fetching movie with ID: {movie_id}")
    movie = media_repo.get_movie(movie_id)
    if not movie:
        log.warning(f"Movie not found: {movie_id}")
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie

@router.get("/tv-shows", response_model=List[TVShowOut])
async def get_tv_shows(skip: int = 0, limit: int = 100):
    """
    Retrieve a list of TV shows from the database.
    
    Parameters:
    - skip: Number of records to skip (for pagination)
    - limit: Maximum number of records to return
    
    Returns:
    - List of TV shows in the specified range
    """
    log.info(f"Fetching TV shows: skip={skip}, limit={limit}")
    try:
        tv_shows = media_repo.get_tv_shows(skip=skip, limit=limit)
        return tv_shows
    except Exception as e:
        log.error(f"Error fetching TV shows: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/tv-shows/{show_id}", response_model=TVShowOut)
async def get_tv_show(show_id: int):
    """
    Retrieve a specific TV show by its ID.
    
    Parameters:
    - show_id: Unique identifier of the TV show
    
    Returns:
    - The TV show with the specified ID, or 404 if not found
    """
    log.info(f"Fetching TV show with ID: {show_id}")
    tv_show = media_repo.get_tv_show(show_id)
    if not tv_show:
        log.warning(f"TV show not found: {show_id}")
        raise HTTPException(status_code=404, detail="TV show not found")
    return tv_show

@router.get("/music", response_model=List[MusicOut])
async def get_music(skip: int = 0, limit: int = 100):
    """
    Retrieve a list of music tracks from the database.
    
    Parameters:
    - skip: Number of records to skip (for pagination)
    - limit: Maximum number of records to return
    
    Returns:
    - List of music tracks in the specified range
    """
    log.info(f"Fetching music tracks: skip={skip}, limit={limit}")
    try:
        music_tracks = media_repo.get_music_tracks(skip=skip, limit=limit)
        return music_tracks
    except Exception as e:
        log.error(f"Error fetching music tracks: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/music/{music_id}", response_model=MusicOut)
async def get_music_track(music_id: int):
    """
    Retrieve a specific music track by its ID.
    
    Parameters:
    - music_id: Unique identifier of the music track
    
    Returns:
    - The music track with the specified ID, or 404 if not found
    """
    log.info(f"Fetching music track with ID: {music_id}")
    music_track = media_repo.get_music(music_id)
    if not music_track:
        log.warning(f"Music track not found: {music_id}")
        raise HTTPException(status_code=404, detail="Music track not found")
    return music_track

# Beginner's Tip: These routes provide the foundation for accessing media data in our API. 
# They follow RESTful principles and include proper error handling and logging.

# Fun Fact: The first movie theater opened in Pittsburgh in 1905 and was called the Nickelodeon - 
# it charged 5 cents (a nickel) for admission! 🎬
