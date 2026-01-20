import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle
import numpy as np
import math

# PLOTEAR VIGA
def viga_plot(espacimiento_var, Mu, n_por_capa, diame_estr, diame_long, b, h, r_L, capas, alto_consumible, ancho_consumible):
    
    plt.style.use("dark_background")
    fig, ax = plt.subplots(figsize=(b*0.1, h*0.1))
    
    ax.text(b/2, -3, f"b = {b} cm", ha='center', va='top', fontsize=10)
    ax.text(b+1.5, h/2, f"h = {h} cm", rotation=90, va='center', fontsize=10)
    ax.add_patch(Rectangle((0, 0), b, h, fill=False, lw=2))
    
    # Lado inferior
    ax.add_patch(Rectangle((r_L, r_L), ancho_consumible+2*diame_estr, diame_estr, color="white"))
    # Lado superior
    ax.add_patch(Rectangle((r_L, h-(r_L+diame_estr)), ancho_consumible+2*diame_estr, diame_estr, color="white"))
    # Lado izquierdo
    ax.add_patch(Rectangle((r_L, r_L), diame_estr, alto_consumible+2*diame_estr, color="white"))
    # Lado derecho
    ax.add_patch(Rectangle((b-(r_L+diame_estr), r_L), diame_estr, alto_consumible+2*diame_estr, color="white"))
    
    # Coordenadas de varillas
    x_cord = []
    y_cord = []
    for i in range(capas):
            separacion_real_x = (ancho_consumible - n_por_capa[i] * diame_long) / (n_por_capa[i] - 1)
            for g in range(n_por_capa[i]):
                n_val = g + 1
                x_cord.append(float(r_L + diame_estr + (n_val - 0.5) * diame_long + (n_val - 1) * separacion_real_x))
    if Mu >= 0:
        for i in range(capas):
            n_val = i + 1
            for g in range(n_por_capa[i]):
                y_cord.append(r_L + diame_estr + (n_val - 0.5) * diame_long + (n_val - 1) * espacimiento_var)
    else:
        for i in range(capas):
            n_val = i + 1
            for g in range(n_por_capa[i]):
                y_cord.append(h - (r_L + diame_estr + (n_val - 0.5) * diame_long + (n_val - 1) * espacimiento_var))
    
    # Dibujarlas
    for x, y in zip(x_cord, y_cord):
        ax.add_patch(Circle((x, y), radius=diame_long/2, color='aqua'))
    
    ax.set_aspect("equal", adjustable="box")
    ax.set_xlim(-0.02, b + 0.02)
    ax.set_ylim(-0.02, h + 0.02)
    ax.set_xlabel("b (m)")
    ax.set_ylabel("h (m)")
    ax.axis('off')

    return fig, ax

