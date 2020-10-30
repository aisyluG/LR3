from PyQt5.QtCore import QObject, pyqtSignal

class ConsoleReader(QObject):
    readed = pyqtSignal(str)

    def __init__(self, semaphore, timer):
        QObject.__init__(self)
        self.process = None
        self.semaphore = semaphore
        self.timer = timer
    def set_pipe(self, process):
        self.process = process.stdout

    def run(self):
        text = []
        while len(text) != 0 or text == []:
            self.semaphore.acquire()
            print('again')
            self.timer.start(2000)
            if self.process is not None:
                print('YEAR')
                text = self.process.readline()
                print(text, '1')
                if text != '':
                    self.readed.emit(text)
            self.semaphore.release()
            self.timer.stop()