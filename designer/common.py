"""Common functions and classes"""

import asyncio
from PyQt5.QtCore import QWidget, QObject, QThread, pyqtSignal

AMINO_ACIDS = set(["A", "C", "D", "E", "F",
                   "G", "H", "I", "K", "L",
                   "M", "N", "P", "Q", "R",
                   "S", "T", "V", "W", "Y"])

def is_aminoacids(s: str, allow_spaces: bool = False) -> bool:
    """Check that the string contains only amino acids"""
    if allow_spaces:
        s = "".join(s.split())
    if not all(c in AMINO_ACIDS for c in s):
        return False
    return True

class AsyncWorker(QObject):
    """Worker to run some task"""
    finished = pyqtSignal(dict)

    def __init__(self, function):
        super(AsyncWorker, self).__init__()
        self.function = function

    def run(self):
        """Run task"""
        result = ""
        try:
            result = self.function()
        except Exception:
            pass
        self.finished.emit(result)

class AsyncWidget(QWidget):
    """Widget that can perform async operations"""
    def __init__(self):
        self.thread = None
        self.worker = None
        self.in_progress = False

    def _on_finish(self, _):
        self.in_progress = False

    def run_async(self, function, on_finish = None):
        """Run some function in an aync way"""
        self.thread = QThread()
        self.worker = AsyncWorker(function)
        self.worker.moveToThread(self.thread)

        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)

        self.thread.started.connect(self.worker.run)
        self.thread.finished.connect(self.thread.deleteLater)

        self.worker.finished.connect(self._on_finish)
        if on_finish:
            self.worker.finished.connect(on_finish)

        self.in_progress = True
        self.thread.start()
