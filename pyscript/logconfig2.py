#-*- coding:utf-8 –*-

import logging.config
import logging.handlers
import logging
import _init_config



logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt': "%Y-%m-%d %H:%M:%S"
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'file': {
            'level': 'DEBUG',
            #'class': 'logging.handlers.RotatingFileHandler',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            # 当达到10MB时分割日志
            #'maxBytes': 1024 * 1024 * 10,
            # 最多保留1000份文件
            #'backupCount': 6000,
            # If delay is true,
            # then file opening is deferred until the first call to emit().
            'delay': True,
            'filename': '/data/checkcode/logs/checkcode_iserror.log',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        '': {
            'handlers': ['file'],
            'level': 'INFO',
        },
    }
})
