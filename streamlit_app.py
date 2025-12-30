import streamlit as st
from snowflake.snowpark.functions import col

st.title(f"Customise Your Smoothie :cup_with_straw: {st.__version__}")
st.write("Choose the fruits you want in your custom Smoothie.")

# ✅ create Snowflake session FIRST (works outside SiS)
cnx = st.connection("snowflake")
session = cnx.session()

name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on your Smoothie will be:", name_on_order)

# ✅ multiselect needs a Python list (not a Snowpark DF)
fruit_rows = (
    session.table("smoothies.public.fruit_options")
    .select(col("FRUIT_NAME"))
    .collect()
)
fruit_options = [r["FRUIT_NAME"] for r in fruit_rows]

ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
    fruit_options,
    max_selections=5
)

if ingredients_list:
    ingredients_string = " ".join(ingredients_list)

    st.write(ingredients_string)

    my_insert_stmt = f"""
        insert into smoothies.public.orders (ingredients, name_on_order)
        values ('{ingredients_string}', '{name_on_order}')
    """

    time_to_insert = st.button("Submit Order")
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success("Your Smoothie is ordered!", icon="✅")

# New section to display smoothiefruit nutrition information
import requests

smoothiefruit_response = requests.get(
    "https://smoothiefroot.com/api/fruit/watermelon",
    timeout=10,
    verify=False
)
st.json(smoothiefruit_response.json())
