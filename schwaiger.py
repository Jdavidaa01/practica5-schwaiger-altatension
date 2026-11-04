"""Calculo de la tension disruptiva por el metodo de Schwaiger (Practica 5,
Alta Tension, Universidad de Cuenca). Procesa datos_practica5.csv y
config.json, y genera resultados/ con tablas, graficas y resumen_para_informe.md.
"""

import json
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

BASE_DIR = Path(__file__).resolve().parent
RESULTADOS_DIR = BASE_DIR / "resultados"

# --- Constantes fisicas ---
KGF_CM2_A_MMHG = 735.559
BAR_A_MMHG = 750.062
BAR_A_TORR = 750.06

# Campo de ruptura por atmosfera, kV/(cm*atm)
ED0_GAS = {
    "aire": 32.0,
    "aire_seco": 32.0,
    "aire_humedo": 32.0,  # se aproxima con el valor del aire seco
    "n2": 35.0,
    "o2": 30.0,
    "sf6": 89.0,
}

# Tabla de Schwaiger eta(p, q=1) en porcentaje
TABLA_SCHWAIGER = pd.DataFrame(
    {
        "p": [1, 1.5, 2, 3, 4, 5, 6, 7, 8, 9, 10, 15, 20],
        "simetrica": [100.0, 85.0, 73.2, 56.3, 44.9, 37.2, 31.8, 27.6, 24.4, 21.8, 19.7, 13.3, 10.0],
        "un_polo_a_tierra": [100.0, 83.4, 66.0, 42.8, 30.8, 23.8, 19.3, 16.3, 14.0, 12.3, 11.0, np.nan, np.nan],
        "esfera_plano": [100.0, 73.2, 56.3, 37.2, 27.6, 21.8, 17.8, 15.2, 13.3, 11.7, 10.5, np.nan, np.nan],
    }
)


def convertir_a_mmhg(valor, unidad):
    """Convierte una presion manometrica a mmHg segun su unidad de origen."""
    if unidad == "kg/cm2":
        return valor * KGF_CM2_A_MMHG
    if unidad == "bar":
        return valor * BAR_A_MMHG
    raise ValueError(f"Unidad de presion no reconocida: {unidad}")


def presion_absoluta_mmhg(p_atm_mmhg, p_man_mmhg):
    return p_atm_mmhg + p_man_mmhg


def densidad_relativa(p_abs_mmhg, temperatura_c):
    """delta = 0.386 * p_abs[mmHg] / (273 + T[C])."""
    delta = 0.386 * p_abs_mmhg / (273 + temperatura_c)
    if not (2.0 <= delta <= 8.0):
        print(
            f"Advertencia: delta={delta:.3f} fuera del rango esperado 2-8; "
            "revisar unidades de presion."
        )
    return delta


def promedio_desviacion(vd_valores):
    """Promedio y desviacion estandar (muestral) de las descargas validas (no NaN)."""
    valores = np.array([v for v in vd_valores if pd.notna(v)], dtype=float)
    promedio = valores.mean()
    desviacion = valores.std(ddof=1) if len(valores) > 1 else 0.0
    return promedio, desviacion


def eta_schwaiger(p_geom, columna):
    """Interpola linealmente el factor de utilizacion (%) para p=(a+r)/r dado."""
    tabla = TABLA_SCHWAIGER.dropna(subset=[columna])
    if p_geom < tabla["p"].min() or p_geom > tabla["p"].max():
        print(f"Advertencia: p={p_geom:.3f} fuera del rango tabulado para '{columna}'.")
    return float(np.interp(p_geom, tabla["p"], tabla[columna]))


def metodo1_simplificado(delta, ed0_kv_cm_atm, a_cm, eta_frac):
    """Vd = Ed * a * eta, con Ed = delta * Ed0 (Ed0 no depende de la distancia)."""
    ed = delta * ed0_kv_cm_atm
    return ed * a_cm * eta_frac


def metodo2_completo(delta, a_cm, eta_frac, gas):
    """Vd = 24.22*delta*alpha + 6.08*sqrt(delta*alpha), alpha = a*eta (ley de Paschen, aire).

    Para N2 se escala por 35/32 (aproximacion indicada en el enunciado).
    """
    alpha = a_cm * eta_frac
    vd = 24.22 * delta * alpha + 6.08 * np.sqrt(delta * alpha)
    if gas.lower() in ("n2", "nitrogeno"):
        vd *= 35.0 / 32.0
    return vd, alpha


