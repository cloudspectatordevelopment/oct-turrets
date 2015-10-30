LOGGING_CONFIG = {
    'version': 1,
    'root': {
        'level': 'NOTSET',
        'handlers': ['default']
    },
    'formatters': {
        'verbose': {
            'format': '[%(asctime)s: %(levelname)s | %(name)s] %(message)s'
        }
    },
    'handlers': {
        'default': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'oct_turrets': {
            'handlers': ['default'],
            'level': 'INFO',
            'propagate': False
        }
    }
}
