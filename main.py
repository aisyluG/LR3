from PyQt5.QtWidgets import QMainWindow, QApplication
from window import Ui_MainWindow
import sys
from subprocess import Popen, PIPE
from multiprocessing import Process, Queue
from PyQt5.QtCore import QProcess, QThread, QSemaphore, pyqtSignal, QTimer
from consoleReader import ConsoleReader
from consoleWriter import ConsoleWriter
from threading import Thread, Timer
from timer import Timer



class Window(QMainWindow):
    semaphore_start_reading = QSemaphore()
    input_sended = pyqtSignal()
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.sem_for_timer = QSemaphore()

        self.reader_Thread = QThread()
        self.reader = ConsoleReader(self.sem_for_timer, self.semaphore_start_reading)
        self.reader.moveToThread(self.reader_Thread)


        # self.timerThread = QThread()
        # self.timer = Timer(self.sem_for_timer, self.reader_Thread)
        # self.timer.moveToThread(self.timerThread)

        self.writer_Thread = QThread()
        self.writer = ConsoleWriter(self.semaphore_start_reading)
        self.writer.moveToThread(self.writer_Thread)


        self.thr_read = Thread(target=self.ff)
        self.thr_write = Thread(target=self.ww)
        # self.thr_timer = Thread(target=self.gg)

        self.ui.startBt.clicked.connect(self.startProcess)
        # self.writer.process_created.connect(self.pp)
        # self.writer.process_created.connect(self.reader.set_pipe)
        self.ui.sendBt.clicked.connect(self.addInput)
        self.writer.value_entered.connect(self.semaphore_start_reading.release)
        self.reader.readed.connect(self.addToConsole)
        # self.timer.timeout.connect(self.newThread)

        self.writer_Thread.start()
        # self.timerThread.start()
        self.reader_Thread.start()

    # def newThread(self):
    #     self.reader_Thread = QThread()
    #     self.reader = ConsoleReader(self.sem_for_timer, self.semaphore_start_reading)
    #     self.reader.moveToThread(self.reader_Thread)
    #
    #     self.reader.set_pipe(self.writer.proc)
    #     self.reader.readed.connect(self.addToConsole)
    #     self.timer.set_readerThread(self.reader_Thread)
    #
    #     self.reader_Thread.start()
    #     print('new thread')
    #     self.semaphore_start_reading.release()
    #     self.thr_read.run()
    #     self.thr_timer.run()

    def addToConsole(self, output):
        self.ui.outputText.append(output)

    def startProcess(self):
        path = self.ui.comandLine.text()
        self.path = path.replace('\\', '/')
            # print(path)
        # self.writer.createProcess(path)
        self.thr_write.start()
        self.thr_read.start()
        # self.thr_timer.start()

    def addInput(self):
        print('x')
        input = self.ui.inputText.text()
        print('y')
        self.ui.outputText.append('>'+input)
        self.writer.write(input)

    def ff(self):
        # self.sem = QSemaphore()
        # self.timerThread = QThread()
        # self.timer = Timer(self.sem)
        # self.timer.moveToThread(self.timerThread)
        # # self.timer.timeout.connect(self.ii)

        # self.timerThread.start()

        # reader_Thread = QThread()
        # self.reader = ConsoleReader(self.semaphore)
        # self.reader.moveToThread(reader_Thread)
        #
        # self.reader.readed.connect(self.addToConsole)

        # reader_Thread.start()

        # self.semaphore.acquire()
        # self.reader.set_pipe(self.writer.proc)
        # self.timer.start()
        print('start read')
        self.reader.run()

    def ww(self):
        print('start process')
        print(self.path)
        self.writer.createProcess(self.path)
        self.reader.set_pipe(self.writer.proc)

    #
    # def gg(self):
    #     print('start timer')
    #     self.timer.start()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = Window()
    main.show()
    sys.exit(app.exec_())