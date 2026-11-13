# 🚀 Memory Bank Quick Start

**Carga completa en < 5 minutos**

---

## 📍 Estás aquí

```
memory-bank/
├── README.md                    ← EMPIEZA AQUÍ (índice)
├── PROJECT_OVERVIEW.md          ← Qué es el proyecto
├── TECHNICAL_STACK.md           ← Stack técnico
├── CURRENT_STATUS.md            ← Estado actual
├── DEVELOPMENT_ROADMAP.md       ← Plan de desarrollo
└── QUICK_START.md               ← Este archivo
```

---

## ⚡ 2-Minute Summary

### 🎯 El Proyecto
**Financial Dashboard** = Visualizador de movimientos financieros  
- Frontend: React + TypeScript + Vite
- Backend: FastAPI + Python
- Datos: Mock con seed=42

### ✅ Qué Funciona
- Dashboard con KPIs (Income, Outcome, Profit, Profit%)
- Gráficos (barras, líneas)
- 9 endpoints API
- Tests unitarios

### ⚠️ Qué Falta (CRÍTICO)
- ❌ Autenticación
- ❌ CORS restringido
- ❌ BD real
- ❌ Tests E2E
- ❌ Seguridad en producción

### 🚀 Próximos Pasos (FASE 0: 2-3 semanas)
1. Implementar JWT (autenticación)
2. Restringir CORS
3. Agregar validación en frontend
4. Logging en backend

---

## 📚 Documentos por Rol

### 👨‍💼 Product Manager
1. **PROJECT_OVERVIEW.md** - Qué construimos
2. **DEVELOPMENT_ROADMAP.md** - Plan y timeline
3. **CURRENT_STATUS.md** - Features vs limitaciones

### 👨‍💻 Desarrollador
1. **PROJECT_OVERVIEW.md** - Overview del producto
2. **TECHNICAL_STACK.md** - Cómo está construido
3. [../PROJECT_RULES.md](../PROJECT_RULES.md) - Cómo codear

### 🤖 Agente de IA
1. **PROJECT_OVERVIEW.md** - Contexto general
2. **TECHNICAL_STACK.md** - Detalles técnicos
3. **CURRENT_STATUS.md** - Estado actual
4. [../.agents/rules/](../.agents/rules/) - Reglas de proyecto

### 🔐 Security Reviewer
1. [CURRENT_STATUS.md - Security Issues](./CURRENT_STATUS.md#-critical---security-issues)
2. [DEVELOPMENT_ROADMAP.md - FASE 0](./DEVELOPMENT_ROADMAP.md#-fase-0-seguridad-crítica-bloqueador)
3. [../.agents/rules/08-security.md](../.agents/rules/08-security.md)

---

## 🎯 Key Facts

| Aspecto | Estado |
|--------|--------|
| **MVP Funcional** | ✅ Sí |
| **Listo Producción** | ❌ No (seguridad) |
| **Autenticación** | ❌ No |
| **BD Real** | ❌ No (mock data) |
| **Tests E2E** | ❌ No |
| **Documentación** | ⚠️ Básica |

---

## 🔥 Critical Path (Bloqueadores)

```
[FASE 0: Seguridad]
│
├─ Autenticación (JWT)          → 1 semana
├─ CORS Restringido             → 2 días
├─ Validación Runtime           → 1 semana
└─ Logging en Backend           → 3 días
│
↓ (~3 semanas)
│
[FASE 1: MVP Sólido]
│
├─ BD Real (PostgreSQL)         → 2 semanas
├─ Tests E2E                    → 1 semana
├─ Variables de Entorno         → 3 días
└─ Manejo de Errores            → 3 días
│
↓ (~5 semanas total)
│
[FASE 2+3: Escala & Producción]
│
```

---

## 💡 Quick Commands

```bash
# Iniciar proyecto
docker compose up --build

# Frontend solo
cd frontend && npm run dev

# Backend solo
cd backend && python -m uvicorn app.main:app --reload

# Tests
npm test                    # Frontend
pytest                     # Backend

# Lint
npm run lint              # Frontend

# Build
npm run build             # Frontend
```

---

## 🗺️ Project Map

```
frontend/                          backend/
├── components/dashboard/          ├── app/
│   ├── kpi-card.tsx              │   ├── main.py (entry)
│   ├── income-outcome-chart.tsx   │   └── routes.py (API)
│   └── ...                        │
├── lib/                           ├── tests/
│   ├── financial-types.ts    ◄───┼─── SHARED TYPES
│   └── financial-utils.ts         │
└── App.tsx                        └── requirements.txt
```

---

## 🎓 Learning Path

### Día 1
- [ ] Leer PROJECT_OVERVIEW.md
- [ ] Correr `docker compose up`
- [ ] Explorar http://localhost:5173
- [ ] Ver http://localhost:8000/docs

### Día 2
- [ ] Leer TECHNICAL_STACK.md
- [ ] Explorar código frontend (`components/`, `lib/`)
- [ ] Explorar código backend (`app/routes.py`)
- [ ] Revisar tipos en `financial-types.ts`

### Día 3
- [ ] Leer CURRENT_STATUS.md
- [ ] Leer DEVELOPMENT_ROADMAP.md
- [ ] Revisar PROJECT_RULES.md
- [ ] Entender convenciones de código

### Día 4+
- [ ] Hacer cambios pequeños (bugfix, refactor)
- [ ] Escribir tests
- [ ] Hacer PR con revisión

---

## ❓ FAQ

### ¿Por dónde empiezo?
1. Leer README.md de memory-bank
2. Leer PROJECT_OVERVIEW.md
3. Correr `docker compose up --build`
4. Explorar código

### ¿Cuál es el estado del proyecto?
MVP funcional pero **NO apto para producción** (ver CURRENT_STATUS.md)

### ¿Cuál es el plan?
Tres fases: Seguridad → MVP Sólido → Escala (ver DEVELOPMENT_ROADMAP.md)

### ¿Cuánto falta para producción?
~6 meses con equipo dedicado (ver DEVELOPMENT_ROADMAP.md timeline)

### ¿Qué es lo más urgente?
Implementar autenticación y restringir CORS (FASE 0, 2-3 semanas)

### ¿Cómo contribuyo?
1. Revisa PROJECT_RULES.md
2. Sigue convenciones
3. Agrega tests
4. Haz PR

---

## 📍 Next Steps

1. **Si eres nuevo**: Lee PROJECT_OVERVIEW.md + TECHNICAL_STACK.md
2. **Si vas a codear**: Lee PROJECT_RULES.md + convenciones
3. **Si revisas seguridad**: Lee CURRENT_STATUS.md (Security Issues)
4. **Si planificas**: Lee DEVELOPMENT_ROADMAP.md

---

**Documentación completa**: [README.md](./README.md)  
**Documentación del proyecto**: [../PROJECT_RULES.md](../PROJECT_RULES.md)

