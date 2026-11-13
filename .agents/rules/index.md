# 📋 Reglas del Proyecto - Índice

**Conjunto de reglas accionables para contribuidores y agentes IA**

Cada regla cita hechos concretos del repositorio (archivo + línea exacta).

---

## 📂 Estructura de Reglas

Las reglas están organizadas en 12 categorías. Consulta la que necesites:

### 🏛️ [Arquitectura](./01-architecture.md) (4 reglas)
- Monorepo con Frontend y Backend separados
- Entry points únicos y claros
- Frontend-Backend comunican vía proxy
- Stack técnico moderno consensuado

### 📝 [Naming Conventions](./02-naming.md) (4 reglas)
- Componentes React en kebab-case
- Importes usan alias @
- Tipos centralizados en financial-types.ts
- Backend usa snake_case

### 🎯 [Developer Experience](./03-dx.md) (3 reglas)
- npm scripts estándar
- TypeScript strict mode
- Hot-reload automático

### 🧪 [Testing](./04-testing.md) (2 reglas)
- Tests unitarios presentes
- Sin E2E tests (limitación actual)

### 📚 [Documentation](./05-documentation.md) (3 reglas)
- README en inglés y español
- .env.example documenta variables
- AGENTS.md para contribuidores

### 🔌 [API Design](./06-api.md) (3 reglas)
- 9 endpoints GET documentados
- Query parameters explícitos
- Response models en todos

### 🎨 [Components](./07-components.md) (3 reglas)
- Record<> para type-safe variants
- Aria labels para accesibilidad
- Funciones puras sin side effects

### 🔐 [Security](./08-security.md) (4 reglas) ⚠️ **2 CRÍTICAS**
- CORS debe ser restringido 🚨
- Endpoints requieren autenticación 🚨
- Validación runtime en frontend
- Backend usa Literal types

### 📊 [Data Handling](./09-data.md) (2 reglas)
- Mock data con seed=42
- Sin caché global (oportunidad mejora)

### ⚡ [Performance](./10-performance.md) (2 reglas)
- Proxy debe ser configurable
- API_BASE_URL debe estar definido

### 🔍 [Observability](./11-observability.md) (2 reglas)
- Agregar logging en backend
- Agregar tracing distribuido

### 📁 [Structure](./12-structure.md) (1 regla)
- Folder structure clara y consistente

---

## ⚡ Acceso Rápido

### 🚨 Si buscas reglas CRÍTICAS:
→ Lee [08-security.md](./08-security.md)

### 🆕 Si vas a crear un nuevo componente:
→ Lee [02-naming.md](./02-naming.md) + [07-components.md](./07-components.md)

### 🔌 Si vas a crear un nuevo endpoint:
→ Lee [06-api.md](./06-api.md) + [08-security.md](./08-security.md)

### ✅ Si vas a hacer code review:
→ Lee todas las categorías relevantes

### 🤖 Si eres un agente IA:
→ Lee [.agents/rules/index.md](./index.md) (este archivo)  
→ Consulta categoría específica  
→ Verifica citas contra código real

---

## 📊 Matriz de Reglas

| Categoría | Reglas | Críticas | Riesgo |
|-----------|--------|----------|--------|
| 🏛️ Arquitectura | 4 | 0 | ✅ Bajo |
| 📝 Naming | 4 | 0 | ✅ Bajo |
| 🎯 DX | 3 | 0 | ✅ Bajo |
| 🧪 Testing | 2 | 0 | ⚠️ Medio |
| 📚 Documentación | 3 | 0 | ⚠️ Medio |
| 🔌 API Design | 3 | 0 | ✅ Bajo |
| 🎨 Componentes | 3 | 0 | ✅ Bajo |
| 🔐 Seguridad | 4 | 2 | 🚨 CRÍTICO |
| 📊 Data | 2 | 0 | ⚠️ Medio |
| ⚡ Performance | 2 | 0 | ⚠️ Medio |
| 🔍 Observability | 2 | 0 | ⚠️ Medio |
| 📁 Estructura | 1 | 0 | ✅ Bajo |

**Total: 33 reglas | 2 críticas | 11 categorías**

---

## 🎯 Formato de Cada Regla

Todas las reglas siguen este formato:

```
REGLA-CAT-###: [Nombre Descriptivo]

Norma: [Lo que deben hacer]

Hecho citado: [Archivo + línea específica]

Por qué: [Justificación concreta]

Aplicación: [Cómo se usa]

Ejemplos: [Código correcto vs incorrecto]
```

---

## 📖 Cómo Usar

### Para Contribuidores Humanos
1. Lee la regla relevante para tu tarea
2. Verifica la cita (archivo + línea) en el código
3. Aplica la norma en tu código
4. Usa los ejemplos como guía

### Para Agentes IA
1. Cuando generes código, consulta reglas relevantes
2. Verifica cada regla contra código real (cita específica)
3. Aplica normas accionables
4. Cita qué reglas seguiste en comentarios de PR

### Para Code Reviewers
1. Usa reglas como checklist
2. Señala violaciones con la regla específica
3. Cita la línea exacta de la regla
4. Vincula a `.agents/rules/` en comments

### Para Project Leaders
1. Usa matriz de riesgo para priorizar
2. Identifica reglas críticas (🚨)
3. Plantea mejoras de categorías ⚠️
4. Trackea cumplimiento de reglas

---

## ✨ Particularidad

**Cada regla cita un hecho concreto del repositorio:**

✓ Archivo exacto + línea específica  
✓ Código verificable  
✓ Justificación concreta  
✓ Ejemplos accionables  

Esto permite:
- Verificar cada regla contra código real
- Entender la raíz de cada norma
- Aplicar consistentemente
- Educar nuevos contribuidores

---

## 🚨 Reglas Críticas (Antes de Producción)

### REGLA-SEC-001: CORS Debe Ser Restringido
**Ubicación**: `backend/app/main.py:6`  
**Acción**: Cambiar `allow_origins=["*"]` a dominios específicos

### REGLA-SEC-002: Endpoints Requieren Autenticación  
**Ubicación**: `backend/app/routes.py` (todos los 9 endpoints)  
**Acción**: Implementar JWT, API keys u OAuth2

---

## 📚 Referencias

- **Documento maestro**: [PROJECT_RULES.md](../../PROJECT_RULES.md)
- **Hallazgos por categoría**: [FINDINGS_BY_CATEGORY.md](../../FINDINGS_BY_CATEGORY.md)
- **Hallazgos concretos**: [CONCRETE_FINDINGS.md](../../CONCRETE_FINDINGS.md)
- **Análisis verificado**: [verification.md](../../verification.md)

---

**Última actualización**: 13 de noviembre de 2026  
**Versión**: 1.0  
**Cada regla cita hechos verificables del repositorio**
