import requests
from bs4 import BeautifulSoup
import os

# Aralık belirle
start_id = 10000001
end_id = 10343763

# Headers ve cookies, curl'den alınanlar
headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-language": "tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7",
    "cache-control": "max-age=0",
    "priority": "u=0, i",
    "sec-ch-ua": '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "none",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36"
}

cookies = {

}

base_url = "https://www.forgottenbooks.com"

# Kayıt klasörü
os.makedirs("pdfler", exist_ok=True)

for book_id in range(start_id, end_id + 1):
    url = f"{base_url}/en/books/CulpepersCompleteHerbal_{book_id}"
    print(f"İşleniyor: {url}")

    try:
        response = requests.get(url, headers=headers, cookies=cookies, timeout=10)
        if response.status_code != 200:
            print(f"Sayfa alınamadı: {response.status_code}")
            continue

        soup = BeautifulSoup(response.text, "html.parser")
        pdf_div = soup.find("div", class_="iconbtn box83")
        if not pdf_div:
            print("PDF bölümü bulunamadı.")
            continue

        pdf_link = pdf_div.find("a")["href"]
        pdf_url = base_url + pdf_link
        pdf_name = pdf_link.split("/")[-1]

        # PDF dosyasını indir
        pdf_resp = requests.get(pdf_url, headers=headers, cookies=cookies)
        if pdf_resp.status_code == 200:
            with open(f"pdfler/{pdf_name}", "wb") as f:
                f.write(pdf_resp.content)
                print(f"İndirildi: {pdf_name}")
        else:
            print(f"PDF alınamadı: {pdf_resp.status_code}")
    except Exception as e:
        print(f"Hata oluştu: {e}")
