# 📋 Reglas del Proyecto - Hallazgos Convertidos a Normas

**Conjunto de reglas accionables derivadas de hechos verificables en el código**

Cada regla cita al menos un hecho concreto del repositorio (archivo + línea).

---

## 🏛️ REGLAS DE ARQUITECTURA

### REGLA-ARCH-001: Monorepo con Frontend y Backend Separados

**Norma**: Mantener frontend y backend en carpetas independientes del mismo repositorio.

**Hecho citado**: Estructura en raíz con carpetas `frontend/` y `backend/` (CONCRETE_FINDINGS.md)

**Por qué**: Facilita versionado compartido, configuración compartida (docker-compose.yml), y tipos compartidos (financial-types.ts)

**Verificable en**:
- `frontend/src/` → Aplicación React independiente
- `backend/app/` → Aplicación FastAPI independiente
- `docker-compose.yml` → Orquestan ambas

**Aplicación**: Nuevas features deben respetar esta separación.

---

### REGLA-ARCH-002: Entry Points Únicos y Claros

**Norma**: Cada aplicación tiene un único entry point principal.

**Hecho citado**: 
- Frontend: `frontend/src/main.tsx` (verification.md, línea 125)
- Backend: `backend/app/main.py` (verification.md, línea 126)

**Por qué**: Claridad absoluta sobre dónde comienza la ejecución. Evita confusiones en debugging.

**Aplicación**: No crear entry points alternativos; si necesitas múltiples, refactoriza el existente.

---

### REGLA-ARCH-003: Frontend-Backend Comunican vía Proxy en Desarrollo

**Norma**: El frontend usa Vite proxy configurado para redirigir `/api/*` al backend.

**Hecho citado**: `frontend/vite.config.ts:9-14` (CONCRETE_FINDINGS.md, línea 119)

```typescript
server: {
  proxy: {
    "/api": {
      target: "http://backend:8000",
      changeOrigin: true,
    },
  },
}
```

**Por qué**: Evita CORS issues en desarrollo. Frontend en puerto 5173, backend en 8000.

**Aplicación**: No cambiar este mapeo sin actualizar documentación. Todos los requests frontend a `/api` usan este proxy.

---

### REGLA-ARCH-004: Stack Técnico Moderno y Consensuado

**Norma**: Frontend usa React 19 + TypeScript 6 + Vite. Backend usa FastAPI + Python.

**Hecho citado**: `frontend/package.json` (React 19.2.4, TypeScript 6.0.2, Vite 8.0.4)

**Por qué**: Versiones actuales ofrecen mejor performance, seguridad y DX.

**Aplicación**: Actualizar dependencias periódicamente. No cambiar frameworks sin consenso.

---

## 📝 REGLAS DE NAMING

### REGLA-NOM-001: Componentes React en kebab-case

**Norma**: Todos los archivos de componentes usan kebab-case.

**Hecho citado**: `frontend/src/components/dashboard/` (CONCRETE_FINDINGS.md, línea 10)

```
✓ kpi-card.tsx
✓ income-outcome-chart.tsx
✓ profit-percent-chart.tsx
✓ dashboard-header.tsx
```

**Por qué**: Consistencia visual y facilita búsquedas (todos coinciden: guiones, lowercase).

**Contraejemplo evitar**: 
- ❌ KpiCard.tsx (PascalCase)
- ❌ kpi_card.tsx (snake_case)

**Aplicación**: Cualquier nuevo componente debe ser `new-component.tsx`.

---

### REGLA-NOM-002: Importes Frontend Usan Alias @

**Norma**: Usar `@` para importar desde `src/`.

**Hecho citado**: `frontend/vite.config.ts:10` (CONCRETE_FINDINGS.md, línea 100) y `frontend/src/App.tsx:8` (CONCRETE_FINDINGS.md, línea 108)

**Código**:
```typescript
// ✓ Correcto
import { KPIRow } from "@/components/dashboard/kpi-row";

// ❌ Evitar
import { KPIRow } from "../../../components/dashboard/kpi-row";
```

**Por qué**: Elimina rutas relativas confusas. Claridad y legibilidad.

**Aplicación**: Todos los imports internos deben usar `@`.

---

### REGLA-NOM-003: Tipos Centralizados en `financial-types.ts`

**Norma**: Todos los tipos compartidos (frontend y backend) se definen en `frontend/src/lib/financial-types.ts`.

