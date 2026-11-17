# Frontend Specs: Funcionalidades del Dashboard

**Versión**: 1.0  
**Fase**: MVP + Phase 2  
**Última actualización**: 2026-11-17

---

## Propósito

Documentación formal de las **tres funcionalidades del dashboard** con:
- ✅ Endpoints consumidos (verificados en `/docs`)
- ✅ Tipos TypeScript de petición y respuesta
- ✅ Parámetros válidos y restricciones
- ✅ Casos límite (edge cases) y comportamiento esperado de la UI

---

## Funcionalidad 1: Filtro por Rango de Fechas

**Descripción**: Cargar y filtrar movimientos financieros por rango de fechas (inclusive). Permite visualizar todos los ingresos y gastos en un período.

### Endpoint

```
GET /api/metrics
```

**Ubicación en /docs**: `/api/metrics` → GET

### Tipos TypeScript

#### Request (Query Parameters)

```typescript
interface GetMetricsRequest {
  /** Fecha inicial inclusiva; formato YYYY-MM-DD. Opcional. */
  start_date?: string | null
  
  /** Fecha final inclusiva; formato YYYY-MM-DD. Opcional. */
  end_date?: string | null
  
  /** Categoría a filtrar: 'suppliers' | 'sales' | 'operational' | 'administrative' | 'others'. Opcional. */
  category?: Category | null
  
  /** Tipo de operación: 'income' | 'outcome'. Opcional. */
  operation_type?: OperationType | null
}
```

#### Response (200 OK)

```typescript
type GetMetricsResponse = FinancialMovement[]

interface FinancialMovement {
  create_date: string        // ISO date YYYY-MM-DD (ej: "2026-09-15")
  amount: number             // Cantidad en moneda decimal (ej: 1250.50)
  operation_type: 'income' | 'outcome'
  category: 'suppliers' | 'sales' | 'operational' | 'administrative' | 'others'
  business_type: 'B2B' | 'B2C'
}
```

**Respuesta vacía**: `[]` (array vacío, no error 404)

### Parámetros: Valores Válidos y Restricciones

| Parámetro | Tipo | Formato | Validación | Default | Notas |
|-----------|------|---------|-----------|---------|-------|
| `start_date` | string | YYYY-MM-DD | Opcional. No tiene min/max. | (ninguno) | Límite inicial inclusivo. Si null u omitido, sin límite inferior. |
| `end_date` | string | YYYY-MM-DD | Opcional. No tiene min/max. | (ninguno) | Límite final inclusivo. Si null u omitido, sin límite superior. |
| `category` | enum | — | `suppliers` \| `sales` \| `operational` \| `administrative` \| `others` | (ninguno) | Opcional. Null u omitido = sin filtro. |
| `operation_type` | enum | — | `income` \| `outcome` | (ninguno) | Opcional. Null u omitido = sin filtro. |

**Validaciones Backend**:
- No valida relación `start_date <= end_date`; API devuelve array vacío si orden es incorrecto.
- Fechas fuera del rango de datos existentes devuelven array vacío.

### Casos Límite (Edge Cases)

#### Caso 1: Rango Sin Datos

**Escenario**: Usuario selecciona `start_date=2020-01-01&end_date=2020-12-31` pero los datos más antiguos son de 2025.

**Request**:
```
GET /api/metrics?start_date=2020-01-01&end_date=2020-12-31
```

**Response (200)**:
```json
[]
```

**Comportamiento UI Esperado**:
- Componente de tabla/lista muestra: **"No movements found for this period"**
- Skeletons desaparecen tras 1-2 segundos.
- KPIs muestran **"—"** (guión).
- Charts vacíos con mensaje: **"No data available to display"**.
- Sugerencia: "Try expanding the date range" (texto gris claro).

#### Caso 2: Rango Completo (12 meses)

**Escenario**: Usuario selecciona `start_date=2025-11-01&end_date=2026-10-28` (todo el período disponible).

**Request**:
```
GET /api/metrics?start_date=2025-11-01&end_date=2026-10-28
```

**Response (200)**: Array con ~360+ movimientos (12 meses × ~30 movimientos/mes).

**Comportamiento UI Esperado**:
- Tabla renderizando todos los movimientos (~360). **MVP no soporta paginación** (feature de Fase 2).
- KPIs calculados correctamente: 
  - Total Income: suma de todos los `amount` con `operation_type=income`
  - Total Outcome: suma de todos los `amount` con `operation_type=outcome`
  - Profit: Income - Outcome
  - Profit %: (Income - Outcome) / Income × 100
