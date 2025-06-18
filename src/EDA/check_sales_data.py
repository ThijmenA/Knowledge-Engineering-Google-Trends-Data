# %%
import pandas as pd

data = pd.read_csv("./sales_data_transformed.csv")

# %%
data

# %%
(data["Multi-channel"] + data["Retail sale via internet"]) / 2

# %%
data["Retail trade"]

# %%
data.columns

# %%
(
    data["Retail sale of clothes and fashion items"]
    + data["Retail sale of consumer electronics"]
    + data["Retail sale of food and drugstore items"]
    + data["Retail sale of other non-food"]
) / 4
