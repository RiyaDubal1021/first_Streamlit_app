#streamlit.stop()

import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLERROR




streamlit.title('My Parents New Healthy Diner')

streamlit.header('Breakfast Menu')

streamlit.text('🥣 Omega 3 & Blueberry & Oatmeal')

streamlit.text('🥗 Kale, Spinach 3 & Rocket Soomethie')

streamlit.text('🐔 Hard-Boiled Free-Range Egg')

streamlit.text('🥑 Avocado Tost')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pandas.read_csv('https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt')
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick and fruit they want to include

fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado', 'Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

#display table on page
streamlit.dataframe(fruits_to_show)

# A new section to display fruityvice advise
fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
streamlit.write('The user entered ', fruit_choice)

streamlit.header("Fruityvice Fruit Advice!")
#Let's removed the line of raw JSON, and separate the base URL from the fruit name (which will make it easier to use a variable there).
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + "kiwi")
streamlit.text(fruityvice_response.json())

# take the json version of the response and normalize it 
fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
# output it on the screen as a table
streamlit.dataframe(fruityvice_normalized)

#query meta data
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT * from fruit_load_list")
my_data_rows = my_cur.fetchall()
streamlit.header("The Fruit Load List Contains:")
streamlit.dataframe(my_data_rows)

# A new section to display fruit to add
fruit_choice2 = streamlit.text_input('What fruit would you like to add?' ,'jackfruit')
streamlit.write('Thanks for adding  ', fruit_choice2)

my_cur.execute("insert into fruit_load_list values ('from streamlit')")
