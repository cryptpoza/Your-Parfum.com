import pandas as pd
import streamlit as st
import random

# Configuración de la página
st.set_page_config(page_title="YourParfum", layout="wide", initial_sidebar_state="collapsed")

# Estilo para la fuente y el color (estilo minimalista de Zara)
st.markdown("""
    <style>
    body {
        font-family: sans-serif;
        color: #1a1a1a;
        background-color: #f7f7f7;
    }
    .st-emotion-cache-1jmveez, .st-emotion-cache-1jmveez.e1fqp12o1 {
        background-color: #ffffff;
        border-radius: 0px;
        border: 1px solid #e0e0e0;
    }
    .st-emotion-cache-1jmveez {
        box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.05);
    }
    h1, h2, h3, h4, h5, h6 {
        color: #000000;
        font-weight: 400;
    }
    h1 {
        font-size: 2.5em;
        text-transform: uppercase;
        letter-spacing: 0.2em;
    }
    h2 {
        font-size: 1.5em;
        font-weight: 300;
        margin-top: 1em;
    }
    p {
        color: #555555;
    }
    .st-emotion-cache-79elbk {
        color: #000000;
        font-weight: bold;
    }
    .st-emotion-cache-1r65h9z {
        border: 1px solid #000000;
        background-color: #ffffff;
        color: #000000;
        padding: 10px 20px;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        font-weight: bold;
    }
    .st-emotion-cache-1r65h9z:hover {
        background-color: #000000;
        color: #ffffff;
    }
    .stRadio > label {
        font-weight: bold;
        color: #000000;
    }
    .stRadio [data-baseweb="radio"] {
        background-color: #ffffff;
    }
    .stRadio [data-baseweb="radio"]:checked {
        background-color: #000000;
    }
    .stWarning {
        background-color: #f5f5f5;
        border-left: 5px solid #cccccc;
        color: #555555;
        font-style: italic;
    }
    .stWarning .st-emotion-cache-1dkeo0u {
        color: #555555;
    }
    </style>
    """, unsafe_allow_html=True)

# Cargar el CSV
try:
    df = pd.read_csv('perfumes.csv')
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
col_logo, col_title = st.columns([1, 4])
with col_logo:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/1/1d/Perfume-bottle-icon.svg/1200px-Perfume-bottle-icon.svg.png", width=100)
with col_title:
    st.title("YourParfum")
    st.markdown("---")
    st.markdown("<h2 style='text-align: left; margin-top: -20px; font-weight: 300;'>Encuentra tu perfume ideal.</h2>", unsafe_allow_html=True)


# Selección de modo
st.markdown("<br>", unsafe_allow_html=True)
modo = st.radio(
    "Selecciona el modo de búsqueda:",
    ("Guía Personalizada", "Explorar por Filtros"),
    horizontal=True
)

st.markdown("---")

if modo == "Guía Personalizada":
    st.header("✨ Guía Personalizada")

    with st.form("guia_form"):
        aroma_preferido = st.selectbox("1. ¿Qué tipo de aroma te atrae más?", tipos_aroma[1:])
        ocasion_uso = st.selectbox("2. ¿Para qué ocasión lo usarías?", ocasiones[1:])
        intensidad_preferida = st.selectbox("3. ¿Qué intensidad prefieres en una fragancia?", intensidades[1:])
        presupuesto = st.slider("4. ¿Cuál es tu presupuesto máximo (€)?", min_value=10, max_value=300, value=100, step=5)
        
        submitted = st.form_submit_button("¡Encontrar mi perfume!")

    if submitted:
        resultados = df[
            (df['Tipo de aroma'] == aroma_preferido) &
            (df['Ocasión'] == ocasion_uso) &
            (df['Intensidad'] == intensidad_preferida) &
            (df['Precio (€)'] <= presupuesto)
        ]
        
        if not resultados.empty:
            st.markdown("<h3 style='text-align: center;'>🎉 ¡Hemos encontrado tu perfume ideal!</h3>", unsafe_allow_html=True)
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
                    st.markdown(f"[🛒 Comprar dupe]({row['Enlace dupe']})")
                    st.markdown("---")
        else:
            st.warning("No encontramos perfumes con esos criterios. Aquí tienes una recomendación popular:")
            recomendacion_popular = df.sample(min(3, len(df)))
            
            for _, row in recomendacion_popular.iterrows():
                st.markdown("<br>", unsafe_allow_html=True)
                col1, col2 = st.columns([1, 2])
                with col1:
                    st.image(row['Imagen (URL)'], width=150)
                with col2:
                    st.markdown(f"**{row['Nombre']}** - {row['Marca']}")
                    st.write(f"💰 Precio: {row['Precio (€)']}€")
                    st.write(f"💎 Dupe: **{row['Dupe barato']}**")
                    st.markdown(f"[🛒 Comprar dupe]({row['Enlace dupe']})")
                    st.markdown("---")

elif modo == "Explorar por Filtros":
    st.header("🔍 Explorar por Filtros")
    
    selected_marca = st.selectbox("Elige una marca:", marcas)
    selected_tipo = st.selectbox("Elige el tipo de aroma:", tipos_aroma)
    selected_intensidad = st.selectbox("Elige la intensidad:", intensidades)
    selected_ocasion = st.selectbox("Elige la ocasión:", ocasiones)
    selected_nota = st.selectbox("Elige una nota olfativa:", notas)
    
    presupuesto = st.slider("Presupuesto máximo (€):", min_value=10, max_value=300, value=150, step=5)

    filtros = (df['Precio (€)'] <= presupuesto)
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
                        st.markdown(f"[🛒 Comprar dupe]({row['Enlace dupe']})")
                        st.markdown("---")
    else:
        st.warning("No encontramos perfumes con esos criterios. Prueba a cambiar los filtros.")

st.markdown("---")
st.markdown('<p style="text-align: center; color: grey;">Creado por Miguel Poza</p>', unsafe_allow_html=True)
