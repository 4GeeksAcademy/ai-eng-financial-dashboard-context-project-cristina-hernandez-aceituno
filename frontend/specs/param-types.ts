import type {
  BusinessType,
  OperationType,
} from '../../src/lib/financial-types'

/** Parámetros opcionales para acotar un rango de fechas. */
export interface DateRangeFilter {
  /** Fecha inicial inclusiva, opcional y nullable; formato OpenAPI date (YYYY-MM-DD). No tiene default ni límites adicionales declarados. */
  start_date?: string | null
  /** Fecha final inclusiva, opcional y nullable; formato OpenAPI date (YYYY-MM-DD). No tiene default ni límites adicionales declarados. */
  end_date?: string | null
}

type GroupBy = 'day' | 'week' | 'month'

export interface AlertsParams extends DateRangeFilter {
  /** Umbral de aumento como proporción; opcional, mínimo 0, sin máximo y default 0.3. */
  threshold?: number
  /** Granularidad opcional: 'day', 'week' o 'month'; default 'month'; no nullable. */
  group_by?: GroupBy
  /** Segmento opcional: 'B2B' o 'B2C', o null; null u omisión no limitan el segmento. OpenAPI no declara default. */
  business_type?: BusinessType | null
}

export interface TopCategoriesParams extends DateRangeFilter {
  /** Tipo de operación opcional: 'income' u 'outcome'; default 'outcome'; no nullable. */
  operation_type?: OperationType
  /** Número entero opcional de resultados, mínimo 1 y máximo 20; default 5; no nullable. */
  limit?: number
  /** Segmento opcional: 'B2B' o 'B2C', o null; null u omisión no limitan el segmento. OpenAPI no declara default. */
  business_type?: BusinessType | null
}
