from datetime import datetime

import dash
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from dash import Input, Output, dcc, html
from plotly.subplots import make_subplots

from .database import driver
from .queries import (
    get_sales_google_trends_data,
    get_sales_google_trends_data_by_date_range,
    get_sales_weather_data,
    get_sales_weather_data_by_date_range,
)

app = dash.Dash(__name__)


def create_monthly_sales_boxplots():
    cols = [
        "retail_sale_via_internet",
        "retail_sale_of_consumer_electronics",
        "retail_sale_of_food_and_drugstore_items",
    ]
    df = get_sales_weather_data(driver)
    from plotly.subplots import make_subplots

    fig = make_subplots(
        rows=1,
        cols=len(cols),
        subplot_titles=[
            "Online Sales",
            "Consumer Electronics",
            "Food & Drugstore Items",
        ],
        shared_yaxes=False,
    )

    for i, col in enumerate(cols):
        fig.add_trace(
            go.Box(
                x=df["month"],
                y=df[col],
                name=col.replace("_", " ").title(),
                boxmean=True,
            ),
            row=1,
            col=i + 1,
        )

    fig.update_layout(
        title="Monthly Sales Distribution",
        height=400,
        showlegend=False,
        margin=dict(l=40, r=40, t=60, b=40),
    )
    for i in range(len(cols)):
        fig.update_xaxes(title_text="Month", row=1, col=i + 1)
        fig.update_yaxes(title_text="Sales", row=1, col=i + 1)
    return fig


def create_weather_monthly_avg_variation_plot2():
    weather_cols = ["temp", "rain", "wind_speed"]
    display_names = {
        "temp": "Temperature",
        "rain": "Precipitation",
        "wind_speed": "Wind Speed",
    }
    df = get_sales_weather_data(driver)
    if "month" not in df.columns:
        df["month"] = pd.to_datetime(df["date"]).dt.month

    monthly_weather_avg = df.groupby("month")[weather_cols].transform("mean")
    weather_variation = df[weather_cols] - monthly_weather_avg

    # Enable secondary y-axis for each row
    fig = make_subplots(
        rows=len(weather_cols),
        cols=1,
        shared_xaxes=True,
        subplot_titles=[
            f"{display_names[col]} with Monthly Avg and Variation"
            for col in weather_cols
        ],
        vertical_spacing=0.05,
        specs=[[{"secondary_y": True}] for _ in weather_cols],
    )

    for i, col in enumerate(weather_cols):
        # Actual values (primary y-axis)
        fig.add_trace(
            go.Scatter(
                x=df["date"],
                y=df[col],
                mode="lines+markers",
                name=f"{display_names[col]} (actual)",
                line=dict(color="blue"),
            ),
            row=i + 1,
            col=1,
            secondary_y=False,
        )
        # Monthly average (primary y-axis)
        fig.add_trace(
            go.Scatter(
                x=df["date"],
                y=monthly_weather_avg[col],
                mode="lines",
                name="Monthly Avg",
                line=dict(dash="dash", color="orange"),
            ),
            row=i + 1,
            col=1,
            secondary_y=False,
        )
        # Variation (secondary y-axis)
        fig.add_trace(
            go.Scatter(
                x=df["date"],
                y=weather_variation[col],
                mode="lines",
                name="Variation",
                line=dict(dash="dot", color="green"),
            ),
            row=i + 1,
            col=1,
            secondary_y=True,
        )
        fig.update_yaxes(
            title_text=display_names[col], row=i + 1, col=1, secondary_y=False
        )
        fig.update_yaxes(title_text="Variation", row=i + 1, col=1, secondary_y=True)

    fig.update_xaxes(title_text="Date", row=len(weather_cols), col=1, tickangle=45)
    fig.update_layout(
        height=350 * len(weather_cols),
        showlegend=True,
        margin=dict(l=40, r=40, t=60, b=40),
    )
    return fig


