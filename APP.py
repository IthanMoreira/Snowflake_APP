import streamlit
import pandas
import requests

import snowflake.connector
from urllib.error import URLError

# Añadimos el titulo de nuestro sitio web

streamlit.title("Listado de comida")

streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado toast')


streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")

# Mostramos el titulo
my_fruit_list = my_fruit_list.set_index('Fruit')

# Seleccion multiple de frutas
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado', 'Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

streamlit.dataframe(fruits_to_show)

# Creacion de funcion
def get_fruityvice_data(this_fruit_choice):
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
    # streamlit.text(fruityvice_response.json())

    # Normalizamos el dato que nos entrega la api rest
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    return fruityvice_normalized


streamlit.header("Fruityvice Fruit Advice!")
try:
    fruit_choice = streamlit.text_input('What fruit would you like information about?')
    if not fruit_choice:
        streamlit.error('Please select a fruit to get information')
    else:
        back_from_function = get_fruityvice_data(fruit_choice)
        # mostramos el dato en formato tabla
        streamlit.dataframe(back_from_function)
except URLError as e:
    streamlit.error()
