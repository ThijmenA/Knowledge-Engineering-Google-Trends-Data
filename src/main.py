import dash
import plotly.express as px
from dash import Input, Output, dcc, html

from .database import driver
from .queries import get_sales_weather_data, get_sales_weather_data_by_date, get_sales_weather_data_by_date_range

app = dash.Dash(__name__)

app.layout = html.Div(
    [
        dcc.Graph(
            id="line-graph",
            figure=px.line(
                get_sales_weather_data(driver),
                x="date",
                y="retail_sale_of_clothes_and_fashion_items",
                markers=True,
            ),
        ),
        dcc.Graph(id="heatmap"),
    ]
)


@app.callback(Output("heatmap", "figure"), Input("line-graph", "relayoutData"))
def update_heatmap(relayoutData):
    columns = [
        "rain",
        "wind_speed",
        "temp",
        "retail_trade",
        "retail_sale_via_internet",
        "multi_channel",
    ]
    title = "Heatmap for all dates"
    if (
        relayoutData
        and "xaxis.range[0]" in relayoutData
        and "xaxis.range[1]" in relayoutData
    ):
        start_date = relayoutData["xaxis.range[0]"].split(" ")[0]
        end_date = relayoutData["xaxis.range[1]"].split(" ")[0]
        df = get_sales_weather_data_by_date_range(driver, start_date, end_date)
        title = f"Heatmap for {start_date[:10]} to {end_date[:10]}"
    else:
        df = get_sales_weather_data(driver)
        title = "Heatmap for all dates"

    corr = df[columns].corr()
    fig = px.imshow(corr, text_auto=True, color_continuous_scale="RdBu", title=title)
    return fig


if __name__ == "__main__":
    app.run(debug=True)
