# ⚡ Reglas de Performance

Reglas sobre optimización, configuración y carga.

---

## REGLA-PERF-001: Proxy Debe Ser Configurable

**Norma**: Proxy está hardcodeado a `http://backend:8000`.

**Hecho citado**: `frontend/vite.config.ts:11` (CONCRETE_FINDINGS.md, línea 270)

```typescript
target: "http://backend:8000",  // ⚠️ Hardcodeado
```

**Por qué**: 
- Solo funciona con docker-compose
- No funciona en `localhost` para desarrollo local
- No flexible para diferentes ambientes

**Aplicación - Mejora**: 
- Hacer configurable:

```typescript
target: process.env.VITE_API_TARGET || "http://localhost:8000"
```

- Permitir override vía variable de ambiente
- Documentar en `.env.example`

---

## REGLA-PERF-002: API_BASE_URL Debe Estar Definido

**Norma**: Frontend define `API_BASE_URL` con default vacío.

**Hecho citado**: `frontend/src/App.tsx:12` (CONCRETE_FINDINGS.md, línea 260)

```typescript
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "";
```

**Por qué**: 
- `""` permite requests a `/api` (relativo)
- Requiere servidor en mismo puerto
- Ambiguo en producción

**Aplicación**: 
- Definir `VITE_API_BASE_URL=http://localhost:8000` en `.env.local`
- En producción: `VITE_API_BASE_URL=https://yourdomain.com`
- Evitar defaults ambiguos

---

## 📚 Referencias

- [PROJECT_RULES.md](../../PROJECT_RULES.md) - Documento maestro de reglas

**Volver al índice**: [index.md](./index.md)
