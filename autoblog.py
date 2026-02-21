import feedparser
from google import genai
import os
from datetime import datetime

# 1. Initialize the Brain
# The new SDK automatically grabs the GEMINI_API_KEY environment variable
client = genai.Client()

# 2. The Data Source (Placeholder feed)
RSS_FEED_URL = "https://techcrunch.com/feed/"

def fetch_news():
    print(f"📡 Fetching raw data from {RSS_FEED_URL}...")
    feed = feedparser.parse(RSS_FEED_URL)
    articles = []
    
    # Grab the top 3 latest articles
    for entry in feed.entries[:3]:
        articles.append(f"Title: {entry.title}\nSummary: {entry.get('summary', '')}\nLink: {entry.link}\n")
    return "\n".join(articles)

def generate_blog_post(news_context):
    print("🧠 Sending to Gemini for synthesis...")
    prompt = f"""
    You are the lead editor of a modern, insightful blog. 
    Read the following three news snippets. Write a 400-word blog post synthesizing this information into one cohesive narrative. 
    Explain why this news matters to the average reader. 
    Maintain a conversational, engaging tone.
    Format the output in clean Markdown.
    
    Raw News Snippets:
    {news_context}
    """
    
    try:
        # Using the new SDK syntax
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt
        )
        return response.text
    except Exception as e:
        print(f"⚠️ API Error: {e}")
        return None

def save_post(content):
    if not content:
        return
        
    print("💾 Formatting and saving file...")
    date_str = datetime.now().strftime('%Y-%m-%d')
    filename = f"_posts/{date_str}-daily-update.md"
    
    os.makedirs("_posts", exist_ok=True)
    
    # Adds the YAML frontmatter required by GitHub Pages to turn this into a web page
    frontmatter = f"---\nlayout: post\ntitle: \"Today's Automated Briefing\"\ndate: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n---\n\n"
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(frontmatter + content)
    print(f"✅ Success! File saved to {filename}")

if __name__ == "__main__":
    news = fetch_news()
    blog_content = generate_blog_post(news)
    save_post(blog_content)