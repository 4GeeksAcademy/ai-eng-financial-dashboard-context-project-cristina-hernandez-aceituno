# Especificación: Componentes Frontend

**Versión**: 1.0  
**Fase**: 2 (Escala & Features)  
**Última actualización**: 2026-11-17

---

## Propósito

Este documento especifica cada componente del dashboard: su contrato de props, responsabilidades, estados, y comportamiento esperado. Resuelve ambigüedades que el brief del PM dejó abiertas y alinea cada componente con los tipos de la Fase 2.

**Cambios respecto a MVP**:
- Especificación formal de props y tipos
- Resolución de casos edge (datos vacíos, loading, error)
- Alineación con tipos de Fase 2 (filtros, paginación, análisis)
- Responsividad definida explícitamente

---

## Tipos Base (Fase 2)

### Core Types (Importados de `financial-types.ts`)

```typescript
// Enums financieros
export type OperationType = 'income' | 'outcome'
export type Category = 'suppliers' | 'sales' | 'operational' | 'administrative' | 'others'
export type BusinessType = 'B2B' | 'B2C'

// Modelos principales
export interface FinancialMovement {
  create_date: string        // ISO date YYYY-MM-DD
  amount: number             // Cantidad en moneda decimal
  operation_type: OperationType
  category: Category
  business_type: BusinessType
}

export interface KPIMetrics {
  totalIncome: number
  totalOutcome: number
  profit: number
  profitPercent: number
}

export interface MonthlyDataPoint {
  month: string              // YYYY-MM format
  income: number
  outcome: number
  profitPercent: number
}
```

### Nuevos Tipos para Fase 2

```typescript
// Desde param-types.ts (Fase 2)
export interface DateRangeFilter {
  start_date?: string | null    // YYYY-MM-DD
  end_date?: string | null      // YYYY-MM-DD
}

export interface AlertsParams extends DateRangeFilter {
  threshold?: number            // 0-∞, default 0.3
  group_by?: 'day' | 'week' | 'month'  // default 'month'
  business_type?: BusinessType | null
}

export interface TopCategoriesParams extends DateRangeFilter {
  operation_type?: OperationType  // default 'outcome'
  limit?: number                  // 1-20, default 5
  business_type?: BusinessType | null
}

// Desde api-types.ts (Fase 2)
export type AlertsResponse = Array<{
  period: string                      // YYYY-MM-DD, YYYY-Www, o YYYY-MM
  outcome_total: number
  baseline_average: number
  increase_ratio: number              // 0.3 = 30%
}>

export type TopCategoriesResponse = Array<{
  category: Category
  operation_type: OperationType
  total_amount: number
}>
```

---

## Componentes Implementados (MVP)

### 1. `DashboardHeader`

**Ubicación**: `frontend/src/components/dashboard/dashboard-header.tsx`

**Propósito**: Encabezado ejecutivo del dashboard. Muestra título, icono y período seleccionado.

#### Props

```typescript
interface DashboardHeaderProps {
  /**
   * Período a mostrar. Formato flexible: puede ser rango (ej: "Nov 2025 — Nov 2026") 
   * o descripción corta (ej: "Full Year 2024").
   * Default: "2024 — Full Year"
   * 
   * RESOLUCIÓN: En Fase 2, este valor provendrá del selector de rango de fechas.
   * Para MVP, es un prop estático opcional.
   */
  period?: string
}
```

#### Comportamiento

- **Siempre visible**: No hay estado loading ni error.
- **Responsive**: 
  - Mobile (< 640px): Flex column, título y período apilados.
  - Desktop (≥ 640px): Flex row, título a la izquierda, período a la derecha.
- **Iconografía**: Icono `LayoutDashboard` (lucide-react) de 18px, dentro de badge redondo.
- **Colores**: 
  - Badge: `bg-primary/10` (fondo), `text-primary` (icono)
  - Título: `text-foreground`, semibold
  - Subtítulo: `text-muted-foreground`, pequeño
  - Período: Badge con borde, `bg-secondary`

#### Ejemplo de Uso

```tsx
<DashboardHeader period="Nov 2025 — Nov 2026" />
```

#### Cambios Esperados en Fase 2

- **Selector de período interactivo**: Dropdown o date picker para cambiar rango.
- **Eventos**: Emitir `onPeriodChange(startDate, endDate)`.
- **Validación**: Verificar que `startDate <= endDate`.

---

### 2. `KPICard`

**Ubicación**: `frontend/src/components/dashboard/kpi-card.tsx`

