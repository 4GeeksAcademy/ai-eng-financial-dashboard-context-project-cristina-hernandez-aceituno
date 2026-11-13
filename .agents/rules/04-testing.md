# 🧪 Reglas de Testing

Reglas sobre pruebas y cobertura de código.

---

## REGLA-TEST-001: Tests Unitarios Presentes

**Norma**: Frontend y backend tienen tests unitarios.

**Hecho citado**: 
- Frontend: `frontend/src/lib/financial-utils.test.ts`
- Backend: `backend/tests/test_routes.py` (CONCRETE_FINDINGS.md, línea 275)

**Por qué**: 
- Verificar funcionalidad correcta
- Evitar regresiones
- Documentación ejecutable

**Aplicación**: 
- Nuevo código debe incluir tests
- Ejecutar antes de commit: `npm test`
- Mantener cobertura mínima

---

## REGLA-TEST-002: Sin Tests E2E (Limitación Actual)

**Norma**: Proyecto actual no tiene tests end-to-end (E2E).

**Hecho citado**: CONCRETE_FINDINGS.md menciona "❌ No hay tests E2E"

**Por qué**: 
- Tests E2E requieren orquestación completa
- Herramientas adicionales (Cypress, Playwright)
- Mayor complejidad

**Aplicación**: 
- Plantear agregar E2E tests en próximas iteraciones
- Usar Cypress o Playwright cuando sea posible
- Priorizar tests críticos (login, pagos, etc)

---

## 📚 Referencias

- [PROJECT_RULES.md](../../PROJECT_RULES.md) - Documento maestro de reglas

**Volver al índice**: [index.md](./index.md)
