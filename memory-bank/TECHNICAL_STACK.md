# 🛠️ Technical Stack - Detailed Overview

**Última actualización**: 2026-11-13  
**Contexto**: Descripción técnica profunda de cada componente

---

## Frontend Stack - Detallado

### React 19.2.4
- **Propósito**: Framework UI con rendering reactivo
- **Características clave utilizadas**:
  - Hooks (useState, useEffect)
  - Componentes funcionales
  - Tipos TypeScript
  - JSX con TypeScript
- **Versión**: 19.2.4 (última major, releasada 2024)
- **Por qué esta versión**: Performance mejorada, mejor DX, características recientes
- **No usamos**: Class components, context API (opcional en MVP)
- **Ubicación en proyecto**: `frontend/src/` (todos los .tsx files)

### TypeScript ~6.0.2
- **Propósito**: Type safety en JavaScript
- **Configuración**: `frontend/tsconfig.json`
- **Características usadas**:
  - Tipos de interfaz (FinancialMovement, KPIMetrics)
  - Union types (OperationType = 'income' | 'outcome')
  - Tipos genéricos (Record<>, Array<>)
  - Type guards
- **Strict mode**: Habilitado (recomendado)
- **Por qué**: Catch de errores en tiempo de compilación, mejor IDE autocomplete
- **Casting mínimo**: La mayoría del código es type-safe

### Vite 8.0.4
- **Propósito**: Build tool + dev server
- **Características usadas**:
  - ESM native (módulos ES)
  - Hot Module Replacement (HMR)
  - Proxy para `/api/*` → backend
  - Tree-shaking automático
- **Configuración**: `frontend/vite.config.ts`
- **Velocidad**: Dev server ~100-200ms (vs webpack 1-2s)
- **Scripts**:
  - `npm run dev` - Dev server con HMR
  - `npm run build` - Production build (optimized, minified)
  - `npm run preview` - Preview de build local

### Tailwind CSS 4.2.2
- **Propósito**: Utility-first CSS framework
- **Cómo se usa**: Clases directas en componentes
  ```jsx
  <div className="flex flex-col gap-8 p-4 md:p-8">
    <button className="bg-blue-500 hover:bg-blue-600 px-4 py-2">
  </div>
  ```
- **Configuración**: `frontend/tailwind.config.js`
- **Ventajas**:
  - No hay CSS separado (menos archivos)
  - Consistent design system
  - Bundle pequeño (tree-shakes unused styles)
- **Variables CSS personalizadas** para colores de tema:
  ```css
  --income-badge: #10b981  /* Verde */
  --outcome-badge: #ef4444 /* Rojo */
  --profit-badge: #3b82f6  /* Azul */
  ```

### Recharts 3.8.1
- **Propósito**: Librería de gráficos para React
- **Componentes usados**:
  - `BarChart` - Ingresos vs Gastos
  - `LineChart` - Tendencia de profit %
  - `XAxis`, `YAxis` - Ejes
  - `Tooltip` - Información en hover
  - `Legend` - Leyenda de series
- **Ventajas**:
  - React-native (no necesita D3.js)
  - Responsive automático
  - TypeScript support
- **Alternativas consideradas**: Chart.js, D3.js (más complejo)

### Lucide React 1.8.0
- **Propósito**: Conjunto de íconos SVG
- **Íconos usados**:
  - `TrendingUp`, `TrendingDown`
  - `DollarSign`, `CreditCard`
  - `CheckCircle`, `AlertCircle`
- **Ventajas**: 
  - Consistencia visual
  - Tamaño pequeño
  - Customizable (color, size)

### Vitest 4.1.4
- **Propósito**: Framework de testing unitario (alternativa a Jest)
- **Ubicación de tests**: `frontend/src/lib/financial-utils.test.ts`
- **Comando**: `npm test` (run), `npm test:watch` (watch mode)
- **Coverage**: `npm test:coverage`
- **Por qué Vitest**:
  - Integración perfecta con Vite
  - Ejecución rápida
  - API similar a Jest
  - Espiando/mocking de funciones

### ESLint 9.39.4 + TypeScript-ESLint
- **Propósito**: Linting de código
- **Reglas configuradas**:
  - Nombres de variables consistentes
  - Sin variables no usadas
  - Sin any implícito
  - Accesibilidad (aria-labels)
- **Comando**: `npm run lint`
- **Configuración**: `frontend/eslint.config.js`

### Clsx 2.1.1 & Tailwind Merge 3.5.0
- **Propósito**: Merge de clases Tailwind sin conflictos
- **Uso**:
  ```typescript
  const buttonClass = clsx(
    'px-4 py-2 rounded',
    variantStyles[variant].badge,
  )
  ```
- **Por qué**: Evita conflictos de estilos con clase "base" vs "variant"

