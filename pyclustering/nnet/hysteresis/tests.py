'''

Unit-tests for Hysteresis Oscillatory Network.

Copyright (C) 2015    Andrei Novikov (spb.andr@yandex.ru)

pyclustering is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

pyclustering is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

'''

import unittest;

from pyclustering.nnet.hysteresis import hysteresis_network;
from pyclustering.nnet import *;

from pyclustering.support import extract_number_oscillations;

class Test(unittest.TestCase):
    def templateOscillationExistance(self, num_osc, own_weight, neigh_weight, steps, time, initial_states = None, initial_outputs = None, conn_repr = conn_represent.MATRIX):
        network = hysteresis_network(num_osc, own_weight, neigh_weight, conn_represent = conn_repr);
        
        if (initial_states is not None):
            network.states = initial_states;
            
        if (initial_outputs is not None):
            network.outputs = initial_outputs;
        
        (t, x) = network.simulate(steps, time);
        
        oscillations = [];
        for index in range(num_osc):
            number_oscillations = extract_number_oscillations(x, index, 0.9);
            oscillations.append(number_oscillations)
            
            assert number_oscillations > 1;
            
        return oscillations;
    
    def testOscillationsOneOscillator(self):
        self.templateOscillationExistance(1, -2, -1, 1000, 10);
        self.templateOscillationExistance(1, -4, -1, 1000, 10);
        
    def testOscillationsTwoOscillators(self):
        self.templateOscillationExistance(2, -4, 1, 1000, 10, [1, 0], [1, 1]);
        self.templateOscillationExistance(2, -4, -1, 1000, 10, [1, 0], [1, 1]);
        
    def testOscillationsFiveOscillators(self):
        self.templateOscillationExistance(5, -4, -1, 1000, 10, [1, 0.5, 0, -0.5, -1], [1, 1, 1, 1, 1]);
        
    def testListConnectionRepresentation(self):
        self.templateOscillationExistance(1, -2, -1, 1000, 10, conn_repr = conn_represent.LIST);
        self.templateOscillationExistance(2, -4, -1, 1000, 10, [1, 0], [1, 1], conn_repr = conn_represent.LIST);
        self.templateOscillationExistance(5, -4, -1, 1000, 10, [1, 0.5, 0, -0.5, -1], [1, 1, 1, 1, 1], conn_repr = conn_represent.LIST);
        
    

if __name__ == "__main__":
    unittest.main();