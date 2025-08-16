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
        
        /* Contenedor de la guía personalizada para centrarla */
        .guide-container {
            width: 70%;
            margin: 0 auto;
            text-align: center;
        }
        
        /* Botón de reinicio */
        .stButton>button {
            border-radius: 0;
            border: 1px solid #000;
            color: #000;
            background-color: transparent;
            font-weight: 500;
            letter-spacing: 0.05em;
            transition: all 0.3s ease;
        }
        .stButton>button:hover {
            background-color: #000;
            color: #fff;
        }

        /* --- BARRA DE BÚSQUEDA --- */
        div.stTextInput>div>div>input {
            border: 1px solid #ccc;
            padding: 10px 15px;
            border-radius: 0;
            box-shadow: none;
        }
        div.stTextInput>div>div>input:focus {
            border-color: #000;
            box-shadow: none;
        }

        /* --- TARJETA DE PRODUCTO REFINADA --- */
        .perfume-card {
            border: none;
            padding: 20px;
            margin-bottom: 20px;
            text-align: center;
            transition: all 0.3s ease-in-out;
            background-color: #f9f9f9;
            border-radius: 8px;
            height: 100%;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }
        .perfume-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 16px rgba(0,0,0,0.08);
        }
        .perfume-card img {
            max-height: 200px;
            margin-bottom: 20px;
            object-fit: contain;
        }
        .perfume-name {
            font-size: 1.1em;
            font-weight: 500;
            color: #000;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }
        .perfume-brand {
            color: #666;
            margin-bottom: 15px;
            font-size: 0.9em;
        }
        
        /* Notas Olfativas */
        .perfume-notes {
            font-size: 0.8em;
            color: #888;
            margin-bottom: 15px;
            font-style: italic;
            flex-grow: 1;
        }

        /* Nueva sección para el dupe, sin fondo y minimalista */
        .dupe-section {
            border-top: 1px solid #eee;
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
        
        .card-buttons {
            margin-top: auto;
        }

        /* --- BOTONES MINIMALISTAS --- */
        a.buy-button {
            display: block; width: 100%; text-align: center; text-decoration: none;
            border-radius: 4px;
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

        /* Estilos de las pestañas */
        .st-emotion-cache-1jicfl2 button {
            border: none;
            border-radius: 0;
            padding: 10px 20px;
            margin-right: 10px;
            background-color: transparent;
            font-weight: 500;
            letter-spacing: 0.05em;
        }
        .st-emotion-cache-1jicfl2 button[aria-selected="true"] {
            border-bottom: 2px solid #000;
            color: #000;
        }
        
        /* Barra de progreso */
        .stProgress > div > div > div > div {
            background-color: #000;
        }

        /* Explicación de la recomendación */
        .recommendation-explanation {
            background-color: #f0f2f6;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 30px;
            border-left: 4px solid #000;
        }
    </style>
    """, unsafe_allow_html=True)

# --- CARGA Y PROCESAMIENTO DE DATOS ---
@st.cache_data
def load_data(file_path):
    try:
        df = pd.read_csv(file_path)
        # Procesar la columna de notas
        df['Notas'] = df['Notas'].astype(str).str.split(',').apply(lambda x: [item.strip().lower() for item in x])
        # Crear una columna de popularidad ficticia para el scoring
        df['Popularidad'] = df.index.map(lambda i: (len(df) - i) * random.uniform(0.8, 1.2))
        return df
    except FileNotFoundError:
        st.error(f"Error: El archivo '{file_path}' no se encontró. Asegúrate de que el archivo está en la misma carpeta.")
        return None

# --- FUNCIÓN PARA MOSTRAR UNA TARJETA DE PERFUME REFINADA ---
def display_perfume_card(perfume):
    notes_formatted = ", ".join([note.capitalize() for note in perfume['Notas']])
    
    html_card = f"""
    <div class="perfume-card">
        <div>
            <img src="{perfume['Imagen (URL)']}" alt="{perfume['Nombre']}">
            <div class="perfume-name">{perfume['Nombre']}</div>
            <div class="perfume-brand">{perfume['Marca']}</div>
            <div class="perfume-notes">{notes_formatted}</div>
        </div>
        <div class="card-buttons">
            <div class="dupe-section">
                <div class="dupe-title">Alternativa de <b>{perfume['Nombre']}</b></div>
                <div class="dupe-name">{perfume['Dupe barato']}</div>
            </div>
            <a href="{perfume['Enlace dupe']}" target="_blank" class="buy-button dupe-button">Ver Dupe</a>
            <a href="{perfume['Enlace original']}" target="_blank" class="buy-button original-button">Ver Original</a>
        </div>
    </div>
    """
    st.markdown(html_card, unsafe_allow_html=True)

# --- ALGORITMO DE PUNTUACIÓN (SCORING) ---
def score_perfumes(df, user_prefs):
    df['score'] = 0.0
    df['score'] = df['Popularidad']

    if 'Tipo de aroma' in user_prefs:
        df.loc[df['Tipo de aroma'] == user_prefs['Tipo de aroma'], 'score'] += 15
    if 'Ocasión' in user_prefs:
        df.loc[df['Ocasión'].str.contains(user_prefs['Ocasión'], case=False), 'score'] += 10
    if 'Intensidad' in user_prefs:
        df.loc[df['Intensidad'] == user_prefs['Intensidad'], 'score'] += 8
    if 'Notas' in user_prefs and user_prefs['Notas']:
        def check_notes(row):
            return sum(1 for note in user_prefs['Notas'] if note.lower() in row['Notas'])
        df['score'] += df.apply(check_notes, axis=1) * 5

    df = df[df['Precio (€)'] <= user_prefs.get('Presupuesto', 1000)].copy()
    return df.sort_values(by='score', ascending=False)

# --- LÓGICA PRINCIPAL DE LA APLICACIÓN ---
def main():
    load_css()
    df = load_data('perfumes_corregido.csv')

    if df is None:
        return

    # --- CABECERA ---
    st.markdown("<h1 style='text-align: center; font-size: 3.5em;'>YourParfum</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; font-weight: 300; margin-top: -20px;'>Encuentra tu aroma perfecto con nuestra IA.</h3>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Responde unas preguntas rápidas y nuestra IA te sugerirá el perfume ideal según tu estilo y ocasión.</p>", unsafe_allow_html=True)
    st.markdown("---")
    
    # Inicializar estado de la sesión
    if 'step' not in st.session_state:
        st.session_state.step = 0
        st.session_state.prefs = {}
        st.session_state.results = pd.DataFrame()

    tab1, tab2 = st.tabs(["✨ Guía Personalizada", "🔎 Explorar Catálogo"])
    
    # --- PESTAÑA 1: GUÍA PERSONALIZADA ---
    with tab1:
        progress_bar = st.progress(0, text="Progreso del cuestionario")
        
        # Lógica del flujo de preguntas
        if st.session_state.step == 0:
            progress_bar.progress(25, text="Paso 1 de 3")
            st.markdown("<p style='text-align: center;'><b>Paso 1:</b> Para empezar, ¿para quién buscas?</p>", unsafe_allow_html=True)
            col1, col2, col3 = st.columns(3)
            with col2:
                selected_genero = st.radio("Género:", ['Hombre', 'Mujer', 'Unisex'], horizontal=True, label_visibility="collapsed")
                if st.button("Siguiente", key="guia_siguiente_1", use_container_width=True):
                    st.session_state.prefs['Género'] = selected_genero
                    st.session_state.step = 1
                    st.rerun()

        elif st.session_state.step == 1:
            progress_bar.progress(50, text="Paso 2 de 3")
            st.markdown("<p style='text-align: center;'><b>Paso 2:</b> Ahora, elige el tipo de aroma y la ocasión.</p>", unsafe_allow_html=True)
            df_genero = df[df['Género'].isin([st.session_state.prefs['Género'], 'Unisex'])].copy()
            
            col1, col2 = st.columns(2)
            with col1:
                st.session_state.prefs['Tipo de aroma'] = st.selectbox("Tipo de aroma:", sorted(df_genero['Tipo de aroma'].unique().tolist()), help="Elige el tipo de fragancia que prefieres.")
            with col2:
                st.session_state.prefs['Ocasión'] = st.selectbox("Ocasión de uso:", sorted(df_genero['Ocasión'].unique().tolist()), help="¿Para qué momento buscas el perfume?")
                
            if st.button("Siguiente", key="guia_siguiente_2", use_container_width=True):
                st.session_state.step = 2
                st.rerun()

        elif st.session_state.step == 2:
            progress_bar.progress(75, text="Paso 3 de 3")
            st.markdown("<p style='text-align: center;'><b>Paso 3:</b> ¿Qué intensidad prefieres y cuál es tu presupuesto?</p>", unsafe_allow_html=True)
            df_genero = df[df['Género'].isin([st.session_state.prefs['Género'], 'Unisex'])].copy()
            
            col1, col2 = st.columns(2)
            with col1:
                st.session_state.prefs['Intensidad'] = st.selectbox("Intensidad preferida:", sorted(df_genero['Intensidad'].unique().tolist()))
            with col2:
                st.session_state.prefs['Presupuesto'] = st.slider("Presupuesto máximo (€):", min_value=10, max_value=int(df['Precio (€)'].max()), value=150, step=5)
            
            st.info("Opcional: puedes escribir notas que te gusten para afinar la búsqueda (separadas por comas).")
            user_notes = st.text_input("Notas (ej. vainilla, limón):", "")
            st.session_state.prefs['Notas'] = [note.strip().lower() for note in user_notes.split(',')] if user_notes else []

            if st.button("✨ Ver mi recomendación ✨", key="guia_finalizar", use_container_width=True):
                df_filtrado = df[df['Género'].isin([st.session_state.prefs['Género'], 'Unisex'])].copy()
                st.session_state.results = score_perfumes(df_filtrado, st.session_state.prefs)
                st.session_state.step = 3
                st.rerun()

        elif st.session_state.step == 3:
            progress_bar.progress(100, text="¡Resultados listos!")
            
            if not st.session_state.results.empty:
                st.header("✨ Tu Recomendación Principal ✨")
                mejor_opcion = st.session_state.results.iloc[0]
                
                # Explicación de la recomendación
                st.markdown(f"""
                <div class="recommendation-explanation">
                    <h4>¿Por qué te recomendamos <b>{mejor_opcion['Nombre']}</b>?</h4>
                    <p>Basado en tus elecciones, este perfume de tipo <strong>{st.session_state.prefs['Tipo de aroma']}</strong> con una intensidad <strong>{st.session_state.prefs['Intensidad']}</strong> es ideal para <strong>{st.session_state.prefs['Ocasión']}</strong>. Las notas de {', '.join(mejor_opcion['Notas'])} encajan perfectamente con tus preferencias.</p>
                </div>
                """, unsafe_allow_html=True)
                
                _, col_main, _ = st.columns([1,2,1])
                with col_main:
                    display_perfume_card(mejor_opcion)

                st.markdown("---")
                st.header("Otras Opciones que te Encantarán")
                
                otras_opciones = st.session_state.results.iloc[1:4]
                if not otras_opciones.empty:
                    cols_other = st.columns(len(otras_opciones))
                    for i, (idx, perfume) in enumerate(otras_opciones.iterrows()):
                        with cols_other[i]:
                            display_perfume_card(perfume)
                
                st.markdown("---")
                if st.button("Reiniciar Guía", key="reiniciar_guia", use_container_width=True):
                    st.session_state.step = 0
                    st.rerun()
            else:
                st.warning("No se encontraron perfumes que coincidan con tu búsqueda. Intenta con otros filtros.")
                if st.button("Reiniciar Guía", key="reiniciar_guia_fail", use_container_width=True):
                    st.session_state.step = 0
                    st.rerun()

    # --- PESTAÑA 2: EXPLORAR CATÁLOGO ---
    with tab2:
        st.header("Explora todo nuestro catálogo")
        
        selected_genero_catalogo = st.radio("PARA QUIÉN BUSCAS:", ['Hombre', 'Mujer', 'Unisex'], horizontal=True, key='genero_catalogo')
        df_catalogo = df[df['Género'].isin([selected_genero_catalogo, 'Unisex'])].copy()

        search_term = st.text_input('Busca por nombre, marca o notas olfativas:', '').strip().lower()
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            selected_marca = st.selectbox("Marca:", ['Todas'] + sorted(df_catalogo['Marca'].unique().tolist()))
        with col2:
            selected_tipo = st.selectbox("Tipo de aroma:", ['Cualquiera'] + sorted(df_catalogo['Tipo de aroma'].unique().tolist()))
        with col3:
            selected_intensidad = st.selectbox("Intensidad:", ['Cualquiera'] + sorted(df_catalogo['Intensidad'].unique().tolist()))
        with col4:
            selected_ocasion = st.selectbox("Ocasión:", ['Cualquiera'] + sorted(df_catalogo['Ocasión'].unique().tolist()))
        
        filtros = (df_catalogo['Género'].isin([selected_genero_catalogo, 'Unisex']))
        if selected_marca != 'Todas': filtros &= (df_catalogo['Marca'] == selected_marca)
        if selected_tipo != 'Cualquiera': filtros &= (df_catalogo['Tipo de aroma'] == selected_tipo)
        if selected_intensidad != 'Cualquiera': filtros &= (df_catalogo['Intensidad'] == selected_intensidad)
        if selected_ocasion != 'Cualquiera': filtros &= (df_catalogo['Ocasión'] == selected_ocasion)

        if search_term:
            filtros &= df_catalogo.apply(lambda row: 
                search_term in str(row['Nombre']).lower() or 
                search_term in str(row['Marca']).lower() or 
                any(search_term in note.lower() for note in row['Notas']), axis=1)

        resultados = df_catalogo[filtros]
        st.markdown("---")
        st.markdown(f"**Perfumes encontrados: {len(resultados)}**")

        if not resultados.empty:
            for i in range(0, len(resultados), 3):
                cols = st.columns(3)
                for j, (idx, row) in enumerate(resultados.iloc[i:i+3].iterrows()):
                    with cols[j]:
                        display_perfume_card(row)
        else:
            st.warning("No hay perfumes que coincidan con tu búsqueda. Intenta con otros filtros.")
    
    # --- AVISO DE PRIVACIDAD Y COOKIES ---
    with st.expander("Información sobre la IA y la fuente de datos"):
        st.write("""
        **¿Cómo funciona nuestra IA?**
        
        Nuestro sistema de recomendación utiliza un algoritmo que puntúa cada perfume en función de tus preferencias. 
        Consideramos el tipo de aroma, la ocasión, la intensidad, tus notas preferidas y el presupuesto para encontrar la mejor coincidencia.
        
        **Fuente de datos:**
        
        La base de datos de perfumes ha sido creada a partir de información pública de marcas y distribuidores.
        """)

    # --- PIE DE PÁGINA ---
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: grey;">
        <p>Creado por Miguel Poza con 🖤</p>
        <p><a href="#">Política de Privacidad</a> | <a href="#">Aviso de Cookies</a></p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
        