app.layout = html.Div(
    children=[
        html.Div(
            # make the div split in two columns
            children=[
                html.Div(
                    children=[
                        html.H1(
                            "E-commerce and Weather Analysis",
                            style={
                                "textAlign": "left",
                                "margin-left": "1.5cm",
                                "font-family": "Arial",
                                "color": "#003366",
                                "font-size": "40px",
                            },
                        ),
                        # dcc.Graph(
                        #    id="weather-monthly-avg-variation",
                        #    figure=create_weather_monthly_avg_variation_plot(),
                        #    style={"width": "100%"},
                        # ),
                        html.H1(
                            "Research Question 1: ",
                            style={"margin-left": "1.5cm", "font-family": "Arial"},
                        ),
                        html.H2(
                            "Sales and Weather Data Analysis",
                            style={"margin-left": "1.5cm", "font-family": "Arial"},
                        ),
                        html.H3(
                            "How do weather conditions (temperature, precipitation, wind) affect purchasing behaviour in the Netherlands?",
                            style={
                                "margin-left": "1.5cm",
                                "font-family": "Arial",
                                "color": "gray",
                            },
                        ),
                        html.Div(
                            style={
                                "display": "flex",
                                "flexDirection": "row",
                                "justifyContent": "space-between",
                                "width": "100%",
                            },
                            children=[
                                dcc.Graph(
                                    id="line-graph",
                                    style={"width": "69%"},
                                ),
                                html.Div(
                                    style={
                                        "display": "flex",
                                        "flexDirection": "column",
                                        "width": "30%",
                                    },
                                    children=[
                                        html.Div(
                                            dcc.Graph(
                                                id="heatmap",
                                                style={"width": "100%"},
                                            )
                                        ),
                                        html.Div(
                                            dcc.Graph(
                                                id="heatmap-seasonality-removed",
                                                style={"width": "100%"},
                                            )
                                        ),
                                    ],
                                ),
                            ],
                        ),
                        dcc.Graph(id="online-sales-variation", style={"width": "100%"}),
                        html.H3(
                            "Answer:",
                            style={"margin-left": "1.5cm", "font-family": "Arial"},
                        ),
                        html.Div(
                            children=[
                                html.P(
                                    "The analysis shows that weather conditions such as temperature, precipitation, and wind speed have a significant impact on purchasing behavior in the Netherlands."
                                ),
                                html.P(
                                    "For instance, higher rain level tend to increase online sales. And higher temperatures generally leads to lower sales overall."
                                ),
                            ],
                            style={
                                "margin-left": "1.5cm",
                                "margin-right": "1.5cm",
                                "font-family": "Arial",
                            },
                        ),
                    ]
                ),
                html.Div(
                    children=[
                        html.H1(
                            "Research Question 2: ",
                            style={"margin-left": "1.5cm", "font-family": "Arial"},
                        ),
                        html.H2(
                            "Seasonal Trends in E-commerce",
                            style={"margin-left": "1.5cm", "font-family": "Arial"},
                        ),
                        html.H3(
                            "What seasonal trends exist in Dutch e-commerce purchasing patterns, and how do they vary by product category? (Identify the most affected categories by season/weather conditions)",
                            style={
                                "margin-left": "1.5cm",
                                "font-family": "Arial",
                                "color": "gray",
                            },
                        ),
                        dcc.Graph(
                            id="monthly-sales-boxplots",
                            figure=create_monthly_sales_boxplots(),
                            style={"width": "100%"},
                        ),
                        html.H3(
                            "Answer:",
                            style={"margin-left": "1.5cm", "font-family": "Arial"},
                        ),
                        html.Div(
                            children=[
                                html.P(
                                    "We can observe some seasonal trends in the purchasing patterns of Dutch e-commerce."
                                ),
                                html.P(
                                    "In paticular, we can see that online sales tend to increase during the winter months. Electonics sales are also higher during the winter months, while food and drugstore items tend to be more stable throughout the year."
                                ),
                            ],
                            style={
                                "margin-left": "1.5cm",
                                "margin-right": "1.5cm",
                                "font-family": "Arial",
                            },
                        ),
                    ]
                ),
                html.Div(
                    children=[
                        html.H1(
                            "Research Question 3: ",
                            style={"margin-left": "1.5cm", "font-family": "Arial"},
                        ),
                        html.H2(
                            "Search Interests vs. Online Sales",
                            style={"margin-left": "1.5cm", "font-family": "Arial"},
                        ),
                        html.H3(
                            "How do search interests correlate with actual purchasing decisions, and can they predict future sales trends?",
                            style={
                                "margin-left": "1.5cm",
                                "font-family": "Arial",
                                "color": "gray",
                            },
                        ),
                        dcc.Graph(
                            id="search-vs-online-sales",
                            style={"width": "100%"},
                        ),
                        dcc.Graph(
                            id="search-vs-sales-categories",
                            style={"width": "100%"},
                        ),
                        html.H3(
                            "Answer:",
                            style={"margin-left": "1.5cm", "font-family": "Arial"},
                        ),
                        html.Div(
                            children=[
                                html.P(
                                    "The analysis shows that search interests do correlate with actual purchasing decisions, and they can be used to predict future sales trends."
                                ),
                                html.P(
                                    "Especially for electronics and fashion categories, search interests tend to lead actual sales. For food and non-food categories, the correlation is less strong."
                                ),
                            ],
                            style={
                                "margin-left": "1.5cm",
                                "margin-right": "1.5cm",
                                "font-family": "Arial",
                            },
                        ),
                    ]
                ),
            ]
        )
    ]
)


