"""
All the simulations needed to genherate the figures are performed by this script.
In particular, it simulates 10000 random requests in the following topologies:
* 10 node ring
* 101 node ring
* 100 node line
* 100 node star
* 100 node square grid
* 13x13 triangular grid
* OSM street network of Harz
* OSM street network of Göttingen
* OSM street network of Berlin
* OSM street network of Berlin with three levels of coarse graining.

The OSM networks are generated by notebooks/gen_streetnetworks_for_simulations.ipynb

The simulation data can then be used by the notebooks/Fig.*.ipynb to generate
the figures in the manuscript.
"""
import numpy as np
import networkx as nx
from collections import defaultdict
import random
import pickle

import os

from toysimulations import ZeroDetourBus, Stop, Request, Network

def req_generator_uniform(graph, num_reqs, req_rate):
    """
    Generates requests with rate=req_rate whose origin and
    destination are drawn uniformly randomly. The requests
    are generated in time as a Poisson process.
    """
    t = 0
    req_idx = 0

    while req_idx < num_reqs:
        orig, dest = random.sample(graph.nodes(), k=2)
        delta_t = np.random.exponential(1/req_rate)

        t += delta_t
        req_idx += 1
        yield Request(req_idx, t, orig, dest)

def simulate_different_request_rates(G, pickle_path, network_type='novolcomp'):
    """
    Simulates different request rates between 0 and 40 on supplied
    graph G. Saves the simulation output as a pickle to pickle_path.

    The `network_type` argument is used to compute route volumes
    during the simulations. If it is set to 'novolcomp', no route
    volume calculation is done. See toysimulations/simulator.py::Network
    for details.

    100 request rates (x), spaced equally between 0.1 and 40 are simulated.
    The request rates are normalized by 2 * average shortest path length, as
    described in the manuscript. 10000 requests are simulated in each case.
    """
    if os.path.exists(pickle_path):
        print("pickle exists, doing nothing")
        return None

    nG = Network(G, network_type=network_type)
    l_avg = nx.average_shortest_path_length(G)

    x_range = list(np.linspace(0.1, 40, 100))

    result = defaultdict(lambda :dict())

    for x in x_range:
        req_data, ins_data = simulate_simgle_request_rate(G, nG, x,network_type, l_avg)

        result[x]['req_data'] = req_data
        result[x]['insertion_data'] = ins_data

        picklable_res = {key: dict(val) for key, val in result.items()}
        with open(pickle_path, 'wb') as f:
            pickle.dump(picklable_res, f)

def simulate_single_request_rate(G, nG, x,network_type, l_avg):
    """
    Simulates only as ingle request rate x. See the docstring of
    `simulate_different_request_rates` for details on the arguments.
    """
    num_reqs = 10000
    req_rate = x/2/l_avg

    sim = ZeroDetourBus(nG,
                        req_generator_uniform(G, num_reqs, req_rate),
                        network_type,
                        random.sample(G.nodes(), k=1)[0]
                       )
    print(f"simulating x={x}")
    sim.simulate_all_requests()
    return sim.req_data, sim.insertion_data

if __name__ == '__main__':
    # Generate data for 10 node ring
    print("doing ring10")
    G = nx.cycle_graph(10)
    pickle_path = '../data/ring_10.pkl'

    simulate_different_request_rates(G, pickle_path, network_type='ring')
    print("done ring10")

    # Generate data for 100 node ring
    print("doing ring100")
    G = nx.cycle_graph(101)
    pickle_path = '../data/ring_100.pkl'
    simulate_different_request_rates(G, pickle_path, network_type='ring')
    print("done ring100")

    # Generate data for 100 node line
    print("doing line100")
    G = nx.grid_graph((100,))
    pickle_path = '../data/line_100.pkl'
    simulate_different_request_rates(G, pickle_path, network_type='line')
    print("done line100")

    # Generate data for 100 node star
    print("doing star100")
    G = nx.star_graph(n=100)
    pickle_path = '../data/star_100.pkl'
    simulate_different_request_rates(G, pickle_path, network_type='star')
    print("done star100")

    # Generate data for 100 node grid
    print("doing grid100")
    G = nx.grid_2d_graph(10, 10)
    pickle_path = '../data/grid_10.pkl'
    simulate_different_request_rates(G, pickle_path, network_type='grid')
    print("done grid100")

    # generate data for 13x13 trigrid
    print("doing trigrid13")
    G = nx.lattice.triangular_lattice_graph(13, 13)
    pickle_path = '../data/trigrid_13.pkl'
    simulate_different_request_rates(G, pickle_path, network_type='trigrid')
    print("done trigrid13")

    # generate data for streetnetworks

    # Göttingen
    print("doing Gö")
    graph_path = '../data/homogenized_networks/goe/'
    G = nx.read_gpickle(f"{graph_path}/G_homog.gpkl")

    pickle_path = '../data/street_goe_homogenized.pkl'
    simulate_different_request_rates(G, pickle_path, network_type='novolcomp')
    print("done Gö")

    # Harz
    print("doing Harz")
    graph_path = '../data/homogenized_networks/harz/'
    G = nx.read_gpickle(f"{graph_path}/G_homog.gpkl")

    pickle_path = '../data/street_harz_homogenized.pkl'
    simulate_different_request_rates(G, pickle_path, network_type='novolcomp')
    print("done Harz")

    # Berlin
    print("doing Berlin")
    graph_path = '../data/homogenized_networks/berlin/'
    G = nx.read_gpickle(f"{graph_path}/G_homog.gpkl")

    pickle_path = '../data/street_berlin_homogenized.pkl'
    simulate_different_request_rates(G, pickle_path, network_type='novolcomp')

    print("done Berlin")
    # Many berlins
    graph_path = '../data/homogenized_networks/berlin/'

    with open(f"{graph_path}/diff_coarse_graining/all_berlin.pkl", 'rb') as f:
        all_Gs = pickle.load(f)

    for coarse_graining_meters, target_edge_length in [
                                                       (200, 400),
                                                       (200, 600),
                                                       (200, 800)
                                                      ]:
        print(f"Doing Berlin {coarse_graining_meters} {target_edge_length }")
        # read the graph
        _,G = all_Gs[coarse_graining_meters][target_edge_length]
        pickle_path = f'../data/street_berlin_homogenized_coarse_graining_meters_{coarse_graining_meters}_target_edge_length_{target_edge_length}.pkl'
        simulate_different_request_rates(G, pickle_path, network_type='novolcomp')
