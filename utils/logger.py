from loguru import logger
import os

# Ensure logs directory exists
os.makedirs("logs", exist_ok=True)

# Remove default
logger.remove()

# Add custom log sink to file
logger.add("logs/nl2sql.log", rotation="1 MB", retention="7 days", level="INFO")
