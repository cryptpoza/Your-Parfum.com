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
        /* ... (todo el CSS permanece igual) ... */
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
        st.error(f"Error: El archivo '{file_path}' no se encontró. Asegúrate de que el archivo está en la misma carpeta.")
        return None

# --- FUNCIÓN PARA MOSTRAR UNA TARJETA DE PERFUME REFINADA ---
def display_perfume_card(perfume, show_details=False):
    with st.container():
        # Estructura de la tarjeta
        st.markdown(f"<div class='perfume-card'>", unsafe_allow_html=True)
        
        # Encabezado con nombre y marca
        st.markdown(f"<h3>{perfume['Nombre']}</h3>", unsafe_allow_html=True)
        st.markdown(f"<p class='perfume-brand'>{perfume['Marca']}</p>", unsafe_allow_html=True)
        
        # Imagen (si existe)
        if 'Imagen' in perfume and pd.notna(perfume['Imagen']):
            st.image(perfume['Imagen'], width=150)
        
        # Detalles básicos
        st.markdown(f"<p><b>Género:</b> {perfume['Género']}</p>", unsafe_allow_html=True)
        st.markdown(f"<p><b>Precio:</b> €{perfume['Precio (€)']}</p>", unsafe_allow_html=True)
        
        # Detalles expandidos
        if show_details:
            st.markdown(f"<p><b>Tipo de aroma:</b> {perfume['Tipo de aroma']}</p>", unsafe_allow_html=True)
            st.markdown(f"<p><b>Intensidad:</b> {perfume['Intensidad']}</p>", unsafe_allow_html=True)
            st.markdown(f"<p><b>Ocasión:</b> {perfume['Ocasión']}</p>", unsafe_allow_html=True)
            st.markdown(f"<p><b>Notas:</b> {', '.join(perfume['Notas'])}</p>", unsafe_allow_html=True)
        
        # Botones de acción
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Ver Original", key=f"original_{perfume['Nombre']}", use_container_width=True):
                st.switch_page(perfume['Link Original'])
        with col2:
            if pd.notna(perfume.get('Link Dupe')):
                if st.button("Ver Dupe", key=f"dupe_{perfume['Nombre']}", use_container_width=True):
                    st.switch_page(perfume['Link Dupe'])
        
        st.markdown("</div>", unsafe_allow_html=True)

# --- ALGORITMO DE PUNTUACIÓN (SCORING) ---
def score_perfumes(df, user_prefs):
    # Filtrar por presupuesto
    df = df[df['Precio (€)'] <= user_prefs['Presupuesto']]
    
    # Inicializar columna de puntuación
    df['puntuacion'] = 0
    
    # Puntos por tipo de aroma
    df.loc[df['Tipo de aroma'] == user_prefs['Tipo de aroma'], 'puntuacion'] += 10
    
    # Puntos por intensidad
    df.loc[df['Intensidad'] == user_prefs['Intensidad'], 'puntuacion'] += 8
    
    # Puntos por ocasión
    df.loc[df['Ocasión'] == user_prefs['Ocasión'], 'puntuacion'] += 8
    
    # Puntos por notas
    if user_prefs['Notas']:
        for note in user_prefs['Notas']:
            df['puntuacion'] += df['Notas'].apply(lambda notes: 3 if note in notes else 0)
    
    # Puntos por popularidad
    df['puntuacion'] += df['Popularidad'] * 0.01
    
    # Ordenar por puntuación
    df = df.sort_values('puntuacion', ascending=False)
    
    return df

