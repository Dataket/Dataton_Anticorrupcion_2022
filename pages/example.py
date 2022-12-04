import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import time

sns.set_theme()

st.sidebar.title('Parametros')

# To add text
st.write('''
# Dataket - Datatón anticorrución 2022 😎
-----
Streamlit soporta texto estilo **Markdown**, LaTeX y emojis:
$$y = mx \\times \\alpha b$$

Algunas notas:
- Puedes revisar el decorador `@st.cache` para no correr todo el código de nuevo cuando se cambie un parámetros.

- Se pueden mostrar tablas, arreglos y dataframes.

- El método st.write() es muy útil para mostrar texto, imágenes, videos, etc. Sin embargo, no te deja modificar los objetos

- Podemos mostrar el progreso de un proceso con `st.progress()`

- Se pueden agregar directamente diversas páginas web con `st.markdown()`
''')

example_dict = {
    'a': {
        'first': 1,
        'second': 2,
        'third': 3,
    },
    'b': 2,
    'c': 3,
    'd': 4,
    'e': 5,
}


# To add a checkbox
if st.checkbox('Mostrar diccionario'):
    st.write(example_dict)


# You can send plt figures, or maybe a seaborn plot
x = np.linspace(0, 10, 100)
fig = plt.figure(figsize=(12, 5))
plt.plot(x, np.sin(x), '-')
plt.plot(x, np.cos(x), '--')
st.write(fig)

# There is also native support for plots
st.line_chart(pd.DataFrame(np.random.randn(20, 3), columns=['a', 'b', 'c']), use_container_width=True)

st.write("Here's our first attempt at using data to create a table:")
st.write(pd.DataFrame({
    'first column': [1, 2, 3, 4],
    'second column': [10, 20, 30, 40]
}))

st.write('## Widgets')

lamb = st.slider('$\lambda$', 0.0, 1.0, 0.5)

x = np.linspace(0, 100, 1000)
fig = plt.figure(figsize=(12, 5))
plt.title('$\lambda$ = {}'.format(lamb))
plt.plot(x, np.sin(lamb * x), '-')
plt.plot(x, np.cos(lamb * x), '--')
st.write(fig)

st.text_input('Escribe algo', 'Hola mundo', key='input')
st.write('El valor del input es:', st.session_state.input)

# Example of selectbox
df_select = pd.DataFrame({
    'first column': [1, 2, 3, 4],
    'second column': [10, 20, 30, 40],
    'fruit': ['apple', 'banana', 'orange', 'apple']
})

option = st.selectbox(
    '¿Cuál es tu fruta favorita?',
     df_select['fruit'].unique())

option2 = st.sidebar.selectbox(
    '¿Cuál es tu segunda fruta favorita?',
     df_select['fruit'].unique())


left_column, middle_column, right_column = st.columns(3)
# You can use a column just like st.sidebar:
a = left_column.button('Press me!')
left_column.image('https://i.imgur.com/jGDtYFc.png', use_column_width=True)

# Or even better, call Streamlit functions inside a "with" block:
with right_column:
    chosen = st.radio(
        'Sorting hat',
        ("Gryffindor", "Ravenclaw", "Hufflepuff", "Slytherin"))
    st.write(f"You are in {chosen} house!")

with middle_column:
    st.write('## ¡Podemos agregar columnas al layout!')

# Add a placeholder
latest_iteration = st.empty()
bar = st.progress(0)

for i in range(100):
  # Update the progress bar with each iteration.
  latest_iteration.text(f'Iteration {i+1}')
  bar.progress(i + 1)
  time.sleep(0.05)