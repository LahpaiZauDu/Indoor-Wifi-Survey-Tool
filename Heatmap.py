import numpy as np
import matplotlib.pyplot as plt
import pykrige.kriging_tools as kt
from pykrige.ok import OrdinaryKriging

xco = ['315.7584670231728', '535.3663101604277', '737.5053475935829',
       '952.1221033868092', '969.590909090909', '972.0864527629233',
       '972.0864527629233', '702.5677361853832', '480.464349376114',
       '240.89215686274508', '58.717468805704016', '108.62834224598919',
       '101.1417112299464', '93.65508021390372']

yco = ['573.8743315508021', '578.8654188948307', '576.3698752228164',
       '576.3698752228164', '379.2219251336899', '207.02941176470597',
       '42.323529411764866', '27.35026737967928', '27.35026737967928',
       '32.34135472370781', '32.34135472370781', '189.56060606060612',
       '359.2575757575758', '568.8832442067736']

rv = ['-68', '-60', '-57', '-58', '-48', '-49', '-51', '-58', '-58',
      '-67', '-65', '-69', '-65', '-73']

xx = [int(float(x)) for x in xco]
yy = [int(float(x)) for x in yco]
rs = [int(float(x)) for x in rv]

x = np.array(xx)
y = np.array(yy)
phi = np.array(rs)

OK = OrdinaryKriging(
    x,
    y,
    phi,
    verbose=True,
    enable_plotting=False,
    nlags=14,
)

OK.variogram_model_parameters

gridx = np.arange(0, 1000, 40, dtype='float64')
gridy = np.arange(0, 600, 40, dtype='float64')
zstar, ss = OK.execute("grid", gridx, gridy)
cmap = plt.cm.get_cmap('RdYlGn', 256)
cax = plt.matshow(zstar, extent=(0, 1000, 0, 600), origin='lower', cmap=cmap)
plt.scatter(x, y, c='k', marker='o')
cbar = plt.colorbar(cax)
plt.title('Porosity estimate')
plt.show()
