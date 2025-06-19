
# src/utils/logger.py
import logging
import logging.config
import yaml
from pathlib import Path
from typing import Optional

def setup_logging(
    default_path: str = 'config/logging.yaml',
    default_level: int = logging.INFO,
    env_key: str = 'LOG_CFG'
) -> None:
    """Configure le système de logging"""
    
    path = Path(default_path)
    value = os.getenv(env_key, None)
    
    if value:
        path = Path(value)
    
    if path.exists():
        with open(path, 'rt') as f:
            logging_config = yaml.safe_load(f.read())
        logging.config.dictConfig(logging_config)
    else:
        logging.basicConfig(
            level=default_level,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(config.log_file),
                logging.StreamHandler()
            ]
        )

def get_logger(name: str) -> logging.Logger:
    """Récupère un logger configuré"""
    return logging.getLogger(name)

# ============================================================================