# 📚 Project Memory Bank

**Última actualización**: 2026-11-13  
**Propósito**: Centralizar la información crítica del proyecto Financial Dashboard para agentes, desarrolladores y stakeholders

---

## 📑 Documentos Principales

### 🎯 [PROJECT_OVERVIEW.md](./PROJECT_OVERVIEW.md)
**Qué leer**: Visión general del proyecto  
**Para quién**: Todos (producto, equipo, nuevos miembros)  
**Tópicos**:
- ¿Qué es el Financial Dashboard?
- Funcionalidades implementadas
- Stack tecnológico (alto nivel)
- Estructura del proyecto
- Convenciones y patrones
- API endpoints disponibles

**Tiempo de lectura**: ~15 minutos

---

### ⚙️ [TECHNICAL_STACK.md](./TECHNICAL_STACK.md)
**Qué leer**: Detalles técnicos profundos  
**Para quién**: Desarrolladores, arquitectos, agentes técnicos  
**Tópicos**:
- Frontend stack (React, TypeScript, Vite, Tailwind, Recharts, etc)
- Backend stack (FastAPI, Uvicorn, Pydantic, pytest)
- Shared data models y tipos centralizados
- DevOps & Infrastructure (Docker, Docker Compose)
- Configuración de build & deployment
- Características de performance
- Comandos de referencia

**Tiempo de lectura**: ~20 minutos

---

### 📊 [CURRENT_STATUS.md](./CURRENT_STATUS.md)
**Qué leer**: Estado actual, funcionalidades, problemas confirmados  
**Para quién**: Equipo de desarrollo, product managers, stakeholders  
**Tópicos**:
- ✅ Features implementadas
- ⚠️ Limitaciones funcionales
- 🚨 Issues críticos de seguridad
- 📈 Estadísticas de código
- 🧪 Cobertura de tests
- 🏗️ Recomendaciones de desarrollo
- 🚀 Release readiness

**Secciones críticas**:
- CORS completamente abierto (crítico)
- Sin autenticación (crítico)
- Sin BD real (funcional)
- Sin tests E2E (importante)

**Tiempo de lectura**: ~15 minutos

---

### 🚀 [DEVELOPMENT_ROADMAP.md](./DEVELOPMENT_ROADMAP.md)
**Qué leer**: Prioridades de desarrollo, fases y timeline  
**Para quién**: Arquitectos, product managers, team leads  
**Tópicos**:
- **FASE 0 (2-3 sem)**: Seguridad crítica (bloqueador)
  - Autenticación (JWT)
  - CORS restringido
  - Validación runtime
  - Logging
  
- **FASE 1 (4-5 sem)**: MVP sólido
  - BD real (PostgreSQL)
  - Tests E2E
  - Variables de entorno
  - Manejo de errores
  
- **FASE 2 (6-8 sem)**: Escala & features
  - Paginación/filtros
  - Caché (Redis)
  - Rate limiting
  - Análisis avanzados
  - Exportación de datos
  
- **FASE 3 (6-8 sem)**: Producción
  - Optimizaciones
  - Monitoreo
  - Seguridad avanzada
  - CI/CD
  - Documentación

- Timeline total: ~24 semanas (6 meses)
- Estimación de recursos
- Success criteria

**Tiempo de lectura**: ~20 minutos

---

## 🎓 Cómo Usar la Memory Bank

### Para Nuevos Miembros del Equipo
1. Leer **PROJECT_OVERVIEW.md** (~15 min) - entiende qué construimos
2. Correr `docker compose up` - experimenta el producto
3. Leer **TECHNICAL_STACK.md** (~20 min) - entiende el stack
4. Ver [../PROJECT_RULES.md](../PROJECT_RULES.md) - entiende las reglas de código
5. Explorar archivos del proyecto - profundizar

### Para Desarrolladores Trabajando en Features
1. Revisar **CURRENT_STATUS.md** - qué ya está hecho
2. Consultar **DEVELOPMENT_ROADMAP.md** - en qué fase estamos
3. Revisar reglas en [../.agents/rules/](../.agents/rules/) - cómo codear
4. Verificar tipos en `frontend/src/lib/financial-types.ts`
5. Seguir convenciones (kebab-case, imports @/, etc)

### Para Agentes/Automatización
1. Revisar todas las fases de roadmap antes de cualquier cambio
2. Consultar **CURRENT_STATUS.md** para entender limitaciones
3. Respetar convenciones en **PROJECT_OVERVIEW.md**
4. Seguir reglas en [../.agents/rules/](../.agents/rules/)
5. No hacer cambios de arquitectura sin consultar roadmap

### Para Stakeholders/Product Managers
1. Leer **PROJECT_OVERVIEW.md** - qué es el producto
2. Revisar **CURRENT_STATUS.md** - features actuales vs limitaciones
3. Estudiar **DEVELOPMENT_ROADMAP.md** - próximos pasos y timeline
4. Preguntar a equipo sobre feasibilidad de nuevas features