**Propósito**: Tarjeta individual de métrica KPI con icono, valor y descripción. Soporta 4 variantes: income, outcome, profit, profitPercent.

#### Props

```typescript
interface KPICardProps {
  /**
   * Etiqueta visible en la tarjeta (mayúscula, en inglés en MVP).
   * Ejemplos: "Total Income", "Total Outcome", "Profit", "Profit Margin"
   * Tipo: string
   */
  label: string

  /**
   * Valor formateado a mostrar (string, ya debe estar formateado).
   * Ejemplos: "$154,000.50", "45.3%", "—" (si null/undefined).
   * Tipo: string
   */
  value: string

  /**
   * Texto descriptivo auxiliar debajo del valor.
   * Ejemplos: "Cumulative revenue from all income movements"
   * Tipo: string
   */
  helperText: string

  /**
   * Icono (componente LucideIcon) a mostrar en badge redondo.
   * Ejemplos: TrendingUp, TrendingDown, DollarSign, BarChart2
   * Tipo: LucideIcon
   */
  icon: LucideIcon

  /**
   * Variante de estilo (determina colores del badge e icono).
   * Valores: 'income' | 'outcome' | 'profit' | 'profitPercent'
   * 
   * RESOLUCIÓN: Mapeo de variantes a variables CSS:
   * - income → --income-badge (verde), --income-badge-fg
   * - outcome → --outcome-badge (rojo), --outcome-badge-fg
   * - profit → --profit-badge (azul), --profit-badge-fg
   * - profitPercent → --profit-badge (azul), --profit-badge-fg (igual que profit)
   */
  variant: 'income' | 'outcome' | 'profit' | 'profitPercent'

  /**
   * Estado de carga. Si true, renderiza skeleton loaders en lugar del contenido.
   * Default: false
   * Tipo: boolean | undefined
   */
  loading?: boolean
}
```

#### Comportamiento

**Estado Normal**:
- Badge con icono en la esquina superior derecha.
- Valor como título grande (text-3xl, semibold).
- Descripción abajo en gris claro.
- Borde sutil con hover effect (transición color borde).

**Estado Loading**:
- Renderiza tres skeletons:
  1. Fila label + badge (ancho 28, alto 4)
  2. Valor placeholder (ancho 36, alto 8)
  3. Descripción placeholder (ancho 44, alto 3)

**Estado Error**: 
- **No soportado en MVP**. Si `value` es "—" o string vacío, se muestra como tal.
- **Fase 2**: Agregar prop `error?: boolean` para estado rojo.

**Responsive**:
- Ancho: 100% (flex grid adapta columns).
- Alto: Min-content.
- Padding: 6 espacios Tailwind (p-6 = 1.5rem).

#### Variantes de Color (CSS Variables)

```css
:root {
  --income-badge: #dcfce7;      /* Verde claro */
  --income-badge-fg: #166534;   /* Verde oscuro */
  
  --outcome-badge: #fee2e2;     /* Rojo claro */
  --outcome-badge-fg: #991b1b;  /* Rojo oscuro */
  
  --profit-badge: #dbeafe;      /* Azul claro */
  --profit-badge-fg: #1e40af;   /* Azul oscuro */
}
```

#### Ejemplo de Uso

```tsx
<KPICard
  label="Total Income"
  value="$154,000.50"
  helperText="Cumulative revenue from all income movements"
  icon={TrendingUp}
  variant="income"
  loading={false}
/>
```

#### Cambios Esperados en Fase 2

- **Comparativa**: Prop `comparison?: { value: number; label: string }` para mostrar variación (ej: "+5.2%").
- **Trend**: Icono de flecha indicando subida/bajada.
- **Click**: Evento `onClick()` para navegar a detalles (ej: lista de movimientos).

---

### 3. `KPIRow`

**Ubicación**: `frontend/src/components/dashboard/kpi-row.tsx`

**Propósito**: Fila de 4 tarjetas KPI (Income, Outcome, Profit, Profit%). Contenedor que orquesta el layout y pasa datos a `KPICard`.

#### Props

