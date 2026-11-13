# 📁 Reglas de Estructura

Reglas sobre organización de carpetas y archivos.

---

## REGLA-STR-001: Folder Structure Clara y Consistente

**Norma**: Estructura es clara y bien organizada.

**Hecho citado**: 
- Frontend: `frontend/src/components/`, `frontend/src/lib/` (CONCRETE_FINDINGS.md, línea 1)
- Backend: `backend/app/`, `backend/tests/` (CONCRETE_FINDINGS.md, línea 1)

**Estructura esperada**:

```
frontend/src/
├── components/
│   ├── dashboard/         (componentes grandes)
│   └── ui/                (componentes pequeños/reutilizables)
├── lib/
│   ├── financial-types.ts (tipos compartidos)
│   ├── financial-utils.ts (funciones puras)
│   └── financial-utils.test.ts
└── App.tsx, main.tsx

backend/app/
├── routes.py              (endpoints)
├── main.py                (configuración)
└── tests/                 (tests)
```

**Por qué**: 
- Fácil navegar y encontrar código
- Consistencia predecible
- Escalable

**Aplicación**: 
- Mantener estructura
- No crear carpetas "util" generales
- Agrupar por funcionalidad
- Cuando crezca: considerar features/sliced architecture

---

## 📚 Referencias

- [PROJECT_RULES.md](../../PROJECT_RULES.md) - Documento maestro de reglas

**Volver al índice**: [index.md](./index.md)
