from flask import Flask, render_template, request, jsonify
import praw
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Initialize Reddit API client
reddit = praw.Reddit(
    client_id=os.getenv('REDDIT_CLIENT_ID'),
    client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
    user_agent='SnooScout/1.0'
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze')
def analyze():
    return render_template('analyze.html')

@app.route('/post_analysis')
def post_analysis():
    return render_template('post_analysis.html')

@app.route('/search_subreddit')
def search_subreddit():
    query = request.args.get('query', '')
    print(f"Searching for subreddit: {query}")  # Debug output
    subreddits = []
    if query:
        try:
            for subreddit in reddit.subreddits.search(query):
                try:
                    # Get active users count safely
                    active_users = 0
                    try:
                        full_subreddit = reddit.subreddit(subreddit.display_name)
                        active_users = getattr(full_subreddit, 'active_user_count', 0) or 0
                    except Exception as e:
                        print(f"Error getting active users for {subreddit.display_name}: {str(e)}")
                        pass

                    subreddits.append({
                        'name': subreddit.display_name,
                        'title': subreddit.title,
                        'description': subreddit.public_description,
                        'full_description': subreddit.description,
                        'subscribers': subreddit.subscribers,
                        'active_users': active_users,
                        'created_utc': subreddit.created_utc,
                        'over18': subreddit.over18,
                        'url': f"https://reddit.com{subreddit.url}"
                    })
                except Exception as e:
                    print(f"Error processing subreddit {subreddit.display_name}: {str(e)}")
                    continue
        except Exception as e:
            print(f"Error searching subreddits: {str(e)}")
            return jsonify({'error': str(e)}), 500
    print(f"Found {len(subreddits)} subreddits")  # Debug output
    return jsonify(subreddits)

@app.route('/get_posts')
def get_posts():
    subreddit_name = request.args.get('subreddit', '')
    sort_by = request.args.get('sort_by', 'hot')
    time_filter = request.args.get('time_filter', 'day')
    limit = int(request.args.get('limit', 10))
    
    if not subreddit_name:
        return jsonify({'error': 'Subreddit name is required'}), 400
    
    subreddit = reddit.subreddit(subreddit_name)
    posts = []
    
    try:
        if sort_by == 'hot':
            submissions = subreddit.hot(limit=limit)
        elif sort_by == 'rising':
            submissions = subreddit.rising(limit=limit)
        elif sort_by == 'top':
            submissions = subreddit.top(time_filter=time_filter, limit=limit)
        
        for submission in submissions:
            posts.append({
                'id': submission.id,
                'title': submission.title,
                'url': submission.url,
                'score': submission.score,
                'num_comments': submission.num_comments,
                'created_utc': submission.created_utc,
                'selftext': submission.selftext,
                'permalink': f"https://reddit.com{submission.permalink}",
                'view_count': getattr(submission, 'view_count', 0) or 0
            })
        
        return jsonify(posts)
    except Exception as e:
        print(f"Error getting posts: {str(e)}")  # Debug output
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=8080)
