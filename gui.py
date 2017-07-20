import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from tree_generator import get_meta_expr
from evaluator import eval_meta
from differentiator import diff_meta

ui_imported = uic.loadUiType("main_window.ui")[0]

class MyWindow(QMainWindow, ui_imported):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setupUi_more()

    def setupUi_more(self):
        #pushButton
        self.pushButton.clicked.connect(self.run_all)

        #Input
        self.lineEdit.textChanged.connect(self.line_edit_changed)
        self.lineEdit.returnPressed.connect(self.run_all)
        self.deriFrom.returnPressed.connect(self.run_all)
        self.deriTo.returnPressed.connect(self.run_all)
        self.funcFrom.returnPressed.connect(self.run_all)
        self.funcTo.returnPressed.connect(self.run_all)

        #diff scope
        self.scope = 'x'
        self.dxButton.clicked.connect(self.scope_change)
        self.dyButton.clicked.connect(self.scope_change)

        #plot func
        self.funcFig = plt.Figure()
        self.funcCanvas = FigureCanvas(self.funcFig)
        self.funcGraphLayout.addWidget(self.funcCanvas)

        #plot derivative
        self.deriFig = plt.Figure()
        self.deriCanvas = FigureCanvas(self.deriFig)
        self.deriGraphLayout.addWidget(self.deriCanvas)

        #stepsize
        self.step_size = float(self.stepSize.text())
        self.stepSize.textChanged.connect(self.step_size_changed)
        self.stepSize.returnPressed.connect(self.run_all)

        
    def run_all(self):
        try:
            #canonicalize
            self.statusbar.showMessage("Calculating canonical form...")
            meta = get_meta_expr(self.detectedInput.text())
            self.canonicalOutput.setText(str(meta))

            #plot function
            self.statusbar.showMessage("Plotting function...")
            self.plot_func(meta)

            #differentiate
            self.statusbar.showMessage("Calculating derivative...")
            deri = diff_meta(meta, self.scope)
            self.derivativeOutput.setText(str(deri))

            #plot derivative
            self.statusbar.showMessage("Plotting derivative...")
            self.plot_derivative(deri)

            self.statusbar.showMessage("Done.")
        except:
            self.statusbar.showMessage("An Error Occured.")
            QMessageBox.about(self, "Error Message", "An Error Occured.")
    

    def line_edit_changed(self):
        self.detectedInput.setText(self.lineEdit.text())
        self.statusbar.showMessage("Input has changed.")

    def step_size_changed(self):
        try:
            step_size = float(self.stepSize.text())
            assert step_size >= 0.005
            self.step_size = step_size
            self.statusbar.showMessage("Stepsize changed. : %f"%self.step_size)
        except:
            self.statusbar.showMessage("(Error) step size: %f"%self.step_size)

    def scope_change(self):
        if self.dxButton.isChecked():
            self.scope = 'x'
        else:
            self.scope = 'y'
        self.statusbar.showMessage("Differentiation scope has changed.")

    def plot_graph(self, graph, xs, fx, xlabel='x', title='f(x, 0)'):
        graph.clear()
        graph.plot(xs, fx)
        graph.set_xlabel(xlabel)
        graph.set_title(title)
        graph.spines['right'].set_visible(False)
        graph.spines['top'].set_visible(False)


    def plot_func(self, meta):
        graph = self.funcFig.add_subplot(111)
        left_end = float(self.funcFrom.text())
        right_end = float(self.funcTo.text())
        width = right_end - left_end
        assert left_end < right_end
        xs = np.arange(left_end//np.pi, right_end//np.pi+1, self.step_size)
        fx = np.array([eval_meta(meta, x, 0, with_pi=True) for x in xs])
        xs *= np.pi

        self.plot_graph(graph, xs, fx)

        self.funcCanvas.draw()

    def plot_derivative(self, deri):
        graph = self.deriFig.add_subplot(111)
        left_end = float(self.deriFrom.text())
        right_end = float(self.deriTo.text())
        width = right_end - left_end
        assert left_end < right_end
        xs = np.arange(left_end//np.pi, right_end//np.pi+1, self.step_size)
        if self.scope == 'x':
            fx = np.array([eval_meta(deri, x, 0, with_pi=True) for x in xs])
        else:
            fx = np.array([eval_meta(deri, 0, x, with_pi=True) for x in xs])
        xs *= np.pi

        if self.scope == 'x':
            x_label = 'x'
            title = "(d/dx)f(x, 0)"
        else:
            x_label = 'y'
            title = "(d/dy)f(0, y)"
        
        self.plot_graph(graph, xs, fx, x_label, title)
        
        self.deriCanvas.draw()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    my_window = MyWindow()
    my_window.show()
    app.exec_()