@app.callback(
    Output("line-graph", "figure"), Input("online-sales-variation", "relayoutData")
)
def create_weather_monthly_avg_variation_plot(relayoutData):
    display_names = {
        "temp": "Temperature",
        "rain": "Precipitation",
        "wind_speed": "Wind Speed",
    }
    weather_cols = [
        "rain",
        "wind_speed",
        "temp",
    ]
    if (
        relayoutData
        and "xaxis.range[0]" in relayoutData
        and "xaxis.range[1]" in relayoutData
    ):
        start_date = relayoutData["xaxis.range[0]"].split(" ")[0]
        end_date = relayoutData["xaxis.range[1]"].split(" ")[0]
        df = get_sales_weather_data_by_date_range(driver, start_date, end_date)
    else:
        df = get_sales_weather_data(driver)

    monthly_weather_avg = df.groupby("month")[weather_cols].transform("mean")
    weather_variation = df[weather_cols] - monthly_weather_avg

    fig = make_subplots(
        rows=len(weather_cols),
        cols=1,
        shared_xaxes=True,
        subplot_titles=[
            f"{display_names[col]} with Monthly Avg and Variation"
            for col in weather_cols
        ],
        vertical_spacing=0.05,
    )

    for i, col in enumerate(weather_cols):
        # Actual values
        fig.add_trace(
            go.Scatter(
                x=df["date"],
                y=df[col],
                mode="lines+markers",
                name=f"{display_names[col]} (actual)",
                line=dict(),
            ),
            row=i + 1,
            col=1,
        )
        # Monthly average
        fig.add_trace(
            go.Scatter(
                x=df["date"],
                y=monthly_weather_avg[col],
                mode="lines",
                name="Monthly Avg",
                line=dict(dash="dash"),
            ),
            row=i + 1,
            col=1,
        )
        # Variation
        fig.add_trace(
            go.Scatter(
                x=df["date"],
                y=weather_variation[col],
                mode="lines",
                name="Variation",
                line=dict(dash="dot"),
            ),
            row=i + 1,
            col=1,
        )
        fig.update_yaxes(title_text=display_names[col], row=i + 1, col=1)

    fig.update_xaxes(title_text="Date", row=len(weather_cols), col=1, tickangle=45)
    fig.update_layout(
        height=350 * len(weather_cols),
        showlegend=True,
        margin=dict(l=40, r=40, t=60, b=40),
    )
    return fig


