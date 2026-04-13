"""
╔══════════════════════════════════════════════════════════════════════════════╗
║              SVEIR MALL SIMULATION  —  WORKSHOP SCRIPT                      ║
║                                                                              ║
║  Fill in the four functions below to model your own interventions.           ║
║  Run simulation.py when you're ready — it will import your work and          ║
║  show the effects live in the visualization.                                 ║
║                                                                              ║
║  You can also change disease parameters in model.py.                         ║
╚══════════════════════════════════════════════════════════════════════════════╝

QUICK REFERENCE
───────────────
Mall layout   : 120 units wide × 80 units tall
Food court    : centre (60, 40), radius 9
Agent states  : 0 = Susceptible   1 = Vaccinated   2 = Exposed
                3 = Infected      4 = Recovered

(store x, store y, store width, store height, name) - bottom-left anchored
STORES = [
    (2,   4,  16, 14, "ZARA"),   (21,  4, 16, 14, "H&M"),
    (40,  4,  16, 14, "NIKE"),   (59,  4, 16, 14, "APPLE"),
    (78,  4,  16, 14, "GUCCI"),  (98,  4, 16, 14, "BOOKS"),
    (2,  62,  16, 14, "CINEMA"), (21, 62, 16, 14, "GYM"),
    (40, 62,  16, 14, "GAMES"),  (59, 62, 16, 14, "SPORT"),
    (78, 62,  16, 14, "TOYS"),   (98, 62, 16, 14, "TECH"),
    (2,  30,  12, 20, "CAFE"),   (106, 30, 12, 20, "SPA"),
]
"""

import numpy as np


def zone_risk(x, y):
    """
    Return a transmission-rate multiplier for position (x, y).

        1.0   →  normal risk
        > 1.0 →  higher risk  (crowded / poorly ventilated area)
        < 1.0 →  lower risk   (open space / distancing enforced)

    The simulation draws this as a colour heatmap on the mall floor:
    red = high risk, blue = low risk.
    """
    return 1.0


def movement_policy(state, x, y, day, counts, N):
    """
    Called every frame for every agent.
    Return a new (dest_x, dest_y) to redirect the agent,
    or None to let them move freely.

    Parameters
    ----------
    state   int     agent's health state (0–4, see QUICK REFERENCE)
    x, y    float   agent's current position
    day     float   current simulation day
    counts  dict    {0: n_susceptible, 1: n_vaccinated, 2: n_exposed,
                     3: n_infected,    4: n_recovered}
    N       int     total population
    """
    return None


def transmission_modifier(susceptible_state, sx, sy, ix, iy,
                           base_prob, day, counts, N):
    """
    Called when a susceptible/vaccinated agent is within contact range
    of an infected agent.
    Return the actual probability of infection this frame.

    Parameters
    ----------
    susceptible_state  int     state of the at-risk agent (0=S or 1=V)
    sx, sy             float   at-risk agent's position
    ix, iy             float   infected agent's position
    base_prob          float   default probability (already includes zone_risk)
    day                float   current simulation day
    counts             dict    current population counts
    N                  int     total population
    """
    return base_prob


def policy_label(day, counts, N):
    """
    Return a short string to display as a banner on the mall when an
    intervention is active, or '' for no banner.

    Parameters
    ----------
    day     float   current simulation day
    counts  dict    current population counts
    N       int     total population
    """
    return ''