```typescript
interface KPIRowProps {
  /**
   * Métricas calculadas. Si null, renderiza estado loading.
   * Tipo: KPIMetrics | null
   * 
   * Estructura esperada:
   * {
   *   totalIncome: 154000.50,
   *   totalOutcome: 108699.75,
   *   profit: 45300.75,
   *   profitPercent: 29.4
   * }
   */
  metrics: KPIMetrics | null

  /**
   * Fuerza estado de carga (overrides null check en metrics).
   * Default: false
   * Tipo: boolean | undefined
   * 
   * AMBIGÜEDAD RESUELTA: loading es independiente de metrics.
   * Si metrics=null Y loading=false, mostrar "—" (no data).
   * Si loading=true (cualquier state de metrics), mostrar skeletons.
   */
  loading?: boolean
}
```

#### Comportamiento

**Renderizado**:
1. Grid de 4 columnas (responsive):
   - 1 col en mobile (< 640px)
   - 2 cols en tablet (640-1200px)
   - 4 cols en desktop (≥ 1200px)
   - Gap de 1 (4px)

2. Cada columna renderiza un `KPICard` con:
   - `variant`: 'income', 'outcome', 'profit', 'profitPercent'
   - `value`: Formateado según tipo (ver `formatCurrency()` y `formatPercent()`)
   - `helperText`: Descripción fija en inglés
   - `icon`: Hardcodeado (TrendingUp, TrendingDown, DollarSign, BarChart2)
   - `loading`: Heredado de prop

**Formato de Valores**:
- Income/Outcome/Profit: `$1,234.56` (via `formatCurrency(number)`)
- Profit %: `45.3%` (via `formatPercent(number)`)
- Si null: `—` (guión)

#### Estado Null vs Loading

| Caso | metrics | loading | Comportamiento |
|------|---------|---------|-----------------|
| Data normal | {obj} | false | Muestra valores formateados |
| Cargando | null | true | Muestra skeletons de carga |
| Sin data (aún) | null | false | Muestra "—" en todos |
| Cambio de rango | {obj} | true | Muestra skeletons (re-carga) |

#### Ejemplo de Uso

```tsx
// Estado normal
<KPIRow metrics={metrics} loading={false} />

// Cargando
<KPIRow metrics={null} loading={true} />

// Sin data
<KPIRow metrics={null} loading={false} />
```

#### Cambios Esperados en Fase 2

- **Comparativa**: Prop `comparison?: KPIMetrics` para mostrar "vs anterior período".
- **Filtros**: Recibir filtros aplicados y mostrar badge "Income filtered by: B2B".
- **Click en tarjeta**: Navegar a detalles de movimientos.

---

### 4. `IncomeOutcomeChart`

**Ubicación**: `frontend/src/components/dashboard/income-outcome-chart.tsx`

**Propósito**: Gráfico de líneas con 2 series: Income vs Outcome, agrupado por mes. Muestra evolución financiera.

#### Props

```typescript
interface IncomeOutcomeChartProps {
  /**
   * Array de puntos de datos mensuales.
   * Tipo: MonthlyDataPoint[]
   * 
   * Estructura esperada (ejemplo):
   * [
   *   { month: '2025-10', income: 50000, outcome: 32000, profitPercent: 36 },
   *   { month: '2025-11', income: 54757.96, outcome: 41404.44, profitPercent: 24.4 },
   *   ...
   * ]
   */
  data: MonthlyDataPoint[]

  /**
   * Estado de carga. Si true, renderiza skeleton.
   * Default: false
   * Tipo: boolean | undefined
   */
  loading?: boolean
}
```

#### Comportamiento

**Renderizado Normal**:
1. Card container con:
   - Header: Título "Income vs. Outcome", descripción "Monthly revenue and expenditure evolution"
   - Chart area: Alto 280px, ancho 100%

2. Gráfico Recharts (LineChart):
   - 2 líneas: Income (verde) y Outcome (rojo)
   - Eje X: Meses (formato YYYY-MM, renderizado como "Nov '25", "Dec '25", etc.)
   - Eje Y: Moneda (auto-scaled, con grid)
   - Tooltip personalizado mostrando ambas series con `formatCurrency()`
   - Legend debajo (labels: "Income", "Outcome")

**Tooltip Personalizado**:
- Aparece en hover.
- Muestra label (mes), ambas series con colores.
- Formato: "Income: $50,000.00" (sin bordes de entrada).

**Estado Loading**:
- Renderiza skeleton de card + placeholder de chart (280px).

**Estado Sin Datos**:
- Si `data` está vacío o todas las series son 0, mostrar mensaje:
  ```
  "No data available to display"
  ```
- Centrado vertical en área del chart (280px).

**Responsive**:
- Ancho: 100% (ResponsiveContainer).
- Chart re-renderiza automáticamente en resize.

#### Ejemplo de Uso

