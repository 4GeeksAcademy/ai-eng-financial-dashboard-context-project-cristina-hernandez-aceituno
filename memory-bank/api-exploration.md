# Exploracion de API: funcionalidades del ejercicio

**Fecha de verificacion:** 2026-11-16  
**Alcance:** Analisis documental y consultas HTTP de solo lectura. No se modifico la implementacion.

## Metodo y entorno

Se contrastaron los contratos expuestos por `GET /openapi.json` (el esquema que utiliza Swagger en `/docs`) con los modelos y funciones de `backend/app/routes.py`. Las consultas reales se ejecutaron contra el backend local en `http://localhost:8000`. La URL publica de Codespaces redirigio esta terminal a la autenticacion de GitHub, por lo que las pruebas no se hicieron contra el tunel remoto.

Los ejemplos de respuesta que siguen son los observados durante esta ejecucion; la API utiliza datos mock.

## 1. Filtro por rango de fechas

**Endpoint principal:** `GET /api/metrics`

**Parametros:**

| Parametro | Tipo / valores | Obligatorio | Uso |
| --- | --- | --- | --- |
| `start_date` | fecha `YYYY-MM-DD` | No | Limite inicial inclusivo. |
| `end_date` | fecha `YYYY-MM-DD` | No | Limite final inclusivo. |
| `category` | `suppliers`, `sales`, `operational`, `administrative`, `others` | No | Filtro adicional de categoria. |
| `operation_type` | `income` o `outcome` | No | Filtro adicional por tipo de movimiento. |

**Respuesta 200:** lista de movimientos `FinancialMovement`. Cada objeto contiene los campos requeridos `create_date` (fecha), `amount` (numero), `operation_type`, `category` y `business_type` (`B2B` o `B2C`). No devuelve un objeto envolvente, total de resultados ni paginacion.

**Responsabilidad del frontend:** recoger las fechas, enviarlas como query params y mostrar los movimientos devueltos. No necesita volver a filtrar por fechas. Puede combinar con `category` y `operation_type` si el producto lo requiere.

**Verificacion real:**

```text
GET /api/metrics?start_date=2026-09-01&end_date=2026-09-30
HTTP 200; 30 movimientos
Primer create_date: 2026-09-02
Ultimo create_date: 2026-09-28
```

Los dias 1 y 30 no aparecen en esta muestra porque no se genero ningun movimiento en esas fechas; el backend admite ambos limites inclusivamente.

## 2. Tabla de anomalias de gastos con umbral configurable

**Endpoint:** `GET /api/metrics/alerts`

**Parametros:**

| Parametro | Tipo / valores | Obligatorio | Valor por defecto / uso |
| --- | --- | --- | --- |
| `threshold` | numero, minimo `0` | No | `0.3`; proporcion, no porcentaje entero. |
| `group_by` | `day`, `week`, `month` | No | `month`. Define el periodo de agregacion. |
| `start_date`, `end_date` | fecha `YYYY-MM-DD` | No | Acotan los movimientos usados en el calculo. |
| `business_type` | `B2B` o `B2C` | No | Permite limitar el calculo a un segmento. |

**Respuesta 200:** lista de `MetricsAlert` con `period`, `outcome_total`, `baseline_average` e `increase_ratio`, todos requeridos. `increase_ratio` es una proporcion: por ejemplo, `0.3632` representa `36.32%`.

**Calculo confirmado en backend:** primero suma `outcome` por periodo. Para cada periodo posterior al primero, calcula la media de los gastos de los periodos anteriores incluidos. Emite una alerta solo cuando la linea base es mayor que cero y `(outcome_actual - baseline_average) / baseline_average > threshold`. La comparacion es estricta (`>`).

**Responsabilidad del frontend:** mostrar la tabla y, si presenta el aumento como porcentaje, multiplicar `increase_ratio` por 100. El backend ya realiza la deteccion; el frontend no debe recalcular la anomalia.

**Limitaciones:**

- La API no acepta `category` ni `operation_type` para alertas; calcula aumentos del total de `outcome`.
- El primer periodo del resultado no puede generar alerta porque no tiene periodos anteriores en el conjunto consultado.
- `start_date` tambien recorta el historico usado para calcular la media. Para mostrar alertas de un intervalo, la consulta debe incluir periodos anteriores suficientes; la API no separa el rango de visualizacion del rango de referencia.
- `threshold=0.3` equivale a 30%; no hay limite superior documentado, solo minimo cero.

