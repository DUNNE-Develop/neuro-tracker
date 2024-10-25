import numpy as np

import pyqtgraph as pg
from pyqtgraph.Qt import QtCore


app = pg.mkQApp("Raw Data")

win = pg.GraphicsLayoutWidget(show=True, title="Raw Data")
win.resize(800, 800)
win.setWindowTitle('Raw Data')

pg.setConfigOptions(antialias=True)

p6 = win.addPlot(title="Raw Data Updating")
curve = p6.plot(pen='y')
data = np.random.normal(size=(10, 1000))
ptr = 0
def update():
    global curve, data, ptr, p6
    curve.setData(data[ptr % 10])
    if ptr == 0:
        p6.enableAutoRange('xy', False)
    ptr += 1
timer = QtCore.QTimer()
timer.timeout.connect(update)
timer.start(50)
