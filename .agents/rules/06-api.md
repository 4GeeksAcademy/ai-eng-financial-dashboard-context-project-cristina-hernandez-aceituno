# 🔌 Reglas de API Design

Reglas sobre diseño de endpoints y comunicación cliente-servidor.

---

## REGLA-API-001: 9 Endpoints GET Documentados

**Norma**: Backend expone 9 endpoints GET con propósitos claros.

**Hecho citado**: `backend/app/routes.py` (CONCRETE_FINDINGS.md, línea 278)

```
GET /health                          (línea 134)
GET /api/metrics                     (línea 141)
GET /api/metrics/facets              (línea 155)
GET /api/metrics/summary             (línea 162)
GET /api/metrics/categories/top      (línea 179)
GET /api/metrics/comparison          (línea 197)
GET /api/metrics/alerts              (línea 218)
GET /api/metrics/b2b                 (línea 237)
GET /api/metrics/b2c                 (línea 259)
```

**Por qué**: Cobertura clara de funcionalidades de KPIs, métricas, categorías.

**Aplicación**: 
- Nuevos endpoints deben documentarse con línea exacta
- Mantener consistencia de rutas
- Documentar propósito de cada endpoint

---

## REGLA-API-002: Query Parameters Explícitos

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

**Por qué**: 
- Swagger automático
- Type hints claros
- Validación automática
- Documentación autogenerada

**Aplicación**: Todos los params usar `Query(default=...)`.

---

## REGLA-API-003: Response Models Explícitos

**Norma**: Todos los endpoints definen `response_model`.

**Hecho citado**: `backend/app/routes.py:140-142` (CONCRETE_FINDINGS.md, línea 200)

```python
@router.get("/api/metrics", response_model=list[FinancialMovement])
def get_metrics(...) -> list[FinancialMovement]:
    return movements
```

**Por qué**: 
- Validación automática de response
- Documentación Swagger exacta
- Seguridad de tipos

**Aplicación**: No devolver datos sin `response_model` en FastAPI.

---

## 📚 Referencias

- [PROJECT_RULES.md](../../PROJECT_RULES.md) - Documento maestro de reglas

**Volver al índice**: [index.md](./index.md)