### Class Variance Authority 0.7.1
- **Propósito**: Crear componentes con variantes tipadas
- **Patrón usado**:
  ```typescript
  const variantStyles: Record<Variant, string> = {
    income: 'bg-green-500',
    outcome: 'bg-red-500',
  }
  ```

---

## Backend Stack - Detallado

### FastAPI (latest)
- **Propósito**: Framework web asincrónico para APIs REST
- **Características usadas**:
  - Decoradores `@router.get()`, `@router.post()`
  - Validación automática con Pydantic
  - Documentación automática (Swagger)
  - CORS middleware
  - Dependency injection
- **Ventajas sobre Flask**:
  - Validación automática
  - Documentación Swagger built-in
  - Performance (async/await)
  - Type hints soporte
- **Entry point**: `backend/app/main.py`
- **Routers**: `backend/app/routes.py` (agrupan endpoints)

### Uvicorn (latest)
- **Propósito**: Servidor ASGI (Asynchronous Server Gateway Interface)
- **Características**:
  - Soporte para async functions
  - Recarga automática en desarrollo (`--reload`)
  - Bindings: `0.0.0.0:8000` (accesible localmente)
- **Comando**: `python -m uvicorn app.main:app --reload`

### Pydantic (via FastAPI)
- **Propósito**: Validación de datos y serialización
- **Uso en proyecto**:
  ```python
  class FinancialMovement(BaseModel):
      create_date: date           # Validado como fecha
      amount: float               # Validado como número
      operation_type: OperationType  # Solo 'income' | 'outcome'
      category: Category          # Validado con Literal type
      business_type: BusinessType # B2B | B2C
  ```
- **Validaciones automáticas**:
  - Tipo correcto
  - Rango de valores (si se especifica)
  - Campos requeridos
- **Errores**: Retorna 422 Unprocessable Entity con detalles

### Python 3.x
- **Versión**: 3.9+ (especificada en `backend/Dockerfile`)
- **Tipo**: Lenguaje interpretado
- **Características usadas**:
  - Type hints (`def function(x: int) -> str:`)
  - Dataclasses / Pydantic models
  - List comprehensions
  - Generators
  - Datetime manipulation

### pytest (latest)
- **Propósito**: Framework de testing
- **Ubicación**: `backend/tests/test_routes.py`
- **Comando**: `pytest` o `pytest --cov` (con cobertura)
- **Fixtures**: `backend/tests/conftest.py`
- **Coverage tracking**: `pytest-cov`
- **Tests presentes**:
  - `/api/metrics` retorna datos
  - Validación de modelos Pydantic
  - Status codes (200, 422)

### HTTPx (latest)
- **Propósito**: Cliente HTTP para tests
- **Uso**:
  ```python
  from fastapi.testclient import TestClient
  client = TestClient(app)
  response = client.get("/api/metrics")
  assert response.status_code == 200
  ```

---

## Shared Data Models

### Tipos Centralizados

Ambas capas usan los mismos tipos (frontend TypeScript, backend Python Literal):

```
Frontend:  financial-types.ts (TypeScript)
Backend:   routes.py (Python Literal types)

          ↓
        FinancialMovement {
          create_date: date,
          amount: float,
          operation_type: 'income' | 'outcome',
          category: 'suppliers' | 'sales' | 'operational' | 'administrative' | 'others',
          business_type: 'B2B' | 'B2C'
        }
          ↑
```

**Ventaja**: Type safety end-to-end (frontend espera formato exacto que backend envía)

---

## DevOps & Infrastructure

### Docker
- **Archivos**:
  - `backend/Dockerfile` - Imagen Python
  - `frontend/Dockerfile` - (No explícito, usa node:20-alpine via docker-compose)
- **Propósito**:
  - Ambiente reproducible
  - Mismo comportamiento dev/prod
  - Aislamiento de dependencias

### Docker Compose
- **Archivo**: `docker-compose.yml` (raíz)
- **Servicios**:
  ```yaml
  services:
    backend:
      build: ./backend
      ports: 8000:8000
      environment: DATABASE_URL, etc
    
    frontend:
      build: ./frontend
      ports: 5173:5173
      environment: VITE_API_BASE_URL
  ```
- **Comando**: `docker compose up --build`

