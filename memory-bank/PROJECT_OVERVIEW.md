# 📊 Financial Dashboard - Project Memory Bank

**Última actualización**: 2026-11-13  
**Proyecto**: Financial Metrics Dashboard  
**Repositorio**: 4GeeksAcademy/ai-eng-financial-dashboard-context-project-cristina-hernandez-aceituno

---

## 📌 Product Overview

### ¿Qué es?
El **Financial Dashboard** es una aplicación web full-stack que visualiza y analiza movimientos financieros mensuales. Proporciona un análisis integral de ingresos, gastos y márgenes de beneficio a través de una interfaz interactiva con gráficos y KPIs.

### Funcionalidad Principal
- **Métricas Clave (KPIs)**: 
  - Total de ingresos
  - Total de gastos
  - Beneficio neto (income - outcome)
  - Porcentaje de beneficio ((profit / income) × 100)

- **Visualizaciones**:
  - Gráfico de barras: Ingresos vs Gastos por mes
  - Gráfico de líneas: Tendencia de porcentaje de beneficio

- **Datos**:
  - Generados con mock data determinístico (seed=42)
  - Rango: 12 meses (enero a diciembre)
  - Clasificación por tipo (income/outcome), categoría y tipo de negocio (B2B/B2C)

### Caso de Uso
Análisis financiero empresarial para pequeños y medianos negocios (PyMEs). Permite visualizar rapidamente:
- Qué meses fueron más rentables
- Relación ingresos-gastos
- Tendencias de márgenes de beneficio

---

## 🛠️ Technology Stack

### Frontend Stack

| Tecnología | Versión | Propósito |
|-----------|---------|----------|
| **React** | 19.2.4 | Framework UI moderno |
| **TypeScript** | ~6.0.2 | Type safety en JavaScript |
| **Vite** | 8.0.4 | Build tool y dev server |
| **Tailwind CSS** | 4.2.2 | Framework de estilos (utility-first) |
| **Recharts** | 3.8.1 | Librería de gráficos para React |
| **Lucide React** | 1.8.0 | Conjunto de íconos SVG |
| **Class Variance Authority** | 0.7.1 | Gestión de variantes de componentes |
| **Vitest** | 4.1.4 | Framework de testing unitario |
| **ESLint** | 9.39.4 | Linter de código |

**Dev Tools**:
- `@vitejs/plugin-react` - Soporte para JSX/React
- `@tailwindcss/vite` - Plugin Tailwind para Vite
- `typescript-eslint` - Eslint + TypeScript

### Backend Stack

| Tecnología | Versión | Propósito |
|-----------|---------|----------|
| **FastAPI** | (latest) | Framework web asincrónico |
| **Uvicorn** | (latest) | Servidor ASGI |
| **Pydantic** | (via FastAPI) | Validación y serialización |
| **Python** | 3.x | Lenguaje base |
| **pytest** | (latest) | Framework de testing |
| **pytest-cov** | (latest) | Cobertura de tests |
| **httpx** | (latest) | Cliente HTTP para tests |

### Infraestructura

| Herramienta | Propósito |
|-----------|----------|
| **Docker** | Containerización |
| **Docker Compose** | Orquestación multi-contenedor |
| **Git/GitHub** | Control de versiones |

---

## 📁 Project Structure