- Charts renderizados con 12 puntos mensuales (una línea para cada mes).
- Indicador de período en header: **"Nov 2025 — Oct 2026"**

---

## Funcionalidad 2: Tabla de Anomalías de Gastos

**Descripción**: Detectar períodos donde los gastos (`outcome`) excedieron un umbral configurable comparado con el promedio histórico. Muestra alertas de anomalías.

### Endpoint

```
GET /api/metrics/alerts
```

**Ubicación en /docs**: `/api/metrics/alerts` → GET

### Tipos TypeScript

#### Request (Query Parameters)

```typescript
interface GetAlertsRequest {
  /** Umbral de aumento como proporción (0.3 = 30%). Opcional, mínimo 0, sin máximo. */
  threshold?: number
  
  /** Granularidad de agrupación: 'day' | 'week' | 'month'. Opcional, default 'month'. */
  group_by?: 'day' | 'week' | 'month'
  
  /** Fecha inicial para limitar búsqueda y línea base histórica. Opcional. */
  start_date?: string | null
  
  /** Fecha final para limitar búsqueda. Opcional. */
  end_date?: string | null
  
  /** Segmento de negocio: 'B2B' | 'B2C'. Opcional; null u omitido = todos los segmentos. */
  business_type?: 'B2B' | 'B2C' | null
}
```

#### Response (200 OK)

```typescript
type GetAlertsResponse = AlertEntry[]

interface AlertEntry {
  /** Período agregado; formato según group_by:
      - day: YYYY-MM-DD (ej: "2026-03-15")
      - week: YYYY-Www (ej: "2026-W12")
      - month: YYYY-MM (ej: "2026-03")
  */
  period: string
  
  /** Suma de importes outcome en el período. */
  outcome_total: number
  
  /** Promedio de outcome de todos los períodos anteriores incluidos en el cálculo. */
  baseline_average: number
  
  /** Aumento relativo como proporción:
      0.3 = 30%, 1.4968 = 149.68%. Nunca negativo en alertas (solo se reportan aumentos). */
  increase_ratio: number
}
```

**Respuesta vacía**: `[]` (sin alertas en el rango)

### Parámetros: Valores Válidos y Restricciones

| Parámetro | Tipo | Validación | Default | Notas |
|-----------|------|-----------|---------|-------|
| `threshold` | number | ≥ 0 | 0.3 | Proporción (0.3 = 30%). Sin máximo declarado. |
| `group_by` | enum | `'day'` \| `'week'` \| `'month'` | `'month'` | Define format de `period` en respuesta. |
| `start_date` | string | YYYY-MM-DD | (ninguno) | Limita búsqueda Y línea base histórica (limitación importante). |
| `end_date` | string | YYYY-MM-DD | (ninguno) | Límite final de búsqueda (inclusivo). |
| `business_type` | enum | `'B2B'` \| `'B2C'` \| null | (ninguno) | Null u omitido = ambos segmentos. |

**Cálculo Backend** (Fórmula):
```
Para cada período P en [start_date, end_date]:
  baseline_avg = promedio(outcome de todos períodos anteriores a P)
  if baseline_avg > 0 AND (outcome_P - baseline_avg) / baseline_avg > threshold:
    return AlertEntry{period: P, outcome_total: outcome_P, baseline_average: baseline_avg, increase_ratio: ...}
```

**Limitaciones**:
- El primer período NUNCA genera alerta (no hay línea base previa).
- `start_date` limita TANTO la búsqueda como el histórico. No se separan.
- No soporta `category` ni `operation_type` (siempre analiza `outcome` total).

### Casos Límite (Edge Cases)

#### Caso 1: Umbral Muy Alto (Sin Alertas)

**Escenario**: Usuario establece `threshold=5.0` (500% aumento requerido) con `group_by=month`.

**Request**:
```
GET /api/metrics/alerts?threshold=5.0&group_by=month&start_date=2025-11-01&end_date=2026-10-28
```

**Response (200)**:
```json
[]
```

**Comportamiento UI Esperado**:
- Tabla vacía con mensaje: **"No anomalies detected in this period"**
- Badge verde junto al título: **"✓ All spending patterns are normal"**
- Sugerencia: "Try lowering the threshold to 0.2 (20%) to see more alerts" (texto auxiliar).
- Charts normales (sin resaltes de anomalías).

#### Caso 2: Umbral Bajo Con Anomalías (4 Alertas)

**Escenario**: Usuario con `threshold=0.3` (30%) y rango `2025-11-01&end_date=2026-10-28`, `group_by=month`.

**Request**:
```
GET /api/metrics/alerts?threshold=0.3&group_by=month&start_date=2025-11-01&end_date=2026-10-28
```

