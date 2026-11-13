# 📚 Reglas de Documentación

Reglas sobre documentación del proyecto.

---

## REGLA-DOC-001: README en Inglés y Español

**Norma**: Proyecto tiene README.md y README.es.md.

**Hecho citado**: Archivos presentes en raíz (verification.md, línea 85)

**Por qué**: 
- Accesibilidad para comunidades internacional e hispanohablante
- Inclusividad

**Aplicación**: 
- Mantener ambos sincronizados
- Cambio en uno = cambio en otro
- Verificar que explican lo mismo

---

## REGLA-DOC-002: .env.example Documenta Variables

**Norma**: `.env.example` lista todas las variables de ambiente necesarias.

**Hecho citado**: `frontend/.env.example` (CONCRETE_FINDINGS.md, línea 261)

**Por qué**: 
- Nuevos developers saben qué variables configurar
- Evita errores de configuración

**Aplicación**: 
- Actualizar `.env.example` cuando agregues nuevas variables
- Documentar qué hace cada variable
- Incluir valores de ejemplo

---

## REGLA-DOC-003: AGENTS.md Documenta Contribuciones

**Norma**: AGENTS.md guía para contribuidores y agentes IA.

**Hecho citado**: Archivo presente en raíz (verification.md, línea 85)

**Por qué**: 
- Agentes IA entiendan el proyecto
- Contribuidores nuevos sepan cómo aportar

**Aplicación**: 
- Actualizar cuando cambien procesos
- Mantener sincronizado con realidad

---

## 📚 Referencias

- [PROJECT_RULES.md](../../PROJECT_RULES.md) - Documento maestro de reglas

**Volver al índice**: [index.md](./index.md)
