# 🚀 Development Roadmap & Priorities

**Última actualización**: 2026-11-13  
**Horizonte de planificación**: 3 trimestres (9 meses)

---

## 🔴 FASE 0: SEGURIDAD CRÍTICA (Bloqueador)

**Duración estimada**: 2-3 semanas  
**Por qué**: Proyecto no es apto para producción sin esto

### 0.1 Implementar Autenticación (1 semana)
- [ ] Seleccionar mecanismo: JWT (recomendado) vs OAuth2 vs API keys
- [ ] Backend: Crear endpoint `/auth/token` (login)
- [ ] Backend: Middleware de validación de token en todos los endpoints
- [ ] Frontend: Guardar token en localStorage/sessionStorage
- [ ] Frontend: Incluir token en headers de API requests
- [ ] Tests: Validar rechazo de requests sin token

**Decisión recomendada**: JWT con refresh tokens

### 0.2 Restringir CORS (2 días)
- [ ] Identificar dominios permitidos (dev, staging, prod)
- [ ] Actualizar `backend/app/main.py`:
  ```python
  allow_origins=[
    "http://localhost:5173",      # Dev
    "https://staging.example.com", # Staging
    "https://example.com",         # Prod
  ]
  ```
- [ ] Tests para validar CORS headers

### 0.3 Agregar Validación Runtime (1 semana)
- [ ] Frontend: Instalar Zod o io-ts
- [ ] Frontend: Crear schemas para todas las responses
- [ ] Frontend: Validar respuestas antes de usar
- [ ] Manejo de errores de validación

**Schemas requeridos**:
- `FinancialMovement[]`
- `MetricsFacets`
- `MetricsSummaryItem[]`
- `TopCategoryItem[]`

### 0.4 Agregar Logging (3 días)
- [ ] Backend: Instalar `python-json-logger` o similar
- [ ] Backend: Logs estructurados en:
  - Requests (IP, path, método, duration)
  - Errors (stack trace, contexto)
  - Auth (token validation success/fail)
- [ ] Frontend: Errores en consola + sent to logging service (opcional)

---

## 🟠 FASE 1: MVP SÓLIDO (Semanas 4-8)

**Duración estimada**: 4-5 semanas  
**Objetivo**: Proyecto listo para staging

### 1.1 Base de Datos Real (2 semanas)
- [ ] Seleccionar BD: PostgreSQL (recomendado)
- [ ] Crear schema:
  ```sql
  CREATE TABLE financial_movements (
    id UUID PRIMARY KEY,
    user_id UUID NOT NULL,
    create_date DATE NOT NULL,
    amount FLOAT NOT NULL,
    operation_type VARCHAR(20),
    category VARCHAR(50),
    business_type VARCHAR(10),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
  );
  
  CREATE TABLE users (
    id UUID PRIMARY KEY,
    username VARCHAR(50) UNIQUE,
    password_hash VARCHAR(255),
    email VARCHAR(100) UNIQUE,
    created_at TIMESTAMP DEFAULT NOW()
  );
  ```
- [ ] Backend: Migrar de mock data a queries reales
- [ ] Backend: Usar SQLAlchemy u ORM similar
- [ ] Datos seed para testing

### 1.2 Tests E2E (1 semana)
- [ ] Instalar Cypress (recomendado) o Playwright
- [ ] Escribir tests para flujos críticos:
  1. Login → Ver dashboard
  2. Ver KPIs cargados
  3. Gráficos renderizan correctamente
  4. Filtrado por rango de fechas (si implementado)
- [ ] CI/CD: Ejecutar E2E en cada PR
- [ ] Documentar cómo correr tests localmente

### 1.3 Variables de Entorno (3 días)
- [ ] Backend: Crear `.env.example` y documentar
- [ ] Frontend: Crear `.env.example`
- [ ] Configuración por ambiente (dev, staging, prod)
- [ ] Docker: Usar variables en docker-compose.yml

**Variables críticas**:
- `DATABASE_URL`
- `API_BASE_URL`
- `JWT_SECRET`
- `CORS_ORIGINS`
- `NODE_ENV` / `ENVIRONMENT`

