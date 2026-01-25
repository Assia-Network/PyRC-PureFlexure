# Viga-Flexion-Pura 

**Herramienta de automatización para el diseño y verificación de vigas de concreto reforzado sometidas a flexión pura.**

## Descripción

Esta aplicación ha sido desarrollada como una herramienta de apoyo para ingenieros estructurales y estudiantes. Permite determinar el área de acero requerida en vigas y verificar la adecuación de la sección propuesta, considerando las propiedades geométricas, las cargas aplicadas y las características del material.

El algoritmo optimiza la ubicación de las barras respetando rigurosamente el espaciamiento libre mínimo (seleccionando el mayor valor entre **1 pulgada** y el **diámetro de la barra**), asegurando un diseño constructible y apegado a la normativa.

## Características Principales

* **Cálculo Preciso:** Determinación de cuantías mínima, requerida y máxima para asegurar un diseño dúctil.
* **Distribución Automática de Acero:** Algoritmo inteligente que coloca las varillas en la sección transversal respetando el recubrimiento y la separación normativa ($S_{libre} \geq \max(1'', d_b)$).
* **Visualización Gráfica:** Generación automática de diagramas de la sección transversal de la viga con la disposición real de los aceros (usando Matplotlib).
* **Reportes Técnicos en PDF:** Exportación directa de una memoria de cálculo profesional en LaTeX, integrando ecuaciones, datos de entrada y gráficos generados.
* **Verificación de Seguridad:** Comprobación automática de que el área de acero proporcionada ($A_{s,prop}$) cubre la demanda ($A_{s,req}$).

## Tecnologías Utilizadas

* **Python:** Lógica de cálculo y control de flujo.
* **Matplotlib:** Generación de gráficos de la sección de la viga.
* **LaTeX:** Maquetación de la memoria de cálculo de alta calidad.
* **Pillow (PIL):** Procesamiento de imágenes para su inserción en reportes.

---
*Desarrollado para facilitar el flujo de trabajo en el diseño de elementos de concreto reforzado.*

## Descargar App Compilada

[![Descargar App Linux](https://img.shields.io/badge/DESCARGAR_APP-Linux_Ubuntu-00bb2d?style=for-the-badge&logo=linux&logoColor=white)](https://github.com/Assia-Network/PyRC-PureFlexure/releases/download/Downloads/linux_PyRC-PureFlexure.zip)

[![Descargar App Windows](https://img.shields.io/badge/DESCARGAR_APP-Windows-0078D6?style=for-the-badge&logo=windows11&logoColor=white)](https://github.com/Assia-Network/PyRC-PureFlexure/releases/download/windows/PyRC-PureFlexure.exe)

## Requisitos del Sistema

La aplicación es **portable** y la mayoría de sus funciones (cálculo de acero, gráficos) funcionan sin necesidad de instalar nada extra.

Sin embargo, **únicamente para utilizar la función de Generación de Reportes PDF**, es necesario tener instalado un compilador de LaTeX en tu sistema.

A continuación, sigue los pasos según tu sistema operativo:

### 🐧 Para usuarios de Linux (Ubuntu/Debian/Mint)
Abre tu terminal y ejecuta el siguiente comando:

```bash
sudo apt-get update
sudo apt-get install texlive-latex-base texlive-fonts-recommended
```

### 🔲 Para usuarios de Windows (10-11)
Necesitas instalar una distribución de LaTeX llamada **MiKTeX**.

1.  **Descargar:** Ve al sitio oficial y descarga el instalador: [**Descargar MiKTeX**](https://miktex.org/download).
2.  **Verificar:** Una vez descargado, abre tu cmd y ejecuta el siguiente comando:
```bash
pdflatex --version
```
3.  **Instalar:** Ejecuta el archivo descargado y sigue las instrucciones (la configuración por defecto está bien).
4.  ⚠️ **IMPORTANTE:** Al terminar, **reinicia tu computadora**. Esto es obligatorio para que el sistema reconozca el comando `pdflatex`.