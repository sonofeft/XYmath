
from xymath.xy_job import XY_Job
from xymath.gui.xygui import main as run_gui

XY = XY_Job()

# Grams
body_mass = [32000, 37800, 347000, 4200, 196500, 100000, 4290, 
    32000, 65000, 69125, 9600, 133300, 150000, 407000, 115000, 67000, 
    325000, 21500, 58588, 65320, 85000, 135000, 20500, 1613, 1618]

# kcal/hr
metabolic_rate = [49.984, 51.981, 306.770, 10.075, 230.073, 
    148.949, 11.966, 46.414, 123.287, 106.663, 20.619, 180.150, 
    200.830, 224.779, 148.940, 112.430, 286.847, 46.347, 142.863, 
    106.670, 119.660, 104.150, 33.165, 4.900, 4.865]

XY.define_dataset(body_mass, metabolic_rate, wtArr=None, 
    xName='Body Mass', yName='Metabolic Rate', xUnits='g', yUnits='mLO2/hr')

#XY.fit_dataset_to_nonlinear_eqn(run_best_pcent=0, rhs_eqnStr='p1*cos(p2*x) + p2*sin(p1*x)')

run_gui( XY )

