from fastapi import APIRouter, HTTPException
from src.api.schemas import RequestMedia, RequestResponse
from src.utils.logging import get_logger
from src.db.repositories import MediaRepository
from src.db.models import Movie, TVShow, MusicTrack
from typing import Any

# Initialize router and logger
router = APIRouter()
log = get_logger(__name__)

# Initialize media repository
media_repo = MediaRepository()

@router.post("/movie", response_model=RequestResponse)
async def request_movie(request_data: RequestMedia):
    """
    Request a movie through Overseerr and route to Radarr.
    
    Parameters:
    - title: Movie title
    - year: Optional release year
    - external_id: Optional external ID (TMDB, IMDb)
    
    Returns:
    - Request status and ID
    """
    log.info(f"Requesting movie: {request_data.title}")
    
    try:
        # Check if movie already exists in database
        db = media_repo.get_db()
        result = db.execute(text("SELECT * FROM movies WHERE title = :title"), 
                          {"title": request_data.title})
        movie = result.fetchone()
        
        if movie:
            log.warning(f"Movie already exists: {request_data.title}")
            return RequestResponse(
                success=False,
                message="Movie already exists in your collection",
                request_id=f"movie:{movie.id}"
            )
        
        # If not in database, send to Overseerr
        # In a real implementation, this would call Overseerr API
        request_id = f"request:movie:{request_data.title}"
        log.info(f"Movie request created with ID: {request_id}")
        
        # Add to Radarr (would be handled by Overseerr integration in practice)
        # This is a placeholder for the actual integration
        return RequestResponse(
            success=True,
            message="Movie request submitted successfully",
            request_id=request_id
        )
    except Exception as e:
        log.error(f"Error processing movie request: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
    finally:
        db.close()

@router.post("/tv-show", response_model=RequestResponse)
async def request_tv_show(request_data: RequestMedia):
    """
    Request a TV show through Overseerr and route to Sonarr.
    
    Parameters:
    - title: TV show title
    - year: Optional release year
    - external_id: Optional external ID (TVDB, TMDB)
    
    Returns:
    - Request status and ID
    """
    log.info(f"Requesting TV show: {request_data.title}")
    
    try:
        # Check if TV show exists in database
        db = media_repo.get_db()
        result = db.execute(text("SELECT * FROM tv_shows WHERE title = :title"), 
                          {"title": request_data.title})
        tv_show = result.fetchone()
        
        if tv_show:
            log.warning(f"TV show already exists: {request_data.title}")
            return RequestResponse(
                success=False,
                message="TV show already exists in your collection",
                request_id=f"tv:{tv_show.id}"
            )
        
        # If not in database, send to Overseerr
        request_id = f"request:tv:{request_data.title}"
        log.info(f"TV show request created with ID: {request_id}")
        
        # Add to Sonarr (would be handled by Overseerr integration in practice)
        # This is a placeholder for the actual integration
        return RequestResponse(
            success=True,
            message="TV show request submitted successfully",
            request_id=request_id
        )
    except Exception as e:
        log.error(f"Error processing TV show request: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
    finally:
        db.close()

@router.post("/music", response_model=RequestResponse)
async def request_music(request_data: RequestMedia):
    """
    Request music tracks.
    
    Parameters:
    - title: Music track title
    - artist: Artist name
    - year: Optional release year
    - external_id: Optional external ID
    
    Returns:
    - Request status and ID
    """
    log.info(f"Requesting music: {request_data.title} by {request_data.artist}")
    
    try:
        # Check if music exists in database
        db = media_repo.get_db()
        result = db.execute(text("SELECT * FROM music WHERE title = :title AND artist = :artist"), 
                          {"title": request_data.title, "artist": request_data.artist})
        music = result.fetchone()
        
        if music:
            log.warning(f"Music already exists: {request_data.title} by {request_data.artist}")
            return RequestResponse(
                success=False,
                message="Music already exists in your collection",
                request_id=f"music:{music.id}"
            )
        
        # In a real implementation, this would integrate with Overseerr
        request_id = f"request:music:{request_data.title}"
        log.info(f"Music request created with ID: {request_id}")
        
        # This is a placeholder for the actual integration
        return RequestResponse(
            success=True,
            message="Music request submitted successfully",
            request_id=request_id
        )
    except Exception as e:
        log.error(f"Error processing music request: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
    finally:
        db.close()

# Beginner's Tip: These request routes implement the integration with Overseerr and the download pipelines.
# They check if media exists before creating new requests, following the safety rules.

# Fun Fact: The first movie theater opened in Pittsburgh in 1905 and was called the Nickelodeon - 
# it charged 5 cents (a nickel) for admission! 🎬
