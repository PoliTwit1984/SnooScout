# SnooScout 🔍

SnooScout is a powerful Reddit content analysis tool that helps content creators and marketers discover trending topics, analyze discussions, and generate content ideas using AI. It combines Reddit's API with OpenAI's GPT-4 to provide deep insights and content suggestions.

## ✨ Features

- 🔍 **Subreddit Search**: Easily find relevant subreddits with detailed statistics
- 📊 **Post Analysis**: View engagement metrics, comments, and trends
- 🤖 **AI-Powered Insights**: Analyze posts and comments using GPT-4
- 📝 **Content Ideas**: Generate content suggestions for various platforms
- 💡 **Note Taking**: Save ideas and insights for each post
- 🎯 **Custom Analysis**: Request specific content formats (YouTube shorts, long-form videos, blog posts)

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- Reddit API credentials
- OpenAI API key

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/SnooScout.git
cd SnooScout
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root with your API credentials:
```env
REDDIT_CLIENT_ID=your_reddit_client_id
REDDIT_CLIENT_SECRET=your_reddit_client_secret
OPENAI_API_KEY=your_openai_api_key
```

### Running the Application

1. Start the Flask server:
```bash
python app.py
```

2. Open your browser and navigate to:
```
http://127.0.0.1:8080
```

## 🎯 Usage Guide

1. **Search for Subreddits**
   - Enter keywords in the search bar
   - View subreddit statistics and descriptions
   - Select a subreddit to analyze

2. **Configure Post Options**
   - Choose sorting method (Hot, Top, Rising)
   - Select time period for Top posts
   - Set number of posts to fetch

3. **Select Posts**
   - Browse through posts
   - Select posts for analysis
   - Click "Analyze Selected Posts"

4. **Add Notes & Request Content**
   - Add your notes and ideas for each post
   - Specify content creation requests (e.g., "3 YouTube shorts, 1 blog post")
   - Save your notes

5. **Generate AI Analysis**
   - Click "Analyze with AI"
   - View comprehensive analysis including:
     - Products and brands mentioned
     - Key features and benefits
     - Sentiment analysis
     - Content ideas based on your requests

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a feature branch:
```bash
git checkout -b feature/YourFeatureName
```
3. Commit your changes:
```bash
git commit -m 'Add some feature'
```
4. Push to the branch:
```bash
git push origin feature/YourFeatureName
```
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 style guide for Python code
- Use meaningful commit messages
- Add tests for new features
- Update documentation as needed

## 📝 Project Structure

```
SnooScout/
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
├── .env               # Environment variables
├── templates/         # HTML templates
│   ├── index.html     # Home page
│   ├── analyze.html   # Post selection page
│   └── post_analysis.html  # Analysis page
└── static/           # Static assets (future use)
```

## 🔑 Environment Variables

Required environment variables:
```env
REDDIT_CLIENT_ID=your_reddit_client_id
REDDIT_CLIENT_SECRET=your_reddit_client_secret
OPENAI_API_KEY=your_openai_api_key
```

To obtain API credentials:
1. Reddit API: Create an application at https://www.reddit.com/prefs/apps
2. OpenAI API: Get your API key from https://platform.openai.com/account/api-keys

## 🛠️ Tech Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS, JavaScript
- **APIs**: 
  - Reddit API (PRAW)
  - OpenAI GPT-4
- **Styling**: Bootstrap 5
- **Icons**: Font Awesome

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Reddit API (PRAW) for providing access to Reddit data
- OpenAI for their powerful GPT-4 API
- All contributors who help improve this tool

## 📸 Screenshots

[Coming Soon]

## 🚧 Roadmap

- [ ] Add user authentication
- [ ] Implement data export features
- [ ] Add more AI analysis options
- [ ] Create a dashboard for saved analyses
- [ ] Add support for more content platforms
- [ ] Implement batch analysis features

## ⚠️ Known Issues

- Rate limiting may affect large analysis requests
- Some subreddits may have restricted access
- API keys must be kept secure

## 📫 Contact

For questions or support, please [open an issue](https://github.com/yourusername/SnooScout/issues) on GitHub.

---

Made with ❤️ by [Your Name]
