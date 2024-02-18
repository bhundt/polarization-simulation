import streamlit as st
import agentpy as ap
import multiprocessing as mp
import matplotlib.pyplot as plt
import numpy as np

from polarization_model import PolarizationModel


# streamlit application
def run_simulation(
    agents: int, steps: int, exposure_prob: float, tolerance_window: float, movement_coefficient: float
):
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
agents = st.slider("Number of Simulated Agents", 1, 200, 50)
steps = st.select_slider("Number of Simulation Steps", range(0, 20500, 500), 5000)

exp = st.slider("Exposure Probability", 0.0, 1.0, 0.1)
tol = st.slider("Tolerance Window", 0.0, 1.0, 0.25)
react = st.slider("Reaction Coefficient", 0.0, 1.0, 0.25)

with st.spinner("Simulation running..."):
    df = run_simulation(agents, steps, exp, tol, react)
st.success("Simulation done!")

st.subheader("Polarization over Time")
st.line_chart(df.rename(columns={"Var": "Total Polarization"})["Total Polarization"])

st.subheader("Polarization Distribution")
st.bar_chart(df.iloc[-1]["Hist"])
