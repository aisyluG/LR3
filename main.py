from PyQt5.QtWidgets import QMainWindow, QApplication
from window import Ui_MainWindow
import sys
from subprocess import Popen, PIPE
from multiprocessing import Process, Queue
from PyQt5.QtCore import QProcess, QThread, QSemaphore, pyqtSignal, QTimer
from consoleReader import ConsoleReader
from consoleWriter import ConsoleWriter
from threading import Thread


class Window(QMainWindow):
    semaphore = QSemaphore()
    input_sended = pyqtSignal()
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.input = None
        # self.thr = Thread().
        self.timer = QTimer()
        self.reader_Thread = QThread()
        self.reader = ConsoleReader(self.semaphore, self.timer)
        self.reader.moveToThread(self.reader_Thread)

        self.writer_Thread = QThread()
        self.writer = ConsoleWriter(self.semaphore)
        self.writer.moveToThread(self.writer_Thread)

        self.ui.startBt.clicked.connect(self.startProcess)
        self.writer.process_created.connect(self.pp)
        # self.writer.process_created.connect(self.reader.set_pipe)
        self.reader.readed.connect(self.addToConsole)
        self.ui.sendBt.clicked.connect(self.addInput)
        self.timer.timeout.connect(self.ii)
        self.timer.timeout.connect(self.timer.stop)


    def ii(self):
        print('stopped')
        # self.reader_Thread.terminate()
        self.reader.thread().wait()

    def pp(self, process):
        self.reader.set_pipe(process)

    def addToConsole(self, output):
        self.ui.outputText.append(output)

    def startProcess(self):
        path = self.ui.comandLine.text()
        if '\\' in path:
            path = path.replace('\\', '/')
            # print(path)
        self.writer.createProcess(path, self.reader)
        self.reader.run()

    def addInput(self):
        input = self.ui.inputText.text()
        self.writer.write(input)
        self.ui.outputText.append('>'+input)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = Window()
    main.show()
    sys.exit(app.exec_())