import pandas as pd
import streamlit as st

# Configuración de la página
st.set_page_config(page_title="YourParfum", layout="wide", initial_sidebar_state="collapsed")

# Título
st.title("💐 YourParfum - Encuentra tu perfume ideal")
st.markdown("Te ayudamos a encontrar tu perfume perfecto y su dupe más asequible.")
st.markdown("---")

# Cargar el CSV
try:
    df = pd.read_csv('perfumes.csv')
    marcas = ['Todas'] + sorted(df['Marca'].unique().tolist())
    tipos_aroma = ['Cualquiera'] + sorted(df['Tipo de aroma'].unique().tolist())
    intensidades = ['Cualquiera'] + sorted(df['Intensidad'].unique().tolist())
    ocasiones = ['Cualquiera'] + sorted(df['Ocasión'].unique().tolist())
    notas = ['Cualquiera'] + sorted(df['Notas'].str.split(',').explode().str.strip().unique().tolist())
except FileNotFoundError:
    st.error("Error: El archivo 'perfumes.csv' no se encontró. Por favor, asegúrate de haberlo subido a Colab.")
    st.stop()

# Selección de modo
modo = st.radio(
    "Selecciona el modo de búsqueda:",
    ("Guía Personalizada", "Explorar por Filtros"),
    horizontal=True
)

st.markdown("---")

if modo == "Guía Personalizada":
    st.header("✨ Guía Personalizada: Responde para encontrar tu perfume")

    with st.form("guia_form"):
        # Pregunta 1: Preferencia de aroma
        aroma_preferido = st.selectbox(
            "1. ¿Qué tipo de aroma te atrae más?",
            tipos_aroma[1:]
        )

        # Pregunta 2: Ocasión de uso
        ocasion_uso = st.selectbox(
            "2. ¿Para qué ocasión lo usarías?",
            ocasiones[1:]
        )

        # Pregunta 3: Intensidad
        intensidad_preferida = st.selectbox(
            "3. ¿Qué intensidad prefieres en una fragancia?",
            intensidades[1:]
        )
        
        # Pregunta 4: Presupuesto
        presupuesto = st.slider(
            "4. ¿Cuál es tu presupuesto máximo (€)?",
            min_value=10, max_value=300, value=100, step=5
        )

        submitted = st.form_submit_button("¡Encontrar mi perfume!")

    if submitted:
        st.subheader("🎉 ¡Hemos encontrado tu perfume ideal!")
        
        # Lógica de la IA (filtrado avanzado)
        resultados = df[
            (df['Tipo de aroma'] == aroma_preferido) &
            (df['Ocasión'] == ocasion_uso) &
            (df['Intensidad'] == intensidad_preferida) &
            (df['Precio (€)'] <= presupuesto)
        ]
        
        if not resultados.empty:
            resultados_finales = resultados.sample(min(3, len(resultados)))
            
            for _, row in resultados_finales.iterrows():
                col1, col2 = st.columns([1, 2])
                with col1:
                    st.image(row['Imagen (URL)'], width=150)
                with col2:
                    st.write(f"**{row['Nombre']}** - {row['Marca']}")
                    st.write(f"💰 Precio: {row['Precio (€)']}€")
                    st.write(f"💎 Dupe: **{row['Dupe barato']}**")
                    st.markdown(f"[🛒 Comprar dupe]({row['Enlace dupe']})")
                    st.markdown("---")
        else:
            st.warning("No encontramos perfumes con esos criterios. Prueba a cambiar tus respuestas.")
            
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
        filtros &= (df['Notas'].str.contains(selected_nota, case=False, na=False))

    resultados = df[filtros].sort_values(by='Precio (€)').reset_index(drop=True)
    
    total_resultados = len(resultados)
    st.subheader(f"✨ Perfumes encontrados: {total_resultados}")
    
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
st.write("🌸 *YourParfum.com* - Encuentra tu aroma perfecto")