# @app.callback(
#     Output("line-graph", "figure"), Input("online-sales-variation", "relayoutData")
# )
# def update_weather_variation_plot(relayoutData):
#     weather_cols = [
#         "rain",
#         "wind_speed",
#         "temp",
#     ]
#     if (
#         relayoutData
#         and "xaxis.range[0]" in relayoutData
#         and "xaxis.range[1]" in relayoutData
#     ):
#         start_date = relayoutData["xaxis.range[0]"].split(" ")[0]
#         end_date = relayoutData["xaxis.range[1]"].split(" ")[0]
#         df = get_sales_weather_data_by_date_range(driver, start_date, end_date)
#     else:
#         df = get_sales_weather_data(driver)
#
#     monthly_weather_avg = df.groupby("month")[weather_cols].transform("mean")
#     weather_variation = df[weather_cols] - monthly_weather_avg
#
#     fig = make_subplots(
#         rows=len(weather_cols),
#         cols=1,
#         shared_xaxes=True,
#         subplot_titles=[
#             f"{col.replace('_', ' ').capitalize()} - Variation from Monthly Average"
#             for col in weather_cols
#         ],
#         vertical_spacing=0.03,  # Reduced spacing between plots
#     )
#     for i, col in enumerate(weather_cols):
#         fig.add_trace(
#             go.Scatter(
#                 x=df["date"],
#                 y=weather_variation[col],
#                 mode="lines+markers",
#                 name=f"{col.replace('_', ' ')} variation",
#             ),
#             row=i + 1,
#             col=1,
#         )
#         fig.update_yaxes(title_text="Variation", row=i + 1, col=1)
#     fig.update_xaxes(
#         title_text="Date", row=len(weather_cols), col=1, nticks=len(df["date"].unique())
#     )
#     fig.update_layout(
#         height=300 * len(weather_cols),
#         showlegend=False,
#         title="Weather Variation from Monthly Average",
#     )
#     return fig


@app.callback(
    Output("heatmap", "figure"),
    Input("line-graph", "relayoutData"),
    Input("online-sales-variation", "relayoutData"),
)
def update_heatmap(relayoutData, relayoutData2):
    weather_cols = [
        "rain",
        "wind_speed",
        "temp",
    ]
    sales_cols = [
        "multi_channel",
        "retail_sale_of_clothes_and_fashion_items",
        "retail_sale_of_consumer_electronics",
        "retail_sale_of_food_and_drugstore_items",
        "retail_sale_of_other_non_food",
        "retail_sale_via_internet",
        "retail_trade",
    ]
    title = "Correlation: Weather vs. Sales Categories"
    if (
        relayoutData
        and "xaxis.range[0]" in relayoutData
        and "xaxis.range[1]" in relayoutData
    ):
        start_date = relayoutData["xaxis.range[0]"].split(" ")[0]
        end_date = relayoutData["xaxis.range[1]"].split(" ")[0]
        df = get_sales_weather_data_by_date_range(driver, start_date, end_date)

        start_fmt = datetime.strptime(start_date, "%Y-%m-%d").strftime("%b %Y")
        end_fmt = datetime.strptime(end_date, "%Y-%m-%d").strftime("%b %Y")
        title = f"Heatmap for {start_fmt} to {end_fmt}"
    elif (
        relayoutData2
        and "xaxis.range[0]" in relayoutData2
        and "xaxis.range[1]" in relayoutData2
    ):
        start_date = relayoutData2["xaxis.range[0]"].split(" ")[0]
        end_date = relayoutData2["xaxis.range[1]"].split(" ")[0]
        df = get_sales_weather_data_by_date_range(driver, start_date, end_date)

        start_fmt = datetime.strptime(start_date, "%Y-%m-%d").strftime("%b %Y")
        end_fmt = datetime.strptime(end_date, "%Y-%m-%d").strftime("%b %Y")
        title = f"Heatmap for {start_fmt} to {end_fmt}"
    else:
        df = get_sales_weather_data(driver)
        title = "Heatmap for all dates"

    sub_corr = df[weather_cols + sales_cols].corr().loc[weather_cols, sales_cols]
    sub_corr = sub_corr.round(3)
    sub_corr = sub_corr.rename(
        columns={
            "multi_channel": "Multi-Channel Sales",
            "retail_sale_of_clothes_and_fashion_items": "Fashion Sales",
            "retail_sale_of_consumer_electronics": "Electronics Sales",
            "retail_sale_of_food_and_drugstore_items": "Food Sales",
            "retail_sale_of_other_non_food": "Other Non-Food Sales",
            "retail_sale_via_internet": "Online Sales",
            "retail_trade": "Retail Trade",
        },
        index={
            "rain": "Rain",
            "wind_speed": "Wind Speed",
            "temp": "Temperature",
        },
    )
    fig = px.imshow(
        sub_corr.T,  # Transpose so sales categories are y, weather is x
        x=sub_corr.T.columns,
        y=sub_corr.T.index,
        text_auto=True,
        color_continuous_scale="RdBu",
        labels=dict(x="Weather", y="Sales Category", color="Correlation"),
        title=title,
        zmin=-1,
        zmax=1,
    )
    fig.update_layout(xaxis_title="Weather", yaxis_title="Sales Category")
    return fig


