
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
st.set_page_config(page_title="EcoGraph - Emilia Arriaga")

def mercado_dinero(Y, P, B, r, e, ax, limite_superior_i):
    k = 0.5
    h = 100
    mm = (e + 1) / (e + r)
    M = mm * B               # Oferta monetaria nominal M
    L = M / P                # Oferta monetaria real L = M/P

    i_vals = np.linspace(0, limite_superior_i, 100)
    Md = k * Y - h * i_vals
    i_eq = (k * Y - L) / h

    ax.plot(Md, i_vals, label='Curva de Demanda de Dinero (Md)', color='blue')
    ax.axvline(L, color='red', linestyle='--', label='Oferta Monetaria Real (L = M/P)')
    ax.plot([L], [i_eq], 'ko', label=f"Equilibrio: i = {i_eq:.2f}")

    ax.set_xlabel('M/P (Dinero Real)')
    ax.set_ylabel('Tasa de interés (i)')
    ax.set_title('Mercado de Dinero')
    ax.set_xlim(0, max(L, Md.max()) * 1.1)
    ax.set_ylim(0, limite_superior_i)
    ax.legend()
    ax.grid(True)
    return i_eq

def demanda_inversion(I0, b, i, ax, limite_superior_i):
    i_vals = np.linspace(0, limite_superior_i, 100)
    I_vals = I0 - b * i_vals

    ax.plot(I_vals, i_vals, label="Curva de Inversión", color='orange')
    ax.plot([I0 - b * i], [i], 'ko', label=f"i = {i:.2f}")

    ax.set_xlabel("Inversión (I)")
    ax.set_ylabel("Tasa de interés (i)")
    ax.set_title("Demanda de Inversión")
    x_min = min(I_vals) * 1.1 if min(I_vals) < 0 else 0
    x_max = max(I_vals) * 1.1
    ax.set_xlim(x_min, x_max)
    ax.set_ylim(0, limite_superior_i)
    ax.legend()
    ax.grid(True)

def mercado_bienes(Y_max, c, t, I0, G, X, m, i, b, ax):
    Y = np.linspace(0, Y_max, 100)
    C = c * (1 - t) * Y
    I = I0 - b * i
    M = m * Y
    DA = C + I + G + X - M
    DA_limited = np.minimum(DA, Y_max)

    ax.plot(Y, DA_limited, label="DA = C + I + G + X - M", color='purple')
    ax.plot(Y, Y, linestyle='--', label="45°: Y = DA", color='gray')

    ax.set_xlabel("Ingreso (Y)")
    ax.set_ylabel("Demanda Agregada (DA)")
    ax.set_title("Mercado de Bienes")
    ax.set_xlim(0, Y_max)
    ax.set_ylim(0, Y_max)
    ax.legend()
    ax.grid(True)

def main():
    st.title("Modelo IS-LM Interactivo")

    # Variables exógenas con sliders
    Y = st.slider("Ingreso (Y)", 500, 1000, 1000, step=100)
    P = st.slider("Nivel de Precios (P)", 1.0, 20.0, 10.0)
    B = st.slider("Base Monetaria (B)", 500, 5000, 2000, step=100)
    r = st.slider("Coeficiente de Encaje (r)", 0.01, 1.0, 0.1, step=0.01)
    e = st.slider("E/D (e)", 0.01, 1.0, 0.1, step=0.01)
    c = st.slider("Propensión Marginal a Consumir (c)", 0.1, 1.0, 0.8, step=0.05)
    t = st.slider("Tasa Impositiva (t)", 0.0, 0.5, 0.2, step=0.05)
    I0 = st.slider("Inversión Autónoma (I0)", 50, 300, 150, step=10)
    G = st.slider("Gasto Público (G)", 100, 500, 200, step=50)
    X = st.slider("Exportaciones (X)", 0, 300, 100, step=10)
    m = st.slider("Propensión a Importar (m)", 0.0, 0.5, 0.1, step=0.05)
    b = st.slider("Sensibilidad inversión a tasa (b)", 50, 500, 300, step=25)

    # Crear figura y ejes para gráficos
    fig, axs = plt.subplots(1, 3, figsize=(20, 5))

    # Cálculo del límite superior de i para los gráficos
    k = 0.5
    mm = (e + 1) / (e + r)
    M = mm * B
    L = M / P
    i_max_mdinero = (k * Y) / 100 * 1.2
    i_max_inversion = (I0 / b) * 1.2
    limite_superior_i = max(i_max_mdinero, i_max_inversion)

    i_eq = mercado_dinero(Y, P, B, r, e, axs[0], limite_superior_i)
    demanda_inversion(I0, b, i_eq, axs[1], limite_superior_i)
    mercado_bienes(1000, c, t, I0, G, X, m, i_eq, b, axs[2])

    st.pyplot(fig)

if __name__ == "__main__":
    main()