### Para Reviews de Seguridad
1. Leer sección de "CRITICAL Security Issues" en **CURRENT_STATUS.md**
2. Revisar [../.agents/rules/08-security.md](../.agents/rules/08-security.md)
3. Consultar reglas de autenticación, CORS, validación
4. Revisar **DEVELOPMENT_ROADMAP.md** FASE 0 (seguridad)

---

## 🔑 Quick Reference

### Critical Issues (Bloqueadores)
- ❌ CORS abierto a `["*"]` - [Ver detalles](./CURRENT_STATUS.md#cors-completely-open)
- ❌ Sin autenticación en endpoints - [Ver detalles](./CURRENT_STATUS.md#no-authenticationauthorization)
- ❌ Sin validación en frontend - [Ver detalles](./CURRENT_STATUS.md#no-runtime-validation)

### Convenciones Principales
- 📁 Componentes React: **kebab-case** (ej: `kpi-card.tsx`)
- 🔤 Imports: **@/path** (alias @ = src/)
- 📝 Backend: **snake_case** (ej: `generate_mock_movements()`)
- 🏷️ Tipos: **PascalCase** (ej: `KPIMetrics`)
- 🎯 Literales: **snake_case** (ej: `operation_type`, `business_type`)

### Comandos Principales
```bash
# Desarrollo
docker compose up --build          # Iniciar todo
npm run dev                        # Solo frontend
npm run test                       # Tests frontend
pytest                            # Tests backend

# Build
npm run build                      # Frontend production
docker build -t backend .          # Backend imagen

# Verificación
npm run lint                       # Frontend linting
npm test:coverage                  # Frontend coverage
pytest --cov=app                   # Backend coverage
```

### Endpoints API
```
GET  /api/metrics              → Movimientos financieros
GET  /api/metrics/summary      → Resumen por período
GET  /api/metrics/top-categories → Top categorías
GET  /api/metrics/comparison   → Comparativa períodos
GET  /api/metrics/alert        → Alertas anomalías
GET  /api/metrics/facets       → Metadatos
GET  /api/health               → Health check
```

### Estructura Clave
```
frontend/src/
  ├── components/dashboard/     ← Componentes de negocio
  ├── components/ui/            ← Componentes genéricos
  ├── lib/
  │   ├── financial-types.ts   ← TIPOS CENTRALIZADOS
  │   └── financial-utils.ts   ← Funciones puras
  └── App.tsx                  ← Componente principal

backend/app/
  ├── main.py                  ← Entry point
  └── routes.py                ← API endpoints + modelos
```

---

## 📌 Important Notes

### Seguridad
⚠️ **Proyecto NO es apto para producción** sin completar FASE 0 del roadmap
- Faltan: Autenticación, CORS restringido, validación runtime, logging
- [Ver detalles completos](./CURRENT_STATUS.md#fase-0-seguridad-crítica-bloqueador)

### MVP Status
✅ **Dashboard visual funciona**, pero:
- Datos son mock (seed=42)
- Sin BD real
- Sin filtros avanzados
- Sin E2E tests
- [Ver roadmap para próximos pasos](./DEVELOPMENT_ROADMAP.md)

### Actualizaciones de Memoria
Esta memory bank debe actualizarse cuando:
- Se completa una fase del roadmap
- Se descubren nuevas limitaciones críticas
- Se hacen cambios de arquitectura
- Se agregan nuevas convenciones

---

## 🔗 Referencias Externas

### Documentación del Proyecto
- [README.md](../README.md) - Documentación general
- [PROJECT_RULES.md](../PROJECT_RULES.md) - Reglas completas
- [CONCRETE_FINDINGS.md](../CONCRETE_FINDINGS.md) - Hallazgos verificables

### Reglas para Agentes
- [.agents/rules/](../.agents/rules/) - Todas las reglas
  - `01-architecture.md` - Reglas de arquitectura
  - `02-naming.md` - Convenciones de nombres
  - `04-testing.md` - Reglas de testing
  - `08-security.md` - Seguridad

### Tecnologías
- [React 19 Docs](https://react.dev)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)
- [Vite Guide](https://vitejs.dev/guide/)
- [Tailwind CSS Docs](https://tailwindcss.com/docs)
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [Docker Docs](https://docs.docker.com/)

---

## 📧 Questions?

Si tienes preguntas sobre:
- **¿Qué está implementado?** → Ver [CURRENT_STATUS.md](./CURRENT_STATUS.md)
- **¿Cómo funciona X?** → Ver [PROJECT_OVERVIEW.md](./PROJECT_OVERVIEW.md) o [TECHNICAL_STACK.md](./TECHNICAL_STACK.md)
- **¿Cuál es el plan?** → Ver [DEVELOPMENT_ROADMAP.md](./DEVELOPMENT_ROADMAP.md)
- **¿Cómo debo codear?** → Ver [../PROJECT_RULES.md](../PROJECT_RULES.md)
- **¿Cuáles son los riesgos?** → Ver [CURRENT_STATUS.md - Limitaciones](./CURRENT_STATUS.md#confirmed-limitations--issues)

---

**Mantén esta documentación actualizada. Conocimiento compartido = equipo más efectivo.** 🚀