```
.
├── .agents/
│   ├── rules/                    # Reglas del proyecto para agentes
│   │   ├── 01-architecture.md
│   │   ├── 02-naming.md
│   │   ├── 03-dx.md
│   │   ├── 04-testing.md
│   │   ├── 05-documentation.md
│   │   ├── 06-api.md
│   │   ├── 07-components.md
│   │   ├── 08-security.md
│   │   ├── 09-data.md
│   │   ├── 10-performance.md
│   │   ├── 11-observability.md
│   │   ├── 12-structure.md
│   │   └── index.md
│   └── skills/                   # Skills disponibles para agentes
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── dashboard/        # Componentes del dashboard
│   │   │   │   ├── kpi-card.tsx
│   │   │   │   ├── kpi-row.tsx
│   │   │   │   ├── dashboard-header.tsx
│   │   │   │   ├── income-outcome-chart.tsx
│   │   │   │   └── profit-percent-chart.tsx
│   │   │   └── ui/               # Componentes reutilizables
│   │   │       ├── card.tsx
│   │   │       └── skeleton.tsx
│   │   ├── lib/
│   │   │   ├── financial-types.ts    # TIPOS CENTRALIZADOS
│   │   │   ├── financial-utils.ts    # Funciones puras
│   │   │   ├── financial-utils.test.ts
│   │   │   └── utils.ts
│   │   ├── App.tsx               # Componente principal
│   │   └── main.tsx              # Entry point
│   ├── vite.config.ts            # Configuración con proxy
│   ├── tailwind.config.js        # Configuración Tailwind
│   ├── tsconfig.json
│   ├── package.json
│   ├── .env.example
│   └── eslint.config.js
│
├── backend/
│   ├── app/
│   │   ├── main.py               # Entry point + CORS config
│   │   └── routes.py             # Endpoints API + modelos Pydantic
│   ├── tests/
│   │   ├── conftest.py
│   │   └── test_routes.py
│   ├── requirements.txt
│   └── Dockerfile
│
├── memory-bank/                  # 📍 Documentación de proyecto (esta carpeta)
│   ├── PROJECT_OVERVIEW.md       # Este archivo
│   ├── TECHNICAL_STACK.md        # Stack técnico detallado
│   ├── CURRENT_STATUS.md         # Estado actual y limitaciones
│   └── DEVELOPMENT_ROADMAP.md    # Prioridades de desarrollo
│
├── docker-compose.yml
├── verification.md
├── CONCRETE_FINDINGS.md          # Hallazgos verificables
├── PROJECT_RULES.md              # Reglas del proyecto
├── FINDINGS_BY_CATEGORY.md       # Hallazgos agrupados
├── AGENTS.md
├── README.md
└── README.es.md
```

### Entry Points

- **Frontend**: `frontend/src/main.tsx` → Puerto 5173 (Vite)
- **Backend**: `backend/app/main.py` → Puerto 8000 (Uvicorn)

### Conexión Frontend-Backend

```typescript
// frontend/vite.config.ts (líneas 9-14)
server: {
  proxy: {
    "/api": {
      target: "http://backend:8000",
      changeOrigin: true,
    },
  },
}
```

El frontend usa Vite proxy para redirigir `/api/*` al backend. Esto evita CORS issues en desarrollo.

---

## 💡 Key Conventions & Patterns

### Naming Conventions

| Ámbito | Convención | Ejemplo |
|--------|-----------|---------|
| Componentes React | kebab-case | `kpi-card.tsx`, `income-outcome-chart.tsx` |
| Funciones/Métodos | camelCase (JS) / snake_case (Python) | `computeKPIs()`, `generate_mock_movements()` |
| Tipos/Interfaces | PascalCase | `KPIMetrics`, `FinancialMovement` |
| Literales de tipo | snake_case | `operation_type`, `business_type` |
| Imports con alias | `@/` | `@/components/dashboard/kpi-card` |

### Import Alias Configuration

Frontend usa `@/` para imports relativos a `src/`:

```typescript
// Configurado en frontend/vite.config.ts
resolve: {
  alias: {
    "@": path.resolve(__dirname, "./src"),
  },
}

// Uso en App.tsx
import { KPIRow } from "@/components/dashboard/kpi-row";
import { type FinancialMovement } from "@/lib/financial-types";
```

### Type Centralization

Todos los tipos compartidos entre frontend y backend se definen en:
- **Frontend**: `frontend/src/lib/financial-types.ts`
- **Backend**: Tipos equivalentes con Pydantic en `backend/app/routes.py`

```typescript
// Frontend: financial-types.ts
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

export interface KPIMetrics {
  totalIncome: number
  totalOutcome: number
  profit: number
  profitPercent: number
}
```

