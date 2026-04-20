from fastapi import FastAPI
import json
import os

# Inisialisasi aplikasi FastAPI
app = FastAPI(title="Wired Articles API")

# Endpoint GET
@app.get("/articles")
def get_articles():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, "../data/articles.json")
    
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        return {"error": "File articles.json belum ada nih, coba run scraper-nya dulu."}
    except Exception as e:
        return {"error": str(e)}

# Endpoint tambahan buat ngetes doang
@app.get("/")
def read_root():
    return {"message": "API Responsi UTS IPBD Berjalan! Akses /articles untuk melihat data."}