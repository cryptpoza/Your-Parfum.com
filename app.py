import pandas as pd
import streamlit as st
import random

# Configuración de la página
st.set_page_config(
    page_title="YourParfum",
    layout="wide",
    initial_sidebar_state="collapsed",
    page_icon="🌸"
)

# Estilo para el diseño formal y minimalista
st.markdown("""
    <style>
    .main {
        background-color: #fcfcfc;
        color: #222222;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    }
    
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Georgia', serif;
        font-weight: 300;
        color: #000000;
    }
    
    .st-emotion-cache-1jmveez, .st-emotion-cache-1jmveez.e1fqp12o1 {
        background-color: #ffffff;
        border-radius: 0px;
        border: 1px solid #e0e0e0;
        box-shadow: none;
    }
    
    .st-emotion-cache-1r65h9z {
        border: 1px solid #000000;
        background-color: #ffffff;
        color: #000000;
        padding: 10px 20px;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        font-weight: 500;
        transition: all 0.2s ease;
    }
    
    .st-emotion-cache-1r65h9z:hover {
        background-color: #000000;
        color: #ffffff;
    }

    .stRadio > label {
        font-weight: normal;
        color: #000000;
        font-family: 'Georgia', serif;
    }
    
    .stRadio [data-baseweb="radio"] {
        border-color: #000000;
    }
    
    .stRadio [data-baseweb="radio"]:checked {
        border-color: #000000;
        background-color: #000000;
    }

    .stSelectbox > label, .stSlider > label {
        color: #000000;
        font-weight: normal;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        text-transform: uppercase;
        letter-spacing: 0.1em;
    }

    .stWarning {
        background-color: transparent;
        border: none;
        color: #555555;
        font-style: italic;
        padding-left: 0;
        border-left: none;
    }
    
    .stWarning .st-emotion-cache-1dkeo0u {
        display: none;
    }
    
    .st-emotion-cache-e1nz1l x {
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# Cargar el CSV
try:
    df = pd.read_csv('perfumes.csv')
    generos = ['Hombre', 'Mujer', 'Unisex']
    marcas = ['Todas'] + sorted(df['Marca'].unique().tolist())
    tipos_aroma = ['Cualquiera'] + sorted(df['Tipo de aroma'].unique().tolist())
    intensidades = ['Cualquiera'] + sorted(df['Intensidad'].unique().tolist())
    ocasiones = ['Cualquiera'] + sorted(df['Ocasión'].unique().tolist())
    df['Notas'] = df['Notas'].str.split(',')
    all_notes = df['Notas'].explode().str.strip().unique().tolist()
    notas = ['Cualquiera'] + sorted(all_notes)
except FileNotFoundError:
    st.error("Error: El archivo 'perfumes.csv' no se encontró. Por favor, asegúrate de haberlo subido a GitHub.")
    st.stop()

# Logo y título
st.markdown("<h1 style='text-align: center; font-size: 3em;'>YourParfum</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; font-weight: 300;'>Encuentra tu aroma perfecto.</h3>", unsafe_allow_html=True)
st.markdown("---")

# Nuevo filtro de género al inicio
selected_genero = st.radio(
    "Selecciona el género:",
    generos,
    horizontal=True
)

st.markdown("---")

# Selección de modo
modo = st.radio(
    "Selecciona el modo de búsqueda:",
    ("Guía Personalizada", "Explorar por Filtros"),
    horizontal=True
)

st.markdown("---")

if modo == "Guía Personalizada":
    st.header("Guía Personalizada")

    with st.form("guia_form"):
        aroma_preferido = st.selectbox("1. ¿Qué tipo de aroma te atrae más?", tipos_aroma[1:])
        ocasion_uso = st.selectbox("2. ¿Para qué ocasión lo usarías?", ocasiones[1:])
        intensidad_preferida = st.selectbox("3. ¿Qué intensidad prefieres en una fragancia?", intensidades[1:])
        presupuesto = st.slider("4. ¿Cuál es tu presupuesto máximo (€)?", min_value=10, max_value=300, value=100, step=5)
        
        submitted = st.form_submit_button("¡Encontrar mi perfume!")

    if submitted:
        resultados = df[
            (df['Género'].isin([selected_genero, 'Unisex'])) &
            (df['Tipo de aroma'] == aroma_preferido) &
            (df['Ocasión'] == ocasion_uso) &
            (df['Intensidad'] == intensidad_preferida) &
            (df['Precio (€)'] <= presupuesto)
        ]
        
        st.markdown("<h3 style='text-align: center;'>Resultados</h3>", unsafe_allow_html=True)

        if not resultados.empty:
            resultados_finales = resultados.sample(min(3, len(resultados)))
            
            for _, row in resultados_finales.iterrows():
                st.markdown("<br>", unsafe_allow_html=True)
                col1, col2 = st.columns([1, 2])
                with col1:
                    st.image(row['Imagen (URL)'], width=150)
                with col2:
                    st.markdown(f"**{row['Nombre']}** - {row['Marca']}")
                    st.write(f"💰 Precio: {row['Precio (€)']}€")
                    st.write(f"💎 Dupe: **{row['Dupe barato']}**")
                    
                    st.markdown(f"🛒 [Comprar Original]({row['Enlace original']})")
                    st.markdown(f"🛒 [Comprar Dupe]({row['Enlace dupe']})")
                    st.markdown("---")
        else:
            st.warning("No encontramos perfumes con esos criterios. Aquí tienes una recomendación popular:")
            recomendacion_popular = df.sample(min(3, len(df))]
            
            for _, row in recomendacion_popular.iterrows():
                st.markdown("<br>", unsafe_allow_html=True)
                col1, col2 = st.columns([1, 2])
                with col1:
                    st.image(row['Imagen (URL)'], width=150)
                with col2:
                    st.markdown(f"**{row['Nombre']}** - {row['Marca']}")
                    st.write(f"💰 Precio: {row['Precio (€)']}€")
                    st.write(f"💎 Dupe: **{row['Dupe barato']}**")
                    st.markdown(f"🛒 [Comprar Original]({row['Enlace original']})")
                    st.markdown(f"🛒 [Comprar Dupe]({row['Enlace dupe']})")
                    st.markdown("---")

elif modo == "Explorar por Filtros":
    st.header("Explorar por Filtros")
    
    selected_marca = st.selectbox("Elige una marca:", marcas)
    selected_tipo = st.selectbox("Elige el tipo de aroma:", tipos_aroma)
    selected_intensidad = st.selectbox("Elige la intensidad:", intensidades)
    selected_ocasion = st.selectbox("Elige la ocasión:", ocasiones)
    selected_nota = st.selectbox("Elige una nota olfativa:", notas)
    
    presupuesto = st.slider("Presupuesto máximo (€):", min_value=10, max_value=300, value=150, step=5)

    filtros = (df['Precio (€)'] <= presupuesto)
    filtros &= (df['Género'].isin([selected_genero, 'Unisex']))
    if selected_marca != 'Todas':
        filtros &= (df['Marca'] == selected_marca)
    if selected_tipo != 'Cualquiera':
        filtros &= (df['Tipo de aroma'] == selected_tipo)
    if selected_intensidad != 'Cualquiera':
        filtros &= (df['Intensidad'] == selected_intensidad)
    if selected_ocasion != 'Cualquiera':
        filtros &= (df['Ocasión'] == selected_ocasion)
    if selected_nota != 'Cualquiera':
        filtros &= (df['Notas'].apply(lambda x: selected_nota in [n.strip() for n in x]))

    resultados = df[filtros].sort_values(by='Precio (€)').reset_index(drop=True)
    
    total_resultados = len(resultados)
    st.markdown(f"**✨ Perfumes encontrados: {total_resultados}**")
    
    if not resultados.empty:
        resultados_por_pagina = 6
        if 'pagina_actual' not in st.session_state:
            st.session_state.pagina_actual = 0
            
        col_izq, col_der = st.columns([1, 10])
        with col_izq:
            if st.session_state.pagina_actual > 0:
                if st.button("⬅️ Anterior"):
                    st.session_state.pagina_actual -= 1
        with col_der:
            if (st.session_state.pagina_actual + 1) * resultados_por_pagina < total_resultados:
                if st.button("Siguiente ➡️"):
                    st.session_state.pagina_actual += 1

        inicio = st.session_state.pagina_actual * resultados_por_pagina
        fin = inicio + resultados_por_pagina
        resultados_pagina = resultados.iloc[inicio:fin]
        
        for i in range(0, len(resultados_pagina), 3):
            cols = st.columns(3)
            for j in range(3):
                if i + j < len(resultados_pagina):
                    row = resultados_pagina.iloc[i + j]
                    with cols[j]:
                        st.image(row['Imagen (URL)'], width=150, use_column_width='auto')
                        st.write(f"**{row['Nombre']}**")
                        st.write(f"*{row['Marca']}*")
                        st.write(f"💰 Precio: {row['Precio (€)']}€")
                        st.write(f"💎 Dupe: **{row['Dupe barato']}**")
                        st.markdown(f"🛒 [Comprar Original]({row['Enlace original']})")
                        st.markdown(f"🛒 [Comprar Dupe]({row['Enlace dupe']})")
                        st.markdown("---")
    else:
        st.warning("No encontramos perfumes con esos criterios. Prueba a cambiar los filtros.")

st.markdown("---")
st.markdown('<p style="text-align: center; color: grey;">Creado por Miguel Poza</p>', unsafe_allow_html=True)
            
