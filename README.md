# Practica 5 - Descargas en gases aislantes (metodo de Schwaiger)

## Requisitos

- Python 3.11 o superior (se uso Python 3.13.9 de Anaconda en este equipo).
- Entorno virtual `.venv` ya creado en esta carpeta.

## Instalacion

```powershell
.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## Datos de entrada

- `datos_practica5.csv`: una fila por presion ensayada, con gas, presion
  manometrica, unidad (`kg/cm2` o `bar`) y las descargas Vd (columnas
  `Vd_1_kV` ... `Vd_5_kV`, las que apliquen; dejar vacias las que no se
  usaron).
- `config.json`: diametro de las esferas, separacion `a`, temperatura,
  presion atmosferica local y tipo de conexion (`un_polo_a_tierra` o
  `simetrica`).

## Ejecucion

```powershell
.venv\Scripts\python.exe schwaiger.py
```

Esto imprime la tabla de resultados en consola, genera en `resultados/`:

- `resultados.csv` y `resultados.xlsx`
- `vd_vs_presion_absoluta.png`, `vd_vs_ps.png`, `comparacion_<gas>.png`,
  `error_relativo.png`
- `resumen_para_informe.md`

y abre automaticamente `simulador_schwaiger.html` en el navegador
predeterminado: una calculadora interactiva (sliders de diametro,
separacion, temperatura y presion atmosferica) que recalcula eta, delta
y los dos metodos de Schwaiger en vivo. Es un archivo HTML autocontenido
(sin servidor ni conexion a internet necesarios salvo para las
tipografias); tambien se puede abrir con doble clic sin correr el
script.

## Nota sobre los datos de esta corrida

Los valores de Vd en `datos_practica5.csv` corresponden al informe de
referencia (esferas de 4,5 cm de diametro, separacion 1,1 cm), mientras
que `config.json` usa la geometria de este trabajo (esferas de 8 cm,
separacion 0,25 cm). Esta combinacion fue una decision explicita para
esta corrida y produce errores relativos altos (~70 %) frente al metodo
de Schwaiger, porque no corresponde a un unico ensayo fisico real. Para
resultados comparables con mediciones propias, se debe reemplazar
`datos_practica5.csv` con los Vd medidos realmente con las esferas de
8 cm.
