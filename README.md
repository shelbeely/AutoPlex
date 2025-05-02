# AutoPlex Media LLM System

## Overview
Integrated media management system combining Plex, Overseerr, Sonarr, Radarr, FastAPI, Langchain, SQL, and OpenRouter for intelligent media discovery and management.

## Architecture
```mermaid
graph TD
    A[Plex Media Server] --> B{SQL Database}
    C[Overseerr] --> D[FastAPI GUI]
    D --> E[Langchain]
    E --> F[OpenRouter]
    B --> E
    E --> G[Radarr/Sonarr]
    H[User] --> D
    D --> H
```

## Key Features
- Natural language media queries
- AI-powered recommendations with rationale
- Automated download requests
- Multi-media support (movies, TV shows, music)
- Material Design 3 compliant GUI

## Media Types & Metadata
```mermaid
graph LR
    I[Media Types] --> J[Movies]
    I --> K[TV Shows]
    I --> L[Music]
    
    J --> M[Metadata Fields]
    K --> N[Metadata Fields]
    L --> O[Metadata Fields]
```

## Query Processing
```mermaid
flowchart LR
    P[User Query] --> Q[Intent Detection]
    Q --> R{SQL Filter}
    R --> S[Vector Search]
    S --> T[Structured Results]
    T --> U[GUI Display]
```

## Recommendation Engine
```mermaid
graph TD
    V[User History] --> W[Embedding Similarity]
    X[Genre/Creator Overlap] --> W
    W --> Y[Recommendation Rationale]
    Y --> Z[Structured Output]
```

## Download Workflow
```mermaid
sequenceDiagram
    participant User
    participant GUI
    participant Overseerr
    participant Radarr
    participant Sonarr

    User->>GUI: Request Media
    GUI->>Overseerr: Check Availability
    Overseerr->>Radarr: Movie Request
    Overseerr->>Sonarr: TV Show Request
    Radarr->>GUI: Status Update
    Sonarr->>GUI: Status Update
    GUI->>User: Confirmation
```

## Database Schema
```mermaid
erDiagram
    MOVIES ||--o{ MEDIA : "media_type"
    TV_SHOWS ||--o{ MEDIA : "media_type"
    MUSIC ||--o{ MEDIA : "media_type"
    
    MEDIA {
        string title
        string media_type
        int release_year
    }
    
    MOVIES {
        string director
        string runtime
    }
    
    TV_SHOWS {
        int seasons
        int episodes
    }
    
    MUSIC {
        string artist
        string album
    }
```

## Safety & Security
- Input sanitization at all entry points
- NSFW content filtering (explicit/implicit)
- Data validation before API calls
- "I don't know" fallback for uncertain data

## Installation
```bash
# Clone repository
git clone https://github.com/yourusername/autoplex.git
cd autoplex

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env with your Plex, Overseerr, Radarr/Sonarr API keys and database credentials

# Initialize database
python init_db.py

# Start the application
uvicorn main:app --reload
```

## Usage Examples
- "Find 80s sci-fi movies under 2 hours"
- "Show all unwatched TV shows"
- "What songs by Daft Punk do I have?"