```tsx
<IncomeOutcomeChart 
  data={monthlyData} 
  loading={isLoading} 
/>
```

#### Cambios Esperados en Fase 2

- **Filtro por categoría**: Prop `category?: Category` para filtrar líneas.
- **Filtro por business type**: Prop `businessType?: BusinessType` para datos B2B/B2C.
- **Período ajustable**: Prop `groupBy?: 'day' | 'week' | 'month'` para agrupar.
- **Descarga**: Botón "Download CSV" en header.

---

### 5. `ProfitPercentChart`

**Ubicación**: `frontend/src/components/dashboard/profit-percent-chart.tsx`

**Propósito**: Gráfico de líneas con una serie: Profit Margin % mensual. Muestra tendencia de rentabilidad.

#### Props

```typescript
interface ProfitPercentChartProps {
  /**
   * Array de puntos de datos mensuales.
   * Tipo: MonthlyDataPoint[]
   * Solo se usa el campo `profitPercent` de cada punto.
   */
  data: MonthlyDataPoint[]

  /**
   * Estado de carga. Si true, renderiza skeleton.
   * Default: false
   * Tipo: boolean | undefined
   */
  loading?: boolean
}
```

#### Comportamiento

**Renderizado Normal**:
1. Card container con:
   - Header: Título "Profit Margin %", descripción "Monthly profit as a percentage of total income"
   - Chart area: Alto 280px, ancho 100%

2. Gráfico Recharts (LineChart):
   - 1 línea: Profit % (azul, variable CSS `--chart-profit`)
   - Eje X: Meses (formato YYYY-MM, renderizado como "Nov '25", etc.)
   - Eje Y: Porcentaje (0-100%, con grid)
   - Línea de referencia en 0% (ReferenceLine con línea punteada)
   - Tooltip personalizado mostrando valor con 1 decimal: "45.3%"

**Tooltip Personalizado**:
- Muestra mes y valor con 1 decimal: "Profit margin: 45.3%"

**Estado Loading**:
- Skeleton de card + placeholder de chart (280px).

**Estado Sin Datos**:
- Si `data` está vacío o todos los `profitPercent` son 0, mostrar:
  ```
  "No data available to display"
  ```

**Responsive**:
- Ancho: 100%.
- Chart re-renderiza en resize.

#### Ejemplo de Uso

```tsx
<ProfitPercentChart 
  data={monthlyData} 
  loading={isLoading} 
/>
```

#### Cambios Esperados en Fase 2

- **Benchmark**: Línea horizontal para "Target profit %" (ej: 30%) con color gris.
- **Anomalías**: Resaltar puntos donde profit cae < threshold.
- **Click en punto**: Mostrar detalles de mes (movimientos, categorías).

---

## Componentes Base (UI)

### 6. `Card`, `CardHeader`, `CardTitle`, `CardDescription`

**Ubicación**: `frontend/src/components/ui/card.tsx`

**Propósito**: Componentes base (layout primitivos) para contenedores de tarjeta.

#### Contrato

```typescript
// Card (contenedor principal)
function Card({ className, ...props }: React.ComponentProps<'div'>): JSX.Element

// CardHeader (contenedor de encabezado)
function CardHeader({ className, ...props }: React.ComponentProps<'div'>): JSX.Element

// CardTitle (título dentro de header)
function CardTitle({ className, ...props }: React.ComponentProps<'div'>): JSX.Element

// CardDescription (descripción dentro de header)
function CardDescription({ className, ...props }: React.ComponentProps<'div'>): JSX.Element
```

#### Estilos

- **Card**: `bg-card`, rounded-xl, border, shadow-sm, flex flex-col gap-6, padding
- **CardHeader**: Grid layout, `@container` queries, padding especial, gap-2
- **CardTitle**: `font-semibold`, `leading-none`
- **CardDescription**: `text-muted-foreground`, pequeño, `text-sm`

**No agregar props complejos**: Son primitivos, solo acepta `className` y props HTML.

---

### 7. `Skeleton`

**Ubicación**: `frontend/src/components/ui/skeleton.tsx`

**Propósito**: Placeholder animado para estados de carga.

#### Contrato

```typescript
function Skeleton({ className, ...props }: React.ComponentProps<'div'>): JSX.Element
```

#### Comportamiento

- Fondo gris claro: `bg-accent`
- Animación pulse: `animate-pulse` (Tailwind)
- Border radius: `rounded-md`
- Acepta className personalizado para tamaño (ancho/alto)

