import numpy as np
import pandas as pd
import plotly.express as px
import csv

value = []
x = []
y = []
z = []
pn = pd.read_clipboard()
pn.head()

fig = px.scatter_3d(pn, x='dim_0', y='dim_1', z='dim_2',  color='bruh')
fig.show()