# --- FUNCIÓN PARA BÚSQUEDA AUTOMÁTICA ---
def get_search_options(df):
    options = []
    # Nombres de perfumes
    for nombre in df['Nombre'].unique():
        options.append(f"👑 {nombre}")
    # Marcas
    for marca in df['Marca'].unique():
        options.append(f"🏷️ {marca}")
    # Notas
    all_notes = set()
    for note_list in df['Notas']:
        all_notes.update(note_list)
    for note in all_notes:
        options.append(f"🌸 {note}")
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
            progress_text = "Paso 1 de 3"
            progress_bar = st.progress(0, text=progress_text)
            progress_bar.progress(25, text=progress_text)
            
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
            progress_text = "Paso 2 de 3"
            progress_bar = st.progress(0, text=progress_text)
            progress_bar.progress(50, text=progress_text)
            
            st.markdown(
                "<p style='text-align: center; font-size: 1.2rem;'>"
                "<b>Paso 2:</b> Ahora, elige el tipo de aroma y la ocasión"
                "</p>", 
                unsafe_allow_html=True
            )
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
            progress_text = "Paso 3 de 3"
            progress_bar = st.progress(0, text=progress_text)
            progress_bar.progress(75, text=progress_text)
            
            st.markdown(
                "<p style='text-align: center; font-size: 1.2rem;'>"
                "<b>Paso 3:</b> ¿Qué intensidad prefieres y cuál es tu presupuesto?"
                "</p>", 
                unsafe_allow_html=True
            )
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
            progress_text = "¡Resultados listos!"
            progress_bar = st.progress(0, text=progress_text)
            progress_bar.progress(100, text=progress_text)
            
            if not st.session_state.results.empty:
                st.header("✨ Tu Recomendación Principal ✨")
                mejor_opcion = st.session_state.results.iloc[0]
                
                # Explicación de la recomendación
                st.markdown(f"""
                <div class="recommendation-explanation">
                    <h4>¿Por qué te recomendamos <b>{mejor_opcion['Nombre']}</b>?</h4>
                    <p>Basado en tus elecciones, este perfume de tipo <strong>{st.session_state.prefs['Tipo de aroma']}</strong> con una intensidad <strong>{st.session_state.prefs['Intensidad']}</strong> es ideal para <strong>{st.session_state.prefs['Ocasión']}</strong>. Las notas de {', '.join(mejor_opcion['Notas'])} encajan perfectamente con tus preferencias.</p>
                    <p><b>Cómo funciona nuestra IA:</b> Nuestro algoritmo analiza tus preferencias y las compara con nuestra base de datos de más de 30 perfumes, considerando tipo, intensidad, ocasión, notas olfativas y presupuesto para encontrar las mejores coincidencias.</p>
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
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Reiniciar Guía", key="reiniciar_guia", use_container_width=True):
                        st.session_state.step = 0
                        st.rerun()
                with col2:
                    if st.button("Explorar Catálogo", key="explorar_catalogo", use_container_width=True):
                        st.session_state.tab_active = "🔎 Explorar Catálogo"
                        st.rerun()
            else:
                st.warning("No se encontraron perfumes que coincidan con tu búsqueda. Intenta con otros filtros.")
                if st.button("Reiniciar Guía", key="reiniciar_guia_fail", use_container_width=True):
                    st.session_state.step = 0
                    st.rerun()

    # --- PESTAÑA 2: EXPLORAR CATÁLOGO ---
    with tab2:
        st.header("Explora todo nuestro catálogo")
        
        # Género con botones
        st.markdown("<p style='margin-bottom: 10px;'><b>PARA QUIÉN BUSCAS:</b></p>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        genero_options = ['Hombre', 'Mujer', 'Unisex']
        selected_genero_catalogo = st.session_state.get('selected_genero_catalogo', 'Hombre')
        
        with col1:
            if st.button("Hombre", key="catalogo_hombre", use_container_width=True):
                selected_genero_catalogo = 'Hombre'
        with col2:
            if st.button("Mujer", key="catalogo_mujer", use_container_width=True):
                selected_genero_catalogo = 'Mujer'
        with col3:
            if st.button("Unisex", key="catalogo_unisex", use_container_width=True):
                selected_genero_catalogo = 'Unisex'
        
        st.session_state.selected_genero_catalogo = selected_genero_catalogo
        df_catalogo = df[df['Género'].isin([selected_genero_catalogo, 'Unisex'])].copy()
        
        # Búsqueda con autocompletado nativo
        search_options = get_search_options(df_catalogo)
        search_term = st.selectbox(
            "Busca por nombre, marca o notas olfativas:", 
            options=search_options,
            index=None,
            placeholder="Escribe o selecciona una opción..."
        )
        
        # Filtros en tarjetas
        st.markdown("<div class='filter-card'>", unsafe_allow_html=True)
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            selected_marca = st.selectbox("Marca:", ['Todas'] + sorted(df_catalogo['Marca'].unique().tolist()))
        with col2:
            # Filtro dinámico para tipo de aroma
            if selected_marca == 'Todas':
                tipo_options = ['Cualquiera'] + sorted(df_catalogo['Tipo de aroma'].unique().tolist())
            else:
                marca_filtrada = df_catalogo[df_catalogo['Marca'] == selected_marca]
                tipo_options = ['Cualquiera'] + sorted(marca_filtrada['Tipo de aroma'].unique().tolist())
            selected_tipo = st.selectbox("Tipo de aroma:", tipo_options)
        with col3:
            temp_df = df_catalogo
            if selected_marca != 'Todas':
                temp_df = temp_df[temp_df['Marca'] == selected_marca]
            if selected_tipo != 'Cualquiera':
                temp_df = temp_df[temp_df['Tipo de aroma'] == selected_tipo]
            intensidad_options = ['Cualquiera'] + sorted(temp_df['Intensidad'].unique().tolist())
            selected_intensidad = st.selectbox("Intensidad:", intensidad_options)
        with col4:
            temp_df_ocasion = df_catalogo
            if selected_marca != 'Todas':
                temp_df_ocasion = temp_df_ocasion[temp_df_ocasion['Marca'] == selected_marca]
            if selected_tipo != 'Cualquiera':
                temp_df_ocasion = temp_df_ocasion[temp_df_ocasion['Tipo de aroma'] == selected_tipo]
            if selected_intensidad != 'Cualquiera':
                temp_df_ocasion = temp_df_ocasion[temp_df_ocasion['Intensidad'] == selected_intensidad]
            ocasion_options = ['Cualquiera'] + sorted(temp_df_ocasion['Ocasión'].unique().tolist())
            selected_ocasion = st.selectbox("Ocasión:", ocasion_options)
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Filtro de precio
        st.markdown("<div class='filter-card'>", unsafe_allow_html=True)
        min_price = int(df_catalogo['Precio (€)'].min())
        max_price = int(df_catalogo['Precio (€)'].max())
        price_range = st.slider("Rango de precios (€):", min_value=min_price, max_value=max_price, value=(min_price, max_price))
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Aplicar filtros
        filtros = (df_catalogo['Género'].isin([selected_genero_catalogo, 'Unisex']))
        if selected_marca != 'Todas': 
            filtros &= (df_catalogo['Marca'] == selected_marca)
        if selected_tipo != 'Cualquiera': 
            filtros &= (df_catalogo['Tipo de aroma'] == selected_tipo)
        if selected_intensidad != 'Cualquiera': 
            filtros &= (df_catalogo['Intensidad'] == selected_intensidad)
        if selected_ocasion != 'Cualquiera': 
            filtros &= (df_catalogo['Ocasión'] == selected_ocasion)
        filtros &= (df_catalogo['Precio (€)'] >= price_range[0]) & (df_catalogo['Precio (€)'] <= price_range[1])

        if search_term:
            # Procesar el término de búsqueda según el tipo
            if search_term.startswith("👑"):
                perfume_name = search_term[2:].strip()
                filtros &= (df_catalogo['Nombre'] == perfume_name)
            elif search_term.startswith("🏷️"):
                brand_name = search_term[2:].strip()
                filtros &= (df_catalogo['Marca'] == brand_name)
            elif search_term.startswith("🌸"):
                note_name = search_term[2:].strip().lower()
                filtros &= df_catalogo['Notas'].apply(lambda notes: note_name in [n.lower() for n in notes])
            else:
                filtros &= (
                    df_catalogo['Nombre'].str.contains(search_term, case=False) |
                    df_catalogo['Marca'].str.contains(search_term, case=False) |
                    df_catalogo['Notas'].apply(lambda notes: any(search_term.lower() in note.lower() for note in notes))
                )

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
            
        # Botón para volver a la guía
        if st.button("Probar la Guía Personalizada", key="volver_guia", use_container_width=True):
            st.session_state.tab_active = "✨ Guía Personalizada"
            st.session_state.step = 0
            st.rerun()
    
    # --- AVISO DE PRIVACIDAD Y COOKIES ---
    with st.expander("ℹ️ Información sobre la IA y la fuente de datos"):
        st.markdown("""
        **¿Cómo funciona nuestra IA?**
        
        Nuestro sistema de recomendación utiliza un algoritmo avanzado que analiza múltiples factores:
        
        - **Preferencias personales**: Tipo de aroma, intensidad, ocasión y notas favoritas
        - **Cara
