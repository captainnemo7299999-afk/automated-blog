import feedparser
from google import genai
import os
from datetime import datetime

# Initialize the Brain
client = genai.Client()

# UPGRADE 1: The Target
# Shifting away from general tech to Global Finance & FinTech. 
# This keeps us out of the standard aggregator echo chambers.
RSS_FEED_URL = "https://techcrunch.com/category/fintech/feed/"

def fetch_news():
    print(f"📡 Fetching raw data from {RSS_FEED_URL}...")
    feed = feedparser.parse(RSS_FEED_URL)
    articles = []
    
    for entry in feed.entries[:3]:
        articles.append(f"Title: {entry.title}\nSummary: {entry.get('summary', '')}\n")
    return "\n".join(articles)

def generate_blog_post(news_context):
    print("🧠 Sending to Gemini for synthesis and image generation...")
    
    # UPGRADE 2 & 3: The Voice and The Images
    prompt = f"""
    You are a sharp, insightful financial technology analyst. 
    Read the following three news snippets. Write a 400-word blog post synthesizing this information into one cohesive narrative. Focus on global finance, digital economies, and shifting markets.
    Maintain a sophisticated, analytical, yet accessible tone.
    
    CRUCIAL FORMATTING INSTRUCTIONS:
    1. First, think of a 5-word visual description of the core theme of your article (e.g., global-finance-digital-money-future).
    2. Start your response with this exact markdown image tag, replacing the ALL CAPS section with your 5-word description separated by hyphens:
       ![Article Header Image](https://image.pollinations.ai/prompt/YOUR-FIVE-WORD-DESCRIPTION-HERE?width=800&height=400&nologo=true)
    3. Below the image, write your article in clean Markdown.
    
    Raw News Snippets:
    {news_context}
    """
    
    try:
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
    
    frontmatter = f"---\nlayout: post\ntitle: \"Market Shift: Today's Financial Tech Briefing\"\ndate: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n---\n\n"
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(frontmatter + content)
    print(f"✅ Success! V2.0 File saved to {filename}")

if __name__ == "__main__":
    news = fetch_news()
    blog_content = generate_blog_post(news)
    save_post(blog_content)
