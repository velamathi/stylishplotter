import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import os
import datetime
import random
import plotly.graph_objs as go
from plotly.subplots import make_subplots

app = dash.Dash(__name__)

def update_fig_margin(fig):
    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        # template='plotly_dark'
    )
    return fig


# Define function to read symlinked file
def read_file():
    linked_path = "/home/slay3r/Downloads/current_date"
    linked_file = os.readlink(linked_path)
    text = linked_file.split(".")[0]
    # with open(os.readlink(), 'r') as f:
    #     text = f.read()
    return text
# CSS style for centering the text
style_center = {
    'text-align': 'left'
}

# Define layout of dashboard
app.layout = html.Div([
    html.H1("Dashboard", style=style_center),
    html.Div(id="file-update", style=style_center),
    html.Div(id="text-update", style=style_center),
    html.Div(id="time-update", style=style_center),
    dcc.Graph(id="graph"),
    dcc.Graph(id="graph1"),
    dcc.Interval(
        id='interval-component',
        interval=1000*15, # Update every 5 seconds
        n_intervals=0
    )
])

# Define callback to update file name
@app.callback(Output("file-update", "children"),
              [Input("interval-component", "n_intervals")])
def update_file(n):
    file_path = os.readlink("/home/slay3r/Downloads/current_date")
    file_name = os.path.basename(file_path)
    file_name = file_name.split(".")[0]
    return f"Current Timestamp: {file_name}"

# Define callback to update text
@app.callback(Output("text-update", "children"),
              [Input("interval-component", "n_intervals")])
def update_text(n):
    text = read_file()
    return text

# Define callback to update time
@app.callback(Output("time-update", "children"),
              [Input("interval-component", "n_intervals")])
def update_time(n):
    now = datetime.datetime.now()
    current_time = now.strftime("%Y-%m-%d %H:%M:%S")
    return f"Current Time: {current_time}"

# Define callback to update graph
@app.callback([Output("graph", "figure"),
              Output('graph1', 'figure')],
              [Input("interval-component", "n_intervals")])
def update_graph(n):
    fig = make_subplots(rows=1, cols=2, column_width=[0.5, 0.5],
                        specs=[[{"type": "scatter"},{"type": "scatter"}]])


    # Generate random data for the four traces
    x_data = list(range(1, 10))
    y_data_1 = [random.randint(1, 10) for i in range(10)]
    y_data_2 = [random.randint(1, 10) for i in range(10)]
    y_data_3 = [random.randint(1, 10) for i in range(10)]
    y_data_4 = [random.randint(1, 10) for i in range(10)]
    y_data_5 = [random.randint(1, 10) for i in range(10)]
    y_data_6 = [random.randint(1, 10) for i in range(10)]

    # Append the traces to the subplot grid
    fig.add_trace(go.Scatter(x=x_data, y=y_data_1, mode='lines', name='Random Numbers 1'), row=1, col=1)
    fig.add_trace(go.Scatter(x=x_data, y=y_data_2, mode='lines', name='Random Numbers 2'), row=1, col=2)

    fig1 = make_subplots(rows=1, cols=4, column_width=[0.25, 0.25, 0.25, 0.25],
                         specs=[[{"type": "scatter"}, {"type": "scatter"},{"type": "scatter"},{"type": "scatter"}]])

    fig1.add_trace(go.Scatter(x=x_data, y=y_data_3, mode='lines', name='Random Numbers 3'), row=1, col=1)
    fig1.add_trace(go.Scatter(x=x_data, y=y_data_4, mode='lines', name='Rambo'), row=1, col=2)
    fig1.add_trace(go.Scatter(x=x_data, y=y_data_5, mode='lines', name='ashwin'), row=1, col=3)
    fig1.add_trace(go.Scatter(x=x_data, y=y_data_6, mode='lines', name='jaspal'), row=1, col=4)

    # Update subplot layout
    fig.update_layout(height=600, showlegend=False)
    fig1.update_layout(height=600, showlegend=False)
    fig = update_fig_margin(fig)
    fig1 = update_fig_margin(fig1)

    return fig, fig1


if __name__ == '__main__':
    app.run_server(port=8053, debug=True)