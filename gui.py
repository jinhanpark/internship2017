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

        #diff scope
        self.scope = 'x'
        self.dxButton.clicked.connect(self.scope_change)
        self.dyButton.clicked.connect(self.scope_change)

        self.funcFig = plt.Figure()
        self.funcCanvas = FigureCanvas(self.funcFig)
        self.funcGraphLayout.addWidget(self.funcCanvas)
        self.setLayout(self.funcGraphLayout)

        self.deriFig = plt.Figure()
        self.deriCanvas = FigureCanvas(self.deriFig)
        self.deriGraphLayout.addWidget(self.deriCanvas)

        
    def btn_clicked(self):
        self.statusbar.showMessage("Calculating...")
        
        try:
            #canonicalization and plotting
            meta = get_meta_expr(self.detectedInput.text())
            self.canonicalOutput.setText(str(meta))
            self.plot_func(meta)

            #differentiation and plotting
            deri = diff_meta(meta, self.scope)
            self.derivativeOutput.setText(str(deri))
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

    def eval_result(self, meta, xs, scope = 'x'):
        fx = []
        for x in xs:
            try:
                if scope == 'x':
                    result = eval_meta(meta, '%f'%x, 0)
                else:
                    result = eval_meta(meta, 0, '%f'%x)
            except:
                result = np.nan
            fx.append(result)
        return np.array(fx)
        

    def plot_func(self, meta):
        graph = self.funcFig.add_subplot(111)
        left_end = float(self.funcFrom.value())
        right_end = float(self.funcTo.value())
        assert left_end < right_end
        xs = np.arange(left_end, right_end+0.02, 0.01)
        fx = self.eval_result(meta, xs)
        graph.clear()
        graph.plot(xs, fx)
        max_pt = np.nanmax(fx)
        min_pt = np.nanmin(fx)
        height = max_pt-min_pt
        width = right_end - left_end
        if height > 10*width:
            mid = fx[int(len(fx)/2)]
            top = mid+3*width
            bottom = mid-3*width
        else:
            top = max_pt
            bottom = min_pt
        fx[fx>top+5*width] = np.nan
        fx[fx<bottom-5*width] = np.nan
        if np.isnan(fx).any():
            gap = 0
        else:
            gap = 0.5
        graph.clear()
        graph.plot(xs, fx)
        graph.set_xlabel('x')
        graph.set_title('f(x, 0)')
        graph.set_xlim([left_end, right_end])
        graph.set_ylim([max(bottom, np.nanmin(fx)) - gap,
                        min(top, np.nanmax(fx)) + gap])

        self.funcCanvas.draw()

    def plot_derivative(self, deri):
        graph = self.deriFig.add_subplot(111)
        graph.clear()
        left_end = float(self.deriFrom.text())
        right_end = float(self.deriTo.text())
        assert left_end < right_end
        xs = np.arange(left_end, right_end+0.02, 0.01)
        fx = self.eval_result(deri, xs, self.scope)
        graph.clear()
        graph.plot(xs, fx)
        max_pt = np.nanmax(fx)
        min_pt = np.nanmin(fx)
        height = max_pt-min_pt
        width = right_end - left_end
        if height > 10*width:
            mid = fx[int(len(fx)/2)]
            top = mid+3*width
            bottom = mid-3*width
        else:
            top = max_pt
            bottom = min_pt
        fx[fx>top+5*width] = np.nan
        fx[fx<bottom-5*width] = np.nan
        if np.isnan(fx).any():
            gap = 0
        else:
            gap = 0.5
        graph.clear()
        graph.plot(xs, fx)
        if self.scope == 'x':
            graph.set_xlabel('x')
            graph.set_title("(d/dx)f(x, 0)")
        else:
            graph.set_xlabel('y')
            graph.set_title("(d/dy)f(0, y)")

        graph.set_xlim([left_end, right_end])
        graph.set_ylim([max(bottom, np.nanmin(fx)) - gap,
                        min(top, np.nanmax(fx)) + gap])

        self.deriCanvas.draw()


if (__name__ == "__main__"):
    app = QApplication(sys.argv)
    my_window = MyWindow()
    my_window.show()
    app.exec_()
