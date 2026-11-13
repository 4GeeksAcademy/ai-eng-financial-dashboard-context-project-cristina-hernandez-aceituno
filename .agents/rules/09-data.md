# 📊 Reglas de Data Handling

Reglas sobre manejo de datos, caché y generación de datos mock.

---

## REGLA-DATA-001: Mock Data con seed=42

**Norma**: Datos mock generados con `seed=42` para reproducibilidad.

**Hecho citado**: `backend/app/routes.py:140` (en 8 endpoints) (CONCRETE_FINDINGS.md, línea 295)

```python
movements = generate_mock_movements(seed=42)
```

Aparece en:
- `/api/metrics`
- `/api/metrics/facets`
- `/api/metrics/summary`
- `/api/metrics/categories/top`
- `/api/metrics/comparison`
- `/api/metrics/alerts`
- `/api/metrics/b2b`
- `/api/metrics/b2c`

**Por qué**: 
- Reproducibilidad en tests
- Siempre mismos datos
- Predecible para debugging

**Aplicación**: 
- No cambiar seed sin actualizar tests
- Documentar cambios
- Usar para testing y demostración

---

## REGLA-DATA-002: Sin Caché Global de Datos

**Norma**: Cada endpoint genera datos desde cero (sin caché).

**Hecho citado**: 8 endpoints en `backend/app/routes.py` llaman a `generate_mock_movements` (CONCRETE_FINDINGS.md, línea 295)

**Por qué**: 
- Datos siempre frescos
- Pero: potencial desperdicio computacional

**Aplicación - Mejora futura**: 
- Considerar cachear globalmente:

```python
CACHED_MOVEMENTS = None

def get_movements():
    global CACHED_MOVEMENTS
    if CACHED_MOVEMENTS is None:
        CACHED_MOVEMENTS = generate_mock_movements(seed=42)
    return CACHED_MOVEMENTS
```

- Mejoraría performance
- Mantendría consistencia de datos

---

## 📚 Referencias

- [PROJECT_RULES.md](../../PROJECT_RULES.md) - Documento maestro de reglas

**Volver al índice**: [index.md](./index.md)
