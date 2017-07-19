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
        self.pushButton.clicked.connect(self.btn_clicked)

        #Input
        self.lineEdit.textChanged.connect(self.line_edit_changed)
        self.lineEdit.returnPressed.connect(self.btn_clicked)
        self.deriFrom.returnPressed.connect(self.btn_clicked)
        self.deriTo.returnPressed.connect(self.btn_clicked)
        self.funcFrom.returnPressed.connect(self.btn_clicked)
        self.funcTo.returnPressed.connect(self.btn_clicked)

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

        
    def btn_clicked(self):
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

    def scope_change(self):
        if self.dxButton.isChecked():
            self.scope = 'x'
        else:
            self.scope = 'y'
        self.statusbar.showMessage("Differentiation scope has changed.")

    def rescale_and_truncate(self, fx, width):
        max_pt = np.nanmax(fx)
        min_pt = np.nanmin(fx)
        height = max_pt - min_pt

        if height > 6*width:
            mid = fx[int(len(fx)/2)]
            if np.isnan(mid):
                mid = (max_pt + min_pt)/2
            top = mid + 1*width
            bottom = mid - 1*width
        else:
            top = max_pt
            bottom = min_pt

        height = top-bottom

        if np.isnan(fx).any():
            gap = 0
        else:
            gap = 0.5
        
        top += gap
        bottom -= gap

        return bottom, top

    def plot_graph(self, graph, xs, fx, left_end, right_end, bottom, top, xlabel='x', title='f(x, 0)'):
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

        bottom, top = self.rescale_and_truncate(fx, width)

        self.plot_graph(graph, xs, fx, left_end, right_end, bottom, top)

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
        bottom, top = self.rescale_and_truncate(fx, width)

        if self.scope == 'x':
            x_label = 'x'
            title = "(d/dx)f(x, 0)"
        else:
            x_label = 'y'
            title = "(d/dy)f(0, y)"
        
        self.plot_graph(graph, xs, fx, left_end, right_end, bottom, top, x_label, title)

        # graph.clear()
        # graph.plot(xs, fx)
        # if self.scope == 'x':
        #     graph.set_xlabel('x')
        #     graph.set_title("(d/dx)f(x, 0)")
        # else:
        #     graph.set_xlabel('y')
        #     graph.set_title("(d/dy)f(0, y)")

        # graph.set_xlim([left_end, right_end])
        # graph.set_ylim([bottom, top])

        self.deriCanvas.draw()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    my_window = MyWindow()
    my_window.show()
    app.exec_()
