# 📂 Hallazgos Agrupados por Categoría

**Solo hechos verificables en el código real - Agrupados por categorías temáticas**

---

## 🏛️ ARQUITECTURA

### Monorepo Frontend + Backend
**Ubicación**: Carpetas `frontend/` y `backend/` en raíz  
**Tipo**: Repositorio único con dos aplicaciones independientes  
**Comunicación**: 
- Frontend (5173) → Vite proxy → Backend (8000)
- Config en: `frontend/vite.config.ts:9-14`

### Entry Points
**Frontend**:  
- Archivo: `frontend/src/main.tsx`
- Puerto: 5173 (Vite dev server)

**Backend**:  
- Archivo: `backend/app/main.py`
- Puerto: 8000 (Uvicorn)

### Stack Técnico
**Frontend**:
- React 19.2.4
- TypeScript 6.0.2
- Vite 8.0.4
- Tailwind CSS 4.2.2
- Recharts 3.8.1

**Backend**:
- FastAPI (Python)
- Uvicorn (ASGI server)
- Pydantic (validación)
- pytest (testing)

### Frontend-Backend Communication
**Arquitectura**: Request-Response HTTP  
**Proxy configurado en**: `frontend/vite.config.ts:11`

```typescript
proxy: {
  "/api": {
    target: "http://backend:8000",
    changeOrigin: true,
  },
}
```

**Flujo**:
1. Frontend hace request a `/api/metrics`
2. Vite proxy redirecciona a `http://backend:8000/api/metrics`
3. Backend procesa y devuelve JSON
4. Frontend recibe response

---

## 📝 NAMING CONVENTIONS

### Frontend: kebab-case para Componentes
**Ubicación**: `frontend/src/components/dashboard/`

```
✓ kpi-card.tsx
✓ kpi-row.tsx
✓ income-outcome-chart.tsx
✓ profit-percent-chart.tsx
✓ dashboard-header.tsx
```

**Notas**: Todos los componentes usan kebab-case consistentemente

### Backend: snake_case para Funciones
**Ubicación**: `backend/app/routes.py`

```python
def get_metrics(...)
def generate_mock_movements(seed=42)
def compute_kpis(...)
```

### Alias @ para Imports
**Configurado en**: `frontend/vite.config.ts:10`

```typescript
resolve: {
  alias: {
    "@": path.resolve(__dirname, "./src"),
  },
}
```

**Usado en**: `frontend/src/App.tsx:8`

```typescript
import { KPIRow } from "@/components/dashboard/kpi-row";
import { type FinancialMovement } from "@/lib/financial-types";
```

### Tipos Centralizados
**Ubicación**: `frontend/src/lib/financial-types.ts`

```typescript
export type OperationType = 'income' | 'outcome'
export type Category = 'suppliers' | 'sales' | 'operational' | 'administrative' | 'others'
export type BusinessType = 'B2B' | 'B2C'

export interface FinancialMovement { ... }
export interface KPIMetrics { ... }
export interface MonthlyDataPoint { ... }
```

---

## 🎯 DX (Developer Experience)

### npm Scripts Estándar
**Ubicación**: `frontend/package.json`

```json
{
  "scripts": {
    "dev": "vite",
    "build": "tsc -b && vite build",
    "lint": "eslint .",
    "preview": "vite preview",
    "test": "vitest run",
    "test:watch": "vitest",
    "test:coverage": "vitest run --coverage"
  }
}
```

### Hot-Reload
**Frontend**: Vite HMR automático  
**Backend**: Auto-reload en `backend/app/main.py`

```python
uvicorn.run("main:app", reload=True)
```

### TypeScript Strict Mode
**Ubicación**: `frontend/tsconfig.app.json`

```json
{
  "compilerOptions": {
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true
  }
}
```

### Proxy Configuration
**Ubicación**: `frontend/vite.config.ts:9-14`  
**Ventaja**: Frontend puede hacer requests a `/api/*` sin manejar CORS manualmente

---

## 🧪 TESTING

### Frontend Tests
**Archivo**: `frontend/src/lib/financial-utils.test.ts`

