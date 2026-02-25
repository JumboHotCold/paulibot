import sqlite3
import sqlite_vec
from sentence_transformers import SentenceTransformer
import json
import logging
import sys
import os

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

# Ensure we're in the right directory
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from chatbot.data import LOCATIONS, STAFF, ADMISSIONS_FAQ
    logger.info("Successfully imported FAQ data from chatbot.data")
except ImportError as e:
    logger.error(f"Failed to import chatbot.data: {e}")
    sys.exit(1)

def extract_faqs():
    """Extract and format FAQs from the local data file into plain text chunks."""
    chunks = []
    
    # Extract Locations
    for key, data in LOCATIONS.items():
        text = f"Location: {data['name']}. {data['description']}"
        if data.get('map_available'):
             text += " A map is available for this location."
        chunks.append({
            "source": f"location_{key}",
            "text": text
        })
        
    # Extract Staff
    for key, data in STAFF.items():
        text = f"Staff: {data['name']}, {data['position']}. Office located at {data['office']}."
        chunks.append({
            "source": f"staff_{key}",
            "text": text
        })
        
    # Extract Admissions FAQ
    for key, text in ADMISSIONS_FAQ.items():
        chunks.append({
            "source": f"faq_{key}",
            "text": f"Admission Information on {key}: {text}"
        })
        
    return chunks

def setup_db(chunks):
    """Set up the sqlite-vec in-memory database and insert embedded chunks."""
    logger.info("Loading embedding model (all-MiniLM-L6-v2) - This may take a moment on first run to download...")
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    logger.info(f"Generating embeddings for {len(chunks)} text chunks...")
    db = sqlite3.connect(":memory:")
    
    db.enable_load_extension(True)
    sqlite_vec.load(db)
    db.enable_load_extension(False)
    
    # Ensure vec loaded correctly
    vec_version = db.execute("select vec_version()").fetchone()[0]
    logger.info(f"Loaded sqlite-vec version {vec_version}")

    # Create tables
    db.execute("CREATE TABLE faq_chunks (id INTEGER PRIMARY KEY, source TEXT, text TEXT)")
    # For all-MiniLM-L6-v2, dimension is 384
    db.execute("CREATE VIRTUAL TABLE vec_faq USING vec0(embedding float[384])")
    
    # Insert data
    for i, chunk in enumerate(chunks):
        row_id = i + 1
        source = chunk["source"]
        text = chunk["text"]
        
        # Compute embedding
        embedding = model.encode(text).tolist()
        
        # Insert raw text + metadata
        db.execute("INSERT INTO faq_chunks (id, source, text) VALUES (?, ?, ?)", (row_id, source, text))
        
        # Insert vector embedding
        db.execute("INSERT INTO vec_faq (rowid, embedding) VALUES (?, ?)", 
                   (row_id, sqlite_vec.serialize_float32(embedding)))
                   
    db.commit()
    logger.info("Successfully inserted embeddings into sqlite-vec database.")
    
    return db, model

def search(db, model, query, limit=2):
    """Perform a semantic vector search against the database."""
    query_vector = model.encode(query).tolist()
    
    # Perform vector search using vec0
    rows = db.execute(
        """
        SELECT faq_chunks.text, faq_chunks.source, vec_distance_L2(vec_faq.embedding, ?) as distance
        FROM vec_faq
        LEFT JOIN faq_chunks ON faq_chunks.id = vec_faq.rowid
        WHERE vec_faq.embedding MATCH ? AND k = ?
        ORDER BY distance
        """,
        (sqlite_vec.serialize_float32(query_vector), sqlite_vec.serialize_float32(query_vector), limit)
    ).fetchall()
    
    return rows

def main():
    logger.info("--- PauliBot RAG PoC Started ---")
    chunks = extract_faqs()
    db, model = setup_db(chunks)
    
    # Test Queries
    test_queries = [
        "Where can I pay my tuition?",
        "Who is the head of the IT department?",
        "How do I enroll in SPUS?"
    ]
    
    print("\n" + "="*50)
    print("Executing Semantic Searches")
    print("="*50)
    
    for q in test_queries:
        print(f"\n[USER QUERY] -> {q}")
        results = search(db, model, q)
        for i, (text, source, distance) in enumerate(results):
            print(f"  Result {i+1} [Distance: {distance:.4f}]: {text}")

if __name__ == "__main__":
    main()
