from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.db.models import Base, Movie, TVShow, Season, Episode, MusicTrack, UserHistory, UserPreferences
from src.utils.logging import get_logger

# Initialize logger
log = get_logger(__name__)

def init_database(db_url: str = "sqlite:///./test.db"):
    """
    Initialize the database with all tables.
    
    Parameters:
    - db_url: Database connection URL (default is SQLite for development)
    """
    try:
        # Create engine
        engine = create_engine(db_url, connect_args={"check_same_thread": False})
        
        # Create all tables
        Base.metadata.create_all(bind=engine)
        log.info("Database tables created successfully")
        
        # Verify table creation
        verify_tables(engine)
        
        # Add sample data if database is empty
        if is_database_empty(engine):
            add_sample_data(engine)
        
        return True
    except Exception as e:
        log.error(f"Error initializing database: {str(e)}")
        return False

def verify_tables(engine):
    """Verify that all expected tables exist in the database."""
    from sqlalchemy import inspect
    inspector = inspect(engine)
    existing_tables = inspector.get_table_names()
    
    required_tables = [
        'movies', 'tv_shows', 'seasons', 'episodes', 
        'music', 'user_history', 'user_preferences'
    ]
    
    missing_tables = [table for table in required_tables if table not in existing_tables]
    
    if missing_tables:
        log.warning(f"Missing tables in database: {missing_tables}")
    else:
        log.info("All required tables exist in the database")

def is_database_empty(engine):
    """Check if the database is empty by checking the movies table."""
    try:
        Session = sessionmaker(bind=engine)
        session = Session()
        
        # Check if movies table is empty
        count = session.query(Movie).count()
        session.close()
        return count == 0
    except Exception as e:
        log.error(f"Error checking if database is empty: {str(e)}")
        return True

def add_sample_data(engine):
    """Add sample data to the database for testing purposes."""
    try:
        Session = sessionmaker(bind=engine)
        session = Session()
        
        # Add sample AI-themed movie - Ex Machina (2014)
        sample_movie = Movie(
            title="Ex Machina",
            original_title="Ex Machina",
            summary="A young programmer is selected to participate in a groundbreaking experiment in artificial intelligence by evaluating the human qualities of a highly advanced humanoid A.I.",
            tagline="There is no gene for being human.",
            genres="Sci-Fi,Drama,Thriller",
            keywords="artificial intelligence,robot,consciousness,ethics",
            release_year=2014,
            release_date="2015-01-21",
            runtime_minutes=108,
            aspect_ratio="2.35:1",
            studio="Universal Pictures",
            production_companies="DNA Films,Universal Pictures",
            directors="Alex Garland",
            writers="Alex Garland",
            producers="Andrew Macdonald,Allon Reich",
            cast="Domhnall Gleeson,Alicia Vikander,Oscar Isaac",
            voice_actors="",
            content_rating="R",
            audio_languages="English",
            subtitle_languages="English,Spanish,French",
            file_path="/movies/Ex Machina (2014)/ExMachina.mp4",
            file_size=5200,
            format="MP4",
            codec="H.264",
            resolution="1080p",
            rating_imdb=7.7,
            rating_tmdb=7.2,
            rating_rotten_tomatoes=92,
            plex_rating=8.5,
            user_rating=8.7,
            watch_count=5,
            last_played="2025-04-18",
            external_ids=json.dumps({"tmdb": "tt0470752", "imdb": "tt0470752"}),
            added_date="2023-01-01",
            updated_date="2025-04-18"
        )
        
        # Add sample AI-themed TV show - Westworld (2016)
        sample_show = TVShow(
            title="Westworld",
            original_title="Westworld",
            summary="A futuristic theme park populated by android hosts becomes the setting for a complex exploration of artificial consciousness and free will.",
            tagline="Where every desire is possible.",
            genres="Sci-Fi,Drama,Action",
            keywords="artificial intelligence,robotics,consciousness,ethics",
            release_year=2016,
            release_date="2016-10-02",
            first_air_date="2016-10-02",
            last_air_date="2022-08-14",
            seasons_count=4,
            episodes_count=36,
            status="Ended",
            runtime_per_episode=60,
            networks="HBO",
            production_companies="HBO,Warner Bros. Television",
            creators="Jonathan Nolan,Lisa Joy",
            showrunners="Jonathan Nolan,Lisa Joy",
            producers="J.J. Abrams,Arnold W. Eisen",
            cast="Evan Rachel Wood,Thandiwe Newton,Jeffrey Wright",
            guest_stars="Ed Harris,Vincent Cassel",
            rating_imdb=8.5,
            rating_tmdb=8.3,
            plex_rating=8.7,
            user_rating=8.9,
            content_rating="TV-MA",
            audio_languages="English",
            subtitle_languages="English,Spanish,French",
            file_path="/tv_shows/Westworld",
            total_file_size=250000,
            external_ids=json.dumps({"tvdb": "310893", "tmdb": "63247"}),
            added_date="2023-01-01",
            updated_date="2025-04-18"
        )
        
        # Add sample season - Westworld Season 1
        sample_season = Season(
            show_id=1,
            season_number=1,
            episode_count=10,
            summary="In a high-tech Western-themed amusement park, the android hosts begin to develop self-awareness through their interactions with human guests.",
            release_date="2016-10-02",
            file_path="/tv_shows/Westworld/Season 1"
        )
        
        # Add sample episode - The Original
        sample_episode = Episode(
            season_id=1,
            episode_number=1,
            title="The Original",
            summary="A host in Westworld begins to question her reality while a wealthy investor tests the park's limits.",
            release_date="2016-10-02",
            runtime_minutes=63,
            file_path="/tv_shows/Westworld/Season 1/Episode 1 - The Original.mp4",
            file_size=1200
        )
        
        # Add sample AI-themed music track - The Algorithm
        sample_music = MusicTrack(
            title="The Algorithm",
            album="Goddess",
            artist="Banksy",
            album_artist="Banksy",
            track_number=5,
            disc_number=1,
            genres="Electronic,Dubstep,Experimental",
            keywords="artificial intelligence,technology,future",
            release_year=2023,
            release_date="2023-06-15",
            duration_seconds=245,
            composers="Banksy,The Algorithm",
            producers="Banksy,The Algorithm",
            featured_artists="",
            audio_codec="FLAC",
            bitrate=1411,
            sample_rate=44100,
            channels=2,
            file_path="/music/Banksy/Goddess/The Algorithm.flac",
            file_size=58,
            play_count=8,
            last_played="2025-04-17",
            user_rating=4.7,
            album_art_url="https://i.scdn.co/image/ab67616d0000b273f7db43292a6a99b21f31a35e"
        )
        
        # Add all to database
        session.add_all([
            sample_movie, 
            sample_show, 
            sample_season, 
            sample_episode, 
            sample_music
        ])
        
        # Commit changes
        session.commit()
        log.info("Sample data added to the database")
        
    except Exception as e:
        log.error(f"Error adding sample data: {str(e)}")
        session.rollback()
    finally:
        session.close()

# Beginner's Tip: This initialization script creates all database tables based on the defined models,
# verifies that the tables exist, and adds sample data if the database is empty. The sample data
# now includes realistic media entries that follow the metadata requirements.

# Fun Fact: SQLite was created in 2000 by D. Richard Hipp and is now the most widely deployed database engine in the world!
