import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# Create a simple line chart
x = np.linspace(0, 10, 100)
y = np.sin(x)

# Use Streamlit to display the chart
st.title('Streamlit Line Chart Example')
st.line_chart(plt.plot(x, y))