**Response (200)**: 4 alertas

```json
[
  {
    "period": "2025-12",
    "outcome_total": 103378.98,
    "baseline_average": 41404.44,
    "increase_ratio": 1.4968
  },
  {
    "period": "2026-03",
    "outcome_total": 88076.90,
    "baseline_average": 55334.29,
    "increase_ratio": 0.5917
  },
  {
    "period": "2026-06",
    "outcome_total": 80212.01,
    "baseline_average": 57416.50,
    "increase_ratio": 0.3970
  },
  {
    "period": "2026-08",
    "outcome_total": 82189.37,
    "baseline_average": 60291.89,
    "increase_ratio": 0.3632
  }
]
```

**Comportamiento UI Esperado**:
- **AlertsTable** (nuevo componente Fase 2) renderiza 4 filas:
  ```
  Período  | Gasto Total | Promedio Histórico | Aumento   | % Aumento
  2025-12  | $103,378.98 | $41,404.44         | $61,974.54| 149.7% ⚠️🔴
  2026-03  | $88,076.90  | $55,334.29         | $32,742.61| 59.2%  ⚠️🟠
  2026-06  | $80,212.01  | $57,416.50         | $22,795.51| 39.7%  ⚠️🟡
  2026-08  | $82,189.37  | $60,291.89         | $21,897.48| 36.3%  ⚠️🟡
  ```
- Color de fondo de fila: Rojo (>100%) → Naranja (50-100%) → Amarillo (25-50%)
- Icono ⚠️ en cada fila.
- Contador en header: **"4 anomalies detected"** (badge rojo).
- Gráfico de Profit % muestra línea de referencia en baseline_average (línea punteada gris).

---

## Funcionalidad 3: Comparativa de Ingresos B2B vs. B2C

**Descripción**: Comparar ingresos entre dos segmentos de negocio (B2B y B2C) en el mismo período. Requiere dos llamadas al backend.

### Endpoints

```
GET /api/metrics/summary?business_type=B2B&group_by=month&start_date=...&end_date=...
GET /api/metrics/summary?business_type=B2C&group_by=month&start_date=...&end_date=...
```

**Ubicación en /docs**: `/api/metrics/summary` → GET

**Alternativa (no recomendada)**:
- `GET /api/metrics/b2b` y `GET /api/metrics/b2c` (devuelven movimientos sin agregar)

### Tipos TypeScript

#### Request (Query Parameters - Dos llamadas)

```typescript
interface GetSummaryRequest {
  /** Segmento: 'B2B' | 'B2C'. Requerido para hacer dos solicitudes separadas. */
  business_type: 'B2B' | 'B2C'
  
  /** Granularidad: 'day' | 'week' | 'month'. Opcional, default 'month'. */
  group_by?: 'day' | 'week' | 'month'
  
  /** Fecha inicial. Opcional; DEBE ser igual en ambas llamadas. */
  start_date?: string | null
  
  /** Fecha final. Opcional; DEBE ser igual en ambas llamadas. */
  end_date?: string | null
  
  /** Categoría a filtrar. Opcional; DEBE ser igual en ambas llamadas. */
  category?: Category | null
  
  /** Tipo de operación. Opcional; DEBE ser igual en ambas llamadas. */
  operation_type?: OperationType | null
}
```

**Nota Importante**: Las dos llamadas deben usar parámetros idénticos (menos `business_type`) para garantizar que los períodos coincidan.

#### Response (200 OK - Dos Respuestas)

```typescript
type GetSummaryResponse = SummaryEntry[]

interface SummaryEntry {
  /** Período agregado; formato según group_by:
      - day: YYYY-MM-DD
      - week: YYYY-Www
      - month: YYYY-MM
  */
  period: string
  
  /** Ingresos totales en el período (sum de amounts con operation_type=income). */
  income: number
  
  /** Gastos totales en el período (sum de amounts con operation_type=outcome). */
  outcome: number
  
  /** Beneficio neto: income - outcome. */
  net: number
}
```

**Ejemplo de Respuesta B2B**:
```json
[
  { "period": "2025-11", "income": 54757.96, "outcome": 32847.15, "net": 21910.81 },
  { "period": "2025-12", "income": 51204.50, "outcome": 35156.78, "net": 16047.72 },
  ...
]
```

**Ejemplo de Respuesta B2C** (mismo período, números diferentes):
```json
[
  { "period": "2025-11", "income": 56268.85, "outcome": 28456.09, "net": 27812.76 },
  { "period": "2025-12", "income": 53421.23, "outcome": 31245.67, "net": 22175.56 },
  ...
]
```

