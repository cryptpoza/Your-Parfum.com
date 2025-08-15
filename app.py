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
        :root {
            --primary-color: #1a1a1a;
            --secondary-color: #4a4a4a;
            --accent-color: #d4af37;
            --light-bg: #f8f8f8;
            --card-shadow: 0 4px 12px rgba(0,0,0,0.05);
        }
        
        html, body, [class*="st-"] {
            font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
            background-color: #FFFFFF;
            color: var(--primary-color);
        }

        /* --- TÍTULOS Y CABECERAS --- */
        h1, h2, h3, h4 {
            font-family: 'Garamond', 'Georgia', serif;
            font-weight: 500;
            color: var(--primary-color);
            letter-spacing: 0.02em;
        }
        
        h1 {
            font-size: 3.5rem;
            margin-bottom: 0.5rem;
        }
        
        h2 {
            font-size: 2.2rem;
            margin-bottom: 1.5rem;
        }
        
        h3 {
            font-size: 1.8rem;
            margin-bottom: 1rem;
        }
        
        /* --- LAYOUT PRINCIPAL --- */
        .main .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
            padding-left: 3rem;
            padding-right: 3rem;
            max-width: 1600px;
        }
        
        /* Contenedor de la guía personalizada para centrarla */
        .guide-container {
            width: 80%;
            margin: 0 auto;
            text-align: center;
            padding: 2rem 0;
        }
        
        /* Botones */
        .stButton>button {
            border-radius: 0;
            border: 1px solid var(--primary-color);
            color: var(--primary-color);
            background-color: transparent;
            font-weight: 500;
            letter-spacing: 0.05em;
            transition: all 0.3s ease;
            padding: 10px 24px;
        }
        .stButton>button:hover {
            background-color: var(--primary-color);
            color: #fff;
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }

        /* --- BARRA DE BÚSQUEDA --- */
        div.stTextInput>div>div>input {
            border: 1px solid #ddd;
            padding: 12px 18px;
            border-radius: 0;
            box-shadow: none;
            font-size: 1rem;
        }
        div.stTextInput>div>div>input:focus {
            border-color: var(--accent-color);
            box-shadow: 0 0 0 2px rgba(212, 175, 55, 0.2);
        }

        /* --- TARJETA DE PRODUCTO REFINADA --- */
        .perfume-card {
            border: none;
            padding: 25px;
            margin-bottom: 25px;
            text-align: center;
            transition: all 0.3s ease-in-out;
            background-color: #fff;
            border-radius: 8px;
            height: 100%;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            box-shadow: var(--card-shadow);
            border: 1px solid #eee;
        }
        .perfume-card:hover {
            transform: translateY(-8px);
            box-shadow: 0 12px 24px rgba(0,0,0,0.1);
            border-color: var(--accent-color);
        }
        .perfume-card img {
            max-height: 250px;
            margin-bottom: 20px;
            object-fit: contain;
            transition: transform 0.3s ease;
        }
        .perfume-card:hover img {
            transform: scale(1.05);
        }
        .perfume-name {
            font-size: 1.3rem;
            font-weight: 600;
            color: var(--primary-color);
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 5px;
        }
        .perfume-brand {
            color: var(--secondary-color);
            margin-bottom: 15px;
            font-size: 0.95rem;
            font-weight: 500;
        }
        
        .price-tag {
            background-color: var(--accent-color);
            color: white;
            padding: 4px 10px;
            font-size: 0.9rem;
            font-weight: 500;
            display: inline-block;
            margin-bottom: 15px;
        }
        
        /* Notas Olfativas */
        .perfume-notes {
            font-size: 0.9rem;
            color: var(--secondary-color);
            margin-bottom: 15px;
            line-height: 1.6;
            flex-grow: 1;
        }

        /* Nueva sección para el dupe */
        .dupe-section {
            border-top: 1px solid #eee;
            padding-top: 15px;
            margin-top: 15px;
        }
        .dupe-title {
            font-size: 0.85rem;
            color: var(--secondary-color);
            text-transform: uppercase;
            margin-bottom: 5px;
            letter-spacing: 0.05em;
        }
        .dupe-name {
            font-weight: 600;
            color: var(--primary-color);
            margin-bottom: 10px;
            font-size: 1.05rem;
        }
        
        .card-buttons {
            margin-top: auto;
            display: flex;
            flex-direction: column;
            gap: 10px;
        }

        /* --- BOTONES MINIMALISTAS --- */
        a.buy-button {
            display: block; 
            width: 100%; 
            text-align: center; 
            text-decoration: none;
            border-radius: 4px;
            padding: 12px 0; 
            font-weight: 500;
            transition: all 0.3s ease;
            letter-spacing: 0.05em;
            font-size: 0.9rem;
        }
        a.original-button {
            border: 1px solid var(--primary-color);
            background-color: transparent;
            color: var(--primary-color);
        }
        a.original-button:hover {
            background-color: var(--primary-color);
            color: #fff;
        }
        a.dupe-button {
            border: 1px solid var(--accent-color);
            background-color: var(--accent-color);
            color: #fff;
        }
        a.dupe-button:hover {
            background-color: #c19d2c;
            border-color: #c19d2c;
        }

        /* Estilos de las pestañas */
        .stTabs [role="tablist"] {
            gap: 15px;
            margin-bottom: 2rem;
            border-bottom: 1px solid #eee;
        }
        .stTabs [role="tab"] {
            border: none;
            border-radius: 0;
            padding: 12px 25px;
            background-color: transparent;
            font-weight: 500;
            letter-spacing: 0.05em;
            color: var(--secondary-color);
            transition: all 0.3s ease;
        }
        .stTabs [role="tab"][aria-selected="true"] {
            color: var(--primary-color);
            font-weight: 600;
            border-bottom: 3px solid var(--accent-color);
            background-color: transparent;
        }
        .stTabs [role="tab"]:not([aria-selected="true"]):hover {
            color: var(--accent-color);
        }
        
        /* Barra de progreso */
        .stProgress > div > div > div > div {
            background-color: var(--accent-color);
        }

        /* Explicación de la recomendación */
        .recommendation-explanation {
            background-color: #f9f5eb;
            padding: 25px;
            border-radius: 8px;
            margin-bottom: 30px;
            border-left: 4px solid var(--accent-color);
            box-shadow: var(--card-shadow);
        }
        
        .recommendation-explanation h4 {
            color: var(--primary-color);
            margin-top: 0;
            font-size: 1.4rem;
        }
        
        /* Filtros con estilo de tarjeta */
        .filter-card {
            background-color: #fff;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 20px;
            box-shadow: var(--card-shadow);
            border: 1px solid #eee;
        }
        
        /* Botones de género */
        .gender-buttons {
            display: flex;
            justify-content: center;
            gap: 15px;
            margin-top: 20px;
            margin-bottom: 30px;
        }
        .gender-button {
            flex: 1;
            max-width: 200px;
            padding: 15px;
            text-align: center;
            border: 1px solid #ddd;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.3s ease;
            background-color: #fff;
        }
        .gender-button:hover {
            border-color: var(--accent-color);
            transform: translateY(-3px);
        }
        .gender-button.selected {
            border: 2px solid var(--accent-color);
            background-color: #fdf8e8;
        }
        .gender-button h3 {
            margin: 0;
            font-size: 1.1rem;
            color: var(--primary-color);
        }
        
        /* Detalles del producto */
        .product-detail {
            display: flex;
            gap: 40px;
            margin-top: 30px;
        }
        .product-image {
            flex: 1;
            max-width: 350px;
        }
        .product-info {
            flex: 2;
        }
        .pyramid-container {
            display: flex;
            gap: 20px;
            margin-top: 20px;
        }
        .pyramid-section {
            flex: 1;
            background-color: #f9f5eb;
            padding: 20px;
            border-radius: 8px;
        }
        .pyramid-title {
            font-weight: 600;
            color: var(--accent-color);
            text-transform: uppercase;
            font-size: 0.9rem;
            margin-bottom: 10px;
            letter-spacing: 0.05em;
        }
        
        /* Estilo para chips */
        .note-chip {
            display: inline-block;
            padding: 5px 12px;
            background-color: #f0f2f6;
            border-radius: 20px;
            margin: 5px;
            font-size: 0.85rem;
        }
        
        /* Responsive */
        @media (max-width: 768px) {
            .main .block-container {
                padding-left: 1.5rem;
                padding-right: 1.5rem;
            }
            .product-detail {
                flex-direction: column;
            }
            .product-image {
                max-width: 100%;
            }
            .pyramid-container {
                flex-direction: column;
            }
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
def display_perfume_card(perfume, show_details=False):
    notes_formatted = ", ".join([note.capitalize() for note in perfume['Notas']])
    
    if show_details:
        # Vista detallada del perfume
        st.markdown(f"<div class='perfume-name'>{perfume['Nombre']}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='perfume-brand'>{perfume['Marca']}</div>", unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 2])
        with col1:
            st.image(perfume['Imagen (URL)'], use_column_width=True)
        with col2:
            st.markdown(f"<div class='price-tag'>€{perfume['Precio (€)']}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='perfume-notes'><b>Notas:</b> {notes_formatted}</div>", unsafe_allow_html=True)
            st.markdown(f"<div><b>Intensidad:</b> {perfume['Intensidad']}</div>", unsafe_allow_html=True)
            st.markdown(f"<div><b>Ocasiones:</b> {perfume['Ocasión']}</div>", unsafe_allow_html=True)
            st.markdown(f"<div><b>Tipo de aroma:</b> {perfume['Tipo de aroma']}</div>", unsafe_allow_html=True)
            
            # Pirámide olfativa (simulada)
            st.markdown("<div class='pyramid-title'>Pirámide Olfativa</div>", unsafe_allow_html=True)
            col_top, col_mid, col_base = st.columns(3)
            with col_top:
                st.markdown("<div class='pyramid-section'><div class='pyramid-title'>Notas de Salida</div>", unsafe_allow_html=True)
                st.write(", ".join(perfume['Notas'][:2]).capitalize())
            with col_mid:
                st.markdown("<div class='pyramid-section'><div class='pyramid-title'>Notas de Corazón</div>", unsafe_allow_html=True)
                st.write(", ".join(perfume['Notas'][2:5]).capitalize())
            with col_base:
                st.markdown("<div class='pyramid-section'><div class='pyramid-title'>Notas de Fondo</div>", unsafe_allow_html=True)
                st.write(", ".join(perfume['Notas'][5:]).capitalize() if len(perfume['Notas']) > 5 else "N/A")
            
            # Botones de compra
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"<a href='{perfume['Enlace dupe']}' target='_blank' class='buy-button dupe-button'>Ver Alternativa</a>", unsafe_allow_html=True)
            with col2:
                st.markdown(f"<a href='{perfume['Enlace original']}' target='_blank' class='buy-button original-button'>Ver Original</a>", unsafe_allow_html=True)
            
            # Botón para volver
            if st.button("Volver al Catálogo", use_container_width=True):
                st.session_state.show_details = False
                st.rerun()
    else:
        # Tarjeta normal
        html_card = f"""
        <div class="perfume-card" onclick="window.location.href='?perfume={perfume['Nombre']}'">
            <div>
                <img src="{perfume['Imagen (URL)']}" alt="{perfume['Nombre']}">
                <div class="perfume-name">{perfume['Nombre']}</div>
                <div class="perfume-brand">{perfume['Marca']}</div>
                <div class="price-tag">€{perfume['Precio (€)']}</div>
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

# --- FUNCIÓN PARA BÚSQUEDA AUTOMÁTICA ---
def get_search_options(df):
    options = []
    # Opciones de nombres de perfumes
    for nombre in df['Nombre'].unique():
        options.append(f"👑 {nombre}")
    
    # Opciones de marcas
    for marca in df['Marca'].unique():
        options.append(f"🏷️ {marca}")
    
    # Opciones de notas
    all_notes = set()
    for notes_list in df['Notas']:
        all_notes.update(notes_list)
    for note in all_notes:
        options.append(f"🌸 {note.capitalize()}")
    
    return options

# --- LÓGICA PRINCIPAL DE LA APLICACIÓN ---
def main():
    load_css()
    df = load_data('perfumes_corregido.csv')

    if df is None:
        return

    # Manejo de estado para vista de detalles
    if 'show_details' not in st.session_state:
        st.session_state.show_details = False
        st.session_state.selected_perfume = None
    
    # Verificar si se solicitó un perfume específico en la URL
    query_params = st.query_params
    if 'perfume' in query_params:
        perfume_name = query_params['perfume']
        perfume = df[df['Nombre'] == perfume_name]
        if not perfume.empty:
            st.session_state.show_details = True
            st.session_state.selected_perfume = perfume.iloc[0]

    # --- CABECERA ---
    st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
    st.markdown("<h1>YourParfum</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='font-weight: 300; margin-top: -20px;'>Encuentra tu aroma perfecto con nuestra IA</h3>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Responde unas preguntas rápidas y nuestra IA te sugerirá el perfume ideal según tu estilo y ocasión.</p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("---")
    
    # Inicializar estado de la sesión
    if 'step' not in st.session_state:
        st.session_state.step = 0
        st.session_state.prefs = {}
        st.session_state.results = pd.DataFrame()

    # Vista de detalles del perfume
    if st.session_state.show_details and st.session_state.selected_perfume is not None:
        display_perfume_card(st.session_state.selected_perfume, show_details=True)
        return

    tab1, tab2 = st.tabs(["✨ Guía Personalizada", "🔎 Explorar Catálogo"])
    
    # --- PESTAÑA 1: GUÍA PERSONALIZADA ---
    with tab1:
        # Lógica del flujo de preguntas
        if st.session_state.step == 0:
            progress_bar = st.progress(0, text="Progreso del cuestionario")
            progress_bar.progress(25, text="Paso 1 de 3")
            st.markdown(
                "<p style='text-align: center; font-size: 1.2rem;'>"
                "<b>¡Bienvenido!</b> Empecemos a encontrar tu perfume ideal en 3 sencillos pasos"
                "</p>", 
                unsafe_allow_html=True
            )
            
            st.markdown("<div class='gender-buttons'>", unsafe_allow_html=True)
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("Hombre", key="hombre", use_container_width=True):
                    st.session_state.prefs['Género'] = 'Hombre'
                    st.session_state.step = 1
                    st.rerun()
            with col2:
                if st.button("Mujer", key="mujer", use_container_width=True):
                    st.session_state.prefs['Género'] = 'Mujer'
                    st.session_state.step = 1
                    st.rerun()
            with col3:
                if st.button("Unisex", key="unisex", use_container_width=True):
                    st.session_state.prefs['Género'] = 'Unisex'
                    st.session_state.step = 1
                    st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

        elif st.session_state.step == 1:
            progress_bar = st.progress(0, text="P
