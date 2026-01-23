import sys
sys.path.append("utils")
import streamlit as st
import re
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle
import numpy as np
import io
import subprocess, base64
import utils as ut
from PIL import Image, ImageOps

# Configuración de página
st.set_page_config(
    page_title="Acero en Vigas a flexión pura", 
    page_icon=r"https://raw.githubusercontent.com/AssiaFB/Imgenes-de-AssiaFB/refs/heads/main/Ping%C3%BCino%20nocturno%20trabajando%20en%20laptop.png", 
    layout="wide"
)

# Función para cargar CSS externo
def load_css(file_name):
    try:
        with open(file_name) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        st.error(f"No se encontró el archivo de estilos: {file_name}")

# Cargar el CSS desde la carpeta style
load_css("style/style.css")

# TITULO
st.markdown("""
<div class="assiafb-title">Calculadora de acero a flexión</div>
""", unsafe_allow_html=True)

# Descripción
st.markdown("""
<div class="assiafb-section">
  <p>
    Esta aplicación ha sido desarrollada como una herramienta de apoyo para ingenieros y estudiantes, permitiendo determinar el área de 
    acero requerida en vigas sometidas a flexión pura y verificar la sección propuesta bajo normativas vigentes. Además de considerar las propiedades 
    geométricas, las cargas y los materiales, garantizando el cumplimiento de la separación mínima libre entre barras (tomando el mayor valor entre 1 pulgada 
    y el diámetro de la barra) para asegurar un diseño eficiente y constructible.
  </p>
</div>
""", unsafe_allow_html=True)

# TARGET Autor
st.markdown("""
<div class="assiafb-author-card">
  <h3>Autor: Jesús Bautista</h3>
  <div class="assiafb-links">
    <a class="assiafb-link" href="https://www.linkedin.com/in/jesus-bautista-ing-civil/" target="_blank">
      <img src="https://cdn.jsdelivr.net/gh/simple-icons/simple-icons/icons/linkedin.svg" alt="LinkedIn">
    </a>
    <a class="assiafb-link" href="https://www.youtube.com/@bitbuilderx" target="_blank">
      <img src="https://cdn.jsdelivr.net/gh/simple-icons/simple-icons/icons/youtube.svg" alt="YouTube">
    </a>
    <a class="assiafb-link" href="https://github.com/Assia-Network" target="_blank">
      <img src="https://cdn.jsdelivr.net/gh/simple-icons/simple-icons/icons/github.svg" alt="GitHub">
    </a>
  </div>
</div>
""", unsafe_allow_html=True)

# Datos de entrada
st.markdown("<div class='section-title'>Ingresar parámetros:</div>", unsafe_allow_html=True)

# CAJAS NUMERICAS DE TEXTO
with st.expander("", expanded=True):

    # Momentos

    col1, col2, col3 = st.columns(3)
    
    with col1:
        Mcm = st.number_input("Momento CM (tonf·m)", step=0.0001, value=10.00, format='%.3f')
        
    with col2:
        Mcv = st.number_input("Momento CV (tonf·m)", step=0.001, value=6.00, format='%.3f')
        
    with col3:
        Mcs = st.number_input("Momento CS (tonf·m)", step=0.001, value=1.00, format='%.3f')

    # Propiedades mecanicas

    col1, col2, col3 = st.columns(3)
    
    with col1:
        autor = st.text_input("Autor", value="Jesús B.")
        
    with col2:
        f_c = st.number_input("f'c (kgf/cm²)", min_value=0.0001, step=0.001, value=210.00, format='%.3f')
        
    with col3:
        f_y = st.number_input("f'y (kgf/cm²)", min_value=0.0001, step=0.001, value=4200.00, format='%.3f')

    # Propiedades Geometricas
        
    col1, col2, col3 = st.columns(3)
    
    with col1:
        b = st.number_input("Ancho de viga (cm)", min_value=0.0001, step=0.001, value=30.00, format='%.3f')
        
    with col2:
        h = st.number_input("Altura de viga (cm)", min_value=0.0001, step=0.001, value=50.00, format='%.3f')
        
    with col3:
        diame_long = st.number_input("ø Longitudinal (in)", min_value=0.00010, step=0.001, value=1.00, format='%.3f')

    # Propiedades Geometricas
        
    col1, col2, col3 = st.columns(3)
    
    with col1:
        diame_estr = st.number_input("ø Estribo (in)", min_value=0.0001, step=0.001, value=0.5, format='%.3f')
        
    with col2:
        ecu = st.number_input("Defromación unitaria de concreto", min_value=0.0001, step=0.001, value=0.003, format='%.4f')
        
    with col3:
        Es = st.number_input("Módulo de elasticidad del acero (kgf/cm²)", min_value=0.0001, step=0.001, value=2e6, format='%.3e')

    # Propiedades Geometricas
        
    col1, col2, col3 = st.columns(3)
    
    with col1:
        r_L = st.number_input("Recubrimiento libre (cm)", min_value=0.0001, step=0.001, value=4.00, format='%.3f')
        
    with col2:
        capas = st.number_input("Capas de acero", min_value=1, step=1, value=2, format='%.d')
        
    with col3:
        n_por_capa_txt = st.text_input("N° de varillas por capa (ejemplo: 3→2)", value="3-2")
    

    # Tipo de diseño

    col1, col2, col3 = st.columns(3)

    with col1:
        etiqueta_v = st.text_input("Etiqueta de viga", value="A-B")
    with col2:
        coef_pbal = st.selectbox("Tipo de diseño", ["Comunes", "Esenciales"])
    with col3:
        escala_imagen = st.number_input("Escala de la imagen", min_value=0.0001, step=0.001, value=0.8, format='%.3f')

