import logging
import os

import certifi
from dotenv import load_dotenv
from openai import OpenAI
from pymongo import MongoClient
from pymongo.collection import Collection
from langchain_openai import OpenAIEmbeddings


OPENAI_MODEL = "gpt-4.1-mini"
EMBED_MODEL = "text-embedding-3-small"
RAG_DB_NAME = "rag_demo_db"
RAG_COLLECTION_NAME = "rag_docs"
logger = logging.getLogger(__name__)


def get_openai_key() -> str:
    load_dotenv()
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        logger.error("OPENAI_API_KEY is missing from environment.")
        raise ValueError("Missing OPENAI_API_KEY")
    logger.debug("OPENAI_API_KEY loaded successfully.")
    return key


def get_mongo_uri() -> str:
    load_dotenv()
    uri = os.getenv("MONGODB_URI")
    if not uri:
        logger.error("MONGODB_URI is missing from environment.")
        raise ValueError("Missing MONGODB_URI")
    logger.debug("MONGODB_URI loaded successfully.")
    return uri


def get_openai_client() -> OpenAI:
    logger.info("Creating OpenAI client instance.")
    return OpenAI(api_key=get_openai_key())


def get_mongo_collection(
    db_name: str = RAG_DB_NAME,
    collection_name: str = RAG_COLLECTION_NAME,
) -> Collection:
    logger.info("Connecting to MongoDB collection '%s.%s'.", db_name, collection_name)
    # Use certifi's CA bundle so Atlas TLS verifies on macOS / Python builds
    # whose default ssl context lacks system issuers ("unable to get local issuer certificate").
    ca = os.getenv("MONGODB_TLS_CA_FILE") or certifi.where()
    client = MongoClient(get_mongo_uri(), tlsCAFile=ca)
    return client[db_name][collection_name]


def get_embeddings(openai_key: str | None = None) -> OpenAIEmbeddings:
    logger.info("Initializing OpenAI embeddings model '%s'.", EMBED_MODEL)
    return OpenAIEmbeddings(model=EMBED_MODEL, api_key=openai_key or get_openai_key())
