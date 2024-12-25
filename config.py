import os
import sys
from pathlib import Path
from loguru import logger


if getattr(sys, 'frozen', False):
    ROOT_DIR = Path(sys.executable).parent.absolute()
else:
    ROOT_DIR = Path(__file__).parent.parent.absolute()


logi_path = os.path.join(ROOT_DIR)

logger.add(
    f'{os.path.join(logi_path, "claim.log")}',
    format='{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}',
    level='INFO'
)