# Numero de varillas a lista
n_por_capa_list = list(map(int, re.findall(r"\d+\.?\d*", n_por_capa_txt)))
n_por_capa_arr = np.array(n_por_capa_list, dtype=int)

# COMB
Mu_dis = [1.4*Mcm+1.7*Mcv, 1.25*(Mcv+Mcm)+Mcs, 1.25*(Mcv+Mcm)-Mcs, 0.9*Mcm+Mcs, 0.9*Mcm-Mcs]

min_Mu, max_Mu = min(Mu_dis), max(Mu_dis)

if abs(min_Mu) > abs(max_Mu):
    Mu=min_Mu
else:
    Mu=max_Mu

if len(n_por_capa_arr) == capas and 1 not in n_por_capa_arr:
    # Verificación de distribución
    diame_estr_cm = diame_estr * 2.54
    diame_long_cm = diame_long * 2.54
    espacimiento_var = max(2.54, diame_long_cm)
    
    d = h - (r_L + diame_estr_cm + (capas/2)*diame_long_cm + espacimiento_var*(capas-1)/2)
    alto_acero = capas*diame_long_cm + espacimiento_var*(capas-1)
    alto_consumible = h - 2*(diame_estr_cm + r_L)
    ancho_consumible = b - 2*(diame_estr_cm + r_L)
    
    if all(ancho_consumible >= x for x in (n_por_capa_arr * diame_long_cm + (n_por_capa_arr - 1) * espacimiento_var)) and alto_consumible >= alto_acero:
        fig, ax = ut.viga_plot(espacimiento_var, Mu, n_por_capa_arr, diame_estr_cm, diame_long_cm, b, h, r_L, capas, alto_consumible, ancho_consumible)
        viga_graf = io.BytesIO()
        fig.savefig(viga_graf, format="png", dpi=400, facecolor=fig.get_facecolor(), bbox_inches='tight')
        viga_graf.seek(0)

        # Invertir color
        imgen_org = Image.open(viga_graf)

        imagen_invert = ImageOps.invert(imgen_org.convert("RGB"))

        # Guardar png
        nombre_archivo = "grafico_viga.png"
        imagen_invert.save(nombre_archivo)

        # Codificacion
        b64_viga_plot = base64.b64encode(viga_graf.getvalue()).decode()
        st.markdown(
            f"""
            <div style="text-align:center;">
                <img src="data:image/png;base64,{b64_viga_plot}" width="300">
            </div>
            """,
            unsafe_allow_html=True
        )
        
    else:
        if alto_acero - alto_consumible > 0:
            st.markdown(f"""
            <div class="assiafb-alert">
            <p><strong>⚠️ Advertencia:</strong> Parte del refuerzo se encuentra fuera de los límites de la sección de la altura, excediendo {(alto_acero - alto_consumible):.2f} cm.</p>
            <p>Revisa las dimensiones y el número de varillas por capa antes de continuar con el cálculo estructural.</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="assiafb-alert">
            <p><strong>⚠️ Advertencia:</strong> Parte del refuerzo se encuentra fuera de los límites de la sección de la base.</p>
            <p>Revisa las dimensiones y el número de varillas por capa antes de continuar con el cálculo estructural.</p>
            </div>
            """, unsafe_allow_html=True)
