# This file is part of OMG-tools.
#
# OMG-tools -- Optimal Motion Generation-tools
# Copyright (C) 2016 Ruben Van Parys & Tim Mercy, KU Leuven.
# All rights reserved.
#
# OMG-tools is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 3 of the License, or (at your option) any later version.
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA
import sys
sys.path.insert(0, "/home/tim/Dropbox/EigenDocumenten/Doctoraat/MotionPlanning/omg-tools") 
from omgtools import *

# create vehicle
vehicle = Dubins(#shapes=Rectangle(width=0.4, height=0.1),
				 bounds={'vmax': 0.8, 'wmax': 60., 'wmin': -60.},  # in deg
                 options={'knot_intervals':5})
# vehicle.set_options({'safety_distance': 0.1})
# vehicle.set_options({'1storder_delay': True, 'time_constant': 0.1})
# vehicle.set_options({'input_disturbance': {'fc':0.01, 'stdev':0.05*np.ones(2)}})

vehicle.set_initial_conditions([0., 0., 0.])  # input orientation in deg
vehicle.set_terminal_conditions([3., 3., 0.])

# create environment
environment = Environment(room={'shape': Square(5.), 'position': [1.5, 1.5]})

trajectories = {'velocity': {0.5: [0.3, 0.0]}}
environment.add_obstacle(Obstacle({'position': [1., 1.]}, shape=Circle(0.5),
                                  trajectories=trajectories))

# create a point-to-point problem
problem = Point2point(vehicle, environment, freeT=True)
# extra solver settings which may improve performance
# problem.set_options({'solver': {'ipopt.linear_solver': 'ma57'}})
problem.set_options({'solver': {'ipopt.hessian_approximation': 'limited-memory'}})
# problem.set_options({'solver': {'ipopt.warm_start_bound_push': 1e-6}})
# problem.set_options({'solver': {'ipopt.warm_start_mult_bound_push': 1e-6}})
# problem.set_options({'solver': {'ipopt.mu_init': 1e-5}})
problem.init()

# create simulator
simulator = Simulator(problem)
simulator.plot.set_options({'knots': True, 'prediction': False})
simulator.plot.show('scene')
simulator.plot.show('input')
simulator.plot.show('state')

# run it!
simulator.run()

# show/save some results
simulator.plot.show_movie('scene', repeat=False)
# simulator.plot.save_movie('input', number_of_frames=4)
# simulator.plot.save('a', time=3)
