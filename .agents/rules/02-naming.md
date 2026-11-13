# 📝 Reglas de Naming Conventions

Reglas sobre nombres de archivos, variables, funciones y tipos.

---

## REGLA-NOM-001: Componentes React en kebab-case

**Norma**: Todos los archivos de componentes usan kebab-case.

**Hecho citado**: `frontend/src/components/dashboard/` (CONCRETE_FINDINGS.md, línea 10)

```
✓ kpi-card.tsx
✓ income-outcome-chart.tsx
✓ profit-percent-chart.tsx
✓ dashboard-header.tsx
```

**Por qué**: Consistencia visual y facilita búsquedas (todos coinciden: guiones, lowercase).

**Contraejemplos a evitar**:
- ❌ KpiCard.tsx (PascalCase)
- ❌ kpi_card.tsx (snake_case)
- ❌ kpiCard.tsx (camelCase)

**Aplicación**: Cualquier nuevo componente debe ser `new-component.tsx`.

---

## REGLA-NOM-002: Importes Frontend Usan Alias @

**Norma**: Usar `@` para importar desde `src/`.

**Hecho citado**: 
- Configurado en `frontend/vite.config.ts:10` (CONCRETE_FINDINGS.md, línea 100)
- Usado en `frontend/src/App.tsx:8` (CONCRETE_FINDINGS.md, línea 108)

```typescript
// ✓ Correcto
import { KPIRow } from "@/components/dashboard/kpi-row";
import { computeKPIs } from "@/lib/financial-utils";

// ❌ Evitar
import { KPIRow } from "../../../components/dashboard/kpi-row";
import { computeKPIs } from "../../lib/financial-utils";
```

**Por qué**: 
- Elimina rutas relativas confusas
- Claridad y legibilidad
- Fácil refactorizar (rutas no cambian si mueves archivo)

**Aplicación**: Todos los imports internos deben usar `@`.

---

## REGLA-NOM-003: Tipos Centralizados en financial-types.ts

**Norma**: Todos los tipos compartidos (frontend y backend) se definen en `frontend/src/lib/financial-types.ts`.

**Hecho citado**: `frontend/src/lib/financial-types.ts` (CONCRETE_FINDINGS.md, línea 125)

```typescript
export type OperationType = 'income' | 'outcome'
export type Category = 'suppliers' | 'sales' | 'operational' | 'administrative' | 'others'
export type BusinessType = 'B2B' | 'B2C'

export interface FinancialMovement { ... }
export interface KPIMetrics { ... }
export interface MonthlyDataPoint { ... }
```

**Por qué**: 
- Sincronización frontend-backend
- Una fuente de verdad para tipos
- Evita desincronizaciones

**Aplicación**: 
- Nuevos tipos van aquí
- Backend importa (o espeja) desde aquí
- Actualizar cuando cambien tipos

---

## REGLA-NOM-004: Backend usa snake_case

**Norma**: Funciones y variables en backend usan snake_case.

**Hecho citado**: `backend/app/routes.py` (CONCRETE_FINDINGS.md, línea 173)

```python
def get_metrics(...)
def generate_mock_movements(seed=42)
def compute_kpis(movements)
```

**Por qué**: Convención Python estándar (PEP 8).

**Aplicación**: Coherencia con estándares de Python. No cambiar.

---

## 📚 Referencias

- [PROJECT_RULES.md](../../PROJECT_RULES.md) - Documento maestro de reglas
- [FINDINGS_BY_CATEGORY.md](../../FINDINGS_BY_CATEGORY.md) - Hallazgos por categoría

**Volver al índice**: [index.md](./index.md)