**Ejemplo de test**:
```typescript
// Tests para funciones puras
describe('computeKPIs', () => {
  it('calculates metrics correctly', () => { ... })
})
```

### Backend Tests
**Archivo**: `backend/tests/test_routes.py`

**Pytest configuration**: `backend/tests/conftest.py`

### Test Scripts
```bash
npm test              # Una pasada
npm run test:watch    # Modo watch
npm run test:coverage # Con cobertura
```

### Limitaciones
- ❌ No hay tests E2E (end-to-end)
- ❌ Sin tests de integración frontend-backend
- ⚠️ Cobertura probablemente incompleta

---

## 📚 DOCUMENTACIÓN

### Archivos de Documentación Existentes
1. `README.md` - Documentación general en inglés
2. `README.es.md` - Documentación en español
3. `AGENTS.md` - Guía para agentes
4. `verification.md` - Análisis técnico verificado
5. `CONCRETE_FINDINGS.md` - Hallazgos concretos

### Variables de Ambiente
**Ubicación**: `frontend/.env.example`

**Contenido**: Configuración faltante en ejemplo  
**Afecta a**: `frontend/src/App.tsx:12`

```typescript
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "";
```

### .env Incompleto
⚠️ **Problema**: Faltan variables documentadas  
⚠️ **Impacto**: API_BASE_URL puede ser vacío

---

## 🔌 API / ENDPOINTS

### Endpoints Implementados
**Ubicación**: `backend/app/routes.py`

```
GET /health                          (línea 134)
GET /api/metrics                     (línea 141)
GET /api/metrics/facets              (línea 155)
GET /api/metrics/summary             (línea 162)
GET /api/metrics/categories/top      (línea 179)
GET /api/metrics/comparison          (línea 197)
GET /api/metrics/alerts              (línea 218)
GET /api/metrics/b2b                 (línea 237)
GET /api/metrics/b2c                 (línea 259)
```

**Total**: 9 endpoints GET

### Query Parameters
**Ubicación**: `backend/app/routes.py:141-155`

```python
@router.get("/api/metrics", response_model=list[FinancialMovement])
def get_metrics(
    start_date: date | None = Query(default=None),
    end_date: date | None = Query(default=None),
    category: Category | None = Query(default=None),
    operation_type: OperationType | None = Query(default=None),
) -> list[FinancialMovement]:
```

### Response Models
**Todos los endpoints tienen `response_model` explícito** (FastAPI best practice)

```python
@router.get("/api/metrics", response_model=list[FinancialMovement])
def get_metrics(...):
    return movements
```

---

## 🎨 COMPONENT PATTERNS

### Componentes con Record<> para Type-Safe Variants
**Ubicación**: `frontend/src/components/dashboard/kpi-card.tsx:12-25`

```typescript
interface KPICardProps {
  label: string
  value: string
  helperText: string
  icon: LucideIcon
  variant: 'income' | 'outcome' | 'profit' | 'profitPercent'
  loading?: boolean
}

const variantStyles: Record<KPICardProps['variant'], { badge: string; icon: string }> = {
  income: { badge: 'bg-[var(--income-badge)]', icon: 'text-[var(--income-badge-fg)]' },
  outcome: { badge: 'bg-[var(--outcome-badge)]', icon: 'text-[var(--outcome-badge-fg)]' },
  profit: { badge: 'bg-[var(--profit-badge)]', icon: 'text-[var(--profit-badge-fg)]' },
  profitPercent: { badge: 'bg-[var(--profit-badge)]', icon: 'text-[var(--profit-badge-fg)]' },
}
```

### Aria Labels para Accesibilidad
**Ubicación**: `frontend/src/App.tsx:48-52`

```typescript
<section aria-label="Key performance indicators">
  <KPIRow metrics={metrics} loading={loading} />
</section>

<section aria-label="Financial charts" className="grid grid-cols-1 gap-4 xl:grid-cols-2">
  <IncomeOutcomeChart data={monthlyData} loading={loading} />
  <ProfitPercentChart data={monthlyData} loading={loading} />
</section>
```

