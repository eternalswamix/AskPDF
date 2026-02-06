import logging
import logging.config
import os
import json
from datetime import datetime

class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_obj = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
            "funcName": record.funcName,
            "lineNo": record.lineno,
        }
        if record.exc_info:
            log_obj["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_obj)

def setup_logging():
    log_dir = "logs"
    enable_file_logging = False

    # Try creating log dir (handles Read-Only File System on Serverless/Vercel)
    try:
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        enable_file_logging = True
    except OSError:
        # Fallback to console-only logging if file system is read-only
        pass

    logging_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": "[%(asctime)s] %(levelname)s in %(module)s: %(message)s",
            },
            "json": {
                "()": JSONFormatter,
            }
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": "INFO",
                "formatter": "default",
                "stream": "ext://sys.stdout"
            }
        },
        "root": {
            "level": "INFO",
            "handlers": ["console"]
        }
    }

    if enable_file_logging:
        logging_config["handlers"]["file"] = {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "INFO",
            "formatter": "json",
            "filename": os.path.join(log_dir, "app.log"),
            "maxBytes": 10485760, # 10MB
            "backupCount": 5
        }
        logging_config["root"]["handlers"].append("file")

    logging.config.dictConfig(logging_config)
