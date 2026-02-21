import feedparser
from google import genai
import os
from datetime import datetime
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
    Write the article in clean Markdown. Do NOT include an image tag.
    
    Raw News Snippets:
    {news_context}
    """
    
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt
        )
        
        # UPGRADE 4.0: The Cache-Buster Image Test
        # Using Picsum to guarantee it bypasses all browser ad-blockers
        random_seed = random.randint(1, 10000)
        image_url = f"https://picsum.photos/seed/{random_seed}/800/400"
        
        # If this works, the broken icon will be replaced with a real photo
        image_html = f'<img src="{image_url}" alt="System Check Image" style="width:100%; border-radius:8px; margin-bottom:20px;">\n\n'
        
        return image_html + response.text
        
    except Exception as e:
        print(f"⚠️ API Error: {e}")
        return None

def save_post(content):
    if not content:
        return
        
    print("💾 Formatting and saving file...")
    date_str = datetime.now().strftime('%Y-%m-%d')
    time_str = datetime.now().strftime('%H-%M-%S') # Adds the exact second
    
    # By adding the exact time to the filename, we FORCE a brand new post
    filename = f"_posts/{date_str}-{time_str}-update.md"
    
    os.makedirs("_posts", exist_ok=True)
    
    frontmatter = f"---\nlayout: default\ntitle: \"Market Shift: Today's Financial Tech Briefing\"\ndate: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n---\n\n"
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(frontmatter + content)
    print(f"✅ Success! V3 File saved to {filename}")

if __name__ == "__main__":
    news = fetch_news()
    blog_content = generate_blog_post(news)
    save_post(blog_content)