**Hecho citado**: `frontend/src/lib/financial-types.ts` (CONCRETE_FINDINGS.md, línea 125)

```typescript
export type OperationType = 'income' | 'outcome'
export type Category = 'suppliers' | 'sales' | 'operational' | 'administrative' | 'others'
export type BusinessType = 'B2B' | 'B2C'

export interface FinancialMovement { ... }
export interface KPIMetrics { ... }
```

**Por qué**: Sincronización frontend-backend. Una fuente de verdad para tipos.

**Aplicación**: Nuevos tipos deben ir aquí. Backend importa (o espeja) desde aquí.

---

### REGLA-NOM-004: Backend usa snake_case

**Norma**: Funciones y variables en backend usan snake_case.

**Hecho citado**: `backend/app/routes.py` (CONCRETE_FINDINGS.md, línea 173)

```python
def get_metrics(...)
def generate_mock_movements(seed=42)
```

**Por qué**: Convención Python estándar (PEP 8).

**Aplicación**: Coherencia con estándares de Python. No cambiar.

---

## 🎯 REGLAS DE DEVELOPER EXPERIENCE

### REGLA-DX-001: npm Scripts Estándar

**Norma**: Frontend expone scripts estándar para dev, build, lint, test.

**Hecho citado**: `frontend/package.json` (CONCRETE_FINDINGS.md, línea 149)

```json
{
  "scripts": {
    "dev": "vite",
    "build": "tsc -b && vite build",
    "lint": "eslint .",
    "test": "vitest run",
    "test:watch": "vitest",
    "test:coverage": "vitest run --coverage"
  }
}
```

**Por qué**: Developers esperan `npm run dev`, `npm run build`, `npm test`.

**Aplicación**: Mantener estos scripts. No cambiar nombres.

---

### REGLA-DX-002: TypeScript Strict Mode Habilitado

**Norma**: Frontend tiene TypeScript strict mode activado.

**Hecho citado**: `frontend/tsconfig.app.json` (CONCRETE_FINDINGS.md, línea 160)

```json
{
  "compilerOptions": {
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true
  }
}
```

**Por qué**: Detecta errores en tiempo de compilación, no en runtime.

**Aplicación**: No desactivar estas flags. Resolver errores TypeScript antes de commit.

---

### REGLA-DX-003: Hot-Reload Automático

**Norma**: Tanto frontend (Vite HMR) como backend (Uvicorn reload=True) tienen hot-reload.

**Hecho citado**: 
- Frontend: Vite automático en `vite.config.ts`
- Backend: `backend/app/main.py` con `reload=True` (CONCRETE_FINDINGS.md, línea 309)

**Por qué**: Feedback inmediato al cambiar código. Desarrollo ágil.

**Aplicación**: No desactivar en desarrollo. Usa en producción con `reload=False`.

---

## 🧪 REGLAS DE TESTING

### REGLA-TEST-001: Tests Unitarios Presentes

**Norma**: Frontend y backend tienen tests unitarios.

**Hecho citado**: 
- Frontend: `frontend/src/lib/financial-utils.test.ts`
- Backend: `backend/tests/test_routes.py` (CONCRETE_FINDINGS.md, línea 275)

**Por qué**: Verificar funcionalidad y evitar regresiones.

**Aplicación**: Nuevo código debe incluir tests. Ejecutar antes de commit: `npm test`

---

### REGLA-TEST-002: Sin Tests E2E (Limitación Actual)

**Norma**: Proyecto actual no tiene tests end-to-end (E2E).

**Hecho citado**: CONCRETE_FINDINGS.md menciona "❌ No hay tests E2E"

**Por qué**: Tests E2E requieren orquestación completa, herramientas adicionales.

**Aplicación**: Plantear agregar E2E tests (Cypress, Playwright) en próximas iteraciones.

---

## 📚 REGLAS DE DOCUMENTACIÓN

### REGLA-DOC-001: README en Inglés y Español

**Norma**: Proyecto tiene README.md y README.es.md.

**Hecho citado**: Archivos presentes en raíz (verification.md, línea 85)

**Por qué**: Accesibilidad para comunidades internacional e hispanohablante.

**Aplicación**: Mantener ambos sincronizados. Cambio en uno = cambio en otro.

---