def error_relativo(vd_calc, vd_medido):
    return abs(vd_calc - vd_medido) / vd_medido * 100.0


def validar_separacion(a_cm, diametro_cm):
    radio = diametro_cm / 2.0
    cumple = a_cm <= radio
    if not cumple:
        print(
            f"Advertencia: a={a_cm} cm supera D/2={radio} cm; "
            "el criterio de esferas (campo cuasi-uniforme) no se cumple."
        )
    return cumple


def cargar_config(ruta=BASE_DIR / "config.json"):
    with open(ruta, "r", encoding="utf-8") as f:
        return json.load(f)


def cargar_datos(ruta=BASE_DIR / "datos_practica5.csv"):
    return pd.read_csv(ruta)


def procesar(df, config):
    """Aplica la cadena de calculo de Schwaiger a cada fila (cada presion ensayada)."""
    diametro = config["diametro_esferas_cm"]
    a_cm = config["separacion_a_cm"]
    temperatura = config["temperatura_C"]
    p_atm_mmhg = config["presion_atm_Cuenca_mmHg"]
    conexion = config["conexion"]

    radio = diametro / 2.0
    p_geom = (a_cm + radio) / radio
    validar_separacion(a_cm, diametro)

    eta_aplicada = eta_schwaiger(p_geom, conexion) / 100.0
    eta_simetrica = eta_schwaiger(p_geom, "simetrica") / 100.0

    columnas_vd = [c for c in df.columns if c.startswith("Vd_") and c.endswith("_kV")]

    filas = []
    for _, fila in df.iterrows():
        gas = fila["gas"]
        p_man_mmhg = convertir_a_mmhg(fila["presion_manometrica"], fila["unidad_presion"])
        p_abs_mmhg = presion_absoluta_mmhg(p_atm_mmhg, p_man_mmhg)
        p_abs_bar = p_abs_mmhg / BAR_A_MMHG
        delta = densidad_relativa(p_abs_mmhg, temperatura)

        vd_prom, vd_std = promedio_desviacion([fila[c] for c in columnas_vd])
        p_s_bar_cm = p_abs_bar * a_cm

        ed0 = ED0_GAS.get(gas.lower().replace(" ", "_"), ED0_GAS["aire"])
        vd1 = metodo1_simplificado(delta, ed0, a_cm, eta_aplicada)
        vd2, alpha = metodo2_completo(delta, a_cm, eta_aplicada, gas)

        err1 = error_relativo(vd1, vd_prom)
        err2 = error_relativo(vd2, vd_prom)

        filas.append(
            {
                "gas": gas,
                "p_man": fila["presion_manometrica"],
                "unidad_presion": fila["unidad_presion"],
                "p_abs_mmHg": p_abs_mmhg,
                "p_abs_bar": p_abs_bar,
                "delta": delta,
                "p_geom": p_geom,
                "eta_aplicada_pct": eta_aplicada * 100.0,
                "eta_simetrica_pct": eta_simetrica * 100.0,
                "alpha_cm": alpha,
                "p_s_bar_cm": p_s_bar_cm,
                "Vd_medido_prom_kV": vd_prom,
                "Vd_medido_std_kV": vd_std,
                "Vd_metodo1_kV": vd1,
                "Vd_metodo2_kV": vd2,
                "error1_pct": err1,
                "error2_pct": err2,
            }
        )

    return pd.DataFrame(filas)


def _formateador_coma(valor, _pos=None):
    return f"{valor:.1f}".replace(".", ",")


def _aplicar_estilo(ax):
    ax.xaxis.set_major_formatter(FuncFormatter(_formateador_coma))
    ax.yaxis.set_major_formatter(FuncFormatter(_formateador_coma))
    ax.set_facecolor("white")
    ax.legend()


