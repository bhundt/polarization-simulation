import streamlit as st

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
    'This app simulates the evolution of societal polarization over time as discussed in \nthe paper ["Preventing extreme polarization of political attitudes"](https://www.pnas.org/content/118/50/e2102139118) by Axelrod et. al.'
)

st.subheader("Simulation Settings")
agents = st.slider("Number of Simulated Agents", 1, 100, 30)
steps = st.select_slider("Number of Simulation Steps", range(0, 20500, 500), 5000)

exp = st.slider("Exposure Probability (how likely is an encounter with a differnt opinion)", 0.0, 1.0, 0.1)
tol = st.slider("Tolerance Window (tolerance to other opinios)", 0.0, 1.0, 0.25)
react = st.slider("Reaction Coefficient (strength of reaction to diverging opinions)", 0.0, 1.0, 0.25)

with st.spinner("Simulation running..."):
    df = run_simulation(agents, steps, exp, tol, react)
st.success("Simulation done!")

st.subheader("Polarization vs. Time")
st.line_chart(df.rename(columns={"Var": "Total Polarization"})["Total Polarization"])

st.subheader("Polarization Distribution")
st.bar_chart(df.iloc[-1]["Hist"])