@app.callback(
    Output("heatmap-seasonality-removed", "figure"),
    Input("line-graph", "relayoutData"),
    Input("online-sales-variation", "relayoutData"),
)
def update_heatmap_seasonality_removed(relayoutData, relayoutData2):
    weather_cols = [
        "rain",
        "wind_speed",
        "temp",
    ]
    sales_cols = [
        "multi_channel",
        "retail_sale_of_clothes_and_fashion_items",
        "retail_sale_of_consumer_electronics",
        "retail_sale_of_food_and_drugstore_items",
        "retail_sale_of_other_non_food",
        "retail_sale_via_internet",
        "retail_trade",
    ]
    title = "Correlation: Weather vs. Sales Categories"
    if (
        relayoutData
        and "xaxis.range[0]" in relayoutData
        and "xaxis.range[1]" in relayoutData
    ):
        start_date = relayoutData["xaxis.range[0]"].split(" ")[0]
        end_date = relayoutData["xaxis.range[1]"].split(" ")[0]
        df = get_sales_weather_data_by_date_range(driver, start_date, end_date)

        start_fmt = datetime.strptime(start_date, "%Y-%m-%d").strftime("%b %Y")
        end_fmt = datetime.strptime(end_date, "%Y-%m-%d").strftime("%b %Y")
        title = f"Heatmap for {start_fmt} to {end_fmt}"
    elif (
        relayoutData2
        and "xaxis.range[0]" in relayoutData2
        and "xaxis.range[1]" in relayoutData2
    ):
        start_date = relayoutData2["xaxis.range[0]"].split(" ")[0]
        end_date = relayoutData2["xaxis.range[1]"].split(" ")[0]
        df = get_sales_weather_data_by_date_range(driver, start_date, end_date)

        start_fmt = datetime.strptime(start_date, "%Y-%m-%d").strftime("%b %Y")
        end_fmt = datetime.strptime(end_date, "%Y-%m-%d").strftime("%b %Y")
        title = f"Heatmap (Seasonality Removed) for {start_fmt} to {end_fmt}"
    else:
        df = get_sales_weather_data(driver)
        title = "Heatmap (Seasonality Removed) for all dates"

    df_adj = df.copy()
    seasonal_col = "month"

    for col in weather_cols + sales_cols:
        monthly_mean = df.groupby(seasonal_col)[col].transform("mean")
        df_adj[col] = df[col] - monthly_mean

    sub_corr = df_adj[weather_cols + sales_cols].corr().loc[weather_cols, sales_cols]
    sub_corr = sub_corr.round(3)
    sub_corr = sub_corr.rename(
        columns={
            "multi_channel": "Multi-Channel Sales",
            "retail_sale_of_clothes_and_fashion_items": "Fashion Sales",
            "retail_sale_of_consumer_electronics": "Electronics Sales",
            "retail_sale_of_food_and_drugstore_items": "Food Sales",
            "retail_sale_of_other_non_food": "Other Non-Food Sales",
            "retail_sale_via_internet": "Online Sales",
            "retail_trade": "Retail Trade",
        },
        index={
            "rain": "Rain",
            "wind_speed": "Wind Speed",
            "temp": "Temperature",
        },
    )

    fig = px.imshow(
        sub_corr.T,  # Transpose so sales categories are y, weather is x
        x=sub_corr.T.columns,
        y=sub_corr.T.index,
        text_auto=True,
        color_continuous_scale="RdBu",
        labels=dict(x="Weather", y="Sales Category", color="Correlation"),
        title=title,
        zmin=-1,
        zmax=1,
    )
    fig.update_layout(xaxis_title="Weather", yaxis_title="Sales Category")
    return fig


