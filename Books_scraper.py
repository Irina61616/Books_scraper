import requests
from bs4 import BeautifulSoup
import json
import csv

def get_page(url):
    try:
        response = requests.get(url)
        response.raise_for_status()

        response.encoding = 'utf-8' 
        return response.text

    except requests.RequestException as e:
        print(f"Error while getting page: {e}")
        return None

def scrape_books(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    books = []

    for book in soup.find_all('article', class_='product_pod'):
        
        name = book.h3.a['title']

      
        price_text = book.find('p', class_='price_color').text.strip()
        price = float(price_text.replace('£', ''))

        stock_text = book.find('p', class_='instock availability').text.strip()
        in_stock = "In stock" in stock_text

        books.append({
            "name": name,
            "price": price,
            "in_stock": in_stock
        })

    return books


def save_to_json(books, filename):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(books, f, indent=4, ensure_ascii=False)

def save_to_csv(books, filename):
    with open(filename, "w", newline='', encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["name", "price", "in_stock"])
        writer.writeheader()
        writer.writerows(books)

def main():
    base_url = "https://books.toscrape.com/catalogue/page-{}.html"
    all_books = []

    for i in range(1, 4):  
        print(f"Parsing page {i}...")
        html_content = get_page(base_url.format(i))

        if html_content:
            books = scrape_books(html_content)
            all_books.extend(books)

    save_to_json(all_books, "books.json")
    print("Done! Data saved to books.json")
    save_to_csv(all_books, "books.csv")
    print("Done! Data saved to books.csv")


if __name__ == "__main__":
    main()