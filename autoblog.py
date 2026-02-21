import feedparser
from google import genai
import os
from datetime import datetime
import urllib.parse
import random

# Initialize the Brain
client = genai.Client()

# UPGRADE 5.0: The Aggregator Engine
# A list of multiple diverse news sources
RSS_FEEDS = [
    "https://techcrunch.com/category/fintech/feed/",
    "https://finance.yahoo.com/news/rss",
    "https://cointelegraph.com/rss"
]

def fetch_news():
    print("📡 Fetching raw data from multiple sources...")
    articles = []
    
    # Loop through every website in our list
    for url in RSS_FEEDS:
        print(f"   -> Reading: {url}")
        try:
            feed = feedparser.parse(url)
            # Grab the top 2 latest articles from EACH feed
            for entry in feed.entries[:2]:
                title = entry.get('title', 'No Title')
                summary = entry.get('summary', '')
                articles.append(f"Source: {url}\nTitle: {title}\nSummary: {summary}\n")
        except Exception as e:
            print(f"   ⚠️ Error reading {url}: {e}")
            
    # Combine all articles separated by a dashed line
    return "\n---\n".join(articles)

def generate_blog_post(news_context):
    print("🧠 Sending massive data packet to Gemini for synthesis...")
    prompt = f"""
    You are a sharp, insightful financial technology analyst. 
    Read the following curated news snippets from multiple global sources. 
    Write a 500-word blog post synthesizing this diverse information into one cohesive narrative. 
    Look for underlying trends connecting traditional markets, startups, and digital economies.
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
        
        # Using the final AI Image Engine (Pollinations)
        safe_prompt = urllib.parse.quote("abstract highly detailed digital global finance economy technology")
        random_seed = random.randint(1, 100000)
        image_url = f"https://image.pollinations.ai/prompt/{safe_prompt}?width=800&height=400&nologo=true&seed={random_seed}"
        
        image_html = f'<img src="{image_url}" alt="Financial Header Image" style="width:100%; border-radius:8px; margin-bottom:20px;">\n\n'
        
        return image_html + response.text
        
    except Exception as e:
        print(f"⚠️ API Error: {e}")
        return None

def save_post(content):
    if not content:
        return
        
    print("💾 Formatting and saving file...")
    date_str = datetime.now().strftime('%Y-%m-%d')
    time_str = datetime.now().strftime('%H-%M-%S') 
    
    # Keeping the exact time in the filename to bypass browser caching!
    filename = f"_posts/{date_str}-{time_str}-update.md"
    
    os.makedirs("_posts", exist_ok=True)
    
    frontmatter = f"---\nlayout: default\ntitle: \"Global Markets: Today's Financial Tech Briefing\"\ndate: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n---\n\n"
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(frontmatter + content)
    print(f"✅ Success! V4 File saved to {filename}")

if __name__ == "__main__":
    news = fetch_news()
    blog_content = generate_blog_post(news)
    save_post(blog_content)
