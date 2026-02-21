import feedparser
from google import genai
import os
from datetime import datetime
import urllib.parse
import random

# Initialize the Brain
client = genai.Client()

RSS_FEED_URL = "https://techcrunch.com/category/fintech/feed/"

def fetch_news():
    print(f"📡 Fetching raw data from {RSS_FEED_URL}...")
    feed = feedparser.parse(RSS_FEED_URL)
    articles = []
    
    for entry in feed.entries[:3]:
        articles.append(f"Title: {entry.title}\nSummary: {entry.get('summary', '')}\n")
    return "\n".join(articles)

def generate_blog_post(news_context):
    print("🧠 Sending to Gemini for synthesis...")
    
    prompt = f"""
    You are a sharp, insightful financial technology analyst. 
    Read the following three news snippets. Write a 400-word blog post synthesizing this information into one cohesive narrative. Focus on global finance, digital economies, and shifting markets.
    Maintain a sophisticated, analytical, yet accessible tone.
    Write the article in clean Markdown. Do NOT include an image tag, I will handle that.
    
    Raw News Snippets:
    {news_context}
    """
    
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt
        )
        
        # UPGRADE 3.1: Python handles the image link safely so it never breaks
        # We add a random seed so Pollinations gives a fresh image every single day
        safe_prompt = urllib.parse.quote("abstract highly detailed digital global finance economy technology")
        random_seed = random.randint(1, 100000)
        image_url = f"https://image.pollinations.ai/prompt/{safe_prompt}?width=800&height=400&nologo=true&seed={random_seed}"
        image_markdown = f'<img src="{image_url}" alt="Financial Header Image" style="width:100%; border-radius:8px; margin-bottom:20px;">\n\n'
        
        return image_markdown + response.text
        
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
    
    frontmatter = f"---\nlayout: default\ntitle: \"Market Shift: Today's Financial Tech Briefing\"\ndate: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n---\n\n"
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(frontmatter + content)
    print(f"✅ Success! V2.1 File saved to {filename}")

if __name__ == "__main__":
    news = fetch_news()
    blog_content = generate_blog_post(news)
    save_post(blog_content)

