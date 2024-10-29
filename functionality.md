# SnooScout Functionality Documentation

## Overview
SnooScout is a web application that enables users to search for subreddits, analyze their posts, and add notes/ideas for selected posts. The application is built using Flask for the backend and vanilla JavaScript with Bootstrap for the frontend.

## Technical Stack

### Backend
- Python 3.x
- Flask (Web Framework)
- PRAW (Python Reddit API Wrapper)
- python-dotenv (Environment Variable Management)

### Frontend
- HTML5
- JavaScript (Vanilla)
- Bootstrap 5.3.0 (CSS Framework)
- Font Awesome 6.0.0 (Icons)

## Project Structure
```
SnooScout/
├── app.py                 # Main Flask application
├── .env                   # Environment variables (not in repo)
├── requirements.txt       # Python dependencies
└── templates/
    ├── index.html        # Home page/Subreddit search
    ├── analyze.html      # Post selection page
    └── post_analysis.html # Ideas & notes input page
```

## Environment Setup

### Required Environment Variables (.env)
```
REDDIT_CLIENT_ID=your_client_id
REDDIT_CLIENT_SECRET=your_client_secret
```

### Dependencies (requirements.txt)
```
flask
praw
python-dotenv
```

## Feature Documentation

### 1. Subreddit Search (index.html)

#### Implementation
- **Frontend**: `index.html`
- **API Endpoint**: `/search_subreddit`
- **Method**: GET

#### Functionality
1. Users can search for subreddits using a search input
2. Results display:
   - Subreddit title
   - Description
   - Subscriber count
   - Active users
   - Creation date
3. Each result has:
   - "View Posts" button
   - "Visit Subreddit" link

#### Key Components
```javascript
// Search functionality
async function searchSubreddits() {
    const query = document.getElementById('searchInput').value.trim();
    // Makes API call to /search_subreddit
    // Displays results using displaySubreddits()
}

// Result display
function displaySubreddits(subreddits) {
    // Creates cards for each subreddit
    // Includes stats and action buttons
}
```

### 2. Post Selection (analyze.html)

#### Implementation
- **Frontend**: `analyze.html`
- **API Endpoint**: `/get_posts`
- **Method**: GET

#### Functionality
1. Configurable post fetching:
   - Sort by: Hot, Rising, Top
   - Time filter: Day, Week, Month, Year (for Top sort)
   - Post limit: 10, 25, 50, 100
2. Post selection:
   - Checkbox for each post
   - Visual feedback for selected posts
   - Selected count display
3. Next button to proceed with selected posts

#### Key Components
```javascript
// Post selection state
let selectedPosts = new Set();

// Selection toggle
function togglePostSelection(postId) {
    // Handles post selection
    // Updates UI and selection count
}

// Proceed to analysis
function proceedToAnalysis() {
    // Stores selected posts in localStorage
    // Redirects to post_analysis page
}
```

### 3. Post Analysis (post_analysis.html)

#### Implementation
- **Frontend**: `post_analysis.html`
- **Storage**: localStorage for post data and notes

#### Functionality
1. Displays selected posts with:
   - Title
   - Content
   - Statistics (upvotes, comments, views)
   - Creation date
2. Ideas & Notes section for each post:
   - Textarea for free-form input
   - Auto-save functionality
3. Save button for all notes

#### Key Components
```javascript
// Save functionality
function saveIdeas() {
    // Collects all ideas/notes
    // Stores in localStorage
}

// Load saved ideas
function loadSavedIdeas() {
    // Retrieves previously saved ideas
    // Populates textareas
}
```

## API Endpoints Documentation

### 1. /search_subreddit
- **Method**: GET
- **Parameters**: 
  - query (string): Search term
- **Response**: Array of subreddit objects
```json
[
    {
        "name": "subreddit_name",
        "title": "Subreddit Title",
        "description": "Description",
        "subscribers": 1234,
        "active_users": 123,
        "created_utc": 1234567890,
        "url": "https://reddit.com/r/subreddit_name"
    }
]
```

### 2. /get_posts
- **Method**: GET
- **Parameters**:
  - subreddit (string): Subreddit name
  - sort_by (string): "hot", "rising", or "top"
  - time_filter (string): "day", "week", "month", "year" (for top sort)
  - limit (integer): Number of posts to fetch
- **Response**: Array of post objects
```json
[
    {
        "id": "post_id",
        "title": "Post Title",
        "url": "post_url",
        "score": 123,
        "num_comments": 45,
        "created_utc": 1234567890,
        "selftext": "Post content",
        "permalink": "https://reddit.com/r/subreddit/comments/post_id",
        "view_count": 678
    }
]
```

## State Management

### LocalStorage Keys
1. **allPosts**: All fetched posts from subreddit
   ```javascript
   localStorage.setItem('allPosts', JSON.stringify(posts));
   ```

2. **selectedPosts**: Posts selected for analysis
   ```javascript
   localStorage.setItem('selectedPosts', JSON.stringify(selectedPosts));
   ```

3. **savedIdeas**: Ideas and notes for posts
   ```javascript
   localStorage.setItem('savedIdeas', JSON.stringify(savedIdeas));
   ```

## Error Handling

### Frontend
- Loading states with spinners
- Error messages for failed API calls
- Validation for user inputs
- Fallbacks for missing data

### Backend
- Try-catch blocks for Reddit API calls
- Error response formatting
- Input validation
- Logging for debugging

## Security Considerations
1. Environment variables for API credentials
2. Input sanitization
3. Error message sanitization
4. CORS considerations
5. Rate limiting (Reddit API)

## Development Setup
1. Clone repository
2. Create .env file with Reddit API credentials
3. Install dependencies: `pip install -r requirements.txt`
4. Run application: `python app.py`
5. Access at: `http://127.0.0.1:8080`

## Deployment Considerations
1. Production WSGI server (e.g., Gunicorn)
2. Environment variable management
3. Error logging
4. Rate limiting
5. Caching strategies
6. Database integration for persistence (if needed)

This documentation provides a comprehensive overview of the SnooScout application's functionality and implementation details. Developers can use this as a guide to understand, maintain, or recreate the application.
