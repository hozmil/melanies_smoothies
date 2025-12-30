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



url = "https://smoothiefroot.com/api/fruit/watermelon"
resp = requests.get(url, timeout=10)

st.write("Status:", resp.status_code)
st.write("Content-Type:", resp.headers.get("content-type", ""))
# Show a bit of the raw response so you can see what it really is
st.text(resp.text[:500])

if resp.ok and "application/json" in resp.headers.get("content-type", ""):
    data = resp.json()
    st.dataframe(data=data, use_container_width=True)
else:
    st.error("API did not return JSON (see status/text above).")