#### Ejemplo de Uso

```tsx
<Skeleton className="h-5 w-52" />  <!-- Largo, estrecho -->
<Skeleton className="h-8 w-8 rounded-lg" />  <!-- Cuadrado con border radius -->
<Skeleton className="h-[280px] w-full rounded-lg" />  <!-- Full-width chart placeholder -->
```

---

## Ambigüedades Resueltas

| Ambigüedad | Resolución |
|-----------|-----------|
| ¿Período hardcodeado o dinámico? | MVP: prop `period` (string). Fase 2: selector interactivo con `onPeriodChange()`. |
| ¿Valores formateados o sin format? | Caller debe pasar `value` ya formateado (string). KPIRow usa `formatCurrency()` y `formatPercent()`. |
| ¿Qué ocurre si metrics es null? | Si `loading=false`, mostrar "—". Si `loading=true`, mostrar skeletons. |
| ¿Error state en componentes? | MVP: no existe. Fase 2: agregar prop `error?: boolean` y renderizar en rojo. |
| ¿Responsividad breakpoints? | Mobile (<640px): 1 col. Tablet (640-1200px): 2 cols. Desktop (≥1200px): 4 cols. |
| ¿Tooltip en gráficos? | Personalizado, con formatCurrency() para moneda y .toFixed(1) para porcentajes. |
| ¿Datos vacíos en charts? | Mostrar "No data available to display" (centrado, 280px). |
| ¿Variables CSS para colores? | Sí, usar `var(--income-badge)`, etc. Definidas en root. |
| ¿States de loading/error? | Loading: prop `loading?: boolean`. Error: Fase 2 (nuevo prop `error?: boolean`). |
| ¿Props adicionales en Fase 2? | Comparativas, filtros, eventos onClick, descarga de datos. |

---

## Hoja de Ruta (Roadmap)

### MVP (Actual)
- ✅ DashboardHeader (periodo estático)
- ✅ KPICard (4 variantes)
- ✅ KPIRow (layout grid responsivo)
- ✅ IncomeOutcomeChart (2 series)
- ✅ ProfitPercentChart (1 serie)
- ✅ Componentes base (Card, Skeleton)

### Fase 2: Escala & Features
- [ ] Nuevos componentes:
  - `AlertsTable` (lista de anomalías, params desde AlertsParams)
  - `CategoriesChart` (pie/donut, datos desde TopCategoriesResponse)
  - `FilterBar` (selector de rango, negocio, categoría, operation_type)
  - `PaginationControl` (prev/next, limit/offset)
  - `DataExport` (botón CSV/JSON)

- [ ] Mejoras a existentes:
  - DashboardHeader: Selector de período interactivo
  - KPICard: Comparativa, trend arrows, error state
  - KPIRow: Filtros aplicados (badges), drill-down onClick
  - Charts: Filtro por categoría, groupBy dinámico

### Fase 3: Producción & Polish
- [ ] Performance: Code splitting, lazy load charts
- [ ] Accesibilidad: ARIA labels, keyboard navigation
- [ ] Temas: Dark mode (ya existe), light mode
- [ ] I18n: Traducción a múltiples idiomas

---

## Referencias

- **API Spec**: [frontend/specs/financial-metrics-api.md](financial-metrics-api.md)
- **Tipos**: [frontend/src/lib/financial-types.ts](../src/lib/financial-types.ts)
- **Params/Response**: [frontend/specs/api-types.ts](api-types.ts), [param-types.ts](param-types.ts)
- **Utils**: [frontend/src/lib/financial-utils.ts](../src/lib/financial-utils.ts)
- **Roadmap**: [memory-bank/DEVELOPMENT_ROADMAP.md](../../memory-bank/DEVELOPMENT_ROADMAP.md)

---

## Checklist de Implementación

### Completados ✅
- [x] DashboardHeader renderiza correctamente
- [x] KPICard con 4 variantes y state loading
- [x] KPIRow con grid responsivo
- [x] IncomeOutcomeChart con 2 series y tooltip
- [x] ProfitPercentChart con 1 serie
- [x] Componentes base (Card, Skeleton)

### Pendiente para Fase 2
- [ ] Validar props en componentes (usar Zod o TypeScript strict)
- [ ] Agregar stories en Storybook (opcional)
- [ ] Documentar ejemplos de uso en componentes nuevos
- [ ] Agregar error state a todos los componentes
- [ ] Mejorar accessibilidad (ARIA, keyboard nav)