def generar_reporte_viga( tupla_date, diseno, autor, f_c, f_y, Es, b, h, ecu, diametro_long, diametro_est, r_libre, coef_pbal, Mdise, MU, peralte, ps, p_min, p_min_final, beta1, pb, coef_pbal_real, pmax, p_dise):
    ubi, escala, varillas_totales = tupla_date
    
    return rf"""
        \documentclass[12pt, a4paper]{{article}}
        \usepackage[utf8]{{inputenc}}
        \usepackage[T1]{{fontenc}}
        \usepackage{{lmodern}}
        \usepackage{{geometry}}
        \geometry{{margin=2.5cm}}
        \usepackage[spanish]{{babel}}
        \AtBeginDocument{{\decimalpoint}}
        \usepackage{{float}}
        \usepackage{{graphicx}}
        \usepackage{{float}}

        \title{{Diseño de viga {diseno}}}
        \author{{{autor}}}
        \date{{\today}}

        \begin{{document}}
        
        \maketitle
        
        \section{{Datos Registrados}}

        En la siguiente tabla se presentan los principales parámetros y propiedades del material utilizados para el diseño de la viga:

        \begin{{itemize}}
            \item Resistencia a la compresión del concreto ($f'_c$) : {{{f_c:.2f}}} $\text{{kgf/cm}}^2$
            \item Resistencia a la fluencia del acero ($f_y$) : {{{f_y:.2f}}} $\text{{kgf/cm}}^2$
            \item Módulo de elasticidad del acero ($E_s$) : {{{Es:.0f}}} $\text{{kgf/cm}}^2$
            \item Ancho de la viga ($b$) : {{{b:.2f}}} cm
            \item Altura total de la viga ($h$) : {{{h:.2f}}} cm
            \item Deformación unitaria del concreto ($\varepsilon_c$) : {{{ecu:.4f}}}
            \item Diámetro del refuerzo longitudinal ($\phi_L$) : {{{diametro_long*2.54:.2f}}} cm
            \item Diámetro del estribo ($\phi_e$) : {{{diametro_est*2.54:.2f}}} cm
            \item Recubrimiento libre del concreto ($r$) : {{{r_libre:.2f}}} cm
            \item Coeficiente del tipo de estructura : {{{coef_pbal}}}
            \item Equivalencia 1 in : {{{2.54}}} cm
            \item Numero de varillas totales: {{{varillas_totales}}} var.
        \end{{itemize}}

        En la Figura \ref{{fig:viga_resultado}} se muestra el esquema gráfico resultante del diseño:

        \begin{{figure}}[H]
        \centering
        \caption{{Gráfico de la distribución de aceros en la Viga}}
        \includegraphics[scale={escala/5}]{{{ubi}}}
        \label{{fig:viga_resultado}}
        \end{{figure}}

        \section{{Combinaciones de Carga}}

        Las combinaciones de carga se expresan en unidades de $tonf \cdot m$, conforme a los factores de mayoración establecidos por el diseño por resistencia:

        \begin{{itemize}}
            \item $Mu_1$ : $1.4 M_{{cm}} + 1.7 M_{{cv}} = {{{Mdise[0]:.2f}}}$
            \item $Mu_2$ : $1.25 (M_{{cm}} + M_{{cv}}) + M_{{cs}} = {{{Mdise[1]:.2f}}}$
            \item $Mu_3$ : $1.25 (M_{{cm}} + M_{{cv}}) - M_{{cs}} = {{{Mdise[2]:.2f}}}$
            \item $Mu_4$ : $0.9 M_{{cm}} + M_{{cs}} = {{{Mdise[3]:.2f}}}$
            \item $Mu_5$ : $0.9 M_{{cm}} - M_{{cs}} = {{{Mdise[4]:.2f}}}$
        \end{{itemize}}

        Como combinación crítica, se adopta el \textbf{{momento último}} correspondiente a: \textbf{{{MU:.2f} tonf·m}}.

        \\
        \\
        \\
        \section{{Calculo de cuantia requerida}}
        
        Primero, se determina el \textbf{{peralte efectivo}} de la viga, el cual representa la distancia entre la fibra extrema en compresión y el centroide del refuerzo longitudinal a tracción.  
        Este valor es fundamental para el cálculo de la resistencia a flexión y se obtiene mediante la siguiente expresión:

        \[
        d = h - (r + \phi_e + 0.5 \cdot \phi_L)
        \]

        donde:

        \begin{{itemize}}
            \item $d$ : peralte efectivo de la viga (cm)
            \item $h$ : altura total de la sección (cm)
            \item $r$ : recubrimiento libre de concreto (cm)
            \item $\phi_e$ : diámetro del estribo (cm)
            \item $\phi_L$ : diámetro de la barra longitudinal (cm)
        \end{{itemize}}
                
        Sustituyendo los valores en la ecuación, se obtiene un \textbf{{peralte efectivo}} de: \textbf{{{peralte:.2f} (cm)}}.

        Continuando con el cálculo, se plantea la siguiente expresión para la cuantía de refuerzo de acero:

        \[
         \rho_{{requerido}} = \frac{{f'c}}{{1.18 \cdot f'y}}  \cdot \left[ 1 - \sqrt{{1 - \frac{{2.36 \cdot |M_{{último}}|}}{{\phi_{{flexión}} \cdot f'c \cdot b \cdot d^2 }}   }} \right]
        \]
        
        Donde, finalmente, al realizar las operaciones y reemplazar las magnitudes y coeficientes correspondientes, se obtiene la \textbf{{cuantía de refuerzo requerida}} igual a: \textbf{{{ps:.4f}}}.
        
        \section{{Cálculo de cuantía mínima}}

        Para garantizar un adecuado comportamiento estructural de la viga ante esfuerzos de flexión, se determina la \textbf{{cuantía mínima}} conforme a las expresiones establecidas en la normativa, las cuales aseguran que la sección sea dúctil y capaz de desarrollar deformaciones controladas antes de la falla.

        \begin{{itemize}}
            \item \[
            \frac{{0.7 \cdot \sqrt{{f'_c}}}}{{f_y}} = {{{p_min[0]:.4f}}}
            \]
            \item \[
            \frac{{14}}{{f_y}} = {{{p_min[1]:.4f}}}
            \]
        \end{{itemize}}

        Donde, finalmente, se adopta el valor mayor entre ambas expresiones, obteniéndose una \textbf{{cuantía mínima final}} de: \textbf{{{p_min_final:.4f}}}.

        \section{{Cálculo de cuantía máxima}}

        Para estimar la cuantía límite se emplea el parámetro $\beta_1$ de la tabla~\ref{{tab:beta1}} (distribución rectangular equivalente de esfuerzos en el concreto).
        A continuación se presenta la tabla:

        \begin{{table}}[H]
        \centering
        \caption{{Valores de $\beta_1$ en función de $f'_c$}}
        \label{{tab:beta1}}
        \begin{{tabular}}{{c c}}
        \hline
        $\;f'_c\;$(MPa) & $\beta_1$ \\ \hline
        $17 \le f'_c \le 28$ & $0.85$ \\
        $28 < f'_c < 55$ & $0.85 - \frac{{0.05\,(f'_c-28)}}{{7}}$ \\
        $f'_c \ge 55$ & $0.65$ \\
        \hline
        \end{{tabular}}
        \end{{table}}
        
        Con base en la Tabla~\ref{{tab:beta1}} y el valor de resistencia del concreto considerado,
        se obtiene:
        \[
        \beta_1 = \textbf{{{beta1:.2f}}}
        \]        
        
        La \textbf{{cuantía balanceada}} se determina mediante:
        \[
        \rho_{{\text{{bal}}}} \;=\;
        0.85 \cdot \frac{{f'c}}{{f'y}} \cdot \beta_1 \cdot
        \left( \frac{{\varepsilon_{{cu}} \cdot E_s}}{{\varepsilon_{{cu}} \cdot E_s + f_y}} \right)
        \]
        
        Sustituyendo en la expresión, la \textbf{{cuantía balanceada}} resulta:

        \[
        \rho_{{\text{{bal}}}} = \textbf{{{pb:.4f}}}
        \]
        
        El \textbf{{coeficiente de reducción}} aplicado para la cuantía máxima en estructuras de tipo {{{coef_pbal}}}
        corresponde a un valor de \textbf{{{coef_pbal_real}}}.  
        Este factor permite limitar la ductilidad y controlar el estado balanceado de la sección, reduciendo la
        cuantía balanceada previamente calculada.

        Al aplicar dicha reducción, la \textbf{{cuantía máxima resultante}} es:

        \[
        \rho_{{\max}} = {{{pmax:.4f}}}
        \]

        Este valor representa el límite superior de cuantía admisible en el diseño, garantizando un comportamiento
        flexible y evitando una falla frágil en la zona comprimida del concreto.

        \section{{Comparación entre cuantía mínima, requerida y máxima}}

        Con el propósito de verificar el cumplimiento normativo y garantizar un diseño estructural seguro y eficiente, se realiza la comparación entre la \textbf{{cuantía mínima}}, la \textbf{{cuantía requerida}} y, de ser necesario, la \textbf{{cuantía máxima permitida}}.

        Primero, se compara la cuantía mínima con la requerida, considerando que para efectos prácticos de diseño se adopta el valor mayor entre ambas, ya que este asegura una capacidad resistente adecuada de la sección:

        \[
        Cuantía \thinspace mínima = {{{p_min_final:.4f}}}
        \quad | \quad
        Cuantía \thinspace requerida = {{{ps:.4f}}}
        \]

        Al observar los resultados, se adopta para el diseño una \textbf{{cuantía de acero}} igual a: \textbf{{{p_dise:.4f}}}.

        Ahora, se compara la \textbf{{cuantía de diseño}} con la \textbf{{cuantía máxima permitida}}, verificando que la cuantía adoptada cumpla con los límites normativos. En caso de encontrarse dentro de los valores establecidos, se confirma su validez para el dimensionamiento de la sección.

        \[
        Cuantía \thinspace de \thinspace diseño = {{{p_dise:.4f}}}
        \quad | \quad
        Cuantía \thinspace máxima = {{{pmax:.4f}}}
        \]

        De acuerdo con la comparación, la cuantía seleccionada cumple con los requisitos normativos, por lo que se procede a determinar el área de refuerzo correspondiente mediante la siguiente expresión:

        \[
        A_{{acero}} = \rho_{{diseño}} \cdot b \cdot d
        \]

        Al realizar las operaciones, se obtiene un área de acero requerida de \textbf{{{p_dise*b*peralte:.2f}}} $\text{{cm}}^2$.

        \section{{Verificación de la Distribución de Acero}}
        Para materializar el área de acero requerida calculada anteriormente de \textbf{{{p_dise*b*peralte:.2f}}} $\text{{cm}}^2$, se ha propuesto una distribución de armadura longitudinal compuesta por:
        
        \begin{{itemize}}
            \item Cantidad de varillas: \textbf{{{varillas_totales}}}
            \item Diámetro de la barra: \textbf{{{diametro_long*2.54:.2f}}} cm
        \end{{itemize}}

        A continuación, se calcula el área de acero real proporcionada ($A_{{s,prov}}$) y se verifica si satisface la demanda:

        \[
        A_{{s,prov}} = N \cdot \frac{{\pi \cdot \phi^2}}{{4}} = {{{varillas_totales}}} \cdot \frac{{\pi \cdot {{{diametro_long*2.54:.2f}}}^2}}{{4}}
        \]

        \[
        A_{{s,prov}} = \textbf{{{varillas_totales*math.pi*(diametro_long*2.54/2)**2:.2f}}} \text{{ cm}}^2
        \]

        Finalmente, comparamos el área proporcionada con el área requerida:

        \[
        A_{{s,prop}} \geq A_{{s,req}} \quad \Rightarrow \quad {{{varillas_totales*math.pi*(diametro_long*2.54/2)**2:.2f}}} \geq {{{p_dise*b*peralte:.2f}}}
        \]

        \textbf{{Conclusión:}} El diseño propuesto \textbf{{{"CUMPLE" if varillas_totales*math.pi*(diametro_long*2.54/2)**2 >= p_dise*b*peralte else "NO CUMPLE"}}} con los requerimientos de resistencia.

        \end{{document}}
        """