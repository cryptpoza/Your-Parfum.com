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

# --- ESTILOS CSS MEJORADOS ---
def load_css():
    st.markdown("""
    <style>
        /* --- FUENTES Y COLORES BASE --- */
        html, body, [class*="st-"] {
            font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
            background-color: #FFFFFF;
            color: #1a1a1a;
        }

        /* --- TÍTULOS Y CABECERAS --- */
        h1, h2, h3 {
            font-family: 'Garamond', 'Georgia', serif;
            font-weight: 400;
            color: #000000;
        }
        
        /* --- MEJORAS DE DISEÑO --- */
        .perfume-card img {
            max-height: 250px;  /* Imágenes más grandes */
        }
        
        .guide-container {
            width: 70%;
            margin: 0 auto;
            text-align: center;
        }
        
        /* Botones de selección estilo tarjeta */
        .option-card {
            border: 1px solid #ddd;
            padding: 15px;
            border-radius: 8px;
            text-align: center;
            cursor: pointer;
            transition: all 0.3s;
            margin-bottom: 10px;
        }
        .option-card:hover {
            border-color: #000;
            background-color: #f9f9f9;
        }
        .option-card.selected {
            border: 2px solid #000;
            background-color: #fff;
        }
        
        /* Mensaje de transparencia IA */
        .ai-transparency {
            background-color: #f8f9fa;
            border-left: 4px solid #4a90e2;
            padding: 15px;
            margin: 20px 0;
            border-radius: 4px;
            font-size: 0.9em;
        }
        
        /* Ocultar elementos de Streamlit */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .stDeployButton {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- CARGA Y PROCESAMIENTO DE DATOS ---
@st.cache_data
def load_data(file_path):
    try:
        df = pd.read_csv(file_path)
        df['Notas'] = df['Notas'].astype(str).str.split(',').apply(lambda x: [item.strip().lower() for item in x])
        df['Popularidad'] = df.index.map(lambda i: (len(df) - i) * random.uniform(0.8, 1.2))
        return df
    except FileNotFoundError:
        st.error(f"Error: Archivo no encontrado. Verifica que '{file_path}' esté en el directorio.")
        return None

# --- FUNCIÓN PARA MOSTRAR PERFUME ---
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
    """
    
    if pd.notna(perfume['Dupe barato']):
        html_card += f"""
            <div class="dupe-section">
                <div class="dupe-title">Alternativa de <b>{perfume['Nombre']}</b></div>
                <div class="dupe-name">{perfume['Dupe barato']}</div>
            </div>
            <a href="{perfume['Enlace dupe']}" target="_blank" class="buy-button dupe-button">Ver Dupe</a>
        """
    
    html_card += f"""
            <a href="{perfume['Enlace original']}" target="_blank" class="buy-button original-button">Ver Original</a>
        </div>
    </div>
    """
    st.markdown(html_card, unsafe_allow_html=True)

# --- ALGORITMO DE RECOMENDACIÓN ---
def score_perfumes(df, user_prefs):
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

# --- LÓGICA PRINCIPAL ---
def main():
    load_css()
    df = load_data('perfumes_corregido.csv')

    if df is None:
        return

    # --- CABECERA MEJORADA ---
    st.markdown("<h1 style='text-align: center; font-size: 3.5em;'>YourParfum</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; font-weight: 300; margin-top: -20px;'>Tu aroma perfecto, descubierto por IA</h3>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>¡Bienvenido! Descubre tu perfume ideal en 3 sencillos pasos.</p>", unsafe_allow_html=True)
    st.markdown("---")
    
    # Estado de sesión
    if 'step' not in st.session_state:
        st.session_state.step = 0
        st.session_state.prefs = {}
        st.session_state.results = pd.DataFrame()

    tab1, tab2 = st.tabs(["✨ Guía Personalizada", "🔎 Explorar Catálogo"])
    
    # --- GUÍA PERSONALIZADA MEJORADA ---
    with tab1:
        progress_bar = st.progress(0, text="Progreso del cuestionario")
        
        if st.session_state.step == 0:
            progress_bar.progress(25, text="Paso 1 de 3")
            st.markdown("<p style='text-align: center;'><b>Paso 1:</b> ¡Empecemos! ¿Para quién buscas perfume?</p>", unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns(3)
            options = ['Hombre', 'Mujer', 'Unisex']
            
            for i, option in enumerate(options):
                with [col1, col2, col3][i]:
                    if st.button(option, key=f"gender_{option}", use_container_width=True, 
                                help=f"Selecciona perfumes para {option}"):
                        st.session_state.prefs['Género'] = option
                        st.session_state.step = 1
                        st.rerun()

        elif st.session_state.step == 1:
            progress_bar.progress(50, text="Paso 2 de 3")
            st.markdown("<p style='text-align: center;'><b>Paso 2:</b> Selecciona tus preferencias de aroma</p>", unsafe_allow_html=True)
            df_genero = df[df['Género'].isin([st.session_state.prefs['Género'], 'Unisex'])].copy()
            
            # Selector de tipo de aroma con tarjetas
            st.markdown("**Tipo de aroma:**")
            tipos = sorted(df_genero['Tipo de aroma'].unique().tolist())
            cols = st.columns(len(tipos))
            for i, tipo in enumerate(tipos):
                with cols[i]:
                    st.markdown(f'<div class="option-card" onclick="this.classList.toggle(\'selected\')">{tipo}</div>', 
                               unsafe_allow_html=True)
                    if st.button(tipo, key=f"tipo_{tipo}", use_container_width=True):
                        st.session_state.prefs['Tipo de aroma'] = tipo
            
            # Selector de ocasión con tarjetas
            if 'Tipo de aroma' in st.session_state.prefs:
                st.markdown("**Ocasión de uso:**")
                ocasiones = sorted(df_genero['Ocasión'].unique().tolist())
                cols_ocasion = st.columns(len(ocasiones))
                for i, ocasion in enumerate(ocasiones):
                    with cols_ocasion[i]:
                        st.markdown(f'<div class="option-card" onclick="this.classList.toggle(\'selected\')">{ocasion}</div>', 
                                   unsafe_allow_html=True)
                        if st.button(ocasion, key=f"ocasion_{ocasion}", use_container_width=True):
                            st.session_state.prefs['Ocasión'] = ocasion
            
            # Botón de siguiente
            if 'Ocasión' in st.session_state.prefs:
                if st.button("Siguiente", key="guia_siguiente_2", use_container_width=True):
                    st.session_state.step = 2
                    st.rerun()

        elif st.session_state.step == 2:
            progress_bar.progress(75, text="Paso 3 de 3")
            st.markdown("<p style='text-align: center;'><b>Paso 3:</b> Preferencias finales</p>", unsafe_allow_html=True)
            df_genero = df[df['Género'].isin([st.session_state.prefs['Género'], 'Unisex'])].copy()
            
            # Intensidad con tarjetas
            st.markdown("**Intensidad preferida:**")
            intensidades = sorted(df_genero['Intensidad'].unique().tolist())
            cols_intensidad = st.columns(len(intensidades))
            for i, intensidad in enumerate(intensidades):
                with cols_intensidad[i]:
                    st.markdown(f'<div class="option-card" onclick="this.classList.toggle(\'selected\')">{intensidad}</div>', 
                               unsafe_allow_html=True)
                    if st.button(intensidad, key=f"intensidad_{intensidad}", use_container_width=True):
                        st.session_state.prefs['Intensidad'] = intensidad
            
            # Presupuesto
            if 'Intensidad' in st.session_state.prefs:
                st.markdown("**Presupuesto máximo (€):**")
                max_price = int(df['Precio (€)'].max())
                st.session_state.prefs['Presupuesto'] = st.slider(
                    "", min_value=10, max_value=max_price, 
                    value=min(150, max_price), step=5, 
                    label_visibility="collapsed"
                )
                
                # Notas con autocompletar sugerido
                st.markdown("**Notas preferidas (opcional):**")
                all_notes = set([note for sublist in df['Notas'] for note in sublist])
                user_notes = st.text_input("Ej: vainilla, limón, madera", "", 
                                          help="Escribe tus notas favoritas separadas por comas")
                st.session_state.prefs['Notas'] = [note.strip().lower() for note in user_notes.split(',')] if user_notes else []

                if st.button("✨ Encontrar mi perfume ideal ✨", key="guia_finalizar", use_container_width=True):
                    df_filtrado = df[df['Género'].isin([st.session_state.prefs['Género'], 'Unisex'])].copy()
                    st.session_state.results = score_perfumes(df_filtrado, st.session_state.prefs)
                    st.session_state.step = 3
                    st.rerun()

        elif st.session_state.step == 3:
            progress_bar.progress(100, text="¡Resultados listos!")
            
            if not st.session_state.results.empty:
                st.header("✨ Tu Recomendación Principal ✨")
                mejor_opcion = st.session_state.results.iloc[0]
                
                # Explicación IA
                st.markdown(f"""
                <div class="recommendation-explanation">
                    <h4>¿Por qué te recomendamos <b>{mejor_opcion['Nombre']}</b>?</h4>
                    <p>Basado en tus preferencias de <strong>{st.session_state.prefs.get('Tipo de aroma', 'aroma')}</strong>, 
                    intensidad <strong>{st.session_state.prefs.get('Intensidad', 'media')}</strong> 
                    para <strong>{st.session_state.prefs.get('Ocasión', 'diarias')}</strong>.</p>
                    <div class="ai-transparency">
                        <strong>¿Cómo funciona nuestra IA?</strong><br>
                        Nuestro algoritmo analiza tus preferencias y las compara con más de {len(df)} perfumes, 
                        buscando coincidencias en notas olfativas, intensidad y ocasión de uso.
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                _, col_main, _ = st.columns([1,2,1])
                with col_main:
                    display_perfume_card(mejor_opcion)

                st.markdown("---")
                st.header("Otras Opciones que te pueden gustar")
                
                otras_opciones = st.session_state.results.iloc[1:4]
                if not otras_opciones.empty:
                    cols_other = st.columns(len(otras_opciones))
                    for i, (idx, perfume) in enumerate(otras_opciones.iterrows()):
                        with cols_other[i]:
                            display_perfume_card(perfume)
                
                st.markdown("---")
                if st.button("Reiniciar Guía", key="reiniciar_guia", use_container_width=True):
                    st.session_state.step = 0
                    st.session_state.prefs = {}
                    st.rerun()

    # --- CATÁLOGO MEJORADO ---
    with tab2:
        st.header("Explora nuestro catálogo completo")
        
        selected_genero_catalogo = st.radio("PARA QUIÉN BUSCAS:", ['Hombre', 'Mujer', 'Unisex'], horizontal=True, key='genero_catalogo')
        df_catalogo = df[df['Género'].isin([selected_genero_catalogo, 'Unisex'])].copy()

        search_term = st.text_input('Buscar por nombre, marca o notas:', '', placeholder="Escribe para buscar...")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            marcas = ['Todas'] + sorted(df_catalogo['Marca'].unique().tolist())
            selected_marca = st.selectbox("Marca:", marcas)
        with col2:
            tipos = ['Cualquiera'] + sorted(df_catalogo['Tipo de aroma'].unique().tolist())
            selected_tipo = st.selectbox("Tipo de aroma:", tipos)
        with col3:
            intensidades = ['Cualquiera'] + sorted(df_catalogo['Intensidad'].unique().tolist())
            selected_intensidad = st.selectbox("Intensidad:", intensidades)
        with col4:
            ocasiones = ['Cualquiera'] + sorted(df_catalogo['Ocasión'].unique().tolist())
            selected_ocasion = st.selectbox("Ocasión:", ocasiones)
        
        # Filtro de presupuesto
        st.markdown("**Rango de precios:**")
        min_price = int(df_catalogo['Precio (€)'].min())
        max_price = int(df_catalogo['Precio (€)'].max())
        price_range = st.slider("", min_value=min_price, max_value=max_price, 
                              value=(min_price, max_price), step=5,
                              label_visibility="collapsed")
        
        # Aplicar filtros
        filtros = (df_catalogo['Género'].isin([selected_genero_catalogo, 'Unisex']))
        if selected_marca != 'Todas': filtros &= (df_catalogo['Marca'] == selected_marca)
        if selected_tipo != 'Cualquiera': filtros &= (df_catalogo['Tipo de aroma'] == selected_tipo)
        if selected_intensidad != 'Cualquiera': filtros &= (df_catalogo['Intensidad'] == selected_intensidad)
        if selected_ocasion != 'Cualquiera': filtros &= (df_catalogo['Ocasión'] == selected_ocasion)
        filtros &= (df_catalogo['Precio (€)'] >= price_range[0]) & (df_catalogo['Precio (€)'] <= price_range[1])

        if search_term:
            filtros &= df_catalogo.apply(lambda row: 
                search_term.lower() in str(row['Nombre']).lower() or 
                search_term.lower() in str(row['Marca']).lower() or 
                any(search_term.lower() in note.lower() for note in row['Notas']), axis=1)

        resultados = df_catalogo[filtros]
        st.markdown("---")
        st.markdown(f"**Perfumes encontrados: {len(resultados)}**")

        if not resultados.empty:
            cols = st.columns(3)
            for i, (idx, perfume) in enumerate(resultados.iterrows()):
                with cols[i % 3]:
                    display_perfume_card(perfume)
        else:
            st.warning("No encontramos perfumes con esos filtros. Prueba ajustando tus criterios.")
    
    # --- FOOTER CON INFORMACIÓN DE AFILIADOS ---
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; font-size: 0.85em; color: #666; padding: 20px;">
        <p>Algunos enlaces son de afiliados. Si realizas una compra a través de ellos, 
        podemos recibir una comisión sin costo adicional para ti. Esto nos ayuda a mantener el servicio.</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
