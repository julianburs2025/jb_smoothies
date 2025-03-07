# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col


helpful_links = [
    "https://docs.streamlit.io",
    "https://docs.snowflake.com/en/developer-guide/streamlit/about-streamlit",
    "https://github.com/Snowflake-Labs/snowflake-demo-streamlit",
    "https://docs.snowflake.com/en/release-notes/streamlit-in-snowflake"
]
cnx = st.connection("snowflake")
session = cnx.session()
# Write directly to the app
st.title(":cup_with_straw: Customize your smoothie!:cup_with_straw:")
st.write(
    """ Choose the fruits you want in your custom Smoothie!"""
)


# ord_filled = ("False")
name_on_order = st.text_input("Name on Smoothie")
st.write("The name on your smoothie will be: ", name_on_order)

# Get the current credentials
session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('Fruit_name'))
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients'
    , my_dataframe
    , max_selections=5
)
if ingredients_list:  
    ingredients_string=''
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen+' '
   # st.write(ingredients_string)  
   
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order )
            values ('""" + ingredients_string + """','"""+name_on_order+"""')"""
    
   # st.write(my_insert_stmt)
   # st.stop
    
    time_to_insert = st.button('Submit order')   
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered,'+name_on_order+'!', icon="✅")
   

   