@app.callback(
    Output("online-sales-variation", "figure"), Input("line-graph", "relayoutData")
)
def update_online_sales_variation(relayoutData):
    if (
        relayoutData
        and "xaxis.range[0]" in relayoutData
        and "xaxis.range[1]" in relayoutData
    ):
        start_date = relayoutData["xaxis.range[0]"].split(" ")[0]
        end_date = relayoutData["xaxis.range[1]"].split(" ")[0]
        df = get_sales_weather_data_by_date_range(driver, start_date, end_date)
    else:
        df = get_sales_weather_data(driver)

    sales_col = "retail_sale_via_internet"
    monthly_sales_avg = df.groupby("month")[sales_col].transform("mean")
    sales_variation = df[sales_col] - monthly_sales_avg

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=df["date"],
            y=sales_variation,
            mode="lines+markers",
            name="Online Sales",
            line=dict(color="purple"),
        )
    )
    fig.update_layout(
        title="Online Sales Variation from Monthly Average",
        xaxis_title="Date",
        yaxis_title="Variation",
        showlegend=False,
        height=400,
        margin=dict(l=40, r=40, t=60, b=40),
    )

    fig.update_xaxes(tickangle=45, nticks=len(df["date"].unique()))
    fig.update_yaxes(gridcolor="lightgray")
    return fig


@app.callback(
    Output("search-vs-online-sales", "figure"),
    Input("search-vs-sales-categories", "relayoutData"),
)
def update_search_vs_online_sales(relayoutData):
    if (
        relayoutData
        and "xaxis.range[0]" in relayoutData
        and "xaxis.range[1]" in relayoutData
    ):
        start_date = relayoutData["xaxis.range[0]"].split(" ")[0]
        end_date = relayoutData["xaxis.range[1]"].split(" ")[0]
        df = get_sales_google_trends_data_by_date_range(driver, start_date, end_date)
        title = f"Average Search Interest vs. Online Sales ({start_date} to {end_date})"
    else:
        df = get_sales_google_trends_data(driver)
        title = "Average Search Interest vs. Online Sales"

    search_cols = [
        "fashion_search",
        "electronics_search",
        "food_search",
        "non_food_search",
    ]
    df["Avg Search Interest"] = df[search_cols].mean(axis=1)

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=df["date"],
            y=df["Avg Search Interest"],
            mode="lines+markers",
            name="Avg Search Interest",
            marker=dict(symbol="circle"),
            line=dict(color="#1f77b4"),
            yaxis="y",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=df["date"],
            y=df["retail_sale_via_internet"],
            mode="lines+markers",
            name="Retail Sale via Internet",
            marker=dict(symbol="circle"),
            line=dict(color="#ff7f0e"),
            yaxis="y2",
        )
    )

    fig.update_layout(
        title=title,
        xaxis_title="Date",
        yaxis=dict(
            title=dict(text="Avg Search Interest", font=dict(color="#1f77b4")),
            tickfont=dict(color="#1f77b4"),
        ),
        yaxis2=dict(
            title=dict(text="Retail Sale via Internet", font=dict(color="#ff7f0e")),
            tickfont=dict(color="#ff7f0e"),
            overlaying="y",
            side="right",
        ),
        legend=dict(x=0, y=1),
        height=400,
        margin=dict(l=40, r=40, t=60, b=40),
    )
    fig.update_xaxes(tickangle=45)
    return fig


