# 🔍 Reglas de Observability

Reglas sobre logging, tracing y monitoreo.

---

## REGLA-OBS-001: Agregar Logging en Backend

**Norma**: Backend actualmente sin logging.

**Hecho citado**: `backend/app/routes.py` sin `print()`, `logging.info()` (CONCRETE_FINDINGS.md, línea 322)

**Por qué**: 
- Debugging imposible en producción
- Auditoría ausente
- Sin trazabilidad de requests

**Aplicación**: 
- Implementar logging:

```python
import logging

logger = logging.getLogger(__name__)

@router.get("/api/metrics")
def get_metrics(...):
    logger.info(f"Fetching metrics with filters: {filters}")
    try:
        movements = generate_mock_movements(seed=42)
        logger.info(f"Returned {len(movements)} movements")
        return movements
    except Exception as e:
        logger.error(f"Error: {e}", exc_info=True)
        raise
```

- Usar niveles apropiados: INFO, WARNING, ERROR
- Incluir contexto relevante
- Loguear errores con stack trace

---

## REGLA-OBS-002: Agregar Tracing Distribuido (Futuro)

**Norma**: Proyecto sin tracing distribuido.

**Por qué**: 
- Debugging de requests frontend-backend requiere correlación
- Seguir request a través de componentes
- Medir latencia end-to-end

**Aplicación - Futuro**: 
- Implementar OpenTelemetry o similar
- Usar correlation IDs
- Exportar a sistema de observability (Jaeger, DataDog)

---

## 📚 Referencias

- [PROJECT_RULES.md](../../PROJECT_RULES.md) - Documento maestro de reglas

**Volver al índice**: [index.md](./index.md)