else:
    if 1 not in n_por_capa_arr:
        st.markdown("""
        <div class="assiafb-alert">
        <p><strong>⚠️ Advertencia:</strong> El número de capas de acero no coincide con la cantidad de varillas asignadas por capa.</p>
        <p>Verifica los datos de entrada antes de continuar con el cálculo para asegurar la coherencia del refuerzo.</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="assiafb-alert">
        <p><strong>⚠️ Advertencia:</strong> Se recomienda que el número de barras por capa sea como mínimo dos, de acuerdo con las buenas prácticas de armado.</p>
        <p>Verifica los datos de entrada antes de continuar con el cálculo para asegurar la coherencia del refuerzo.</p>
        </div>
        """, unsafe_allow_html=True)


# Info de error

info_error = 0

# Diseño
try:
    peralte = d

    # Numero de varillas
    varillas_totales = n_por_capa_arr.sum()

    # Cuantia Requerida
    ps = (f_c/(1.18*f_y))*(1-(1-(2.36*abs(Mu)*1e5)/(0.9*f_c*b*peralte**2))**0.5)  

    # Cuantia Minima

    p_min=[(0.7*f_c**0.5)/f_y, 14/f_y]

    p_min_final=max(p_min)

    # ELección de la cuantia de diseño en base al minimo
    if p_min_final>ps:
        p_dise=p_min_final
    else:
        p_dise=ps

    # Determinación de beta1
    if 173.35<=f_c and f_c<=285.52:
        beta1=0.85
    elif 285.52<f_c and f_c<560.85:
        beta1=0.85-(0.05*(f_c/10.1972-28)/7)
    else:
        beta1=0.65

    # Cuantia Balanceada y Maxima

    pb=(0.85*f_c/f_y)*beta1*(ecu*Es)/(ecu*Es+f_y)
    
    if coef_pbal == "Comunes":
        coef_pbal_real=0.75
    else:
        coef_pbal_real=0.5
        
    pmax=coef_pbal_real*pb

    if pmax < p_dise:
        st.markdown("""
        <div class="assiafb-alert">
        <p><strong>❌ Advertencia:</strong> Se debe diseñar doblemente armado o aumentar las dimensiones de la sección, forzando a no continuar ... </p>
        </div>
        """, unsafe_allow_html=True)

        info_error = 1

        raise ValueError("Se debe diseñar doblemente armado, forzando a no continuar.")  #Siguiente version

    # Reporte
    ty2="Reporte".upper()
    st.markdown(
        f"<div style='font-weight:bold; color:#2E86C1; font-size:24px;'>{ty2}</div>",
        unsafe_allow_html=True)

    # FUNCTION
    latex = ut.generar_reporte_viga((nombre_archivo, escala_imagen, varillas_totales), etiqueta_v, autor, f_c, f_y, Es, b, h, ecu, diame_long, diame_estr, r_L, coef_pbal, Mu_dis, Mu, peralte, ps, p_min, p_min_final, beta1, pb, coef_pbal_real, pmax, p_dise)

    # Guardar txt
    with open("reporte.tex", "w", encoding="utf-8") as f:
        f.write(latex)

    # Compilat latex
    subprocess.run(["pdflatex", "-interaction=nonstopmode", "reporte.tex"], stdout=subprocess.DEVNULL)

    # Leer pdf
    with open("reporte.pdf", "rb") as f:
        pdf_bytes = f.read()

    # Streamlit
    b64=base64.b64encode(pdf_bytes).decode()
    st.markdown(f"""
    <style>
    .pdf-container {{
        width: 100%;
        height: 100vh;
    }}
    </style>
    <div class="pdf-container">
        <object 
            data="data:application/pdf;base64,{b64}" 
            type="application/pdf" 
            width="100%" 
            height="100%">
            <p>Tu navegador no permite visualizar este PDF directamente. 
            <a href="data:application/pdf;base64,{b64}" download="reporte.pdf">Descárgalo aquí</a>.</p>
        </object>
    </div>
    """,  unsafe_allow_html=True)

except:
    if info_error == 0:
        st.markdown("""
        <div class="assiafb-alert">
        <p><strong>❌ Ocurrió un error:</strong> La sección de la Viga es insuficiente o el momento ultimo es demasiado grande</p>
        </div>
        """, unsafe_allow_html=True)