### REGLA-DOC-002: .env.example Documenta Variables

**Norma**: `.env.example` lista todas las variables de ambiente necesarias.

**Hecho citado**: `frontend/.env.example` (CONCRETE_FINDINGS.md, línea 261)

**Por qué**: Nuevos developers saben qué variables configurar.

**Aplicación**: Actualizar `.env.example` cuando agregues nuevas variables.

---

### REGLA-DOC-003: Documentación Técnica Separada

**Norma**: AGENTS.md documenta cómo contribuir.

**Hecho citado**: Archivo presente en raíz (verification.md, línea 85)

**Por qué**: Agentes IA y contribuidores nuevos entiendan el proyecto.

**Aplicación**: Actualizar AGENTS.md cuando cambien procesos.

---

## 🔌 REGLAS DE API DESIGN

### REGLA-API-001: 9 Endpoints GET Documentados

**Norma**: Backend expone 9 endpoints GET con propósitos claros.

**Hecho citado**: `backend/app/routes.py` (CONCRETE_FINDINGS.md, línea 278)

```
GET /health                    (línea 134)
GET /api/metrics               (línea 141)
GET /api/metrics/facets        (línea 155)
GET /api/metrics/summary       (línea 162)
GET /api/metrics/categories/top (línea 179)
GET /api/metrics/comparison    (línea 197)
GET /api/metrics/alerts        (línea 218)
GET /api/metrics/b2b           (línea 237)
GET /api/metrics/b2c           (línea 259)
```

**Por qué**: Cobertura clara de funcionalidades de KPIs, métricas, categorías.

**Aplicación**: Nuevos endpoints deben documentarse con línea exacta.

---

### REGLA-API-002: Query Parameters Explícitos

**Norma**: Endpoints aceptan Query params tipados explícitamente.

**Hecho citado**: `backend/app/routes.py:141-155` (CONCRETE_FINDINGS.md, línea 194)

```python
@router.get("/api/metrics", response_model=list[FinancialMovement])
def get_metrics(
    start_date: date | None = Query(default=None),
    end_date: date | None = Query(default=None),
    category: Category | None = Query(default=None),
    operation_type: OperationType | None = Query(default=None),
) -> list[FinancialMovement]:
```

**Por qué**: Swagger automático. Type hints claros. Validación automática.

**Aplicación**: Todos los params usar `Query(default=...)`.

---

### REGLA-API-003: Response Models Explícitos

**Norma**: Todos los endpoints definen `response_model`.

**Hecho citado**: `backend/app/routes.py:140-142` (CONCRETE_FINDINGS.md, línea 200)

```python
@router.get("/api/metrics", response_model=list[FinancialMovement])
def get_metrics(...) -> list[FinancialMovement]:
    return movements
```

**Por qué**: Validación automática de response. Documentación Swagger exacta.

**Aplicación**: No devolver datos sin `response_model` en FastAPI.

---

## 🎨 REGLAS DE COMPONENTES

### REGLA-COMP-001: Record<> para Type-Safe Variants

**Norma**: Componentes con múltiples variantes usan `Record<>`.

**Hecho citado**: `frontend/src/components/dashboard/kpi-card.tsx:12-25` (CONCRETE_FINDINGS.md, línea 130)

```typescript
const variantStyles: Record<KPICardProps['variant'], { badge: string; icon: string }> = {
  income: { badge: 'bg-[var(--income-badge)]', icon: 'text-[var(--income-badge-fg)]' },
  outcome: { badge: 'bg-[var(--outcome-badge)]', icon: 'text-[var(--outcome-badge-fg)]' },
  profit: { badge: 'bg-[var(--profit-badge)]', icon: 'text-[var(--profit-badge-fg)]' },
  profitPercent: { badge: 'bg-[var(--profit-badge)]', icon: 'text-[var(--profit-badge-fg)]' },
}
```

**Por qué**: TypeScript previene falta de keys. Claridad visual. Type-safe.

**Aplicación**: Usar para componentes con 2+ variantes.

---

### REGLA-COMP-002: Aria Labels para Accesibilidad

**Norma**: Secciones principales tienen `aria-label`.

**Hecho citado**: `frontend/src/App.tsx:48-52` (CONCRETE_FINDINGS.md, línea 140)

```typescript
<section aria-label="Key performance indicators">
  <KPIRow metrics={metrics} loading={loading} />
</section>

<section aria-label="Financial charts">
  ...
</section>
```