### 1.4 Manejo de Errores Consistente (3 días)
- [ ] Backend: Error response wrapper:
  ```python
  {
    "success": false,
    "error": {
      "code": "INVALID_DATE_RANGE",
      "message": "Start date must be before end date",
      "details": {...}
    }
  }
  ```
- [ ] Frontend: Mensajes de error amigables
- [ ] Error logging centralizado

---

## 🟡 FASE 2: ESCALA & FEATURES (Semanas 9-16)

**Duración estimada**: 6-8 semanas  
**Objetivo**: Funcionalidades avanzadas y performance

### 2.1 Paginación y Filtros (1 semana)
- [ ] Backend: Query parameters:
  - `limit` (default 50, max 500)
  - `offset` para paginación
  - `start_date`, `end_date` para rango
  - `operation_type`, `category`, `business_type` para filtros
- [ ] Frontend: UI para filtros
- [ ] Frontend: Componente de paginación
- [ ] Tests: Verificar parámetros

**Endpoint mejorado**:
```
GET /api/metrics?limit=50&offset=0&start_date=2024-01-01&end_date=2024-12-31&operation_type=income
```

### 2.2 Caché en Backend (1 semana)
- [ ] Instalar Redis
- [ ] Caché de:
  - `/api/metrics/facets` (válido 1 hora)
  - `/api/metrics/summary` (válido 30 min)
  - Invalidación en cambios
- [ ] Metrics de caché hit/miss

### 2.3 Rate Limiting (3 días)
- [ ] Instalar `slowapi` (FastAPI)
- [ ] Límites por IP/usuario:
  - Sin autenticar: 10 req/min
  - Autenticado: 100 req/min
- [ ] Headers X-RateLimit-*

### 2.4 Análisis Avanzados (2 semanas)
- [ ] Backend: Comparativa año-a-año
- [ ] Backend: Estadísticas por categoría (total, promedio, desv. est.)
- [ ] Backend: Detección de anomalías
- [ ] Frontend: Nuevo chart: "Category breakdown" (pie/donut)
- [ ] Frontend: Comparativa en cards de KPI

### 2.5 Exportación de Datos (1 semana)
- [ ] Backend: Endpoint para CSV
- [ ] Backend: Endpoint para JSON
- [ ] Frontend: Botón "Download report"
- [ ] Archivos: `financial_report_2024_11.csv`

---

## 🟢 FASE 3: PRODUCCIÓN & POLISH (Semanas 17-24)

**Duración estimada**: 6-8 semanas  
**Objetivo**: Listo para usuarios reales

### 3.1 Optimizaciones Frontend (1 semana)
- [ ] Code splitting: Lazy load charts
- [ ] Compresión: Gzip en nginx
- [ ] Tree-shaking: Verificar bundle size
- [ ] Lighthouse: Score >= 90
- [ ] Performance profiling

### 3.2 Optimizaciones Backend (1 semana)
- [ ] Índices en BD: `(user_id, create_date)`, `category`, `operation_type`
- [ ] Query optimization: Explique planes
- [ ] Connection pooling
- [ ] Compresión de responses

### 3.3 Monitoreo & Observabilidad (1 semana)
- [ ] Backend: APM (Application Performance Monitoring)
  - Opción: Datadog, New Relic, o auto-hosted (Prometheus)
- [ ] Métricas:
  - Response times (p50, p95, p99)
  - Error rates
  - Database query times
- [ ] Alertas automáticas

### 3.4 Testing & QA (2 semanas)
- [ ] Aumentar cobertura a >= 80%
- [ ] Tests de carga (k6 o similiar)
- [ ] Testing de seguridad (OWASP top 10)
- [ ] Manual QA en staging

### 3.5 Documentación (1 semana)
- [ ] README mejorado con screenshots
- [ ] Guía de contribución
- [ ] API documentation (OpenAPI/Swagger)
- [ ] Architecture decision records (ADRs)
- [ ] Runbook para operaciones

