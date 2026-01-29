import logging
import os
import sys


def setup_logging():
    """Configure logging for the application."""
    os.makedirs("logs", exist_ok=True)
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler("logs/tracker.log"),
        ]
    )