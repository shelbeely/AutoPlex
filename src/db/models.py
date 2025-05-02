from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship, declarative_base
from src.utils.logging import get_logger

# Initialize logger
log = get_logger(__name__)

Base = declarative_base()

class Movie(Base):
    __tablename__ = 'movies'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(255), index=True)
    original_title = Column(String(255))
    summary = Column(Text)
    tagline = Column(String(255))
    genres = Column(String(255), index=True)
    keywords = Column(String(255))
    collections = Column(String(255))
    release_year = Column(Integer, index=True)
    release_date = Column(DateTime)
    runtime_minutes = Column(Integer)
    aspect_ratio = Column(String(50))
    studio = Column(String(255))
    production_companies = Column(String(255))
    directors = Column(String(255))
    writers = Column(String(255))
    producers = Column(String(255))
    cast = Column(String(255))
    voice_actors = Column(String(255))
    content_rating = Column(String(50))
    audio_languages = Column(String(255))
    subtitle_languages = Column(String(255))
    file_path = Column(String(255), index=True)
    file_size = Column(Integer)
    format = Column(String(50))
    codec = Column(String(50))
    resolution = Column(String(50))
    rating_imdb = Column(Float)
    rating_tmdb = Column(Float)
    rating_rotten_tomatoes = Column(Float)
    plex_rating = Column(Float)
    user_rating = Column(Float)
    watch_count = Column(Integer)
    last_played = Column(DateTime)
    external_ids = Column(JSON)
    added_date = Column(DateTime)
    updated_date = Column(DateTime)
    
    def __repr__(self):
        return f"<Movie(title='{self.title}', year={self.release_year})>"

class TVShow(Base):
    __tablename__ = 'tv_shows'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(255), index=True)
    original_title = Column(String(255))
    summary = Column(Text)
    tagline = Column(String(255))
    genres = Column(String(255), index=True)
    keywords = Column(String(255))
    first_air_date = Column(DateTime)
    last_air_date = Column(DateTime)
    seasons_count = Column(Integer)
    episodes_count = Column(Integer)
    status = Column(String(50))
    runtime_per_episode = Column(Integer)
    networks = Column(String(255))
    production_companies = Column(String(255))
    creators = Column(String(255))
    showrunners = Column(String(255))
    producers = Column(String(255))
    cast = Column(String(255))
    guest_stars = Column(String(255))
    rating_imdb = Column(Float)
    rating_tmdb = Column(Float)
    plex_rating = Column(Float)
    user_rating = Column(Float)
    content_rating = Column(String(50))
    audio_languages = Column(String(255))
    subtitle_languages = Column(String(255))
    file_path = Column(String(255), index=True)
    total_file_size = Column(Integer)
    external_ids = Column(JSON)
    added_date = Column(DateTime)
    updated_date = Column(DateTime)
    
    # Relationships
    seasons = relationship("Season", back_populates="show")
    
    def __repr__(self):
        return f"<TVShow(title='{self.title}', seasons={self.seasons_count})>"

class Season(Base):
    __tablename__ = 'seasons'
    
    id = Column(Integer, primary_key=True)
    show_id = Column(Integer, ForeignKey('tv_shows.id'))
    season_number = Column(Integer)
    episode_count = Column(Integer)
    summary = Column(Text)
    release_date = Column(DateTime)
    file_path = Column(String(255))
    
    # Relationships
    show = relationship("TVShow", back_populates="seasons")
    episodes = relationship("Episode", back_populates="season")
    
    def __repr__(self):
        return f"<Season(number={self.season_number}, episodes={self.episode_count})>"

class Episode(Base):
    __tablename__ = 'episodes'
    
    id = Column(Integer, primary_key=True)
    season_id = Column(Integer, ForeignKey('seasons.id'))
    episode_number = Column(Integer)
    title = Column(String(255))
    summary = Column(Text)
    release_date = Column(DateTime)
    runtime_minutes = Column(Integer)
    file_path = Column(String(255))
    file_size = Column(Integer)
    format = Column(String(50))
    codec = Column(String(50))
    resolution = Column(String(50))
    audio_languages = Column(String(255))
    subtitle_languages = Column(String(255))
    watched = Column(Integer)
    last_played = Column(DateTime)
    
    # Relationships
    season = relationship("Season", back_populates="episodes")
    
    def __repr__(self):
        return f"<Episode(number={self.episode_number}, title='{self.title}')>"

class MusicTrack(Base):
    __tablename__ = 'music'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(255), index=True)
    album = Column(String(255))
    artist = Column(String(255), index=True)
    album_artist = Column(String(255))
    track_number = Column(Integer)
    disc_number = Column(Integer)
    genres = Column(String(255), index=True)
    tags = Column(String(255))
    lyrics = Column(Text)
    release_year = Column(Integer, index=True)
    release_date = Column(DateTime)
    duration_seconds = Column(Integer)
    composers = Column(String(255))
    producers = Column(String(255))
    featured_artists = Column(String(255))
    audio_codec = Column(String(50))
    bitrate = Column(Integer)
    sample_rate = Column(Integer)
    channels = Column(Integer)
    file_path = Column(String(255), index=True)
    file_size = Column(Integer)
    play_count = Column(Integer)
    last_played = Column(DateTime)
    user_rating = Column(Float)
    album_art_url = Column(String(255))
    
    def __repr__(self):
        return f"<MusicTrack(title='{self.title}', artist='{self.artist}')>"

class UserHistory(Base):
    __tablename__ = 'user_history'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(String(255), index=True)
    media_type = Column(String(50))
    media_id = Column(Integer)
    timestamp = Column(DateTime)
    action = Column(String(50))
    
    def __repr__(self):
        return f"<UserHistory(user='{self.user_id}', action='{self.action}')>"

class UserPreferences(Base):
    __tablename__ = 'user_preferences'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(String(255), index=True)
    preferred_genres = Column(String(255))
    preferred_media_types = Column(String(255))
    disliked_genres = Column(String(255))
    watch_history = Column(String(255))
    favorite_artists = Column(String(255))
    preferred_languages = Column(String(255))
    
    def __repr__(self):
        return f"<UserPreferences(user='{self.user_id}')>"

# Beginner's Tip: These models implement the database schema as defined in the .clinerules documentation.
# Each class represents a table in the database with fields matching the metadata requirements for movies, TV shows, and music.

# Fun Fact: The first relational database model was proposed in 1970 by Edgar F. Codd at IBM Research!