@app.callback(
    Output("search-vs-sales-categories", "figure"),
    Input("search-vs-online-sales", "relayoutData"),
)
def update_search_vs_sales_categories(relayoutData):
    category_map = {
        "fashion_search": "retail_sale_of_clothes_and_fashion_items",
        "electronics_search": "retail_sale_of_consumer_electronics",
        "food_search": "retail_sale_of_food_and_drugstore_items",
        "non_food_search": "retail_sale_of_other_non_food",
    }
    n = len(category_map)

    # Color palette (extend or change as needed)
    colors = [
        "#1f77b4",
        "#ff7f0e",
        "#2ca02c",
        "#d62728",
        "#9467bd",
        "#8c564b",
        "#e377c2",
        "#7f7f7f",
    ]

    # Get data
    if (
        relayoutData
        and "xaxis.range[0]" in relayoutData
        and "xaxis.range[1]" in relayoutData
    ):
        start_date = relayoutData["xaxis.range[0]"].split(" ")[0]
        end_date = relayoutData["xaxis.range[1]"].split(" ")[0]
        df_sales = get_sales_weather_data_by_date_range(driver, start_date, end_date)
        df_search = get_sales_google_trends_data_by_date_range(
            driver, start_date, end_date
        )
    else:
        df_sales = get_sales_weather_data(driver)
        df_search = get_sales_google_trends_data(driver)

    # Merge on date
    df_combined = df_search.merge(df_sales, on="date", how="inner")

    fig = make_subplots(
        rows=n,
        cols=1,
        shared_xaxes=True,
        subplot_titles=[
            f"{search_col.replace('_', ' ').title()} vs. {sales_col.replace('_', ' ').title()}"
            for search_col, sales_col in category_map.items()
        ],
        vertical_spacing=0.07,
        specs=[[{"secondary_y": True}] for _ in range(n)],
    )

    for i, (search_col, sales_col) in enumerate(category_map.items()):
        search_color = colors[i % len(colors)]
        sales_color = colors[(i + n) % len(colors)]
        # Search interest (left y-axis)
        fig.add_trace(
            go.Scatter(
                x=df_combined["date"],
                y=df_combined[search_col],
                mode="lines+markers",
                name=search_col.replace("_", " ").title(),
                marker=dict(color=search_color),
                line=dict(color=search_color),
            ),
            row=i + 1,
            col=1,
            secondary_y=False,
        )
        # Sales (right y-axis)
        fig.add_trace(
            go.Scatter(
                x=df_combined["date"],
                y=df_combined[sales_col],
                mode="lines+markers",
                name=sales_col.replace("_", " ").title(),
                marker=dict(color=sales_color),
                line=dict(color=sales_color),
            ),
            row=i + 1,
            col=1,
            secondary_y=True,
        )
        fig.update_yaxes(
            title_text="Search Interest",
            row=i + 1,
            col=1,
            secondary_y=False,
            color=search_color,
        )
        fig.update_yaxes(
            title_text="Sales", row=i + 1, col=1, secondary_y=True, color=sales_color
        )

    fig.update_xaxes(title_text="Date", row=n, col=1, tickangle=45)
    fig.update_layout(
        height=300 * n,
        showlegend=True,
        title="Google Trends Search vs. Sales Categories",
        margin=dict(l=40, r=40, t=60, b=40),
    )

    return fig


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=8050)
