import logging
import os


class DjangoLogger:

    def __init__(self, name='Django_Logger', rootOutputPath='./Django_Logger.log', homePath=None):

        if not homePath or not os.path.isdir(homePath):
            self.homePath = os.getcwd()
        self.homePath = homePath
        
        self.name = name
        self.rootlog = logging.getLogger(name)

        # Add File hander with home/Django_logger.log
        fh = logging.FileHandler(filename=rootOutputPath+'.log')
        self.rootlog.addHandler(fh)
        self.metaLog = self.make_meta_log()
        
    
    def make_meta_log(self):
        metaLog = self.rootlog.getChild('Meta_Django')
        metaPath = os.path.join(self.homePath, 'metaLog.log')
        metaHandler = self.generate_handler(metaPath)
        metaLog.addHandler(metaHandler)
        return metaLog

    
    def make_log(self, name='child'):
        """ Make a log with rootLog.getChild(name)
            Attaches a file handler from self.generate_handler

        Args:
            outputPath (Path): .log file Path, passes into self.generate_handler()
            name (str, optional): name of child log; resolves to 'home.child'. Defaults to 'child'.

        Returns:
            newLog: new logger object
        """        
        newLog = self.rootlog.getChild(name)
        fileHandler = self.generate_handler(name)
        newLog.addHandler(fileHandler)
        return newLog
    
    def generate_handler(self, name):
        """ Generate a file handler for a logger obj

        Args:
            path (Path): Path to assign the fileHandler to

        Returns:
            fileHandler: File Handler Obj to attach to log
        """        
        fmt = '%(levelname)s : %(message)s - %(name)s - %(asctime)s'
        formatter = logging.Formatter(fmt,datefmt='%I:%M:%S:%ms %p')
        filePath = os.path.join(self.homePath, name + '.log')
        fileHandler = logging.FileHandler(filePath)
        fileHandler.setFormatter(formatter)
        return fileHandler