import plotly.express as px
import dash_html_components as html
import dash_core_components as dcc
import dash
import pandas as pd
from dash import Dash, html, dcc, Input, Output
import altair as alt

df = pd.read_csv('./data//world-data-gapminder_raw.csv')

# Setup app and layout/frontend
app = Dash(__name__,  external_stylesheets=[
           'https://codepen.io/chriddyp/pen/bWLwgP.css'])
app.layout = html.Div([
    html.Iframe(
        id='scatter',
        style={'border-width': '0', 'width': '100%', 'height': '400px'}),
    dcc.Dropdown(
        id='xcol-widget',
        value='Horsepower',  # REQUIRED to show the plot on the first page load
        options=[{'label': col, 'value': col} for col in df.columns])
        ])

# Set up callbacks/backend


@app.callback(
    Output('scatter', 'srcDoc'),
    Input('xcol-widget', 'value'))
def plot_altair(xcol):
    chart = alt.Chart(df.query("year==2007")).mark_point(
        filled=True, opacity=0.5).encode(
        alt.X('life_expectancy', scale=alt.Scale(domain=(50, 85))),
        alt.Y('income', scale=alt.Scale(
            type='log', base=10, domain=(1000, 80000))),
        size=alt.Size('population', legend=None),
        tooltip=['country', 'year', 'life_expectancy', 'income', 'population'],
        color='region').interactive()
    return chart.to_html()



if __name__ == '__main__':
    app.run_server(debug=True)

# fig = px.scatter(df.query("year==2007"), x="income", y="life_expectancy",
#                  size="population", color="region",
#                  hover_name="country", log_x=True, size_max=60)



# app = dash.Dash()
# app.layout = html.Div([
#     dcc.Graph(figure=fig)
# ])

# # Turn off reloader if inside Jupyter
# app.run_server(debug=True, use_reloader=False)