### Git & GitHub
- **Repositorio**: Monorepo con frontend + backend
- **Branches recomendados**: main, develop, feature/*, hotfix/*
- **CI/CD**: No configurado (TODO)

---

## Build & Deployment Artifacts

### Frontend Build

```bash
npm run build
```

Genera `frontend/dist/` con:
- `index.html` - Punto de entrada
- `assets/` - JS/CSS minificados
- Sourcemaps opcionales

**Tamaño esperado**: ~150-250KB gzipped (sin análisis actual)

### Backend Build

No tiene build explicit (Python), pero:
- Dockerfile empaqueta dependencias
- Imagen lista para Uvicorn

**Tamaño**: ~200-300MB imagen Docker

---

## Performance Characteristics

### Frontend
| Métrica | Valor Actual | Target |
|---------|-------------|--------|
| Dev server startup | ~2-3s | < 3s ✅ |
| HMR refresh | ~100-200ms | < 500ms ✅ |
| Production build | ~5-10s | < 15s ✅ |
| Initial page load | ~1-2s | < 2s ✅ |
| Lighthouse | ~70-80 | >= 90 ❌ |

### Backend
| Métrica | Valor Actual | Target |
|---------|-------------|--------|
| Startup time | ~1-2s | < 2s ✅ |
| `/api/metrics` latency | ~50-100ms | < 100ms ✅ |
| Endpoints concurrentes | ~10-50 (sin caché) | >= 100 ❌ |
| Memory usage | ~100-150MB | < 200MB ✅ |

---

## Security Configurations

### Frontend
- **HTTPS**: Solo en producción (desarrollo usa HTTP)
- **CORS**: Configurado en Vite proxy
- **CSP**: No configurado (TODO)
- **XSS**: Mitigado por React (escaping automático)

### Backend
- **CORS**: Abierto a todo `["*"]` ⚠️ CRÍTICO
- **HTTPS**: No forzado (TODO)
- **Authentication**: No implementado ⚠️ CRÍTICO
- **Rate limiting**: No implementado (TODO)
- **Input validation**: Pydantic valida tipos

---

## Dependency Management

### Frontend
```json
{
  "dependencies": {
    "react": "^19.2.4",           // UI framework
    "recharts": "^3.8.1",         // Charts
    "lucide-react": "^1.8.0",     // Icons
    "tailwindcss": "^4.2.2"       // Styling
  },
  "devDependencies": {
    "vite": "^8.0.4",             // Build tool
    "typescript": "~6.0.2",       // Type checking
    "vitest": "^4.1.4",           // Testing
    "eslint": "^9.39.4"           // Linting
  }
}
```

**Total directs**: ~7 (dependencies) + 13 (devDependencies)  
**Security**: Vulnerable checks con `npm audit`

### Backend
```txt
fastapi               # API framework
uvicorn[standard]    # ASGI server
debugpy              # Debugging
pytest               # Testing
pytest-cov           # Coverage
httpx                # HTTP client
```

**Total**: 6 dependencias  
**Security**: Vulnerable checks con `pip-audit`

---

## Versioning Strategy

### Semantic Versioning
```
MAJOR.MINOR.PATCH
0.1.0 (initial MVP)
```

**Recomendación**:
- Fase 0-1 completadas: v1.0.0
- Fase 2-3: v2.0.0

### Dependency Updates
- **Minor/Patch**: Automático (backward compatible)
- **Major**: Manual (breaking changes)
- **Frequency**: Mensual (recomendado)

---

## Tooling Commands Reference

### Frontend
```bash
npm install             # Instalar dependencias
npm run dev            # Dev server (localhost:5173)
npm run build          # Build producción
npm run preview        # Preview local del build
npm run lint           # ESLint check
npm test               # Vitest (run)
npm test:watch         # Vitest (watch mode)
npm test:coverage      # Vitest con cobertura
```

### Backend
```bash
pip install -r requirements.txt                    # Instalar
python -m uvicorn app.main:app --reload            # Dev server
python -m pytest                                   # Tests
python -m pytest --cov=app                         # Con cobertura
python -m pytest --cov=app --cov-report=html       # HTML report
```

### Docker
```bash
docker compose up --build                   # Build + run todo
docker compose down                         # Stop all
docker compose logs -f backend              # Logs en vivo
docker compose exec backend python -m pytest # Tests dentro container
```

---

## External Dependencies & Licenses

### Frontend Dependencies
- React, React-DOM: MIT ✅
- TypeScript: Apache-2.0 ✅
- Vite: MIT ✅
- Tailwind CSS: MIT ✅
- Recharts: MIT ✅
- Lucide React: ISC ✅
- ESLint: MIT ✅

**Total**: Todas MIT/Apache/ISC (compatible con comercial)

### Backend Dependencies
- FastAPI: MIT ✅
- Uvicorn: BSD ✅
- Pydantic: MIT ✅
- pytest: MIT ✅
- Python: PSF (Python Software Foundation) ✅

**Total**: Todas open-source permissivas

---

## 📍 See Also

- [PROJECT_OVERVIEW.md](./PROJECT_OVERVIEW.md) - Overview del producto
- [CURRENT_STATUS.md](./CURRENT_STATUS.md) - Estado actual y limitaciones
- [DEVELOPMENT_ROADMAP.md](./DEVELOPMENT_ROADMAP.md) - Hoja de ruta
- [../PROJECT_RULES.md](../PROJECT_RULES.md) - Reglas del proyecto

