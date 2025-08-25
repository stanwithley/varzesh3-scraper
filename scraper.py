import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.varzesh3.com"

def fetch_news():
    response = requests.get(BASE_URL)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    news_list = []

    for item in soup.find_all("a", class_="title"):
        title = item.get_text(strip=True)
        url = item["href"]
        full_url = BASE_URL + url if url.startswith("/") else url

        summary = "خلاصه‌ای موجود نیست"
        date = "تاریخ مشخص نیست"

        news_list.append({
            "title": title,
            "url": full_url,
            "summary": summary,
            "date": date
        })

    return news_list

if __name__ == "__main__":
    news = fetch_news()
    for n in news:
        print(n)