### 3.6 CI/CD Mejora (3 días)
- [ ] GitHub Actions o GitLab CI/CD
- [ ] Pipeline:
  1. Lint
  2. Tests unitarios
  3. Tests E2E
  4. Build de imagen Docker
  5. Deploy a staging
- [ ] Branch protection rules

### 3.7 Seguridad Avanzada (1 semana)
- [ ] HTTPS/SSL obligatorio
- [ ] Security headers (HSTS, CSP, X-Frame-Options)
- [ ] CSRF tokens para mutaciones
- [ ] SQL injection prevention (ORM mitiga esto)
- [ ] XSS prevention (React mitiga esto)
- [ ] Security audit

---

## 🎯 Roadmap Visual

```
FASE 0: Seguridad            [====] 2-3 sem
FASE 1: MVP Sólido           [=========] 4-5 sem
FASE 2: Escala & Features    [=============] 6-8 sem
FASE 3: Producción & Polish  [=============] 6-8 sem

Total: ~5-6 meses de desarrollo a tiempo completo
Con equipo de 2-3 devs: ~2-3 meses
```

---

## 📊 Estimated Timeline

| Fase | Inicio | Fin | Duración | Equipo |
|------|--------|-----|----------|--------|
| Fase 0 | Sem 1 | Sem 3 | 3 sem | 1-2 devs |
| Fase 1 | Sem 4 | Sem 8 | 5 sem | 2 devs |
| Fase 2 | Sem 9 | Sem 16 | 8 sem | 2-3 devs |
| Fase 3 | Sem 17 | Sem 24 | 8 sem | 3 devs + QA |

**Total**: 24 semanas (~6 meses)

---

## 💰 Resource Requirements

### Infraestructura Recomendada
- **BD**: PostgreSQL managed (AWS RDS, DigitalOcean, etc)
- **Caché**: Redis managed
- **APM**: Datadog trial o similiar
- **CDN**: CloudFlare (free plan)
- **Container Registry**: GitHub Packages (gratis)

### Costos Estimados (Mes)
- DB: $20-50/mes
- Cache: $10-20/mes
- APM: $0-100/mes (depende de volumen)
- CDN: $0-30/mes
- **Total**: $30-200/mes

---

## 🎓 Learning & Upskilling

Equipo necesita conocimiento en:
1. JWT + OAuth2 (autenticación)
2. PostgreSQL + SQL optimization
3. Redis (caché)
4. Docker + Kubernetes (deployment)
5. CI/CD pipelines
6. E2E testing (Cypress)
7. Performance profiling & optimization
8. Security best practices

---

## ✅ Success Criteria

### Fase 0
- [ ] No hay warnings de seguridad en OWASP
- [ ] Todos los endpoints requieren autenticación
- [ ] CORS restringido a dominios permitidos

### Fase 1
- [ ] BD funcionando con datos reales
- [ ] Tests E2E ejecutándose en CI/CD
- [ ] Zero secrets en repositorio

### Fase 2
- [ ] Soporta 100k+ movimientos sin lag
- [ ] Nuevos endpoints de análisis funcionan
- [ ] Export de reportes implementado

### Fase 3
- [ ] Lighthouse score >= 90
- [ ] Uptime >= 99.5%
- [ ] Latency p95 < 200ms
- [ ] Cobertura de tests >= 80%

---

## 🔄 Maintenance & Support

### Post-Lanzamiento (Semana 25+)
- [ ] Monitoreo 24/7 (al menos alertas automáticas)
- [ ] Respuesta a bugs críticos: < 4 horas
- [ ] Respuesta a bugs menores: < 1 semana
- [ ] Updates de dependencias: mensual
- [ ] Security patches: inmediato
- [ ] Performance reviews: trimestral

---

## 📍 See Also

- [CURRENT_STATUS.md](./CURRENT_STATUS.md) - Estado actual y limitaciones
- [PROJECT_OVERVIEW.md](./PROJECT_OVERVIEW.md) - Descripción del producto
- [../PROJECT_RULES.md](../PROJECT_RULES.md) - Reglas del proyecto

