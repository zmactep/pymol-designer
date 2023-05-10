"""Entry point to plugin"""
import warnings
warnings.filterwarnings("ignore")

from pymol.plugins import addmenuitemqt 
from PyQt5.QtWidgets import QDialog, QTabWidget, QLineEdit, \
                            QPushButton, QVBoxLayout, QHBoxLayout

from .folding.widget import FoldingWidget

# global reference to avoid garbage collection of our dialog
dialog = None

def __init_plugin__(_app=None):
    addmenuitemqt('Designer', run_plugin_gui)

def run_plugin_gui():
    """Runs dialog of the plugin"""
    global dialog

    if not dialog:
        dialog = PluginDialog()
    dialog.show()

class PluginDialog(QDialog):
    """Main dialog of the plugin"""
    def __init__(self):
        super(PluginDialog, self).__init__()
        self.setup_ui()
        self.setup_ss()

    def setup_ui(self):
        """Makes pretty view"""
        self.tabs = QTabWidget()
        self.folding_widget = FoldingWidget()
        self.tabs.addTab(self.folding_widget, "Ig Folding")

        self.status_line = QLineEdit()
        self.status_line.setEnabled(False)

        self.config_button = QPushButton("🔧")
        self.config_button.setEnabled(False)

        hbox = QHBoxLayout()
        hbox.addWidget(self.status_line)
        hbox.addWidget(self.config_button)

        vbox = QVBoxLayout()
        vbox.addWidget(self.tabs)
        vbox.addLayout(hbox)

        self.setLayout(vbox)

    def setup_ss(self):
        """Setup signals and slots"""
        self.folding_widget.status_changed.connect(self.status_line.setText)
