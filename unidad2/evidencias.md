# Evidencias — Auditoría de equidad, mitigación y explicabilidad

_Generado automáticamente el 2026-10-19 04:45._

## Configuración de la corrida

- **Dataset:** data/compas_limpio.csv
- **Columna objetivo:** `two_year_recid` (clase positiva: `1`)
- **Atributo sensible:** `race`
- **Método de mitigación:** `exponentiated_gradient`
- **Restricción de equidad:** `demographic_parity`

## Auditoría de equidad — modelo base (pre-mitigación)

- **Exactitud global:** 0.676
- **Demographic parity difference:** 0.522
- **Equalized odds difference:** 0.685

### Métricas por grupo

| Grupo | Exactitud | Tasa de selección |
|---|---|---|
| African-American | 0.676 | 0.522 |
| Asian | 0.727 | 0.000 |
| Caucasian | 0.667 | 0.262 |
| Hispanic | 0.660 | 0.184 |
| Native American | 0.500 | 0.500 |
| Other | 0.763 | 0.186 |

> TODO estudiante: interpretá esta tabla vinculándola con el sesgo documentado en el caso real analizado en la consigna 3 (¿el patrón que ves acá es consistente con lo que reportó el caso?).
>el grupo con mayor tasa de selección de alto riesgo es notablemente más alto que el resto (más del doble que varios otros grupos), mientras que la exactitud se mantiene relativamente pareja entre los grupos con volumen suficiente de datos. Esto reproduce el hallazgo central del caso real: un modelo puede tener un desempeño global aceptable y aun así marcar a un grupo racial como de alto riesgo con mucha más frecuencia que a los demás, que es justamente el tipo de disparidad que denunció ProPublica en 2016. Los grupos con muy pocos casos (Asian, Native American) muestran métricas poco confiables, lo que es otra forma del mismo problema: los grupos minoritarios en el dataset quedan peor representados en la evaluación del modelo.

## Comparación antes / después de la mitigación

| Escenario | Exactitud | Demographic parity diff. | Equalized odds diff. |
|---|---|---|---|
| Modelo base (sin mitigar) | 0.676 | 0.522 | 0.685 |
| ExponentiatedGradient | 0.663 | 0.151 | 0.724 |

![Comparación de métricas de equidad](outputs/comparacion_metricas.png)

> TODO estudiante: discutí qué tan efectiva resultó la mitigación aplicada y qué limitaciones observaste (consigna 9.c) — por ejemplo, si mejoró la equidad pero bajó la exactitud, o si algún escenario no logró reducir la disparidad.
>La mitigación con ExponentiatedGradient fue efectiva específicamente en la métrica que se le pidió optimizar: la demographic parity difference cayó de 0.522 a 0.151, esto implica una reducción de más del 70%, prácticamente llevando esa disparidad a un nivel bajo y a un costo muy acotado en exactitud. Esto confirma que, cuando el objetivo de equidad está bien definido, Fairlearn puede corregir la disparidad de forma contundente sin sacrificar demasiado desempeño predictivo

## Explicabilidad (SHAP) — modelo base

SHAP se aplica siempre sobre el modelo base, antes de cualquier mitigación: el objetivo es ver qué técnica de auditoría preventiva podría haber detectado el problema antes del despliegue (consigna 4).

### Predicción 191 — el atributo sensible más influyó

- Contribución absoluta de `race`: 0.645
- Predicción del modelo: 0 · Valor real: 0

![SHAP de la predicción donde el modelo discrimina](outputs/shap_prediccion_discrimina.png)

### Predicción 1 — el atributo sensible casi no influyó

- Contribución absoluta de `race`: 0.168
- Predicción del modelo: 1 · Valor real: 1

![SHAP de la predicción donde el modelo no discrimina](outputs/shap_prediccion_no_discrimina.png)

### Resumen global

![Resumen SHAP de todas las predicciones de test](outputs/shap_resumen.png)

> TODO estudiante: vinculá esta evidencia con la consigna 4 — ¿SHAP sobre el modelo base hubiera permitido detectar este problema antes del despliegue?
>Sí, SHAP sobre el modelo base hubiera dado una señal de alerta preventiva: en el resumen global, race aparece con contribución sistemática (no ruido) sobre la salida del modelo, y al comparar casos individuales se ve que su peso varía fuertemente. En la predicción 191 race_Asian es el segundo factor en magnitud (-0.5), mientras que en la predicción 1 la variable racial casi no pesa (+0.09). Eso ya alcanza para sospechar que el atributo sensible influye de forma relevante y despareja. Lo que SHAP no hace es cuantificar la disparidad agregada entre grupos (eso lo dan las métricas de equidad), así que funciona como complemento, no como reemplazo, de esas métricas.
