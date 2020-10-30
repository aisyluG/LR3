from PyQt5.QtCore import QObject, pyqtSignal
from subprocess import Popen, PIPE


class ConsoleWriter(QObject):
    process_created = pyqtSignal(Popen)

    def __init__(self, semaphore):
        QObject.__init__(self)
        self.semaphore = semaphore
        self.proc = None


    def createProcess(self, path, reader):
        self.proc = Popen(path,  # shell=True,
                     stdin=PIPE, stdout=PIPE, stderr=PIPE, encoding='utf-8')
        self.process_created.emit(self.proc)
        self.semaphore.release(1)

    def write(self, input):
        if self.proc is not None:
            self.semaphore.acquire()
            self.proc.stdin.write(input+'\r\n')
            self.semaphore.release(1)




