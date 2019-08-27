from logging import handlers
import logging

def KTingLog(user_id):
    KTingLogFormatter = logging.Formatter('%(asctime)s,%(message)s')
    
    KTingLogHandler = handlers.TimedRotatingFileHandler(filename='./[{_id}]KTing.log'.format(_id = user_id), 
            when='midnight', interval=1, encoding='utf-8')
    KTingLogHandler.setFormatter(KTingLogFormatter)
    KTingLogHandler.suffix = "%Y%m%d"
    
    KTingLogger = logging.getLogger()
    KTingLogger.setLevel(logging.INFO)
    KTingLogger.addHandler(KTingLogHandler)
    return KTingLogger