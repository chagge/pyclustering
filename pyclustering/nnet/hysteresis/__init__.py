'''

Neural Network: Hysteresis Oscillatory Network

Based on article description:
 - K.Jinno. Oscillatory Hysteresis Associative Memory. 2002.
 - K.Jinno, H.Taguchi, T.Yamamoto, H.Hirose. Dynamical Hysteresis Neural Network for Graph Coloring Problem. 2003.

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

import numpy;

from scipy.integrate import odeint;

from pyclustering.nnet import *;


class hysteresis_network(network, network_interface):
    _name = "Hysteresis Neural Network";
    _states = None;             # list of states of neurons.
    _outputs_buffer = None;     # list of previous outputs of neurons.
    _outputs = None;            # list of current outputs of neurons.
    _weight = None;             # matrix of connection weights between neurons.
    
    @property
    def outputs(self):
        "Returns current outputs of neurons."
        return self._outputs;
    
    @outputs.setter
    def outputs(self, values):
        "Set current outputs of neurons."
        self._outputs = [val for val in values];
        self._outputs_buffer = [val for val in values];
    
    @property
    def states(self):
        "Returns current states of neurons."
        return self._states;
    
    @states.setter
    def states(self, values):
        "Set current states of neurons."
        self._states = [val for val in values];
   
    
    def __init__(self, num_osc, own_weight = -4, neigh_weight = -1, type_conn = conn_type.ALL_TO_ALL, conn_represent = conn_represent.MATRIX):
        "Constructor of hysteresis oscillatory network."
        
        "(in) num_osc            - number of oscillators in the network."
        "(in) own_weight         - weight of connection from oscillator to itself - own weight."
        "(in) neigh_weight       - weight of connection between oscillators."
        "(in) type_conn          - type of connection between oscillators in the network."
        "(in) conn_represent     - internal representation of connection in the network: matrix or list."
        
        super().__init__(num_osc, type_conn, conn_represent);
        
        self._states = [0] * self._num_osc;
        self._outputs = [-1] * self._num_osc;
        self._outputs_buffer = [-1] * self._num_osc;
        
        self._weight = list();
        for index in range(0, self._num_osc, 1):
            self._weight.append( [neigh_weight] * self._num_osc);
            self._weight[index][index] = own_weight;

    
    def neuron_states(self, inputs, t, argv):
        "Returns new value of the neuron (oscillator)."
        
        "(in) inputs    - list of initial values (current) of the neuron - excitatory."
        "(in) t         - current time of simulation."
        "(in) argv      - extra arguments that are not used for integration - index of the neuron."
        
        "Returns new value of the neuron."
        
        xi = inputs[0];
        index = argv;
        
        # own impact
        impact = self._weight[index][index] * self._outputs[index];
        
        for i in range(0, self._num_osc, 1):
            if (self.has_connection(i, index)):
                impact += self._weight[index][i] * self._outputs[i];

        x = -xi + impact;
                
        if (xi > 1): self._outputs_buffer[index] = 1; 
        if (xi < -1): self._outputs_buffer[index] = -1;
       
        return x;
        
    
    def simulate(self, steps, time, solution = solve_type.RK4, collect_dynamic = True):
        "Performs static simulation of hysteresis oscillatory network."
        
        "(in) steps            - number steps of simulations during simulation."
        "(in) time             - time of simulation."
        "(in) solution         - type of solution (solving)."
        "(in) collect_dynamic  - if True - returns whole dynamic of oscillatory network, otherwise returns only last values of dynamics."
        
        "Returns dynamic of oscillatory network. If argument 'collect_dynamic' = True, than return dynamic for the whole simulation time,"
        "otherwise returns only last values (last step of simulation) of dynamic."  
                
        return self.simulate_static(steps, time, solution, collect_dynamic);
    
    
    def simulate_dynamic(self, order, solution, collect_dynamic, step, int_step, threshold_changes):
        "Performs dynamic simulation, when time simulation is not specified, only stop condition."
        "Not supported because of model specific."
        
        raise NameError("Dynamic simulation is not supported due to lack of stop conditions for the model");
    
    
    def simulate_static(self, steps, time, solution = solve_type.RK4, collect_dynamic = False):
        "Performs static simulation of hysteresis oscillatory network."
        
        "(in) steps            - number steps of simulations during simulation."
        "(in) time             - time of simulation."
        "(in) solution         - type of solution (only RK4 is supported for python implementation)."
        "(in) collect_dynamic  - if True - returns whole dynamic of oscillatory network, otherwise returns only last values of dynamics."
        
        "Returns dynamic of oscillatory network. If argument 'collect_dynamic' = True, than return dynamic for the whole simulation time,"
        "otherwise returns only last values (last step of simulation) of dynamic."  

        # Check solver before simulation
        if (solution == solve_type.FAST):
            raise NameError("Solver FAST is not support due to low accuracy that leads to huge error.");
        elif (solution == solve_type.RKF45):
            raise NameError("Solver RKF45 is not support in python version.");

        dyn_state = None;
        dyn_time = None;
        
        if (collect_dynamic == True):
            dyn_state = [];
            dyn_time = [];
            
            dyn_state.append(self._states);
            dyn_time.append(0);
        
        step = time / steps;
        int_step = step / 10;
        
        for t in numpy.arange(step, time + step, step):
            # update states of oscillators
            self._states = self._calculate_states(solution, t, step, int_step);
            
            # update states of oscillators
            if (collect_dynamic == True):
                dyn_state.append(self._states);
                dyn_time.append(t);
            else:
                dyn_state = self._states;
                dyn_time = t;
        
        return (dyn_time, dyn_state);   
    
        
    def _calculate_states(self, solution, t, step, int_step):
        "Calculates new states for neurons using differential calculus. Returns new states for neurons."
        
        "(in) solution    - type solver of the differential equation."
        "(in) t           - current time of simulation."
        "(in) step        - step of solution at the end of which states of oscillators should be calculated."
        "(in) int_step    - step differentiation that is used for solving differential equation."
        
        "Returns new states for neurons (don't assign)."
        next_states = [0] * self._num_osc;
        
        for index in range (0, self._num_osc, 1):            
            result = odeint(self.neuron_states, self._states[index], numpy.arange(t - step, t, int_step), (index , ));
            next_states[index] = result[len(result) - 1][0];
        
        self._outputs = [val for val in self._outputs_buffer];
        return next_states;
    
    
    def allocate_sync_ensembles(self, tolerance = 0.1):
        "Allocate clusters in line with ensembles of synchronous oscillators where each" 
        "synchronous ensemble corresponds to only one cluster."
        
        "(in) tolerance        - maximum error for allocation of synchronous ensemble oscillators."
        
        "Returns list of grours (lists) of indexes of synchronous oscillators"
        "For example [ [index_osc1, index_osc3], [index_osc2], [index_osc4, index_osc5] ]."
        
        clusters = [ [0] ];
        
        for i in range(1, self._num_osc, 1):
            cluster_allocated = False;
            for cluster in clusters:
                for neuron_index in cluster:
                    if ( (self._states[i] < (self._states[neuron_index] + tolerance)) and (self._states[i] > (self._states[neuron_index] - tolerance)) ):
                        cluster_allocated = True;
                        cluster.append(i);
                        break;
                
                if (cluster_allocated == True):
                    break;
            
            if (cluster_allocated == False):
                clusters.append([i]);
        
        return clusters;