from concurrent.futures import Future
from functools import partial
from PyQt6.QtCore import QThread, pyqtSignal, QObject
from PyQt6.QtWidgets import QApplication


def long_running_task(parameter):
    import time
    time.sleep(2)
    return parameter * 2


class Worker(QObject):
    progress = pyqtSignal(int)
    finished = pyqtSignal()
    error = pyqtSignal(str)

    def __init__(self, function, *args, **kwargs):
        super().__init__()
        self._future = Future()
        self._function = partial(function, *args, **kwargs)

    def run(self) -> None:
        try:
            result = self._function()
            self.finished.emit()
            self._future.set_result(result)
        except Exception as e:
            self.error.emit(str(e))
            self._future.set_exception(e)

    def result(self) -> object:
        return self._future.result()

    def wait(self):
        self._future.result()


class WorkerThread(QThread):
    def __init__(self, function, *args, **kwargs):
        super().__init__()
        self._worker = Worker(function, *args, **kwargs)
        self._worker.progress.connect(self.progress_signal.emit)
        self._worker.finished.connect(self.finished_signal.emit)
        self._worker.error.connect(self.error_signal.emit)

    def run(self) -> None:
        self._worker.run()

    progress_signal = pyqtSignal(int)
    finished_signal = pyqtSignal()
    error_signal = pyqtSignal(str)

    def join(self):
        self._worker.wait()


def test_worker():
    app = QApplication([])
    worker = WorkerThread(long_running_task, 7)
    worker.progress_signal.connect(lambda value: print(f"Progress: {value}"))
    worker.error_signal.connect(lambda error: print(f"Error: {error}"))
    worker.finished_signal.connect(lambda: print("Finished"))
    worker.start()
    print("Started")
    worker.join()
    print("Done")
    app.exec()


if __name__ == "__main__":
    test_worker()
