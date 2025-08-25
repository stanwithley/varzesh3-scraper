import sys
from scraper import fetch_news
from database import create_table, insert_news, search_news

def scrape():
    create_table()
    news_list = fetch_news()
    new_count = insert_news(news_list)
    print(f"[+] {new_count} خبر جدید دریافت شد و به DB اضافه شد.")

def search(query):
    results = search_news(query)
    if not results:
        print("[-] خبری پیدا نشد.")
    else:
        for r in results:
            print(f"Title: {r[0]}\nURL: {r[1]}\nSummary: {r[2]}\nDate: {r[3]}\n---")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("استفاده: python main.py scrape | python main.py search <query>")
    elif sys.argv[1] == "scrape":
        scrape()
    elif sys.argv[1] == "search":
        if len(sys.argv) < 3:
            print("لطفاً عبارت جستجو را وارد کنید.")
        else:
            query = " ".join(sys.argv[2:])
            search(query)
    else:
        print("دستور نامعتبر.")
