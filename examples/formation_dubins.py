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
import sys, os
sys.path.insert(0, os.getcwd()+'/..')
from omgtools import *

# create fleet
N = 4
vehicles = [Dubins(bounds={'vmax': 0.7, 'wmax': 60., 'wmin': -60.}) for l in range(N)]
for vehicle in vehicles:
    vehicle.define_knots(knot_intervals=5)

fleet = Fleet(vehicles)
configuration = RegularPolyhedron(0.2, N, np.pi/4.).vertices.T
init_positions = [-1.5, -1.5] + configuration
terminal_positions = [2., 2.] + configuration
init_pose = np.c_[init_positions, np.zeros(N)]
terminal_pose = np.c_[terminal_positions, np.zeros(N)]

fleet.set_configuration(configuration.tolist())
fleet.set_initial_conditions(init_pose.tolist())
fleet.set_terminal_conditions(terminal_pose.tolist())

# create environment
environment = Environment(room={'shape': Square(5.)})
rectangle = Rectangle(width=3., height=0.2)
environment.add_obstacle(Obstacle({'position': [-2.1, -0.5]}, shape=rectangle))
environment.add_obstacle(Obstacle({'position': [1.7, -0.5]}, shape=rectangle))

# create a formation point-to-point problem
options = {'rho': 0.01, 'horizon_time': 10}
problem = FormationPoint2point(fleet, environment, options=options)
problem.set_options({'solver_options': {'ipopt': {'ipopt.linear_solver': 'ma57'}}})
problem.init()

# create simulator
simulator = Simulator(problem)
problem.plot('scene')
fleet.plot('input', knots=True, labels=['v (m/s)', 'w (rad/s)'])
# vehicle.plot('state', knots=True, labels=['x (m)', 'y (m)', 'theta (rad)'])

# run it!
simulator.run()
