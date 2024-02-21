import streamlit as st
import pandas as pd

from polarization_model import PolarizationModel


def run_simulation(
    agents: int, steps: int, exposure_prob: float, tolerance_window: float, movement_coefficient: float
) -> PolarizationModel:
    """
    Run a simulation of the polarization model.

    Parameters:
    agents (int): The number of agents in the simulation.
    steps (int): The number of steps to run the simulation for, can be interpreted as time.
    exposure_prob (float): The probability of agents being exposed to opposing opinions.
    tolerance_window (float): The tolerance window within which agents accept opposing opinions.
    movement_coefficient (float): The movement coefficient that determines the extent of agent movement.

    Returns:
    result.variables.PolarizationModel: The result of the simulation, including the polarization model variables.
    """

    params = {
        "agents": agents,
        "steps": steps,
        "seed": 42,
        "E": exposure_prob,  # exposure prob
        "T": tolerance_window,  # tolerance window
        "R": movement_coefficient,  # movement coefficient
    }

    model = PolarizationModel(params)
    result = model.run()

    return result.variables.PolarizationModel


st.title("Societal Polarization Simulation")
st.markdown(
    'This app simulates the evolution of societal polarization over time as discussed in \nthe paper ["Preventing extreme polarization of political attitudes"](https://www.pnas.org/content/118/50/e2102139118) by Axelrod et. al. You can find the code on [my github](https://github.com/bhundt/polarization-simulation) and see [my blog](https://bhundt.de/2024/02/21/polarizaton-simulation.html) for more information.'
)

st.subheader("Simulation Settings")
agents = st.slider("Number of Agents (number of simulated people)", 1, 100, 30)
steps = st.select_slider(
    "Number of Simulation Steps (essentially the time the simulation runs)", range(0, 20500, 500), 5000
)

exp = st.slider("Exposure Probability (how likely is an encounter with another opinion)", 0.0, 1.0, 0.1)
tol = st.slider("Tolerance Window (tolerance to other opinions)", 0.0, 1.0, 0.25)
react = st.slider("Reaction Coefficient (strength of reaction to other opinions)", 0.0, 1.0, 0.25)

with st.spinner("Simulation running..."):
    df = run_simulation(agents, steps, exp, tol, react)
st.success("Simulation done!")

st.subheader("Polarization vs. Time")
st.markdown(
    "The plot below shows the total polarization of the society over time. It is calculated using the variance of the polarization of all agents. Maximum polarization is therefore 0.25."
)
st.line_chart(df.rename(columns={"Var": "Total Polarization"})["Total Polarization"])

st.subheader("Polarization Distribution")
st.markdown(
    "The plot below shows the distribution of polarization of the society. Polarization is mesured on a scale of 0 to 1 where 0 means complete alignment on one side of the issue while 1 means the complete alignment on the other side of the issues. More people on the edges means stronger overall disagreement."
)
aux_df = pd.DataFrame(
    {
        "Count": df.iloc[-1]["Hist"],
        "Pol-Range": [
            "0 - 0.1",
            "0.1 - 0.2",
            "0.2 - 0.3",
            "0.3 - 0.4",
            "0.4 - 0.5",
            "0.5 - 0.6",
            "0.6 - 0.7",
            "0.7 - 0.8",
            "0.8 - 0.9",
            "0.9 - 1.0",
        ],
    }
)
st.bar_chart(data=aux_df, x="Pol-Range", y="Count")
