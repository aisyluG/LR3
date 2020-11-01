from PyQt5.QtCore import QObject, pyqtSignal
from subprocess import Popen, PIPE


class ConsoleWriter(QObject):
    process_created = pyqtSignal(Popen)
    value_entered = pyqtSignal()

    def __init__(self, semaphore):
        QObject.__init__(self)
        self.semaphore = semaphore
        self.proc = None


    def createProcess(self, path):
        self.proc = Popen(path,  # shell=True,
                     stdin=PIPE, stdout=PIPE, stderr=PIPE, encoding='utf-8')
        # self.process_created.emit(self.proc)
        self.proc.stdin.write('4'+'\r\n')
        # self.proc.stdin.write('4' + '\r\n')
        self.semaphore.release(1)

    def write(self, input):
        if self.proc is not None:
            # self.semaphore.acquire()
            self.proc.stdin.writelines([input+'\r\n'])
            print('entered')
            self.semaphore.release()
            self.value_entered.emit()



