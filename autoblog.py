import feedparser
from google import genai
import os
from datetime import datetime
import urllib.parse
import urllib.request
import random

client = genai.Client()

# 1. THE FIXED CATEGORIES (Auto-Sourced)
FIXED_CATEGORIES = [
    "Global Financial Markets",
    "Video Game Industry",
    "Space Exploration",
    "Global Tax Policy & Fintech Compliance",
    "Global Natural Disasters"
]

# 2. THE RANDOM POOL (Auto-Sourced)
RANDOM_POOL = [
    "Cybersecurity Breaches",
    "Green Energy Vehicles",
    "Artificial Intelligence Tech",
    "Archaeology Discoveries",
    "Biotech Health Science",
    "Hollywood Entertainment"
]

def get_todays_categories():
    today_seed = datetime.now().date().toordinal()
    random.seed(today_seed)
    
    random_keys = random.sample(RANDOM_POOL, 3)
    todays_categories = FIXED_CATEGORIES + random_keys
    
    random.seed()
    return todays_categories

def fetch_news(topic):
    print(f"📡 Dynamically scraping the internet for: {topic}...")
    
    # THE HACK: We ask Google News to aggregate the top 15 sources for us instantly
    safe_topic = urllib.parse.quote(topic)
    url = f"https://news.google.com/rss/search?q={safe_topic}&hl=en-US&gl=US&ceid=US:en"
    
    try:
        feed = feedparser.parse(url)
        articles = []
        # We grab the top 15 headlines across the entire web
        for entry in feed.entries[:15]:
            title = entry.get('title', 'No Title')
            articles.append(f"Headline: {title}\n")
        return "\n---\n".join(articles)
    except Exception as e:
        print(f"⚠️ Error reading aggregator: {e}")
        return ""

def generate_blog_post(category_name, news_context):
    print(f"🧠 Synthesizing {category_name} briefing from 15 global sources...")
    prompt = f"""
    You are a sharp, insightful editorial analyst. 
    Read the following curated breaking news headlines regarding {category_name}. 
    Write a 400-word blog post synthesizing this information into one cohesive narrative. 
    Look for trends connecting the headlines.
    Maintain a sophisticated, analytical, yet accessible tone.
    Write the article in clean Markdown. Do NOT include an image tag.
    
    Raw News Headlines:
    {news_context}
    """
    
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt
        )
        article_text = response.text
    except Exception as e:
        print(f"⚠️ Gemini API Error: {e}")
        return None

    print(f"🖼️ Securing image for {category_name}...")
    try:
        safe_prompt = urllib.parse.quote(f"abstract highly detailed {category_name} professional")
        random_seed = random.randint(1, 100000)
        image_url = f"https://image.pollinations.ai/prompt/{safe_prompt}?width=800&height=400&nologo=true&seed={random_seed}"
        
        os.makedirs("assets", exist_ok=True)
        image_filename = f"header-{random_seed}.jpg"
        image_filepath = f"assets/{image_filename}"
        
        req = urllib.request.Request(image_url, headers={'User-Agent': 'Mozilla/5.0'})
        
        with urllib.request.urlopen(req) as img_response, open(image_filepath, 'wb') as out_file:
            out_file.write(img_response.read())
        
        hosted_image_url = f"https://captainnemo7299999-afk.github.io/automated-blog/assets/{image_filename}"
        image_html = f'<img src="{hosted_image_url}" alt="{category_name} Header Image" style="width:100%; border-radius:8px; margin-bottom:20px;">\n\n'
        
    except Exception:
        print(f"⚠️ Cloudflare blocked the download. Injecting fallback image!")
        fallback_seed = random.randint(1, 10000)
        fallback_url = f"https://picsum.photos/seed/{fallback_seed}/800/400"
        image_html = f'<img src="{fallback_url}" alt="Header Image" style="width:100%; border-radius:8px; margin-bottom:20px;">\n\n'

    return image_html + article_text

def save_post(category_name, content):
    if not content:
        return
    print("💾 Formatting and saving file...")
    date_str = datetime.now().strftime('%Y-%m-%d')
    time_str = datetime.now().strftime('%H-%M-%S') 
    
    safe_title = category_name.replace(" ", "-").replace("&", "and").lower()
    filename = f"_posts/{date_str}-{time_str}-{safe_title}.md"
    os.makedirs("_posts", exist_ok=True)
    
    frontmatter = f"---\nlayout: default\ntitle: \"{category_name}: Today's Briefing\"\ndate: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n---\n\n"
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(frontmatter + content)
    print(f"✅ Success! File saved to {filename}")

STATE_FILE = "assets/_slot_state.txt"

if __name__ == "__main__":
    os.makedirs("assets", exist_ok=True)
    todays_categories = get_todays_categories()
    
    current_slot = 0
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, 'r') as f:
            try:
                current_slot = int(f.read().strip())
            except ValueError:
                current_slot = 0
                
    if current_slot >= 8:
        current_slot = 0

    category_to_run = todays_categories[current_slot]
    
    print(f"\n======================================")
    print(f"⏰ Wake up! It is publishing slot {current_slot + 1} of 8.")
    print(f"🚀 Processing Category: {category_to_run}")
    print(f"======================================")
    
    # We pass the category name directly to the auto-sourcer
    news = fetch_news(category_to_run)
    
    if news:
        blog_content = generate_blog_post(category_to_run, news)
        save_post(category_to_run, blog_content)
    
    next_slot = (current_slot + 1) % 8
    with open(STATE_FILE, 'w') as f:
        f.write(str(next_slot))
        
    print(f"💤 Done. Engine sleeping for 2 hours. Next up: Slot {next_slot + 1}.")
