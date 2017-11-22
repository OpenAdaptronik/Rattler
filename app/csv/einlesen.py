from plotly import __version__
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot

print(__version__) # requires version >= 1.9.0

import plotly
from plotly.graph_objs import Scatter, Layout
import pandas as pd
import plotly.figure_factory  as FF
import plotly.graph_objs as go
data = pd.read_csv('single_time+multidata_equal_Frequency_data.csv')
df = data[['Frequency','Force']]

table = FF.create_table(df)


trace1 = go.Scatter(
    x=list(df['Frequency']),
    y=list(df['Force']),
    mode='lines',
    name='Frequency'
)

layout = go.Layout(
    showlegend=True
)

trace_data = [trace1]
fig = go.Figure(data=trace_data, layout=layout)

plotly.offline.plot(fig)