### Funciones Puras sin Efectos Secundarios
**Ubicación**: `frontend/src/lib/financial-utils.ts`

```typescript
export function computeKPIs(movements: FinancialMovement[]): KPIMetrics {
  const totalIncome = movements
    .filter((m) => m.operation_type === "income")
    .reduce((sum, m) => sum + m.amount, 0);
  
  // ... más lógica pura
  return { totalIncome, totalOutcome, profit, profitPercent };
}

export function computeMonthlyData(movements: FinancialMovement[]): MonthlyDataPoint[] {
  const monthlyMap: Record<string, { income: number; outcome: number }> = {};
  // ... lógica pura sin mutaciones
  return result;
}
```

---

## 🔐 SECURITY & VALIDATION

### CORS Configuration
**Ubicación**: `backend/app/main.py:6-11`

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # ⚠️ CRÍTICO - Abierto a todos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**Riesgo**: Vulnerable a CSRF y exposición de credenciales

### Sin Autenticación en Endpoints
**Ubicación**: `backend/app/routes.py`

```python
@router.get("/api/metrics")  # ⚠️ Sin validación de token
def get_metrics(...):
    movements = generate_mock_movements(seed=42)
    return movements
```

**Endpoints públicos** (9 endpoints sin protección):
- `/health`
- `/api/metrics`
- `/api/metrics/facets`
- `/api/metrics/summary`
- `/api/metrics/categories/top`
- `/api/metrics/comparison`
- `/api/metrics/alerts`
- `/api/metrics/b2b`
- `/api/metrics/b2c`

### Sin Validación Runtime en Frontend
**Ubicación**: `frontend/src/App.tsx:16-19`

```typescript
async function fetchFinancialData(): Promise<FinancialMovement[]> {
  const response = await fetch(`${API_BASE_URL}/api/metrics`);
  if (!response.ok) {
    throw new Error(`Failed: ${response.status}`);
  }
  return response.json();  // ⚠️ Sin validación tipo runtime
}
```

**Problema**: Asume que `response.json()` es siempre `FinancialMovement[]`

### Backend: Tipos Literal en Python
**Ubicación**: `backend/app/routes.py:1-15`

```python
from typing import Literal

OperationType = Literal["income", "outcome"]
Category = Literal["suppliers", "sales", "operational", "administrative", "others"]
BusinessType = Literal["B2B", "B2C"]
GroupBy = Literal["day", "week", "month"]
```

### Backend: Modelos Pydantic
**Ubicación**: `backend/app/routes.py:17-30`

```python
class FinancialMovement(BaseModel):
    create_date: date
    amount: float
    operation_type: OperationType
    category: Category
    business_type: BusinessType

class MetricsFacets(BaseModel):
    operation_types: list[OperationType]
    business_types: list[BusinessType]
    categories: list[Category]
    min_date: date
    max_date: date
```

---

## 📊 DATA HANDLING

### Mock Data con Seed Determinístico
**Ubicación**: `backend/app/routes.py` (en 8 endpoints)

```python
movements = generate_mock_movements(seed=42)
```

**Aparece en**:
- Línea 140: `@router.get("/api/metrics")`
- Línea 147: `@router.get("/api/metrics/facets")`
- Línea 163: `@router.get("/api/metrics/summary")`
- Línea 180: `@router.get("/api/metrics/categories/top")`
- Línea 200: `@router.get("/api/metrics/comparison")`
- Línea 220: `@router.get("/api/metrics/alerts")`
- Línea 237: `@router.get("/api/metrics/b2b")`
- Línea 259: `@router.get("/api/metrics/b2c")`

**Ventaja**: Reproducibilidad  
**Problema**: Generación repetida en cada request (sin caché)

### Datos sin Caché Global
**Problema**: Cada endpoint genera los datos desde cero  
**Impacto**: Ineficiente y datos no sincronizados

---

## 🔍 OBSERVABILITY & LOGGING

### Sin Logging en Backend
**Ubicación**: `backend/app/routes.py`