def graficar_vd_vs_presion(df, out_dir):
    fig, ax = plt.subplots(figsize=(7, 5), facecolor="white")
    for gas, grupo in df.groupby("gas"):
        grupo = grupo.sort_values("p_abs_bar")
        ax.plot(grupo["p_abs_bar"], grupo["Vd_medido_prom_kV"], marker="o", label=gas)
    ax.set_xlabel("Presion absoluta (bar)")
    ax.set_ylabel("Vd medido (kV)")
    _aplicar_estilo(ax)
    fig.savefig(out_dir / "vd_vs_presion_absoluta.png", dpi=300)
    plt.close(fig)


def graficar_vd_vs_ps(df, out_dir):
    fig, ax = plt.subplots(figsize=(7, 5), facecolor="white")
    for gas, grupo in df.groupby("gas"):
        grupo = grupo.sort_values("p_s_bar_cm")
        ax.plot(grupo["p_s_bar_cm"], grupo["Vd_medido_prom_kV"], marker="o", label=gas)
    ax.set_xlabel("Producto p·s (bar·cm)")
    ax.set_ylabel("Vd medido (kV)")
    _aplicar_estilo(ax)
    fig.savefig(out_dir / "vd_vs_ps.png", dpi=300)
    plt.close(fig)


def graficar_comparacion_metodos(df, out_dir):
    for gas, grupo in df.groupby("gas"):
        grupo = grupo.sort_values("p_abs_bar")
        fig, ax = plt.subplots(figsize=(7, 5), facecolor="white")
        ax.plot(grupo["p_abs_bar"], grupo["Vd_medido_prom_kV"], marker="o", label="Vd medido")
        ax.plot(grupo["p_abs_bar"], grupo["Vd_metodo1_kV"], marker="s", label="Metodo 1")
        ax.plot(grupo["p_abs_bar"], grupo["Vd_metodo2_kV"], marker="^", label="Metodo 2")
        ax.set_xlabel("Presion absoluta (bar)")
        ax.set_ylabel("Vd (kV)")
        _aplicar_estilo(ax)
        fig.savefig(out_dir / f"comparacion_{gas}.png", dpi=300)
        plt.close(fig)


def graficar_errores(df, out_dir):
    fig, ax = plt.subplots(figsize=(7, 5), facecolor="white")
    for gas, grupo in df.groupby("gas"):
        grupo = grupo.sort_values("p_abs_bar")
        ax.plot(grupo["p_abs_bar"], grupo["error1_pct"], marker="s", linestyle="--", label=f"{gas} - Metodo 1")
        ax.plot(grupo["p_abs_bar"], grupo["error2_pct"], marker="^", linestyle="--", label=f"{gas} - Metodo 2")
    ax.set_xlabel("Presion absoluta (bar)")
    ax.set_ylabel("Error relativo (%)")
    _aplicar_estilo(ax)
    fig.savefig(out_dir / "error_relativo.png", dpi=300)
    plt.close(fig)


def exportar_tablas(df, out_dir):
    df.to_csv(out_dir / "resultados.csv", index=False, float_format="%.4f")
    df.to_excel(out_dir / "resultados.xlsx", index=False)


