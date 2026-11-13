# 🏛️ Reglas de Arquitectura

Reglas sobre la estructura y organización del proyecto.

---

## REGLA-ARCH-001: Monorepo con Frontend y Backend Separados

**Norma**: Mantener frontend y backend en carpetas independientes del mismo repositorio.

**Hecho citado**: Estructura en raíz con carpetas `frontend/` y `backend/` (CONCRETE_FINDINGS.md, línea 1)

```
frontend/src/
backend/app/
docker-compose.yml  ← Ambas en mismo repo
```

**Por qué**: Facilita versionado compartido, configuración compartida (docker-compose.yml), y tipos compartidos.

**Aplicación**: 
- Nuevas features respetan esta separación
- No mover frontend o backend a otro repositorio
- Mantener docker-compose.yml en raíz

---

## REGLA-ARCH-002: Entry Points Únicos y Claros

**Norma**: Cada aplicación tiene un único entry point principal.

**Hecho citado**: 
- Frontend: `frontend/src/main.tsx` (verification.md, línea 125)
- Backend: `backend/app/main.py` (verification.md, línea 126)

**Por qué**: Claridad absoluta sobre dónde comienza la ejecución. Evita confusiones en debugging.

**Aplicación**: 
- No crear entry points alternativos
- Si necesitas múltiples, refactoriza el existente
- Documentar si cambia el entry point

---

## REGLA-ARCH-003: Frontend-Backend Comunican vía Proxy en Desarrollo

**Norma**: Frontend usa Vite proxy configurado para redirigir `/api/*` al backend.

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

**Por qué**: 
- Evita CORS issues en desarrollo
- Frontend en puerto 5173, backend en 8000
- Transparente para el código frontend

**Aplicación**: 
- No cambiar este mapeo sin actualizar documentación
- Todos los requests frontend a `/api` usan este proxy
- En producción: requests van directamente al backend

---

## REGLA-ARCH-004: Stack Técnico Moderno y Consensuado

**Norma**: Frontend usa React 19 + TypeScript 6 + Vite. Backend usa FastAPI + Python.

**Hecho citado**: `frontend/package.json` (React 19.2.4, TypeScript 6.0.2, Vite 8.0.4)

**Por qué**: 
- Versiones actuales ofrecen mejor performance, seguridad y DX
- Comunidades activas y soporte long-term
- Herramientas modernas y bien documentadas

**Aplicación**: 
- Actualizar dependencias periódicamente
- No cambiar frameworks sin consenso del equipo
- Mantener versiones sincronizadas

---

## 📚 Referencias

- [PROJECT_RULES.md](../../PROJECT_RULES.md) - Documento maestro de reglas
- [FINDINGS_BY_CATEGORY.md](../../FINDINGS_BY_CATEGORY.md) - Hallazgos por categoría
- [CONCRETE_FINDINGS.md](../../CONCRETE_FINDINGS.md) - Hechos concretos del repositorio

**Volver al índice**: [index.md](./index.md)
