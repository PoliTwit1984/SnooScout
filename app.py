from flask import Flask, render_template, request, jsonify
import praw
from dotenv import load_dotenv
import os
from openai import OpenAI
import time

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Initialize Reddit API client
reddit = praw.Reddit(
    client_id=os.getenv('REDDIT_CLIENT_ID'),
    client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
    user_agent='SnooScout/1.0'
)

# Initialize OpenAI
client = OpenAI()

def analyze_with_openai(post_data, comments_data, user_notes=None, content_requests=None):
    try:
        # Prepare the prompt with post and comments data
        prompt = f"""
Analyze this Reddit post and its top comments:

Title: {post_data['title']}
URL: {post_data['permalink']}
Score: {post_data['score']}
Posted: {post_data['created_utc']}
Engagement Rate: {round(post_data['score'] + post_data['num_comments'], 2)}
--------------------------------------------------------------------------------
Post Content:
{post_data['selftext']}
--------------------------------------------------------------------------------
Top Comments:
{comments_data}
"""

        # Add user notes if provided
        if user_notes:
            prompt += f"""
--------------------------------------------------------------------------------
User's Notes & Ideas:
{user_notes}
"""

        # Add content requests if provided
        if content_requests:
            prompt += f"""
--------------------------------------------------------------------------------
Content Creation Requests:
{content_requests}

Please include specific content ideas based on the analysis and user's notes:
"""

        prompt += """
--------------------------------------------------------------------------------
Please analyze this content and extract:
1. Products mentioned (with any mentioned prices)
2. Brands mentioned
3. Key features/benefits discussed
4. Overall sentiment
5. A brief summary of the discussion
"""

        # Add content creation section if requests provided
        if content_requests:
            prompt += """
6. Content Creation Ideas (based on the analysis and user's requests):
   - Provide specific ideas for each requested content type
   - Include key points to cover
   - Suggest angles that would resonate with the audience
"""

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that analyzes Reddit discussions to extract product and brand mentions, along with key insights and content creation ideas."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=2000
        )

        return response.choices[0].message.content
    except Exception as e:
        print(f"OpenAI API error: {str(e)}")
        return f"Error performing analysis: {str(e)}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze')
def analyze():
    return render_template('analyze.html')

@app.route('/post_analysis')
def post_analysis():
    return render_template('post_analysis.html')

@app.route('/analyze_post', methods=['POST'])
def analyze_post():
    try:
        data = request.get_json()
        post_id = data.get('post_id')
        user_notes = data.get('user_notes')
        content_requests = data.get('content_requests')
        
        if not post_id:
            return jsonify({'error': 'Post ID is required'}), 400

        # Get the post and its comments
        submission = reddit.submission(id=post_id)
        submission.comment_sort = 'top'
        submission.comments.replace_more(limit=0)  # Flatten comment tree
        
        # Get top 25 comments
        top_comments = []
        for comment in submission.comments[:25]:
            top_comments.append({
                'body': comment.body,
                'score': comment.score
            })

        # Format comments for analysis
        comments_text = "\n\n".join([
            f"Analyzing comment (Score: {comment['score']}):\n{comment['body'][:200]}..."
            for comment in top_comments
        ])

        # Prepare post data
        post_data = {
            'id': submission.id,
            'title': submission.title,
            'selftext': submission.selftext,
            'score': submission.score,
            'num_comments': submission.num_comments,
            'created_utc': submission.created_utc,
            'permalink': f"https://reddit.com{submission.permalink}"
        }

        # Perform AI analysis
        analysis_result = analyze_with_openai(post_data, comments_text, user_notes, content_requests)

        return jsonify({
            'success': True,
            'analysis': analysis_result
        })

    except Exception as e:
        print(f"Error analyzing post: {str(e)}")
        return jsonify({'error': str(e)}), 500

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

                    # Convert subreddit data to dict for JSON serialization
                    subreddit_data = {
                        'name': subreddit.display_name,
                        'title': getattr(subreddit, 'title', subreddit.display_name),
                        'description': getattr(subreddit, 'public_description', ''),
                        'subscribers': getattr(subreddit, 'subscribers', 0),
                        'active_users': active_users,
                        'created_utc': getattr(subreddit, 'created_utc', 0),
                        'over18': getattr(subreddit, 'over18', False),
                        'url': f"https://reddit.com/r/{subreddit.display_name}"
                    }
                    print(f"Found subreddit: {subreddit_data}")  # Debug output
                    subreddits.append(subreddit_data)
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