def escribir_resumen(df, config, out_dir):
    fila_ejemplo = df.iloc[0]
    radio = config["diametro_esferas_cm"] / 2.0

    tabla_md = df.round(3).to_markdown(index=False)

    contenido = f"""# Resumen para el informe - Practica 5 (Schwaiger)

## Descripcion de los metodos

**Metodo 1 (simplificado).** Supone que el campo de ruptura Ed del gas no
depende de la distancia entre electrodos, solo de la densidad relativa del
aire delta: Ed = delta * Ed0, donde Ed0 es el campo de ruptura del gas a 1
atmosfera. La tension disruptiva se obtiene aplicando el factor de
utilizacion de Schwaiger eta a la distancia real a:

$$V_d = \\eta \\cdot E_d \\cdot a = \\eta \\cdot \\delta \\cdot E_{{d0}} \\cdot a$$

**Metodo 2 (completo).** Usa la distancia ficticia alpha = a * eta y un
campo de ruptura que depende de la distancia mediante la ley de Paschen
para campo homogeneo en aire:

$$V_d = 24{{,}}22 \\cdot \\delta \\cdot \\alpha + 6{{,}}08 \\cdot \\sqrt{{\\delta \\cdot \\alpha}}$$

Para N2 se escala el resultado por la relacion 35/32 como aproximacion,
ya que la ley de Paschen tabulada corresponde al aire.

## Calculo de ejemplo ({fila_ejemplo['gas']}, p_man = {fila_ejemplo['p_man']} {fila_ejemplo['unidad_presion']})

- p_abs = {fila_ejemplo['p_abs_mmHg']:.2f} mmHg = {fila_ejemplo['p_abs_bar']:.4f} bar
- delta = 0,386 * {fila_ejemplo['p_abs_mmHg']:.2f} / (273 + {config['temperatura_C']}) = {fila_ejemplo['delta']:.4f}
- p = (a + r) / r = ({config['separacion_a_cm']} + {radio}) / {radio} = {fila_ejemplo['p_geom']:.4f}
- eta ({config['conexion']}) interpolado = {fila_ejemplo['eta_aplicada_pct']:.2f} %
- Metodo 1: Vd = {fila_ejemplo['eta_aplicada_pct']/100:.4f} * {fila_ejemplo['delta']:.4f} * Ed0 * {config['separacion_a_cm']} = {fila_ejemplo['Vd_metodo1_kV']:.2f} kV
- Metodo 2: alpha = {fila_ejemplo['alpha_cm']:.4f} cm -> Vd = {fila_ejemplo['Vd_metodo2_kV']:.2f} kV
- Vd medido promedio = {fila_ejemplo['Vd_medido_prom_kV']:.2f} kV
- Error Metodo 1 = {fila_ejemplo['error1_pct']:.2f} % ; Error Metodo 2 = {fila_ejemplo['error2_pct']:.2f} %

## Tabla final de resultados

{tabla_md}

## Comentarios tecnicos

La ley de Paschen predice que, en la rama derecha de la curva (productos
p*s altos, como en este ensayo), Vd crece de forma aproximadamente lineal
con el producto p*s. Esa tendencia debe verse en `vd_vs_ps.png`: cada gas
describe una curva creciente y monotonica.

En la comparacion entre gases, el N2 deberia acercarse al aire seco en
rigidez dielectrica (Ed0 mayor, 35 frente a 32 kV/(cm*atm)), mientras que
el aire humedo se aproxima al aire seco porque el vapor de agua captura
electrones y eleva ligeramente la rigidez.

Entre metodos, el Metodo 1 (Ed independiente de la distancia) tiende a
desviarse mas cuanto menor es la distancia ficticia alpha, porque ignora
el termino de campo no homogeneo \\sqrt{{\\delta/\\alpha}} que si incluye el
Metodo 2 a traves de la ley de Paschen. El Metodo 2 suele ajustar mejor a
separaciones pequenas como la de este ensayo (a = {config['separacion_a_cm']} cm).

**Nota:** los valores de Vd medidos en `datos_practica5.csv` provienen de
un ensayo con esferas de 4,5 cm de diametro y 1,1 cm de separacion
(informe de referencia), mientras que `config.json` usa la geometria de
este trabajo (esferas de {config['diametro_esferas_cm']} cm, separacion
{config['separacion_a_cm']} cm). Esta mezcla de geometrias es una decision
explicita de este ejercicio y no corresponde a un ensayo fisico unico; los
errores relativos deben interpretarse con esa salvedad.
"""
    with open(out_dir / "resumen_para_informe.md", "w", encoding="utf-8") as f:
        f.write(contenido)


def main():
    RESULTADOS_DIR.mkdir(exist_ok=True)

    config = cargar_config()
    df_datos = cargar_datos()
    df_resultados = procesar(df_datos, config)

    exportar_tablas(df_resultados, RESULTADOS_DIR)
    graficar_vd_vs_presion(df_resultados, RESULTADOS_DIR)
    graficar_vd_vs_ps(df_resultados, RESULTADOS_DIR)
    graficar_comparacion_metodos(df_resultados, RESULTADOS_DIR)
    graficar_errores(df_resultados, RESULTADOS_DIR)
    escribir_resumen(df_resultados, config, RESULTADOS_DIR)

    pd.set_option("display.max_columns", None)
    pd.set_option("display.width", 160)
    print(df_resultados.round(3))

    return df_resultados


if __name__ == "__main__":
    main()
