from scipy.integrate import solve_ivp
import numpy as np

# ── SVEIR parameters (imported by simulation.py) ─────────────────────────────
BETA    = 0.3    # transmission rate (contacts × prob of infection, per day)
NU      = 0.01   # daily rate at which susceptible people get vaccinated
EPSILON = 0.2    # vaccine leakiness: 0 = perfect protection, 1 = no protection
SIGMA   = 1/5    # rate E → I  (1/SIGMA = 5-day incubation period)
GAMMA   = 1/10   # rate I → R  (1/GAMMA = 10-day infectious period)

# ── Spatial calibration ───────────────────────────────────────────────────────
# The ODE assumes everyone mixes perfectly (well-mixed). The agent sim is
# spatial: agents cluster in corridors and at the food court, so their actual
# contact rate is higher than the uniform average.
#
# SPATIAL_FACTOR scales BETA up in the ODE so its prediction matches the
# faster spread the spatial simulation naturally produces.
#
# E_SEED pre-populates a few Exposed people in the ODE, representing the
# immediate cluster of contacts patient zero makes at the food court on day 0
# — something the ODE can't express with a single I=1, E=0 start.
SPATIAL_FACTOR = 1.5   # empirically calibrated: raises effective R0 from 3 → 4.5
E_SEED         = 5     # initial exposed from the food-court cluster


def sveir_model(t, y, beta, nu, epsilon, sigma, gamma):
    S, V, E, I, R = y
    N = S + V + E + I + R
    dS = -beta*S*I/N  - nu*S
    dV =  nu*S        - epsilon*beta*V*I/N
    dE =  beta*S*I/N  + epsilon*beta*V*I/N - sigma*E
    dI =  sigma*E     - gamma*I
    dR =  gamma*I
    return [dS, dV, dE, dI, dR]


def solve_ode(N_pop, vax_fraction, n_infected, days, e_seed=0):
    """
    Run the SVEIR ODE and return smooth curves scaled to N_pop.

    Parameters
    ----------
    N_pop        : total population size
    vax_fraction : fraction of population that starts vaccinated
    n_infected   : number of initially infected individuals
    days         : how many days to simulate
    e_seed       : extra initially-exposed individuals (food-court cluster)

    Returns
    -------
    t, S, V, E, I, R  — all as numpy arrays of the same length
    """
    n_vax = int(vax_fraction * N_pop)
    n_sus = N_pop - n_vax - n_infected - e_seed
    y0 = [n_sus, n_vax, e_seed, n_infected, 0]

    effective_beta = BETA * SPATIAL_FACTOR

    sol = solve_ivp(
        sveir_model, (0, days), y0,
        args=(effective_beta, NU, EPSILON, SIGMA, GAMMA),
        dense_output=True, max_step=0.2
    )
    t_eval = np.linspace(0, days, days * 20)
    y = sol.sol(t_eval)
    return t_eval, y[0], y[1], y[2], y[3], y[4]


# ── Standalone: run and plot the ODE by itself ────────────────────────────────
if __name__ == '__main__':
    import matplotlib.pyplot as plt

    N = 10000
    t, S, V, E, I, R = solve_ode(N_pop=N, vax_fraction=0.0,
                                  n_infected=1, days=200)
    colors = ['#4A90D9', '#9B59B6', '#F5A623', '#E74C3C', '#2ECC71']
    labels = ['Susceptible', 'Vaccinated', 'Exposed', 'Infected', 'Recovered']

    plt.figure(figsize=(10, 5))
    plt.gca().set_facecolor('#0d0d1a')
    plt.gcf().set_facecolor('#0d0d1a')
    for arr, lbl, col in zip([S, V, E, I, R], labels, colors):
        plt.plot(t, arr, label=lbl, color=col, lw=2)
    plt.xlabel('Days', color='white')
    plt.ylabel('Count', color='white')
    plt.title('SVEIR ODE Model  (spatially calibrated)', color='white')
    plt.tick_params(colors='white')
    plt.legend(facecolor='#1b1b2f', labelcolor='white')
    plt.tight_layout()
    plt.show()
