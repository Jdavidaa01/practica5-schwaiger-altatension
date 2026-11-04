# Resumen para el informe - Practica 5 (Schwaiger)

## Descripcion de los metodos

**Metodo 1 (simplificado).** Supone que el campo de ruptura Ed del gas no
depende de la distancia entre electrodos, solo de la densidad relativa del
aire delta: Ed = delta * Ed0, donde Ed0 es el campo de ruptura del gas a 1
atmosfera. La tension disruptiva se obtiene aplicando el factor de
utilizacion de Schwaiger eta a la distancia real a:

$$V_d = \eta \cdot E_d \cdot a = \eta \cdot \delta \cdot E_{d0} \cdot a$$

**Metodo 2 (completo).** Usa la distancia ficticia alpha = a * eta y un
campo de ruptura que depende de la distancia mediante la ley de Paschen
para campo homogeneo en aire:

$$V_d = 24{,}22 \cdot \delta \cdot \alpha + 6{,}08 \cdot \sqrt{\delta \cdot \alpha}$$

Para N2 se escala el resultado por la relacion 35/32 como aproximacion,
ya que la ley de Paschen tabulada corresponde al aire.

## Calculo de ejemplo (aire_seco, p_man = 3.5 kg/cm2)

- p_abs = 3130.46 mmHg = 4.1736 bar
- delta = 0,386 * 3130.46 / (273 + 22) = 4.0961
- p = (a + r) / r = (0.25 + 4.0) / 4.0 = 1.0625
- eta (un_polo_a_tierra) interpolado = 97.92 %
- Metodo 1: Vd = 0.9792 * 4.0961 * Ed0 * 0.25 = 32.09 kV
- Metodo 2: alpha = 0.2448 cm -> Vd = 30.38 kV
- Vd medido promedio = 101.93 kV
- Error Metodo 1 = 68.52 % ; Error Metodo 2 = 70.20 %

## Tabla final de resultados

| gas         |   p_man | unidad_presion   |   p_abs_mmHg |   p_abs_bar |   delta |   p_geom |   eta_aplicada_pct |   eta_simetrica_pct |   alpha_cm |   p_s_bar_cm |   Vd_medido_prom_kV |   Vd_medido_std_kV |   Vd_metodo1_kV |   Vd_metodo2_kV |   error1_pct |   error2_pct |
|:------------|--------:|:-----------------|-------------:|------------:|--------:|---------:|-------------------:|--------------------:|-----------:|-------------:|--------------------:|-------------------:|----------------:|----------------:|-------------:|-------------:|
| aire_seco   |     3.5 | kg/cm2           |      3130.46 |       4.174 |   4.096 |    1.062 |             97.925 |              98.125 |      0.245 |        1.043 |             101.933 |              2.203 |          32.089 |          30.376 |       68.52  |       70.2   |
| aire_seco   |     3   | kg/cm2           |      2762.68 |       3.683 |   3.615 |    1.062 |             97.925 |              98.125 |      0.245 |        0.921 |              93     |              0.2   |          28.319 |          27.154 |       69.549 |       70.803 |
| aire_seco   |     2.5 | kg/cm2           |      2394.9  |       3.193 |   3.134 |    1.062 |             97.925 |              98.125 |      0.245 |        0.798 |              80.1   |              0.458 |          24.549 |          23.906 |       69.352 |       70.155 |
| aire_seco   |     2   | kg/cm2           |      2027.12 |       2.703 |   2.652 |    1.062 |             97.925 |              98.125 |      0.245 |        0.676 |              72.633 |              0.473 |          20.779 |          20.627 |       71.392 |       71.602 |
| aire_seco   |     1.5 | kg/cm2           |      1659.34 |       2.212 |   2.171 |    1.062 |             97.925 |              98.125 |      0.245 |        0.553 |              59.067 |              1.002 |          17.009 |          17.307 |       71.203 |       70.7   |
| aire_humedo |     3   | kg/cm2           |      2762.68 |       3.683 |   3.615 |    1.062 |             97.925 |              98.125 |      0.245 |        0.921 |              94.4   |              2.007 |          28.319 |          27.154 |       70.001 |       71.236 |
| aire_humedo |     2.5 | kg/cm2           |      2394.9  |       3.193 |   3.134 |    1.062 |             97.925 |              98.125 |      0.245 |        0.798 |              82.1   |              1.153 |          24.549 |          23.906 |       70.099 |       70.882 |
| aire_humedo |     2   | kg/cm2           |      2027.12 |       2.703 |   2.652 |    1.062 |             97.925 |              98.125 |      0.245 |        0.676 |              73.333 |              1.007 |          20.779 |          20.627 |       71.665 |       71.873 |
| aire_humedo |     1.5 | kg/cm2           |      1659.34 |       2.212 |   2.171 |    1.062 |             97.925 |              98.125 |      0.245 |        0.553 |              67.433 |              1.25  |          17.009 |          17.307 |       74.776 |       74.335 |
| aire_humedo |     1   | kg/cm2           |      1291.56 |       1.722 |   1.69  |    1.062 |             97.925 |              98.125 |      0.245 |        0.43  |              64.42  |              4.708 |          13.239 |          13.931 |       79.449 |       78.374 |
| N2          |     3   | kg/cm2           |      2762.68 |       3.683 |   3.615 |    1.062 |             97.925 |              98.125 |      0.245 |        0.921 |              93.5   |              0.624 |          30.974 |          29.699 |       66.873 |       68.236 |
| N2          |     2.5 | kg/cm2           |      2394.9  |       3.193 |   3.134 |    1.062 |             97.925 |              98.125 |      0.245 |        0.798 |              85.267 |              2.136 |          26.851 |          26.147 |       68.51  |       69.335 |
| N2          |     2   | kg/cm2           |      2027.12 |       2.703 |   2.652 |    1.062 |             97.925 |              98.125 |      0.245 |        0.676 |              71.5   |              0.458 |          22.727 |          22.56  |       68.214 |       68.447 |
| N2          |     1.5 | kg/cm2           |      1659.34 |       2.212 |   2.171 |    1.062 |             97.925 |              98.125 |      0.245 |        0.553 |              68.6   |              4.551 |          18.604 |          18.929 |       72.881 |       72.407 |
| N2          |     1   | kg/cm2           |      1291.56 |       1.722 |   1.69  |    1.062 |             97.925 |              98.125 |      0.245 |        0.43  |              61     |              4.359 |          14.48  |          15.237 |       76.262 |       75.021 |

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
el termino de campo no homogeneo \sqrt{\delta/\alpha} que si incluye el
Metodo 2 a traves de la ley de Paschen. El Metodo 2 suele ajustar mejor a
separaciones pequenas como la de este ensayo (a = 0.25 cm).

**Nota:** los valores de Vd medidos en `datos_practica5.csv` provienen de
un ensayo con esferas de 4,5 cm de diametro y 1,1 cm de separacion
(informe de referencia), mientras que `config.json` usa la geometria de
este trabajo (esferas de 8 cm, separacion
0.25 cm). Esta mezcla de geometrias es una decision
explicita de este ejercicio y no corresponde a un ensayo fisico unico; los
errores relativos deben interpretarse con esa salvedad.
