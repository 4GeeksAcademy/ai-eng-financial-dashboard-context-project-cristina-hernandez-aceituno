# 🔐 Reglas de Seguridad ⚠️ CRÍTICO

Reglas sobre seguridad, autenticación y validación.

---

## REGLA-SEC-001: CORS Debe Ser Restringido 🚨 CRÍTICO

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

**Por qué**: 
- Vulnerable a CSRF
- Exposición de datos y credenciales
- Cualquiera puede hacer requests

**Aplicación**:
- **Dev**: Aceptable usar `["*"]`
- **Prod**: Cambiar a dominios específicos:

```python
allow_origins=[
    "https://yourdomain.com",
    "https://www.yourdomain.com"
]
```

---

## REGLA-SEC-002: Endpoints Requieren Autenticación 🚨 CRÍTICO

**Norma**: Todos los 9 endpoints públicos actualmente. Necesitan protección.

**Hecho citado**: `backend/app/routes.py` sin validación de token (CONCRETE_FINDINGS.md, línea 242)

```python
@router.get("/api/metrics")  # ⚠️ Cualquiera puede acceder
def get_metrics(...): 
    return movements
```

**Por qué**: 
- Cualquiera puede acceder a datos financieros
- Sin validación de identidad
- Riesgo crítico en producción

**Aplicación**: 
- Implementar autenticación:
  - JWT tokens
  - API keys
  - OAuth2
- Proteger todos los 9 endpoints
- Validar token en cada request

---

## REGLA-SEC-003: Validación Runtime en Frontend

**Norma**: Frontend no valida tipos de response. Asumir que API devuelve tipos correctos.

**Hecho citado**: `frontend/src/App.tsx:16-19` (CONCRETE_FINDINGS.md, línea 253)

```typescript
async function fetchFinancialData(): Promise<FinancialMovement[]> {
  const response = await fetch(`${API_BASE_URL}/api/metrics`);
  return response.json();  // ⚠️ Sin validación
}
```

**Por qué**: 
- Defensibilidad
- Backend podría cambiar formato
- Evita errores en runtime

**Aplicación**: 
- Usar Zod o Pydantic para validar response:

```typescript
import { z } from 'zod';

const FinancialMovementSchema = z.array(FinancialMovement);
const validated = FinancialMovementSchema.parse(await response.json());
```

---

## REGLA-SEC-004: Backend usa Literal Types

**Norma**: Backend valida con Literal types (Pydantic).

**Hecho citado**: `backend/app/routes.py:1-15` (CONCRETE_FINDINGS.md, línea 164)

```python
OperationType = Literal["income", "outcome"]
Category = Literal["suppliers", "sales", "operational", "administrative", "others"]
BusinessType = Literal["B2B", "B2C"]
```

**Por qué**: 
- Pydantic rechaza valores inválidos automáticamente
- Type safety en tiempo de validación
- Evita valores inesperados

**Aplicación**: 
- Mantener Literal types en models
- No usar strings sin restricción
- Validar siempre en entrada

---

## 📚 Referencias

- [PROJECT_RULES.md](../../PROJECT_RULES.md) - Documento maestro de reglas
- [CONCRETE_FINDINGS.md](../../CONCRETE_FINDINGS.md) - Hallazgos concretos

**Volver al índice**: [index.md](./index.md)