### Parámetros: Valores Válidos y Restricciones

| Parámetro | Tipo | Validación | Default | Notas |
|-----------|------|-----------|---------|-------|
| `business_type` | enum | `'B2B'` \| `'B2C'` | Requerido | Dos solicitudes separadas. |
| `group_by` | enum | `'day'` \| `'week'` \| `'month'` | `'month'` | DEBE ser igual en ambas llamadas. |
| `start_date` | string | YYYY-MM-DD | (ninguno) | Opcional. DEBE ser igual en ambas llamadas. |
| `end_date` | string | YYYY-MM-DD | (ninguno) | Opcional. DEBE ser igual en ambas llamadas. |
| `category` | enum | `suppliers` \| `sales` \| ... | (ninguno) | Opcional. DEBE ser igual en ambas llamadas. |
| `operation_type` | enum | `income` \| `outcome` | (ninguno) | Opcional. DEBE ser igual en ambas llamadas. |

**Restricciones Críticas**:
- No existe endpoint que devuelva ambos segmentos en una sola respuesta.
- Frontend DEBE hacer DOS llamadas en paralelo y emparejar por `period`.
- Si períodos no coinciden (distintos rangos/parámetros), comparativa es inválida.

### Casos Límite (Edge Cases)

#### Caso 1: Segmento Sin Datos en Período

**Escenario**: Usuario selecciona `start_date=2026-09-01&end_date=2026-09-15`. B2B tiene datos, pero B2C no tiene ningún movimiento en esas fechas.

**Request B2B**:
```
GET /api/metrics/summary?business_type=B2B&group_by=month&start_date=2026-09-01&end_date=2026-09-15
```
**Response (200)**:
```json
[
  { "period": "2026-09", "income": 15234.50, "outcome": 8900.00, "net": 6334.50 }
]
```

**Request B2C**:
```
GET /api/metrics/summary?business_type=B2C&group_by=month&start_date=2026-09-01&end_date=2026-09-15
```
**Response (200)**:
```json
[]
```

**Comportamiento UI Esperado**:
- **Chart (Income vs Outcome Comparison)**:
  - Período `2026-09` muestra:
    - B2B: barras visibles (Income: $15,234.50, Outcome: $8,900.00)
    - B2C: barras desaparecen o muestran cero ($0)
  - Tooltip en hover muestra: "B2C: No data for this period"
  
- **KPI Cards para Comparativa**:
  ```
  B2B Income (Sep 2026):  $15,234.50  ✓
  B2C Income (Sep 2026):  —           (guión, sin datos)
  Diferencia:             $15,234.50 (B2B adelante)
  ```

- **Insight**: Badge amarillo: **"⚠️ B2C has no movements in this period"**

#### Caso 2: Comparativa Equilibrada (12 Meses)

**Escenario**: Período completo `start_date=2025-11-01&end_date=2026-10-28`, `group_by=month`. Ambos segmentos con datos similares.

**Request B2B** + **Request B2C** (paralelo):
```
GET /api/metrics/summary?business_type=B2B&group_by=month&start_date=2025-11-01&end_date=2026-10-28
GET /api/metrics/summary?business_type=B2C&group_by=month&start_date=2025-11-01&end_date=2026-10-28
```

**Response**: 12 períodos mensuales cada una.

```
Ejemplo para 2025-11:
B2B: { period: "2025-11", income: 54757.96, outcome: 32847.15, net: 21910.81 }
B2C: { period: "2025-11", income: 56268.85, outcome: 28456.09, net: 27812.76 }

Ejemplo para 2026-10:
B2B: { period: "2026-10", income: 39038.91, outcome: 24670.33, net: 14368.58 }
B2C: { period: "2026-10", income: 67870.76, outcome: 35200.44, net: 32670.32 }
```

**Comportamiento UI Esperado**:
- **Chart Comparativo (Grouped Bars)**:
  ```
  X-Axis: Meses (Nov '25, Dec '25, ..., Oct '26)
  Y-Axis: Income ($)
  
  Cada mes muestra 2 barras:
    - Barra azul (B2B): altura según income B2B
    - Barra naranja (B2C): altura según income B2C
  
  Tooltip: "Nov 2025: B2B $54,757.96 | B2C $56,268.85"
  ```

- **KPI Cards de Comparativa**:
  ```
  B2B Total Income:    $600,000.50
  B2C Total Income:    $650,000.75
  
  Ganador:             B2C (+$50,000.25, +8.3%)
  
  Trend (12 meses):    B2C crece, B2B desciende (badges con flechas)
  ```