**Verificacion real:**

```text
GET /api/metrics/alerts?threshold=0.3&group_by=month&start_date=2025-11-01&end_date=2026-10-28
HTTP 200; 4 alertas
```

| Periodo | `outcome_total` | `baseline_average` | `increase_ratio` |
| --- | ---: | ---: | ---: |
| 2025-12 | 103378.98 | 41404.44 | 1.4968 |
| 2026-03 | 88076.90 | 55334.29 | 0.5917 |
| 2026-06 | 80212.01 | 57416.50 | 0.3970 |
| 2026-08 | 82189.37 | 60291.89 | 0.3632 |

## 3. Comparativa de ingresos B2B vs. B2C

**Opcion recomendada:** consultar dos veces `GET /api/metrics/summary`, con los mismos filtros y `business_type=B2B` y `business_type=B2C` respectivamente.

**Parametros relevantes de `/api/metrics/summary`:**

| Parametro | Tipo / valores | Obligatorio | Uso |
| --- | --- | --- | --- |
| `business_type` | `B2B` o `B2C` | No | Selecciona un solo segmento por solicitud. |
| `group_by` | `day`, `week`, `month` | No | Por defecto `month`; determina la granularidad comparable. |
| `start_date`, `end_date` | fecha `YYYY-MM-DD` | No | Deben ser iguales en ambas solicitudes. |
| `operation_type` | `income` o `outcome` | No | Puede fijarse a `income` para expresar la intencion; tambien se puede omitir y leer el campo `income`. |
| `category` | enumeracion de categorias | No | Filtro adicional; omitir para incluir todas las categorias. |

**Respuesta 200:** lista de `{ period, income, outcome, net }`. El frontend debe emparejar ambas listas por `period` y comparar o graficar el campo `income`; no debe usar `net` para una comparativa de ingresos.

**Alternativa de movimientos:** `GET /api/metrics/b2b` y `GET /api/metrics/b2c` aceptan `start_date`, `end_date`, `category` y `operation_type`, y devuelven listas de `FinancialMovement`. En esa alternativa, el frontend debe seleccionar movimientos `income` y sumar `amount` por periodo y segmento.

**Limitacion:** no hay un endpoint que devuelva B2B y B2C juntos en una sola respuesta. La API de resumen requiere dos solicitudes; los endpoints segmentados devuelven movimientos sin agregar.

**Verificacion real para el rango 2025-11-01 a 2026-10-28:**

```text
GET /api/metrics/summary?group_by=month&start_date=2025-11-01&end_date=2026-10-28&business_type=B2B
HTTP 200; 12 periodos
Primer periodo: 2025-11, income=54757.96
Ultimo periodo: 2026-10, income=39038.91

GET /api/metrics/summary?group_by=month&start_date=2025-11-01&end_date=2026-10-28&business_type=B2C
HTTP 200; 12 periodos
Primer periodo: 2025-11, income=56268.85
Ultimo periodo: 2026-10, income=67870.76
```

Como comprobacion alternativa, `/api/metrics/b2b` y `/api/metrics/b2c`, filtrados por el mismo rango y `operation_type=income`, devolvieron 101 y 96 movimientos, respectivamente. La suma de `amount` fue `615540.72` para B2B y `642606.15` para B2C.

## Contraste con el frontend existente

El dashboard actual realiza `fetch` solo de `/api/metrics` y recibe movimientos. Sus calculos de KPIs y series mensuales se hacen en frontend. Las rutas `/api/metrics/alerts`, `/api/metrics/summary`, `/api/metrics/b2b` y `/api/metrics/b2c` no son usadas por el dashboard actual.

## Referencias de implementacion

- `backend/app/routes.py`: modelos de respuesta, filtros, agrupacion, calculo de alertas y rutas.
- `frontend/src/App.tsx`: llamada actual a `/api/metrics`.
- `frontend/src/lib/financial-utils.ts`: calculos locales de KPIs y agrupacion mensual.
