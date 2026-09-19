import os
import json
import serpapi
from dotenv import load_dotenv

def main():
    load_dotenv()
    client = serpapi.Client(api_key=os.getenv('API_KEY'))
    
    with open("keywords.txt", "r", encoding="utf-8") as keywords_file:
        keywords = [line.strip() for line in keywords_file if line.strip()]
    
    banned_domains = [
        "youtube.com", "facebook.com", "twitter.com", "x.com", 
        "reddit.com", "linkedin.com", "tiktok.com", "instagram.com",
        "pinterest.com", "quora.com", "microsoft.com/en-us/security/business"
    ]
    
    banned_title_words = [
        "how to", "what is", "tutorial", "beginner", "definition", 
        "course", "learn", "symptoms of"
    ]

    collected_results = []
    
    for index, query in enumerate(keywords):
        print(f"[{index + 1}/{len(keywords)}] Searching: {query}")
        
        dorked_query = f"{query} -site:youtube.com -site:facebook.com -site:x.com -site:reddit.com"

        try:
            search_results = client.search({
                "q": dorked_query,
                "hl": "en",
                "gl": "us",
                "google_domain": "google.com"
            })
            
            organic_results = search_results.get("organic_results", [])
            
            for item in organic_results:
                link = item.get("link", "").lower()
                title = item.get("title", "").lower()
                
                if any(banned in link for banned in banned_domains):
                    continue
                
                if any(banned in title for banned in banned_title_words):
                    continue
                
                collected_results.append({
                    "query": query,
                    "title": item.get("title"),
                    "link": item.get("link"),
                    "snippet": item.get("snippet"),
                    "date": item.get("date", "Unknown"),
                    "position": item.get("position")
                })
                
        except Exception as e:
            print(f"Error trying to search '{query}': {e}")
            
    with open("cleaned_results.json", "w", encoding="utf-8") as results_file:
        json.dump(collected_results, results_file, indent=4, ensure_ascii=False)
        
    print("\nSearch finished!")

if __name__ == "__main__":
    main()
