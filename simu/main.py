import simpy
import random

import parameters
import stats

def collect_data(simulations, num_nodes_range):
    data = {sim_name: [] for sim_name in simulations.keys()}
    for num_nodes in num_nodes_range:
        for sim_name, sim_class in simulations.items():
            sim = sim_class(num_nodes)
            sim.run_simulation()
            forwarding_nodes = sim.get_forwarding_nodes_count()  # 假设每个仿真类都有这个方法
            data[sim_name].append(forwarding_nodes)
    return data

def main():
    simulations = {
        'flood': floodSimulation,
        'pflood': pfloodSimulation,
        'prim': primSimulation,
        'pprim': pprimSimulation,
        'mda': mdaSimulation
    }
    num_nodes_range = parameters.NUMBER_OF_NODES
    data = collect_data(simulations, num_nodes_range)

    plot_data(data, num_nodes_range)
