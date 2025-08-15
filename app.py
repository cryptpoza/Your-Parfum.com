import pandas as pd
import streamlit as st
import random

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(
    page_title="YourParfum",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# --- ESTILOS CSS PARA UN DISEÑO PROFESIONAL Y MINIMALISTA ---
def load_css():
    st.markdown("""
    <style>
        /* --- FUENTES Y COLORES BASE --- */
        html, body, [class*="st-"] {
            font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
            background-color: #FFFFFF; /* Fondo blanco puro */
            color: #1a1a1a; /* Negro suave para texto */
        }

        /* --- TÍTULOS Y CABECERAS --- */
        h1, h2, h3 {
            font-family: 'Garamond', 'Georgia', serif; /* Fuente más elegante */
            font-weight: 400;
            color: #000000;
        }
        
        /* --- LAYOUT PRINCIPAL --- */
        .main .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
            padding-left: 5rem;
            padding-right: 5rem;
        }

        /* --- TARJETA DE PRODUCTO REFINADA --- */
        .perfume-card {
            border: none; /* Sin bordes para un look más limpio */
            padding: 10px;
            margin-bottom: 20px;
            text-align: center;
        }
        .perfume-card img {
            max-height: 200px;
            margin-bottom: 20px;
        }
        .perfume-name {
            font-size: 1.1em;
            font-weight: 500; /* Letra más fina */
            color: #000;
            text-transform: uppercase; /* MAYÚSCULAS como en Zara */
            letter-spacing: 0.05em;
        }
        .perfume-brand {
            color: #666;
            margin-bottom: 15px;
            font-size: 0.9em;
        }
        
        /* Estilo refinado para el precio */
        .perfume-price {
            font-size: 1.1em;
            font-weight: 400;
            color: #000;
            margin-bottom: 20px;
        }

        /* Nueva sección para el dupe, sin fondo y minimalista */
        .dupe-section {
            border-top: 1px solid #eee; /* Un separador sutil */
            padding-top: 15px;
            margin-top: 20px;
        }
        .dupe-title {
            font-size: 0.8em;
            color: #888;
            text-transform: uppercase;
            margin-bottom: 5px;
        }
        .dupe-name {
            font-weight: 500;
            color: #000;
            margin-bottom: 10px;
        }

        /* --- BOTONES MINIMALISTAS --- */
        a.buy-button {
            display: block; width: 100%; text-align: center; text-decoration: none;
            border-radius: 0; /* Sin bordes redondeados */
            padding: 12px 0; margin-top: 8px; font-weight: 500;
            transition: all 0.3s ease;
            letter-spacing: 0.05em;
        }
        a.original-button {
            border: 1px solid #000;
            background-color: transparent;
            color: #000;
        }
        a.original-button:hover {
            background-color: #000;
            color: #fff;
        }
        a.dupe-button {
            border: 1px solid #000;
            background-color: #000;
            color: #fff;
        }
        a.dupe-button:hover {
            background-color: #333;
            border-color: #333;
        }
    </style>
    """, unsafe_allow_html=True)

# --- CARGA DE DATOS (CON CACHÉ PARA MAYOR VELOCIDAD) ---
@st.cache_data
def load_data(file_path):
    try:
        df = pd.read_csv(file_path)
        # Asegurarse de que las notas sean tratadas como strings antes de dividir
        df['Notas'] = df['Notas'].astype(str).str.split(',')
        return df
    except FileNotFoundError:
        st.error(f"Error: El archivo '{file_path}' no se encontró. Asegúrate de que el archivo está en el directorio correcto.")
        return None

# --- FUNCIÓN PARA MOSTRAR UNA TARJETA DE PERFUME ---
def display_perfume_card(perfume):
    with st.container():
        # Usamos st.markdown para tener control total con HTML y CSS
        st.markdown(f"""
        <div class="perfume-card">
            <img src="{perfume['Imagen (URL)']}" alt="{perfume['Nombre']}">
            <div class="perfume-name">{perfume['Nombre']}</div>
            <div class="perfume-brand">{perfume['Marca']}</div>
            
            <div class="perfume-price">{perfume['Precio (€)']} €</div>
            
            <a href="{perfume['Enlace original']}" target="_blank" class="buy-button original-button">Comprar Original</a>
            
            <div class="dupe-section">
                <div class="dupe-title">Alternativa / Dupe</div>
                <div class="dupe-name">{perfume['Dupe barato']}</div>
                <a href="{perfume['Enlace dupe']}" target="_blank" class="buy-button dupe-button">Comprar Alternativa</a>
            </div>
        </div>
        """, unsafe_allow_html=True)


# --- LÓGICA PRINCIPAL DE LA APLICACIÓN ---
def main():
    load_css()
    df = load_data('perfumes_corregido.csv')

    if df is None:
        return

    # --- CABECERA ---
    st.markdown("<h1 style='text-align: center; font-size: 3.5em;'>YourParfum</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; font-weight: 300; margin-top: -20px;'>Encuentra tu aroma perfecto.</h3>", unsafe_allow_html=True)
    st.markdown("---")

    # --- SELECCIÓN DE GÉNERO Y MODO ---
    cols_header = st.columns(2)
    with cols_header[0]:
        selected_genero = st.radio("PARA QUIÉN BUSCAS:", ['Hombre', 'Mujer', 'Unisex'], horizontal=True, key='genero')
    with cols_header[1]:
        modo = st.radio("MODO DE BÚSQUEDA:", ("Guía Personalizada", "Explorar Catálogo"), horizontal=True, key='modo')
    
    st.markdown("---")
    
    # Filtrar dataframe por género seleccionado
    df_genero = df[df['Género'].isin([selected_genero, 'Unisex'])].copy()

    # --- MODO: GUÍA PERSONALIZADA ---
    if modo == "Guía Personalizada":
        st.header("Guía Personalizada")
        
        # Opciones para los filtros
        tipos_aroma = sorted(df_genero['Tipo de aroma'].unique().tolist())
        ocasiones = sorted(df_genero['Ocasión'].unique().tolist())
        intensidades = sorted(df_genero['Intensidad'].unique().tolist())

        with st.form("guia_form"):
            col1, col2, col3 = st.columns(3)
            with col1:
                aroma_preferido = st.selectbox("Tipo de aroma que te atrae:", tipos_aroma)
            with col2:
                ocasion_uso = st.selectbox("Ocasión de uso principal:", ocasiones)
            with col3:
                intensidad_preferida = st.selectbox("Intensidad preferida:", intensidades)
            
            presupuesto = st.slider("Presupuesto máximo (€):", min_value=df_genero['Precio (€)'].min(), max_value=df_genero['Precio (€)'].max(), value=150.0, step=5.0)
            
            submitted = st.form_submit_button("✨ ¡Encontrar mi perfume!")

        if submitted:
            st.markdown("---")
            st.markdown("<h2 style='text-align: center;'>Tu recomendación ideal</h2>", unsafe_allow_html=True)
            
            # Lógica de búsqueda mejorada
            resultados = df_genero[
                (df_genero['Tipo de aroma'] == aroma_preferido) &
                (df_genero['Ocasión'] == ocasion_uso) &
                (df_genero['Intensidad'] == intensidad_preferida) &
                (df_genero['Precio (€)'] <= presupuesto)
            ]
            # Si no hay resultados, buscar con menos criterios
            if resultados.empty:
                resultados = df_genero[
                    (df_genero['Tipo de aroma'] == aroma_preferido) &
                    (df_genero['Ocasión'] == ocasion_uso) &
                    (df_genero['Precio (€)'] <= presupuesto)
                ]
            
            if not resultados.empty:
                # Mostrar hasta 3 recomendaciones en columnas
                num_resultados = min(3, len(resultados))
                cols = st.columns(num_resultados)
                for i, (_, row) in enumerate(resultados.sample(num_resultados).iterrows()):
                    with cols[i]:
                        display_perfume_card(row)
            else:
                st.warning("No hemos encontrado una fragancia ideal. Prueba a ajustar los filtros o explora estas opciones populares:")
                # Mostrar 3 opciones populares del género si falla la búsqueda
                cols = st.columns(3)
                for i, (_, row) in enumerate(df_genero.sample(3).iterrows()):
                    with cols[i]:
                        display_perfume_card(row)

    # --- MODO: EXPLORAR CATÁLOGO ---
    elif modo == "Explorar Catálogo":
        st.header("Explorar Catálogo Completo")

        # Columnas para los filtros
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            marcas = ['Todas'] + sorted(df_genero['Marca'].unique().tolist())
            selected_marca = st.selectbox("Marca:", marcas)
        with col2:
            tipos_aroma = ['Cualquiera'] + sorted(df_genero['Tipo de aroma'].unique().tolist())
            selected_tipo = st.selectbox("Tipo de aroma:", tipos_aroma)
        with col3:
            intensidades = ['Cualquiera'] + sorted(df_genero['Intensidad'].unique().tolist())
            selected_intensidad = st.selectbox("Intensidad:", intensidades)
        with col4:
            ocasiones = ['Cualquiera'] + sorted(df_genero['Ocasión'].unique().tolist())
            selected_ocasion = st.selectbox("Ocasión:", ocasiones)
        
        # Aplicar filtros
        filtros = (df_genero['Género'].isin([selected_genero, 'Unisex']))
        if selected_marca != 'Todas': filtros &= (df_genero['Marca'] == selected_marca)
        if selected_tipo != 'Cualquiera': filtros &= (df_genero['Tipo de aroma'] == selected_tipo)
        if selected_intensidad != 'Cualquiera': filtros &= (df_genero['Intensidad'] == selected_intensidad)
        if selected_ocasion != 'Cualquiera': filtros &= (df_genero['Ocasión'] == selected_ocasion)

        resultados = df_genero[filtros]

        st.markdown("---")
        st.markdown(f"**Resultados encontrados: {len(resultados)}**")

        if not resultados.empty:
            # Paginación y visualización en cuadrícula
            resultados_por_pagina = 9
            total_paginas = (len(resultados) - 1) // resultados_por_pagina + 1
            if 'page' not in st.session_state: st.session_state.page = 1
            
            # Controles de paginación
            pag_col1, pag_col2, pag_col3 = st.columns([1,2,1])
            with pag_col1:
                if st.button('⬅️ Anterior') and st.session_state.page > 1:
                    st.session_state.page -= 1
            with pag_col3:
                if st.button('Siguiente ➡️') and st.session_state.page < total_paginas:
                    st.session_state.page += 1
            with pag_col2:
                 st.write(f"Página {st.session_state.page} de {total_paginas}")

            # Mostrar resultados de la página actual
            start_idx = (st.session_state.page - 1) * resultados_por_pagina
            end_idx = start_idx + resultados_por_pagina
            
            for i in range(start_idx, end_idx, 3):
                cols = st.columns(3)
                for j, (idx, row) in enumerate(resultados.iloc[i:i+3].iterrows()):
                    with cols[j]:
                        display_perfume_card(row)
        else:
            st.warning("No hay perfumes que coincidan con tu búsqueda. Intenta con otros filtros.")

    # --- PIE DE PÁGINA ---
    st.markdown("---")
    st.markdown('<p style="text-align: center; color: grey;">Creado por Miguel Poza con 🖤</p>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
    
