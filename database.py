import sqlite3

DB_NAME = "news.db"


def create_connection():
    return sqlite3.connect(DB_NAME)


def create_table():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS news
                   (
                       id
                       INTEGER
                       PRIMARY
                       KEY
                       AUTOINCREMENT,
                       title
                       TEXT,
                       url
                       TEXT
                       UNIQUE,
                       summary
                       TEXT,
                       date
                       TEXT
                   )
                   """)
    cursor.execute("""
    CREATE VIRTUAL TABLE IF NOT EXISTS news_fts USING fts5(
        title, 
        summary, 
        content='news', 
        content_rowid='id'
    )
    """)
    conn.commit()
    conn.close()


def insert_news(news_list):
    conn = create_connection()
    cursor = conn.cursor()
    inserted_count = 0

    for news in news_list:
        cursor.execute("SELECT id FROM news WHERE url = ?", (news["url"],))
        if cursor.fetchone():
            continue

        cursor.execute("""
                       INSERT INTO news (title, url, summary, date)
                       VALUES (?, ?, ?, ?)
                       """, (news["title"], news["url"], news["summary"], news["date"]))
        rowid = cursor.lastrowid
        cursor.execute("""
                       INSERT INTO news_fts(rowid, title, summary)
                       VALUES (?, ?, ?)
                       """, (rowid, news["title"], news["summary"]))
        inserted_count += 1

    conn.commit()
    conn.close()
    return inserted_count


def search_news(query):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
                   SELECT n.title, n.url, n.summary, n.date
                   FROM news_fts f
                            JOIN news n ON f.rowid = n.id
                   WHERE news_fts MATCH ?
                   """, (query,))
    results = cursor.fetchall()
    conn.close()
    return results


if __name__ == "__main__":
    create_table()
