"""Folding window widget"""
import os

import time
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import pyqtSignal, QThread
from PyQt5 import uic

from designer.common import is_aminoacids, AsyncWidget
from designer.folding.igfold import fold_antibody, append_model

class FoldingWidget(AsyncWidget):
    """Widget with folding control"""
    status_changed = pyqtSignal(str)

    def __init__(self):
        super(FoldingWidget, self).__init__()
        uic.loadUi(os.path.join(os.path.dirname(__file__), 'folding_widget.ui'), self)

        self.heavy_chain_pred = ""
        self.light_chain_pred = ""

        self._setup()

    def _set_heavy(self, text):
        self.heavy_chain_pred = text

    def _set_light(self, text):
        self.light_chain_pred = text

    def _check_edit(self, edit, pred_text, set_pred_text):
        text = edit.toPlainText()
        if not is_aminoacids(text, allow_spaces=True):
            edit.setText(pred_text)
        else:
            set_pred_text(text)

    def _check_may_run(self):
        if self.heavy_chain_edit.toPlainText() and not self.in_progress:
            self.run_folding_button.setEnabled(True)
        else:
            self.run_folding_button.setEnabled(False)

    def _on_finish(self, result):
        if result['status'] == 'ok':
            self.status_changed.emit("Folding finished")
            append_model(result['content'])
        else:
            self.status_changed.emit(f"ERROR: {result['content']}")
        self.run_folding_button.setEnabled(True)

    def _run_folding(self):
        heavy_chain = "".join(self.heavy_chain_edit.toPlainText().split())
        light_chain = "".join(self.light_chain_edit.toPlainText().split())
        use_refine = self.refine_checkbox.isChecked()
        self.status_changed.emit("Folding started")
        self.run_folding_button.setEnabled(False)
        self.run_async(lambda: fold_antibody(heavy_chain, light_chain, use_refine),
                       self._on_finish)

    def _setup(self):
        self.heavy_chain_edit.textChanged.connect(lambda: self._check_edit(self.heavy_chain_edit,
                                                                           self.heavy_chain_pred,
                                                                           self._set_heavy))
        self.light_chain_edit.textChanged.connect(lambda: self._check_edit(self.light_chain_edit,
                                                                           self.light_chain_pred,
                                                                           self._set_light))
        self.heavy_chain_edit.textChanged.connect(self._check_may_run)
        self.run_folding_button.clicked.connect(self._run_folding)
