# import logging
# from pymilvus import MilvusClient
# from core.config import settings

# logger = logging.getLogger(__name__)

# class VectorDB:
#     client: MilvusClient | None = None

#     @classmethod
#     def connect(cls):
#         logger.info("Connecting to Milvus...")
#         try:
#             cls.client = MilvusClient(uri=settings.MILVUS_URI, secure=True)
#             logger.info("Milvus connected successfully.")
#         except Exception as e:
#             logger.error(f"Failed to connect to Milvus: {e}")
#             cls.client = None

#     @classmethod
#     def disconnect(cls):
#         if cls.client:
#             logger.info("Disconnecting from Milvus...")
#             cls.client.close()
#             cls.client = None

# vector_db = VectorDB()




import logging
import time
from pymilvus import MilvusClient, MilvusException
from core.config import settings

logger = logging.getLogger(__name__)

class VectorDB:
    client: MilvusClient | None = None

    @classmethod
    def connect(cls, retries: int = 5, delay: int = 3):
        logger.info("Attempting to connect to Milvus at %s", settings.MILVUS_URI)
        for attempt in range(1, retries + 1):
            try:
                cls.client = MilvusClient(uri=settings.MILVUS_URI, secure=False)
                logger.info("Milvus connected successfully on attempt %d", attempt)

                # Log collections to confirm connectivity
                collections = cls.client.list_collections()
                logger.debug("Milvus collections: %s", collections)
                return
            except MilvusException as e:
                logger.warning(
                    "Milvus not ready (attempt %d/%d): %s",
                    attempt, retries, str(e)
                )
                time.sleep(delay)
            except Exception as e:
                logger.exception("Unexpected error while connecting to Milvus")
                time.sleep(delay)

        logger.error("Failed to connect to Milvus after %d attempts", retries)
        cls.client = None

    @classmethod
    def disconnect(cls):
        if cls.client:
            logger.info("Disconnecting from Milvus...")
            try:
                cls.client.close()
                logger.info("Milvus disconnected successfully.")
            except Exception as e:
                logger.exception("Error while disconnecting Milvus")
            finally:
                cls.client = None

vector_db = VectorDB()
