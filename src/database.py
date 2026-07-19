import os
import json
import chromadb
from chromadb.utils import embedding_functions


def get_chroma_client():
    """
    Initializes and returns a persistent ChromaDB client.
    Data is stored in the ./chroma_db folder.
    """
    return chromadb.PersistentClient(path="./chroma_db")


def setup_and_populate_db(json_file_path="./data/sports_facts.json"):
    """
    Reads the offline JSON facts, creates a collection, and populates it.
    This only needs to be run once (or when the JSON data changes).
    """
    client = get_chroma_client()

    # Use ChromaDB's default embedding function (sentence-transformers)
    embedding_fn = embedding_functions.DefaultEmbeddingFunction()

    # Get or create the collection
    collection = client.get_or_create_collection(
        name="sports_history",
        embedding_function=embedding_fn
    )

    # If already populated, skip
    if collection.count() > 0:
        print(f"Database already populated with {collection.count()} facts.")
        return collection

    # Check if data file exists
    if not os.path.exists(json_file_path):
        print(f"Error: Raw fact data file not found at {json_file_path}")
        return collection

    # Load and parse facts
    with open(json_file_path, "r", encoding="utf-8") as f:
        facts_list = json.load(f)

    documents = []
    metadata_list = []
    ids = []

    for idx, item in enumerate(facts_list):
        documents.append(item["fact"])
        # Store sport as metadata so we can filter later
        metadata_list.append({"sport": item["sport"]})
        ids.append(f"fact_{idx}")

    # Bulk add vectors to collection
    collection.add(
        documents=documents,
        metadatas=metadata_list,
        ids=ids
    )

    print(f"Successfully vectorized and stored {len(documents)} facts.")
    return collection


def query_historic_facts(sport: str, query_text: str, n_results: int = 3):
    """
    Queries ChromaDB for historic documents related to a sport.
    Filters results to match the selected sport category.
    """
    client = get_chroma_client()
    embedding_fn = embedding_functions.DefaultEmbeddingFunction()

    collection = client.get_or_create_collection(
        name="sports_history",
        embedding_function=embedding_fn
    )

    # Query with metadata filtering
    results = collection.query(
        query_texts=[query_text],
        n_results=n_results,
        where={"sport": sport}
    )

    # Return matched documents (or empty list if none found)
    return results.get("documents", [[]])[0]