- **Tabla de Resumen**:
  ```
  Período | B2B Income   | B2C Income   | Diferencia | % Ventaja
  2025-11 | $54,757.96   | $56,268.85   | +$1,510.89 | +2.8%
  2025-12 | $51,204.50   | $53,421.23   | +$2,216.73 | +4.3%
  ...     | ...          | ...          | ...        | ...
  2026-10 | $39,038.91   | $67,870.76   | +$28,831.85| +73.9% ⬆️
  ```

---

## Resumen de Tipos Importados

Todos los tipos se importan de los siguientes archivos:

```typescript
// Desde frontend/src/lib/financial-types.ts
export type OperationType = 'income' | 'outcome'
export type Category = 'suppliers' | 'sales' | 'operational' | 'administrative' | 'others'
export type BusinessType = 'B2B' | 'B2C'

export interface FinancialMovement {
  create_date: string
  amount: number
  operation_type: OperationType
  category: Category
  business_type: BusinessType
}

// Desde frontend/specs/api-types.ts (Fase 2)
export interface AlertEntry { ... }
export type AlertsResponse = AlertEntry[]

// Desde frontend/specs/param-types.ts (Fase 2)
export interface DateRangeFilter { ... }
export interface AlertsParams extends DateRangeFilter { ... }
export interface TopCategoriesParams extends DateRangeFilter { ... }
```

---

## Checklist para Implementación Frontend

### Funcionalidad 1: Filtro por Rango de Fechas ✅ MVP
**Estado**: IMPLEMENTADO. No requiere más trabajo.
- [x] UI de selector de fecha
- [x] Llamada GET /api/metrics con parámetros
- [x] Renderizar lista de movimientos
- [x] Calcular KPIs localmente
- [x] Manejo de array vacío (no data)

### Funcionalidad 2: Alertas de Anomalías ⏳ Fase 2
**Estado**: NO IMPLEMENTADO EN MVP. Esperar a Fase 2 (semanas 9-16).
- [ ] Crear componente `AlertsTable` (new)
- [ ] Llamada GET /api/metrics/alerts
- [ ] Selector de `threshold` y `group_by`
- [ ] Tabla con colores según severidad (rojo/naranja/amarillo)
- [ ] Manejo de array vacío (no anomalies)

### Funcionalidad 3: Comparativa B2B vs B2C ⏳ Fase 2
**Estado**: NO IMPLEMENTADO EN MVP. Esperar a Fase 2 (semanas 9-16).
- [ ] Crear componente `ComparisonChart` (new, grouped bars)
- [ ] Dos llamadas paralelas a GET /api/metrics/summary
- [ ] Emparejar respuestas por `period`
- [ ] Renderizar gráfico con dos series
- [ ] Tabla de comparativa con diferencias

---

## Referencias

- [API Specification](./financial-metrics-api.md)
- [Component Specification](./components.md)
- [API Types](./api-types.ts)
- [Parameter Types](./param-types.ts)
- Backend OpenAPI Docs: `http://localhost:8000/docs`

---

## Notas Importantes

1. **Parámetros Opcionales**: Cuando un parámetro es opcional y no se proporciona, el backend asume un comportamiento por defecto (ej: `threshold=0.3`, `group_by=month`).

2. **Formato de Fechas**: Todos los endpoints usan `YYYY-MM-DD` (ISO 8601). Frontend debe serializar correctamente.

3. **Dos Llamadas en Paralelo (B2B vs B2C)**: Usar `Promise.all()` o `Promise.allSettled()` para evitar demoras secuenciales.

4. **MVP vs Fase 2**:
   - **MVP**: Solo Funcionalidad 1 (Filtro por rango de fechas) está implementada.
   - **Funcionalidades 2 y 3**: Se agregarán en Fase 2 (semanas 9-16).
   - Consultar [DEVELOPMENT_ROADMAP.md](../../memory-bank/DEVELOPMENT_ROADMAP.md) para timeline exacto.

4. **Fórmula de Profit %**: 
   ```
   Si income > 0:  profitPercent = (income - outcome) / income * 100
   Si income = 0:  profitPercent = 0 (evitar división por cero)
   ```

5. **Línea Base Histórica**: En alertas, `start_date` limita TANTO la visualización como el cálculo histórico. Esto es un comportamiento existente, no configurable.

6. **Responsabilidades Frontend vs Backend**:
   - **Backend**: Filtrado, agrupación, cálculos de alertas y línea base.
   - **Frontend**: Formateo de valores (moneda, %), paginación, selección de período, renderizado de UI.