**Por qué**: Accesibilidad para screen readers. Semántica clara.

**Aplicación**: Secciones principales deben tener aria-label.

---

### REGLA-COMP-003: Funciones Puras sin Side Effects

**Norma**: Lógica de cálculo (KPIs, datos) en funciones puras.

**Hecho citado**: `frontend/src/lib/financial-utils.ts` (CONCRETE_FINDINGS.md, línea 146)

```typescript
export function computeKPIs(movements: FinancialMovement[]): KPIMetrics {
  const totalIncome = movements
    .filter((m) => m.operation_type === "income")
    .reduce((sum, m) => sum + m.amount, 0);
  // ... lógica pura
  return { totalIncome, totalOutcome, profit, profitPercent };
}
```

**Por qué**: Testeable. Predecible. Reutilizable.

**Aplicación**: Mover lógica de componentes a utils cuando sea posible.

---

## 🔐 REGLAS DE SEGURIDAD

### REGLA-SEC-001: CORS Debe Ser Restringido (⚠️ CRÍTICO)

**Norma**: CORS está abierto a todo (`["*"]`), debe ser configurado en producción.

**Hecho citado**: `backend/app/main.py:6-11` (CONCRETE_FINDINGS.md, línea 230)

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # ⚠️ CRÍTICO
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**Por qué**: Vulnerable a CSRF y exposición de datos.

**Aplicación - Dev**: Aceptable usar `["*"]`  
**Aplicación - Prod**: Cambiar a dominios específicos:
```python
allow_origins=["https://yourdomain.com", "https://www.yourdomain.com"]
```

---

### REGLA-SEC-002: Endpoints Requieren Autenticación (⚠️ CRÍTICO)

**Norma**: Todos los 9 endpoints públicos actualmente. Necesitan protección.

**Hecho citado**: `backend/app/routes.py` sin validación de token (CONCRETE_FINDINGS.md, línea 242)

**Por qué**: Cualquiera puede acceder a datos financieros.

**Aplicación**: Implementar autenticación:
- JWT tokens
- API keys
- OAuth2

---

### REGLA-SEC-003: Validación Runtime en Frontend

**Norma**: Frontend no valida tipos de response. Asumir que API devuelve tipos correctos.

**Hecho citado**: `frontend/src/App.tsx:16-19` (CONCRETE_FINDINGS.md, línea 253)

```typescript
async function fetchFinancialData(): Promise<FinancialMovement[]> {
  const response = await fetch(`${API_BASE_URL}/api/metrics`);
  return response.json();  // ⚠️ Sin validación
}
```

**Por qué**: Defensibilidad. Backend podría cambiar formato.

**Aplicación**: Usar Zod o Pydantic para validar response:
```typescript
const FinancialMovementSchema = z.array(FinancialMovement);
const validated = FinancialMovementSchema.parse(response.json());
```

---

### REGLA-SEC-004: Backend usa Literal Types

**Norma**: Backend valida con Literal types (Pydantic).

**Hecho citado**: `backend/app/routes.py:1-15` (CONCRETE_FINDINGS.md, línea 164)

```python
OperationType = Literal["income", "outcome"]
Category = Literal["suppliers", "sales", "operational", "administrative", "others"]
```

**Por qué**: Pydantic rechaza valores inválidos automáticamente.

**Aplicación**: Mantener Literal types en models. No usar strings sin restricción.

---

## 📊 REGLAS DE DATA HANDLING

### REGLA-DATA-001: Mock Data con seed=42

**Norma**: Datos mock generados con `seed=42` para reproducibilidad.

**Hecho citado**: `backend/app/routes.py:140` (en 8 endpoints) (CONCRETE_FINDINGS.md, línea 295)

```python
movements = generate_mock_movements(seed=42)
```

**Por qué**: Consistencia. Siempre mismos datos. Predecible para tests.

**Aplicación**: No cambiar seed sin actualizar tests. Documentar cambios.

---

### REGLA-DATA-002: Sin Caché Global de Datos

**Norma**: Cada endpoint genera datos desde cero (sin caché).

**Hecho citado**: 8 endpoints en `backend/app/routes.py` llaman a `generate_mock_movements` (CONCRETE_FINDINGS.md, línea 295)

