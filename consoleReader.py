from PyQt5.QtCore import QObject, pyqtSignal, QTimerEvent

class ConsoleReader(QObject):
    readed = pyqtSignal(str)

    def __init__(self, semaphore_timer, semaphore_start_reading):
        QObject.__init__(self)
        self.process = None
        # self.timer = timer
        self.semaphore_timer = semaphore_timer
        self.semaphore_reading = semaphore_start_reading

    def set_pipe(self, process):
        self.process = process

    def run(self):
        text = 1
        while text != '':
            if self.process is not None and self.process.poll() is None:
                # self.semaphore_reading.acq+uire()
                print('YEAR')
                text = self.process.stdout.readline()
                self.semaphore_reading.release()
                self.semaphore_timer.release()
                print(text, '1')
                if text != '':
                    self.readed.emit('Output:' + text)
            else:
                print('ended')