```python
# Backend: routes.py
OperationType = Literal["income", "outcome"]
Category = Literal["suppliers", "sales", "operational", "administrative", "others"]
BusinessType = Literal["B2B", "B2C"]

class FinancialMovement(BaseModel):
    create_date: date
    amount: float
    operation_type: OperationType
    category: Category
    business_type: BusinessType
```

### Component Architecture

- **Componentes de UI**: `frontend/src/components/ui/` (genéricos, reutilizables)
- **Componentes de Negocio**: `frontend/src/components/dashboard/` (específicos del dominio)
- **Funciones Puras**: `frontend/src/lib/financial-utils.ts` (lógica sin side effects)

### Record<> Pattern para Variantes

```typescript
// frontend/src/components/dashboard/kpi-card.tsx
const variantStyles: Record<KPICardProps['variant'], { badge: string; icon: string }> = {
  income: { badge: '...', icon: '...' },
  outcome: { badge: '...', icon: '...' },
  profit: { badge: '...', icon: '...' },
  profitPercent: { badge: '...', icon: '...' },
}
```

### Accessibility

Frontend incluye aria-labels en secciones principales:

```typescript
<section aria-label="Key performance indicators">
  <KPIRow metrics={metrics} loading={loading} />
</section>

<section aria-label="Financial charts" className="grid...">
  <IncomeOutcomeChart data={monthlyData} loading={loading} />
  <ProfitPercentChart data={monthlyData} loading={loading} />
</section>
```

---

## 📊 API Endpoints

Backend expone los siguientes endpoints (todos públicos actualmente - ⚠️ Ver limitaciones):

| Endpoint | Método | Parámetros | Respuesta |
|----------|--------|-----------|----------|
| `/api/metrics` | GET | (ninguno) | `FinancialMovement[]` |
| `/api/metrics/summary` | GET | `period` (query) | `MetricsSummaryItem[]` |
| `/api/metrics/top-categories` | GET | `limit` (query) | `TopCategoryItem[]` |
| `/api/metrics/comparison` | GET | `current_period`, `previous_period` | `MetricsComparison` |
| `/api/metrics/alert` | GET | `period` (query) | `MetricsAlert` |
| `/api/metrics/facets` | GET | (ninguno) | `MetricsFacets` |
| `/api/health` | GET | (ninguno) | `{ status: "ok" }` |

**Documentación interactiva**: http://localhost:8000/docs (Swagger UI)

---

## 🧪 Testing

### Frontend
- **Framework**: Vitest
- **Test files**: `frontend/src/lib/financial-utils.test.ts`
- **Coverage**: Disponible via `npm test:coverage`
- **Comando**: `npm test` (run), `npm test:watch` (watch mode)

### Backend
- **Framework**: pytest
- **Test files**: `backend/tests/test_routes.py`
- **Comando**: `pytest` o `pytest --cov`

### Estado Actual
- ✅ Tests unitarios presentes en ambos lados
- ❌ No hay tests E2E
- ⚠️ Cobertura moderada, hay espacio para mejora

---

## 🚀 How to Run

### Local Development (Recomendado)

```bash
# En la raíz del repositorio
docker compose up --build

# Accedible en:
# Frontend: http://localhost:5173
# Backend: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

### Frontend Only

```bash
cd frontend
npm install
npm run dev
# http://localhost:5173
```

### Backend Only

```bash
cd backend
pip install -r requirements.txt
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
# http://localhost:8000
```

---

## 📍 See Also

- [CURRENT_STATUS.md](./CURRENT_STATUS.md) - Estado actual, funcionalidades y limitaciones confirmadas
- [TECHNICAL_STACK.md](./TECHNICAL_STACK.md) - Stack técnico detallado por componente
- [DEVELOPMENT_ROADMAP.md](./DEVELOPMENT_ROADMAP.md) - Prioridades y próximas features
- [../PROJECT_RULES.md](../PROJECT_RULES.md) - Reglas del proyecto completas
- [../CONCRETE_FINDINGS.md](../CONCRETE_FINDINGS.md) - Hallazgos verificables en código

