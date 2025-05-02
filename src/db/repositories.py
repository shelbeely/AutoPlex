from typing import List, Optional, Dict, Any
from sqlalchemy import create_engine, text, inspect
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from src.utils.logging import get_logger
from src.api.schemas import MovieOut, TVShowOut, MusicOut

# Initialize logger
log = get_logger(__name__)

class MediaRepository:
    def __init__(self, db_url: str = "sqlite:///./test.db"):
        """
        Initialize the database connection and session factory.
        
        Parameters:
        - db_url: Database connection URL (default is SQLite for development)
        """
        self.engine = create_engine(db_url, connect_args={"check_same_thread": False})
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        self._initialize_database()
    
    def _initialize_database(self):
        """Initialize database tables if they don't exist."""
        try:
            # Create tables if they don't exist
            from src.db.models import Base
            Base.metadata.create_all(bind=self.engine)
            log.info("Database initialized successfully")
        except Exception as e:
            log.error(f"Error initializing database: {str(e)}")
            raise
    
    def get_db(self):
        """Get a database session."""
        db = self.SessionLocal()
        try:
            yield db
        finally:
            db.close()
    
    # Movie-related methods
    def get_movies(self, db: Any, skip: int = 0, limit: int = 100) -> List[MovieOut]:
        """Retrieve a list of movies from the database."""
        try:
            result = db.execute(text("SELECT * FROM movies ORDER BY id LIMIT :limit OFFSET :skip"), 
                              {"limit": limit, "skip": skip})
            return [MovieOut(**dict(row)) for row in result]
        except SQLAlchemyError as e:
            log.error(f"Database error in get_movies: {str(e)}")
            raise
    
    def get_movie(self, db: Any, movie_id: int) -> Optional[MovieOut]:
        """Retrieve a specific movie by ID."""
        try:
            result = db.execute(text("SELECT * FROM movies WHERE id = :id"), {"id": movie_id})
            row = result.fetchone()
            return MovieOut(**dict(row)) if row else None
        except SQLAlchemyError as e:
            log.error(f"Database error in get_movie: {str(e)}")
            raise
    
    # TV Show-related methods
    def get_tv_shows(self, db: Any, skip: int = 0, limit: int = 100) -> List[TVShowOut]:
        """Retrieve a list of TV shows from the database."""
        try:
            result = db.execute(text("SELECT * FROM tv_shows ORDER BY id LIMIT :limit OFFSET :skip"), 
                              {"limit": limit, "skip": skip})
            return [TVShowOut(**dict(row)) for row in result]
        except SQLAlchemyError as e:
            log.error(f"Database error in get_tv_shows: {str(e)}")
            raise
    
    def get_tv_show(self, db: Any, show_id: int) -> Optional[TVShowOut]:
        """Retrieve a specific TV show by ID."""
        try:
            result = db.execute(text("SELECT * FROM tv_shows WHERE id = :id"), {"id": show_id})
            row = result.fetchone()
            return TVShowOut(**dict(row)) if row else None
        except SQLAlchemyError as e:
            log.error(f"Database error in get_tv_show: {str(e)}")
            raise
    
    # Music-related methods
    def get_music_tracks(self, db: Any, skip: int = 0, limit: int = 100) -> List[MusicOut]:
        """Retrieve a list of music tracks from the database."""
        try:
            result = db.execute(text("SELECT * FROM music ORDER BY id LIMIT :limit OFFSET :skip"), 
                              {"limit": limit, "skip": skip})
            return [MusicOut(**dict(row)) for row in result]
        except SQLAlchemyError as e:
            log.error(f"Database error in get_music_tracks: {str(e)}")
            raise
    
    def get_music(self, db: Any, music_id: int) -> Optional[MusicOut]:
        """Retrieve a specific music track by ID."""
        try:
            result = db.execute(text("SELECT * FROM music WHERE id = :id"), {"id": music_id})
            row = result.fetchone()
            return MusicOut(**dict(row)) if row else None
        except SQLAlchemyError as e:
            log.error(f"Database error in get_music: {str(e)}")
            raise
    
    # Advanced search methods
    def advanced_search(self, db: Any, media_type: str, filters: str = "", params: Dict = None, 
                       skip: int = 0, limit: int = 100) -> List[Dict]:
        """Perform an advanced search on the database with dynamic filters."""
        try:
            if params is None:
                params = {}
            
            if media_type == "movie":
                base_query = "SELECT * FROM movies"
            elif media_type == "tv":
                base_query = "SELECT * FROM tv_shows"
            elif media_type == "music":
                base_query = "SELECT * FROM music"
            else:
                raise ValueError(f"Invalid media_type: {media_type}")
            
            if filters:
                base_query += f" WHERE {filters}"
            
            base_query += " ORDER BY id LIMIT :limit OFFSET :skip"
            params.update({"limit": limit, "skip": skip})
            
            result = db.execute(text(base_query), params)
            return [dict(row) for row in result]
        except SQLAlchemyError as e:
            log.error(f"Database error in advanced_search: {str(e)}")
            raise
    
    # User-related methods
    def get_user_history(self, db: Any, user_id: str) -> List[Dict]:
        """Get user's watch/listen history."""
        try:
            result = db.execute(text("""
                SELECT * FROM user_history 
                WHERE user_id = :user_id 
                ORDER BY timestamp DESC
            """), {"user_id": user_id})
            return [dict(row) for row in result]
        except SQLAlchemyError as e:
            log.error(f"Database error in get_user_history: {str(e)}")
            raise
    
    def get_user_preferences(self, db: Any, user_id: str) -> Dict:
        """Get user's media preferences."""
        try:
            result = db.execute(text("""
                SELECT * FROM user_preferences 
                WHERE user_id = :user_id
            """), {"user_id": user_id})
            row = result.fetchone()
            return dict(row) if row else {}
        except SQLAlchemyError as e:
            log.error(f"Database error in get_user_preferences: {str(e)}")
            raise
    
    def get_filter_options(self, db: Any, media_type: str) -> Dict[str, List]:
        """Get available filter options for a media type."""
        try:
            inspector = inspect(self.engine)
            
            if media_type == "movie":
                columns = inspector.get_columns("movies")
                return {
                    "genres": self._get_distinct_values(db, "movies", "genres"),
                    "release_year": self._get_distinct_values(db, "movies", "release_year"),
                    "rating": self._get_distinct_values(db, "movies", "rating")
                }
            elif media_type == "tv":
                columns = inspector.get_columns("tv_shows")
                return {
                    "genres": self._get_distinct_values(db, "tv_shows", "genres"),
                    "status": self._get_distinct_values(db, "tv_shows", "status"),
                    "rating": self._get_distinct_values(db, "tv_shows", "rating")
                }
            elif media_type == "music":
                columns = inspector.get_columns("music")
                return {
                    "genres": self._get_distinct_values(db, "music", "genres"),
                    "release_year": self._get_distinct_values(db, "music", "release_year"),
                    "artist": self._get_distinct_values(db, "music", "artist")
                }
            return {}
        except SQLAlchemyError as e:
            log.error(f"Database error in get_filter_options: {str(e)}")
            raise
    
    def _get_distinct_values(self, db: Any, table_name: str, column_name: str) -> List:
        """Helper method to get distinct values from a column."""
        try:
            result = db.execute(text(f"SELECT DISTINCT {column_name} FROM {table_name}"))
            return [row[0] for row in result if row[0] is not None]
        except SQLAlchemyError as e:
            log.error(f"Database error in _get_distinct_values: {str(e)}")
            raise

# Beginner's Tip: This repository class encapsulates all database operations, providing a clean interface 
# for the API routes to interact with the database. It follows the design rules by separating media types 
# and implementing advanced search capabilities.

# Fun Fact: The first relational database was proposed by Edgar F. Codd at IBM in 1970 - the foundation for modern SQL databases!
