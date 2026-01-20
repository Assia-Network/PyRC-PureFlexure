# Viga-Flexion-Pura 

**Herramienta de automatización para el diseño y verificación de vigas de concreto reforzado sometidas a flexión pura.**

## Descripción

Esta aplicación ha sido desarrollada como una herramienta de apoyo para ingenieros estructurales y estudiantes. Permite determinar el área de acero requerida en vigas y verificar la adecuación de la sección propuesta, considerando las propiedades geométricas, las cargas aplicadas y las características del material.

El algoritmo optimiza la ubicación de las barras respetando rigurosamente el espaciamiento libre mínimo (seleccionando el mayor valor entre **1 pulgada** y el **diámetro de la barra**), asegurando un diseño constructible y apegado a la normativa.

## Características Principales

* **Cálculo Preciso:** Determinación de cuantías mínima, requerida y máxima para asegurar un diseño dúctil.
* **Distribución Automática de Acero:** Algoritmo inteligente que coloca las varillas en la sección transversal respetando el recubrimiento y la separación normativa ($S_{libre} \geq \max(1", d_b)$).
* **Visualización Gráfica:** Generación automática de diagramas de la sección transversal de la viga con la disposición real de los aceros (usando Matplotlib).
* **Reportes Técnicos en PDF:** Exportación directa de una memoria de cálculo profesional en LaTeX, integrando ecuaciones, datos de entrada y gráficos generados.
* **Verificación de Seguridad:** Comprobación automática de que el área de acero proporcionada ($A_{s,prov}$) cubre la demanda ($A_{s,req}$).

## Tecnologías Utilizadas

* **Python:** Lógica de cálculo y control de flujo.
* **Matplotlib:** Generación de gráficos de la sección de la viga.
* **LaTeX:** Maquetación de la memoria de cálculo de alta calidad.
* **Pillow (PIL):** Procesamiento de imágenes para su inserción en reportes.

---
*Desarrollado para facilitar el flujo de trabajo en el diseño de elementos de concreto reforzado.*