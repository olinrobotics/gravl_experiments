#!usr/bin/env python3
"""Calculations to define Kubo Estop circuit relays.

For more information, go to the relevant wiki page within this repository.

"""

import matplotlib.pyplot as plt
import numpy as np

# Measured Values
Rmeasured = 43.5 # Measured resistance of entire Estop circuit
R1 = 92 # Coil resistance of 1st Relay
R2 = 83 # Coil resistance of 2nd Relay
R3 = 20 # Adjustable resistance
IMin = 0.1 # Minimum switching current of relays, Amps
V = np.arange(11.5, 13.1, 0.1) # Predicted Battery Voltages

def get_current(v, r1, r2, r3=0, config='series'):
    """Calculates current in system if relays are in series.

    Args:
        v: battery voltage
        r1: coil resistance of relay 1
        r2: coil resistance of relay 2
        r3: adjustable resistance
        config: configuration of relays (series, parallel)

    Returns:
        list of currents across [r1, r2, total]

    """
    out = [0, 0, 0]
    if config == 'series':
        rtotal = r1 + r2 + r3
        out[0] = out[1] = out[2] = v/rtotal

    elif config == 'parallel':
        rtotal = 1/(1/r1 + 1/r2) + r3
        out[2] = v/rtotal
        vmid = v - out[2] * r3
        out[1] = vmid / r2
        out[0] = vmid / r1
    else:
        raise ValueError

    return out


def plot_current_over_voltage(v, r1, r2, r3, imin, config='series'):
    """Plots current in both relays through a range of voltages.

    Args:
        v: numpy array of battery voltages
        r1: coil resistance of relay 1
        r2: coil resistance of relay 2
        r3: adjustable resistance
        imin: minimum current for relay to activate
        config: configuration of relays (series, parallel)
    """
    i = np.array([get_current(vv, r1, r2, r3, config) for vv in v])
    plt.plot(v, i[:,0], 'g')
    plt.plot(v, [imin] * len(v), 'k', dashes=[6, 2])
    plt.plot(v, i[:,1], 'r')
    plt.plot(v, i[:,2], 'b')
    if config == 'series':
        plt.title(f"Relays in Series (R1 = {r1}, R2 = {r2}, R3 = {r3})")
    elif config == 'parallel':
        plt.title(f"Relays in Parallel (R1 = {r1}, R2 = {r2}, R3 = {r3})")

    plt.xlabel('Battery Voltage (V)')
    plt.ylabel('Current (Amps)')
    plt.legend([
        'Relay 1 Current', 'Mimimum Switching Current',
        'Relay 2 Current', 'Total Current'])
    plt.show()


def get_r3_given_current(v, i_min, r1, r2=None, config='parallel'):
    """Chooses an r3 for a given min current.

    Given a minimum current for both relays, chooses an r3 such that
    the highest resistance relay has at least imin current at the lowest v.
    if in series mode, populate r1 and not r2.

    """
    # pdb.set_trace()
    if config == 'parallel':
        i_relay = min(get_current(v[0], r1, r2, config=config))
        if i_relay < i_min:
            raise ValueError(
                "Relay parallel resistance brings current lower than i_min!")
        else:
            v1 = i_min * max(r1, r2)
            i_min2 = v1 / min(r1, r2)
            i_total = i_min + i_min2
            rout = (v[0] - v1)/i_total

    elif config == 'series':
        i_relay = v[0]/r1
        if i_relay < i_min:
            raise ValueError(
                "Relay series resistance brings current lower than i_min!")
        else:
            v1 = i_min * r1
            rout = (v[0] - v1)/i_relay

    return rout


if __name__ == "__main__":
    # plot_current_over_voltage(V, R1, R2, R3, IMin, 'series')
    r3 = get_r3_given_current(V, IMin, R1, R2, 'parallel')
    print(f"Optimal 3rd resistance (calculated): {r3}")
    r3 = get_r3_given_current(V, IMin, Rmeasured, config='series')
    print(f"Optimal 3rd resistance (measured): {r3}")
    # plot_current_over_voltage(V, Rmeasured, r3, IMin, 'series')
    plot_current_over_voltage(V, R1, R2, 10, IMin, 'parallel')
