import os
import psycopg2
from fastapi import FastAPI
from psycopg2.extras import RealDictCursor

app = FastAPI(title="Market Sentinel Intelligence API")
DATABASE_URL = os.getenv("DATABASE_URL")

@app.get("/")
def read_root():
    return {"message": "Sentinel API is Live. Go to /docs"}

@app.get("/history")
async def get_history(topic: str = "Strait of Hormuz"):
    """
    Mengambil data sejarah sentimen dari database PostgreSQL
    """
    try:
        conn = psycopg2.connect(DATABASE_URL)
        # RealDictCursor mengubah hasil SQL jadi format JSON otomatis
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        query = """
        SELECT source, title, sentiment, score, created_at 
        FROM sentiment_history 
        WHERE topic ILIKE %s 
        ORDER BY created_at DESC 
        LIMIT 20
        """
        cur.execute(query, (f"%{topic}%",))
        rows = cur.fetchall()
        
        cur.close()
        conn.close()
        
        return {
            "topic": topic,
            "count": len(rows),
            "data": rows
        }
    except Exception as e:
        return {"error": str(e)}
