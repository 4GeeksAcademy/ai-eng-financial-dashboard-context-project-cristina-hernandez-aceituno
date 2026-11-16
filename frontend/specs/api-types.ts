import type {
  BusinessType,
  Category,
  OperationType,
} from '../src/lib/financial-types'

export interface FacetsResponse {
  /** Tipos de operación disponibles: 'income' o 'outcome'; propiedad requerida y no nullable. */
  operation_types: OperationType[]
  /** Segmentos disponibles: 'B2B' o 'B2C'; propiedad requerida y no nullable. */
  business_types: BusinessType[]
  /** Categorías disponibles: 'suppliers', 'sales', 'operational', 'administrative' u 'others'; requerida y no nullable. */
  categories: Category[]
  /** Fecha mínima de los movimientos; requerida, no nullable y con formato OpenAPI date (YYYY-MM-DD). OpenAPI no declara límites adicionales ni default. */
  min_date: string
  /** Fecha máxima de los movimientos; requerida, no nullable y con formato OpenAPI date (YYYY-MM-DD). OpenAPI no declara límites adicionales ni default. */
  max_date: string
}

export interface AlertEntry {
  /** Periodo agregado; OpenAPI lo define como string sin enum, formato ni patrón. El backend usa YYYY-MM-DD (día), YYYY-Www (semana ISO) o YYYY-MM (mes), según group_by. */
  period: string
  /** Suma de importes outcome del periodo; OpenAPI number sin límites ni default declarados. */
  outcome_total: number
  /** Promedio de outcome de los periodos anteriores incluidos en el cálculo; OpenAPI number sin límites ni default declarados. */
  baseline_average: number
  /** Aumento relativo como proporción (0.3 equivale al 30 %); OpenAPI number sin límites ni default declarados. */
  increase_ratio: number
}

/** Lista de alertas devuelta por GET /api/metrics/alerts. */
export type AlertsResponse = AlertEntry[]

export interface CategoryEntry {
  /** Categoría: 'suppliers', 'sales', 'operational', 'administrative' u 'others'; propiedad requerida y no nullable. */
  category: Category
  /** Tipo de operación agregado: 'income' o 'outcome'; propiedad requerida y no nullable. */
  operation_type: OperationType
  /** Importe agregado para la categoría y operación; OpenAPI number sin límites ni default declarados. */
  total_amount: number
}

/** Lista devuelta por GET /api/metrics/categories/top; el segmento depende del filtro business_type. */
export type TopCategoriesResponse = CategoryEntry[]