**Por qué**: Datos siempre frescos (pero potencial desperdicio).

**Aplicación - Mejora futura**: Cachear globalmente:
```python
CACHED_MOVEMENTS = None

def get_movements():
    global CACHED_MOVEMENTS
    if CACHED_MOVEMENTS is None:
        CACHED_MOVEMENTS = generate_mock_movements(seed=42)
    return CACHED_MOVEMENTS
```

---

## ⚡ REGLAS DE PERFORMANCE

### REGLA-PERF-001: Proxy Debe Ser Configurable

**Norma**: Proxy está hardcodeado a `http://backend:8000`.

**Hecho citado**: `frontend/vite.config.ts:11` (CONCRETE_FINDINGS.md, línea 270)

```typescript
target: "http://backend:8000",  // ⚠️ Hardcodeado
```

**Por qué**: Solo funciona con docker-compose. No funciona en `localhost`.

**Aplicación - Mejora**: Hacer configurable:
```typescript
target: process.env.VITE_API_TARGET || "http://localhost:8000"
```

---

### REGLA-PERF-002: API_BASE_URL Debe Estar Definido

**Norma**: Frontend define `API_BASE_URL` con default vacío.

**Hecho citado**: `frontend/src/App.tsx:12` (CONCRETE_FINDINGS.md, línea 260)

```typescript
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "";
```

**Por qué**: `""` permite requests a `/api` (relativo). Requiere servidor mismo puerto.

**Aplicación**: Definir `VITE_API_BASE_URL=http://localhost:8000` en `.env.local`.

---

## 🔍 REGLAS DE OBSERVABILITY

### REGLA-OBS-001: Agregar Logging en Backend

**Norma**: Backend actualmente sin logging.

**Hecho citado**: `backend/app/routes.py` sin `print()`, `logging.info()` (CONCRETE_FINDINGS.md, línea 322)

**Por qué**: Debugging imposible en producción. Auditoría ausente.

**Aplicación**: Implementar logging:
```python
import logging

logger = logging.getLogger(__name__)

@router.get("/api/metrics")
def get_metrics(...):
    logger.info(f"Fetching metrics with filters: {filters}")
    try:
        movements = generate_mock_movements(seed=42)
        logger.info(f"Returned {len(movements)} movements")
        return movements
    except Exception as e:
        logger.error(f"Error: {e}")
        raise
```

---

### REGLA-OBS-002: Agregar Tracing Distribuido (Futuro)

**Norma**: Proyecto sin tracing distribuido.

**Por qué**: Debugging de requests frontend-backend requiere correlación.

**Aplicación - Futuro**: Implementar OpenTelemetry o similar.

---

## 📁 REGLAS DE ESTRUCTURA

### REGLA-STR-001: Folder Structure Clara y Consistente

**Norma**: Estructura es clara y bien organizada.

**Hecho citado**: 
- Frontend: `frontend/src/components/`, `frontend/src/lib/` (CONCRETE_FINDINGS.md, línea 1)
- Backend: `backend/app/`, `backend/tests/` (CONCRETE_FINDINGS.md, línea 1)

**Por qué**: Fácil navegar y encontrar código.

**Aplicación**: Mantener estructura. No crear carpetas "util" generales. Agrupar por funcionalidad.

---

## ✅ RESUMEN DE REGLAS

| Categoría | Reglas | Críticas |
|-----------|--------|----------|
| ARQUITECTURA | 4 | 0 |
| NAMING | 4 | 0 |
| DX | 3 | 0 |
| TESTING | 2 | 0 |
| DOCUMENTACIÓN | 3 | 0 |
| API | 3 | 0 |
| COMPONENTES | 3 | 0 |
| SEGURIDAD | 4 | 2 críticas |
| DATA | 2 | 0 |
| PERFORMANCE | 2 | 0 |
| OBSERVABILITY | 2 | 0 |
| ESTRUCTURA | 1 | 0 |

**Total: 33 reglas, 2 críticas para producción**

---

## 🎯 REGLAS CRÍTICAS (Antes de Producción)

1. **REGLA-SEC-001**: Cambiar CORS de `["*"]` a dominios específicos
2. **REGLA-SEC-002**: Implementar autenticación en todos los endpoints

---

**Versión**: 1.0  
**Fecha**: 13 de noviembre de 2026  
**Cada regla cita al menos un hecho del repositorio**
