import requests
import time
import pandas as pd
from datetime import datetime
import os

# Configuration
BASE_URL = "http://quotes.toscrape.com"
OUTPUT_DIR = "data/raw/pages"
os.makedirs(OUTPUT_DIR,exist_ok=True)


headers = {
    'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

def fetch_page(url,session):
    try:
        start_time = time.time()
        response = session.get(url,timeout=10)
        response.raise_for_status()
        response_time = time.time() - start_time
        #response_time = response.elapsed.total_seconds()

        return {
            'html' : response.text,
            'status' : response.status_code,
            'size' : len(response.content),
            'time' : response_time,
            'success' : True
        }
    except Exception as e :
        print(f"exception avec url : {url} de type : {e}")
        return {
            'html' : None,
            'status' : None,
            'size' : 0,
            'time' : 0,
            'success' : False
        }


def main():
    # Session
    session = requests.Session()
    session.headers.update(headers)

    urls = [
        f"{BASE_URL}/",
        f"{BASE_URL}/page/2/",
        f"{BASE_URL}/page/3/",
    ]

    repport_data = []

    for i,url in enumerate(urls,1):
        print(f"page {i}/3 : {url}")

        result = fetch_page(url,session)

        if result['success']:
            filename = f"{OUTPUT_DIR}/page_{i}.html"
            with open(filename,'w',encoding='utf-8') as f:
                f.write(result['html'])
            print("html sauvegardé")
            print(f" taille : {result['size']}")
            print(f" temps : {result['time']}")

        repport_data.append({
            'url' : url,
            'status' : result['status'],
            'size_bytes' : result['size'],
            'respond-time_s' : result['time'],
            'success' : result['success'],
            'timestamp' : datetime.now().isoformat()
        })

        time.sleep(1)

    
    df = pd.DataFrame(repport_data)
    df.to_csv('data/output/report.csv', index=False)
    print("Rapport generer")

    session.close()


if __name__ == '__main__':
    main()