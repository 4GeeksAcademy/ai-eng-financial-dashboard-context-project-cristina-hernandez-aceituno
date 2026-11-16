# Spec: Funcionalidades financieras y contratos de API

## Proposito y alcance

Esta spec mapea las tres funcionalidades del ejercicio a los endpoints y modelos que realmente expone el backend. Los contratos se contrastaron con `/openapi.json`, el codigo de `backend/app/routes.py` y consultas HTTP reales. Esta spec documenta el comportamiento existente; no solicita cambios de implementacion.

## Vocabulario de producto y API

| Wording de producto | Campo o calculo real | Aclaracion |
| --- | --- | --- |
| Ingresos | `income` en el resumen; movimientos con `operation_type=income` | La comparativa B2B/B2C debe comparar importes `income`, no el neto. |
| Gastos | `outcome` | La API usa `outcome` para importes de salida. |
| Beneficio neto | `net` en el resumen; `profit` en el KPI del frontend | `net` representa `income - outcome`. No es el valor solicitado para comparar ingresos B2B/B2C. |
| Porcentaje de beneficio | No existe como campo de API | El frontend actual lo calcula como `(income - outcome) / income * 100`; devuelve `0` cuando `income` es cero. No forma parte de las tres funcionalidades de esta spec. |
| Umbral de anomalia | `threshold` y respuesta `increase_ratio` | Ambos son proporciones: `0.3` equivale a 30%; para presentar `increase_ratio` como porcentaje, multiplicar por 100. |
| Periodo agrupado | `group_by` y `period` | `group_by` admite `day`, `week` y `month`; `period` identifica el grupo de la respuesta. |

Los nombres de producto pueden conservarse en la interfaz. Para describir contratos HTTP se usan los campos y valores reales de la API.

## 1. Filtro por rango de fechas

- **Endpoint:** `GET /api/metrics`
- **Parametros:**
  - `start_date`: fecha opcional `YYYY-MM-DD`; limite inicial inclusivo.
  - `end_date`: fecha opcional `YYYY-MM-DD`; limite final inclusivo.
  - `category`: opcional; `suppliers`, `sales`, `operational`, `administrative` u `others`.
  - `operation_type`: opcional; `income` u `outcome`.
- **Respuesta 200:** lista de movimientos `FinancialMovement`, cada uno con `create_date`, `amount`, `operation_type`, `category` y `business_type` (`B2B` o `B2C`). No hay objeto envolvente, total de resultados ni paginacion.
- **Trabajo del frontend:** enviar las fechas y presentar los movimientos devueltos; no necesita aplicar de nuevo el filtro de fechas.
- **Limitaciones:** no existe paginacion. Las fechas sin movimientos simplemente no aparecen en la lista.
- **Verificacion:** `GET /api/metrics?start_date=2026-09-01&end_date=2026-09-30` respondio `200` con 30 movimientos, desde `2026-09-02` hasta `2026-09-28`.

## 2. Tabla de anomalias de gastos con umbral configurable

- **Endpoint:** `GET /api/metrics/alerts`
- **Parametros:**
  - `threshold`: numero opcional, minimo `0`, por defecto `0.3`.
  - `group_by`: opcional, `day`, `week` o `month`; por defecto `month`.
  - `start_date`, `end_date`: fechas opcionales `YYYY-MM-DD`.
  - `business_type`: opcional, `B2B` o `B2C`.
- **Respuesta 200:** lista de objetos `MetricsAlert` con `period`, `outcome_total`, `baseline_average` e `increase_ratio`.
- **Calculo realizado por el backend:** suma `outcome` por periodo, compara cada periodo con el promedio de los periodos anteriores incluidos y devuelve una alerta cuando la linea base es mayor que cero y `(outcome_actual - baseline_average) / baseline_average > threshold`. La comparacion es estricta.
- **Trabajo del frontend:** presentar las filas devueltas. No debe volver a detectar anomalías; si muestra el aumento como porcentaje, convierte `increase_ratio` multiplicandolo por 100.
- **Limitaciones:**
  - No admite `category` ni `operation_type`; analiza el total de `outcome`.
  - El primer periodo no puede generar alerta porque no tiene linea base previa.
  - `start_date` tambien limita el historico usado para la linea base. La API no separa el rango de visualizacion del rango historico.
  - `threshold=0.3` significa 30%. OpenAPI define minimo cero y no declara maximo.
- **Verificacion:** con `threshold=0.3`, `group_by=month`, `start_date=2025-11-01` y `end_date=2026-10-28`, la API respondio `200` con cuatro alertas:

| Periodo | `outcome_total` | `baseline_average` | `increase_ratio` |
| --- | ---: | ---: | ---: |
| 2025-12 | 103378.98 | 41404.44 | 1.4968 |
| 2026-03 | 88076.90 | 55334.29 | 0.5917 |
| 2026-06 | 80212.01 | 57416.50 | 0.3970 |
| 2026-08 | 82189.37 | 60291.89 | 0.3632 |

## 3. Comparativa de ingresos B2B vs. B2C

- **Endpoint recomendado:** dos llamadas a `GET /api/metrics/summary`, una con `business_type=B2B` y otra con `business_type=B2C`.
- **Parametros relevantes:**
  - `business_type`: opcional, `B2B` o `B2C`; una solicitud selecciona un solo segmento.
  - `group_by`: opcional, `day`, `week` o `month`; por defecto `month`.
  - `start_date`, `end_date`: fechas opcionales `YYYY-MM-DD`; mantener iguales en ambas llamadas.
  - `category`: filtro opcional por categoria.
  - `operation_type`: filtro opcional `income` u `outcome`; puede omitirse y comparar el campo `income` de la respuesta.
- **Respuesta 200:** lista de `{ period, income, outcome, net }`.
- **Trabajo del frontend:** emparejar las dos listas por `period` y comparar o graficar `income`. No comparar `net`, porque representa ingresos menos gastos.
- **Alternativa:** `GET /api/metrics/b2b` y `GET /api/metrics/b2c` aceptan `start_date`, `end_date`, `category` y `operation_type`, y devuelven listas `FinancialMovement`. Si se usan, el frontend debe filtrar o solicitar `operation_type=income` y sumar `amount` por periodo.
- **Limitaciones:** no hay endpoint que devuelva ambos segmentos a la vez. El resumen requiere dos solicitudes; las rutas segmentadas devuelven movimientos sin agregar.
- **Verificacion:** con `group_by=month`, `start_date=2025-11-01` y `end_date=2026-10-28`, ambas llamadas al resumen respondieron `200` con 12 periodos. Para `2025-11`, `income` fue `54757.96` (B2B) y `56268.85` (B2C); para `2026-10`, `income` fue `39038.91` (B2B) y `67870.76` (B2C).

## Relacion con el frontend actual

El dashboard actualmente consume solo `GET /api/metrics`, que devuelve movimientos. Sus KPIs y datos mensuales se calculan localmente; las rutas de alertas, resumen y segmentos no estan conectadas al frontend. Los resultados agregados de esta spec no deben tratarse como `FinancialMovement[]`.

## Referencias

- `backend/app/routes.py`: modelos, filtros, agrupacion, alertas y endpoints.
- `frontend/src/App.tsx`: solicitud actual a `/api/metrics`.
- `frontend/src/lib/financial-utils.ts`: calculos locales de KPIs y agrupacion mensual.
- `memory-bank/api-exploration.md`: analisis validado y detalle de consultas reales.