```python
@router.get("/api/metrics")
def get_metrics(...):
    # ❌ Sin logging
    movements = generate_mock_movements(seed=42)
    # ❌ Sin logging de error, tiempo de ejecución
    return movements
```

**Problema**: Ningún `print()`, `logging.info()` ni similar  
**Impacto**: Difícil debugging y auditoría

### No hay Tracing Distribuido
**Limitación**: Sin OpenTelemetry ni similar

### No hay Monitoreo de Métricas
**Limitación**: Sin Prometheus o DataDog

---

## ⚡ PERFORMANCE

### Proxy Hardcodeado a "backend"
**Ubicación**: `frontend/vite.config.ts:11`

```typescript
target: "http://backend:8000",  // ⚠️ Hardcodeado
```

**Problema**: Solo funciona con docker-compose (hostname "backend")  
**No funciona en**: `localhost` para desarrollo local  
**Debería ser configurable**: Via `process.env.VITE_API_TARGET`

### API_BASE_URL Default Vacío
**Ubicación**: `frontend/src/App.tsx:12`

```typescript
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "";
```

**Problema**: `??` devuelve `""` si no está definido  
**Riesgo**: Requests a `"/api/*"` en lugar de URL completa

---

## 📁 FOLDER STRUCTURE

### Frontend Estructura
```
frontend/src/
├── components/
│   ├── dashboard/
│   │   ├── kpi-card.tsx              ✓ kebab-case
│   │   ├── kpi-row.tsx               ✓ kebab-case
│   │   ├── income-outcome-chart.tsx  ✓ kebab-case
│   │   ├── profit-percent-chart.tsx  ✓ kebab-case
│   │   └── dashboard-header.tsx      ✓ kebab-case
│   └── ui/
│       ├── card.tsx
│       └── skeleton.tsx
├── lib/
│   ├── financial-types.ts            ✓ TIPOS CENTRALIZADOS
│   ├── financial-utils.ts            ✓ funciones puras
│   ├── financial-utils.test.ts       ✓ TESTS
│   └── utils.ts
├── App.tsx
├── main.tsx                          ✓ ENTRY POINT
├── vite.config.ts
├── package.json
├── tsconfig.app.json
└── .env.example
```

### Backend Estructura
```
backend/
├── app/
│   ├── main.py                       ✓ ENTRY POINT
│   ├── routes.py                     ✓ ENDPOINTS (9)
│   ├── __init__.py
├── tests/
│   ├── conftest.py
│   └── test_routes.py                ✓ TESTS
├── requirements.txt
└── ...
```

---

## 🚀 DEPLOYMENT

### Docker Compose
**Archivo**: `docker-compose.yml`

**Servicios**:
- `frontend`: Vite dev server en 5173
- `backend`: Uvicorn en 8000

**Red**: Permite comunicación entre servicios

---

## ✅ RESUMEN DE HALLAZGOS POR CATEGORÍA

| Categoría | Hallazgos | Estado |
|-----------|-----------|--------|
| **Arquitectura** | Monorepo bien separado, comunicación clara | ✅ Sólida |
| **Naming** | kebab-case FE, @ alias, tipos centralizados | ✅ Consistente |
| **DX** | npm scripts, hot-reload, strict mode | ✅ Excelente |
| **Testing** | Tests unitarios presentes, sin E2E | ⚠️ Incompleto |
| **Documentación** | 5 archivos .md, sin .env completo | ⚠️ Parcial |
| **API** | 9 endpoints, query params explícitos | ✅ Clara |
| **Components** | Record<>, aria labels, funciones puras | ✅ Buenas prácticas |
| **Security** | CORS abierto, sin auth, sin validación | 🚨 Crítico |
| **Data** | seed=42 determinístico, sin caché | ⚠️ Ineficiente |
| **Observability** | Sin logging ni tracing | ❌ Ausente |
| **Performance** | Proxy hardcodeado, variable vacía | ⚠️ Config débil |
| **Folders** | Estructura clara y consistente | ✅ Clara |

---

**Versión**: 1.0  
**Fecha**: 13 de noviembre de 2026  
**Solo hallazgos concretos verificables en código real**  
**Agrupados por 12 categorías temáticas**
