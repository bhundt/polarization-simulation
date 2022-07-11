import streamlit as st
import agentpy as ap
import multiprocessing as mp
import matplotlib.pyplot as plt
import numpy as np

from polarization_model import PolarizationModel


# def main():
#     params = {
#         'agents': 100,
#         'steps': 10000,
#         #'seed': 42,
#         'E': 0.1,       # exposure porbability
#         'T': 0.25,      # tolerance window
#         'R': 0.25,      # movement coefficient
#         'P': -0.99,       # self interest factor
#         'A': -0.99,       # affective polarization
#     }

#     model = PolarizationModel(params)
#     result = model.run()
#     #print(result.variables.PolarizationModel)

#     # plot polarization over time
#     df = result.variables.PolarizationModel
#     plt.plot(df.index, df['Var'], '.')
#     plt.show()
#     plt.close()

#     # plot polarization histogram
#     hist_values, bins = df.iloc[-1]['Hist'], df.iloc[-1]['Bins']
#     width = 0.7 * (bins[1] - bins[0])
#     center = (bins[:-1] + bins[1:]) / 2

#     plt.bar(center, hist_values, align='center', width=width)
#     plt.show()
#     plt.close()

# if __name__ == "__main__":
#     main()

# streamlit application
def run_simulation(agents: int, steps: int, exposure_prob: float, tolerance_window: float, movement_coefficient: float):
    params = {
        'agents': agents,
        'steps': steps,
        #'seed': 42,
        'E': exposure_prob,       # exposure prob
        'T': tolerance_window,      # tolerance window
        'R': movement_coefficient,      # movement coefficient
        'P': -0.99,       # self interest factor
        'A': -0.99,       # affective polarization
    }

    model = PolarizationModel(params)
    result = model.run()

    return result.variables.PolarizationModel

st.title('Societal Polarization Simulation')

st.subheader('Simulation Settings')
agents = st.slider('Number of Simulated Agents', 1, 200, 100)
steps = st.select_slider('Number of Simulation Steps', range(0, 20500, 500), 2000)

exp = st.slider('Exposure Probability', 0.0, 1.0, 0.1)
tol = st.slider('Tolerance Window', 0.0, 1.0, 0.25)
react = st.slider('Reaction Coefficient', 0.0, 1.0, 0.25)

with st.spinner('Simulation running...'):
    df = run_simulation(agents, steps, exp, tol, react)
st.success('Simulation done!')

st.subheader('Polarization over Time')
st.line_chart(df.rename(columns={'Var': 'Total Polarization'})['Total Polarization'])

st.subheader('Polarization Distribution')
st.bar_chart(df.iloc[-1]['Hist'])