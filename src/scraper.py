import json
import csv
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scrape_wired_pagination():
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    # Kategori yang akan di-scrape
    base_categories = [
        "https://www.wired.com/category/computers",
        "https://www.wired.com/category/science",
        "https://www.wired.com/category/security"
    ]
    
    articles_data = []
    target_count_per_kategori = 100
    total_target = target_count_per_kategori * len(base_categories)
    
    for base_url in base_categories:
        page = 1 
        jumlah_kategori_ini = 0
        
        while jumlah_kategori_ini < target_count_per_kategori:
            if page == 1:
                url = f"{base_url}/"
            else:
                url = f"{base_url}/?page={page}" # Menggunakan format ?page=x
                
            print(f"\n[!] Mengakses: {url}")
            driver.get(url)
            time.sleep(3) 
            
            try:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "div[class*='SummaryItemWrapper']"))
                )
                
                articles = driver.find_elements(By.CSS_SELECTOR, "div[class*='SummaryItemWrapper']")
                
                if not articles:
                    print(f"Halaman kosong di {url}, pindah kategori...")
                    break
                
                for article in articles:
                    if jumlah_kategori_ini >= target_count_per_kategori:
                        break
                        
                    try:
                        title = article.find_element(By.CSS_SELECTOR, "h3, h2").text
                        article_url = article.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
                        
                        try:
                            desc_element = article.find_element(By.CSS_SELECTOR, "div[class*='Dek'], div[class*='dek'], p[class*='summary']")
                            description = desc_element.text
                            if not description: description = "-"
                        except:
                            description = "-"
                            
                        try:
                            author_element = article.find_element(By.CSS_SELECTOR, "[class*='Byline'], [class*='byline'], [data-testid*='Byline']")
                            author_text = author_element.text.strip().title()
                            
                            if author_text:
                                author = author_text if author_text.startswith("By ") else f"By {author_text}"
                            else:
                                author = "By Unknown"
                        except:
                            author = "By Unknown"
                            
                        if title and not any(d['url'] == article_url for d in articles_data):
                            articles_data.append({
                                "title": title,
                                "url": article_url,
                                "description": description,
                                "author": author,
                                "scraped_at": datetime.now().isoformat(),
                                "source": "Wired.com"
                            })
                            
                            # Counter spesifik kategori nambah
                            jumlah_kategori_ini += 1
                            
                            print(f"[{len(articles_data)}/{total_target}] Berhasil ambil: {title[:20]}... | Author: {author}")
                    
                    except Exception as e:
                        continue
                
                # Lanjut ke halaman berikutnya 
                page += 1
                
            except Exception as e:
                print(f"Tidak ada artikel lagi di {url} atau terjadi error. Pindah kategori.")
                break 

    driver.quit()
    
    # Simpan data JSON
    json_output = {
        "session_id": f"wired_session_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        "timestamp": datetime.now().isoformat(),
        "articles_count": len(articles_data),
        "articles": articles_data
    }
    
    with open("data/articles.json", "w", encoding="utf-8") as f:
        json.dump(json_output, f, indent=4, ensure_ascii=False)
    
    # Simpan data CSV
    if articles_data:
        csv_keys = articles_data[0].keys()
        with open("data/articles.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=csv_keys)
            writer.writeheader()
            writer.writerows(articles_data)
            
    print(f"\n[+] SELESAI! Berhasil menyimpan {len(articles_data)} data.")

if __name__ == "__main__":
    scrape_wired_pagination()