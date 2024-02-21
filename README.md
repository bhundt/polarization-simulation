# Political Polarization Simulation using Streamlit
In the paper ["Preventing extreme polarization of political attitudes"](https://www.pnas.org/content/118/50/e2102139118) by Axelrod et. al. the authors present a model of political polarization in which individuals are influenced by the opinions of others.

This repository contains a Streamlit app that simulates the model presented in the paper. The app allows you to change the parameters of the model and see how the political polarization evolves over time. 

[You can try the model on Streamlit](https://bhundt-polarization-simulation.streamlit.app).

See this blogpost for more details: [Political Polarization Simulation using Streamlit](https://bhundt.de/2024/02/21/polarizaton-simulation.html). 

## Local setup & run
The code was tested with Python 3.9.5 and 3.11.7. 

Create a virtual environment and install the required packages:
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Start simulation app with Streamlit:
```bash
streamlit run streamlit_app.py
```