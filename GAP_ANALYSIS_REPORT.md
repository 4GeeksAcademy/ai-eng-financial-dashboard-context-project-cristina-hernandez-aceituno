# 🎯 GAP ANALYSIS REPORT - Financial Dashboard

**Fecha**: 2026-11-18  
**Estado**: ANÁLISIS COMPLETADO POR AGENTE + VERIFICACIÓN MANUAL  
**Criticidad**: 🔴 CRÍTICA  
**Autor**: AI Agent + Code Analysis

---

## 📊 EL GAP IDENTIFICADO

### Problema Raíz
**"No existe una especificación centralizada y versionada de contrato de datos financieros (números, monedas, precisión decimal, redondeo) entre frontend y backend"**

En una aplicación financiera, esto es **crítico**: cambios en el backend (ej: cambiar a 3 decimales, agregar moneda) rompen el frontend sin validación clara.

---

## 📍 EVIDENCIA DEL CODEBASE

### **Hallazgo 1: Redondeo Incompleto en Backend (12 usos de `round()`)**

**Archivo**: [backend/app/routes.py](backend/app/routes.py#L80-L236)

```python
# LÍNEA 80-83: Generación de datos mock
amount = round(random.uniform(800, 12000), 2)   # ✓ 2 decimales
amount = round(random.uniform(500, 9000), 2)    # ✓ 2 decimales

# LÍNEA 182-184: Resumen de métricas
income=round(values["income"], 2),
outcome=round(values["outcome"], 2),
net=round(values["income"] - values["outcome"], 2),

# LÍNEA 205: Top categorías
total_amount=round(total_amount, 2),

# LÍNEA 216: Cálculo neto
return round(income - outcome, 2)

# LÍNEA 234-236: Alertas de métricas
outcome_total=round(item.outcome, 2),
baseline_average=round(baseline, 2),
increase_ratio=round(increase_ratio, 4),  # ⚠️ INCONSISTENCIA: 4 decimales

# LÍNEA 329-332: Comparación de períodos
delta_abs = round(current_net - previous_net, 2)
delta_pct = round((delta_abs / abs(previous_net)) * 100, 2)
```

**Problema**: 12 usos de `round()` **sin** función centralizada. Regla de redondeo **implícita**, no documentada.

---

### **Hallazgo 2: Formateo con Precisión Diferente en Frontend (0 decimales)**

**Archivo**: [frontend/src/lib/financial-utils.ts](frontend/src/lib/financial-utils.ts#L23-L28)

```typescript
const currencyFormatter = new Intl.NumberFormat("en-US", {
  style: "currency",
  currency: "USD",
  minimumFractionDigits: 0,  // ⚠️ CERO decimales para display
  maximumFractionDigits: 0,  // ⚠️ CERO decimales para display
});

export function formatCurrency(value: number): string {
  return currencyFormatter.format(value);  // $1,235 (sin decimales)
}
```

**Problema**: Frontend **trunca/redondea al display** a 0 decimales. Backend envía 2 decimales, frontend muestra 0.

---

### **Hallazgo 3: Test Revela Redondeo Implícito**

**Archivo**: [frontend/src/lib/financial-utils.test.ts](frontend/src/lib/financial-utils.test.ts#L108)

```typescript
it("formats currency without decimals", () => {
  expect(formatCurrency(1234.56)).toBe("$1,235");  // ✓ Redondea a 0 decimales
});

it("formats percent with one decimal", () => {
  expect(formatPercent(15.555)).toBe("15.6%");     // ✓ 1 decimal para porcentajes
});
```

**Problema**: 
- Monedas: 0 decimales (Intl.NumberFormat redondea automáticamente)
- Porcentajes: 1 decimal (`.toFixed(1)`)
- **NO HAY DOCUMENTACIÓN de esta regla**

---

### **Hallazgo 4: Tipos sin Especificación de Precisión**

**Archivo**: [frontend/src/lib/financial-types.ts](frontend/src/lib/financial-types.ts#L1-L28)

```typescript
export interface FinancialMovement {
  create_date: string  // ISO date ✓
  amount: number       // ⚠️ ¿Precisión? ¿Rango? ¿Validación?
  operation_type: OperationType
  category: Category
  business_type: BusinessType
}

export interface KPIMetrics {
  totalIncome: number    // ⚠️ ¿2 decimales? ¿0?
  totalOutcome: number   // ⚠️ ¿Validación de positivo?
  profit: number         // ⚠️ ¿Puede ser negativo?
  profitPercent: number  // ⚠️ ¿0-100 o 0-1?
}
```

**Problema**: `number` es genérico. Sin comentarios de validación, rango, o formato esperado.

**Comparar con backend** [backend/app/routes.py](backend/app/routes.py#L18-L26):
```python
class FinancialMovement(BaseModel):
    create_date: date
    amount: float        # ⚠️ ¿Precisión?
    operation_type: OperationType
    category: Category
    business_type: BusinessType
```

**Ambos igual de genéricos. SIN especificación.**

---

### **Hallazgo 5: Validación de Respuesta en Frontend SIN Contrato**

**Archivo**: [frontend/src/App.tsx](frontend/src/App.tsx#L14-L20)

```typescript
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "";

async function fetchFinancialData(): Promise<FinancialMovement[]> {
  const response = await fetch(`${API_BASE_URL}/api/metrics`);
  if (!response.ok) {
    throw new Error(`Failed to fetch financial data: ${response.status}`);
  }
  return response.json();  // ⚠️ Sin validación de tipos/formato
}
```

**Problema**: 
- SIN validación de respuesta (Zod/Pydantic runtime schema)
- SIN contrato de API versionado
- Comment en [PROJECT_RULES.md](PROJECT_RULES.md#L476-L479) lo reconoce: "Backend podría cambiar formato"

---

### **Hallazgo 6: Sin Documentación de Contrato API**

**Archivos revisados**:
- README.md ✗ (No menciona precisión decimal)
- README.es.md ✗ (No menciona precisión decimal)
- PROJECT_RULES.md ✗ (Regla SEC-003 dice "Backend podría cambiar formato" pero NO especifica qué es el "formato correcto")
- .github/workflows/ ✗ (No existe - sin CI/CD checks de contrato)
- .api-contract.md / API.md ✗ (No existe)

---

## ⚠️ POR QUÉ LAS SKILLS EXISTENTES NO CUBREN ESTO

### **1. `accessibility` (WCAG 2.2)**
- ✓ Cubre: Contraste, keyboard nav, ARIA labels, screen readers
- ✗ **NO cubre**: Validación de datos, contratos de API, tipos de números

---

### **2. `vercel-react-best-practices` (Performance Optimization)**
- ✓ Cubre: Caching, rendering, hydration, SVG precision
- ✗ **NO cubre**: Domain-specific data validation, financial data contracts

**Nota**: SVG precision mencionado en la skill, pero es **coordenadas gráficas**, no datos financieros.

---

### **3. `webapp-testing` (Playwright E2E)**
- ✓ Cubre: Browser automation, UI testing, screenshots, logs
- ✗ **NO cubre**: API contract validation, data type specifications

---

## 🔴 IMPACTO: Por qué es crítico

| Escenario | Riesgo | Severidad |
|-----------|--------|-----------|
| Backend cambia precision a 3 decimales | Frontend rompe (test fallará) | 🔴 CRÍTICO |
| Backend devuelve moneda en EUR, no USD | Display incorrecto ($EUR 1,235) | 🔴 CRÍTICO |
| Redondeo inconsistente en alertas (line 236 usa 4 decimales) | Cálculos divergentes | 🟡 ALTO |
| Sin validación de `amount > 0` | Puede aceptarse montos negativos en backend | 🔴 CRÍTICO |
| Sin versionamiento de API | No hay forma de hacer cambios sin romper | 🔴 CRÍTICO |
| Cambio de zona horaria en `create_date` | Reportes con fechas incorrectas | 🟡 ALTO |

---

## 📊 CONFIRMACIÓN: 5 ARCHIVOS QUE DEMUESTRAN EL GAP

| # | Archivo | Líneas | Hallazgo |
|---|---------|--------|----------|
| 1 | backend/app/routes.py | 80, 182-184, 205, 216, 234-236, 329-332 | 12 usos inconsistentes de `round()` SIN centralización |
| 2 | frontend/src/lib/financial-utils.ts | 23-28 | Formatter hardcodeado con 0 decimales (DISPLAY) |
| 3 | frontend/src/lib/financial-utils.test.ts | 108 | Test revela redondeo implícito (1234.56 → $1,235) |
| 4 | frontend/src/lib/financial-types.ts | 7, 14-18 | Tipos `number` genéricos SIN especificación de precisión |
| 5 | frontend/src/App.tsx | 16-19 | `response.json()` SIN validación de contrato |

---

## 💡 SUGERENCIA DE SKILL REQUERIDA

### **Skill: `financial-data-contract-specification`**

**Propósito**: Validar y documentar contratos de datos financieros en aplicaciones que manejan dinero.

**Cobertura**:

1. **Data Type Validation**
   - Especificar precisión decimal exacta (2 para monedas, 1 para porcentajes)
   - Validar que `amount > 0` (nunca negativos a menos que sea explícito)
   - Validar rango de `profitPercent` (-100 a +100)

2. **API Contract Documentation**
   - Crear `.api-contract.md` con especificación de cada campo
   - Versionado de API (`/api/v1/metrics` vs `/api/v2/metrics`)
   - Change log cuando cambie formato

3. **Frontend-Backend Type Safety**
   - Usar Zod/TypeBox en frontend para validar respuestas
   - Usar Pydantic con validaciones en backend
   - Tests de contrato (contract testing)

4. **Rounding & Precision Rules**
   - Función centralizada: `function roundCurrency(value: number): number`
   - Documentar estrategia: "Siempre floor, nunca round" O "Siempre round"
   - Casos especiales: comisiones, impuestos, conversiones

5. **Currency & Locale Awareness**
   - Especificar moneda (USD, EUR, etc.) en tipos
   - Documentar zona horaria para `create_date`
   - Validación de moneda en cada endpoint

**Ubicación esperada**: `./.agents/skills/financial-data-contract/SKILL.md`

**Triggers**: 
- "Validar contrato de datos"
- "Especificar precision decimal"
- "API contract testing"
- "Financial data validation"

---

## 🚀 PRÓXIMOS PASOS SUGERIDOS

1. **Crear API Contract Spec** (`API_CONTRACT.md`)
   ```markdown
   # API Contract v1.0
   
   ## GET /api/metrics
   
   Response: `FinancialMovement[]`
   
   - `amount`: float, 2 decimals, > 0
   - `create_date`: ISO 8601
   - `operation_type`: "income" | "outcome" (enum)
   
   Display Format (Frontend):
   - `formatCurrency(1234.56)` → "$1,235" (0 decimals)
   ```

2. **Centralizar Redondeo**
   ```typescript
   // frontend/src/lib/financial-utils.ts
   export const CURRENCY_DECIMALS = 0;    // Para display
   export const AMOUNT_DECIMALS = 2;      // Para almacenamiento
   
   export function validateAmount(value: number): void {
     if (value <= 0) throw new Error("Amount must be positive");
     if (Math.abs(value % 1) > 0.01) throw new Error("Max 2 decimals");
   }
   ```

3. **Validación en Frontend**
   ```typescript
   import { z } from 'zod';
   
   const FinancialMovementSchema = z.object({
     amount: z.number().positive().multipleOf(0.01),
     create_date: z.string().datetime(),
   });
   
   const data = FinancialMovementSchema.parse(response);
   ```

4. **Tests de Contrato**
   - Verificar que `computeKPIs()` siempre devuelve máximo 2 decimales en monedas
   - Verificar que backend `round()` es consistente
   - E2E: Backend → API → Frontend → Display

---

## 📝 CONCLUSIÓN

El **Financial Dashboard carece de una especificación centralizada de contrato de datos para valores financieros**. 

Aunque el código **funciona actualmente**, es **frágil**: cualquier cambio en backend (formato, precisión, moneda) romperá frontend sin advertencia clara. 

Este gap es **específico de dominios financieros** y no es cubierto por:
- ❌ Accessibility (WCAG)
- ❌ React performance (Vercel)
- ❌ E2E testing (Playwright)

Requiere una **skill especializada en validación de contratos de datos financieros** que defina, documente y valide reglas de precisión, redondeo, y versionamiento de API.

---

## 🎯 RESUMEN EJECUTIVO FINAL

### El Gap
**No hay especificación centralizada de contrato de datos financieros (precisión decimal, redondeo, rangos, moneda, versioning)**

### Por Qué Importa
- En una app financiera, cambios silenciosos en datos reclasifican como **bugs críticos**
- Backend usa 2 decimales, frontend muestra 0 → mismatch sin documentación
- 12 `round()` dispersas sin regla centralizada
- API sin validación de tipos ni versionado

### Criticidad
🔴 **CRÍTICA** - Riesgo de inconsistencias en datos monetarios

### Skills Existentes
❌ No lo cubren (accessibility, performance, E2E testing son horizontales, no de dominio)

### Skill Propuesta
✅ **`financial-data-contract-specification`** - Validación y documentación de contratos financieros

### Próximos Pasos
1. Crear `API_CONTRACT.md` (definir precisión decimal exacta)
2. Implementar Zod schema en frontend para validación
3. Crear tests de contrato (backend vs frontend)
4. Documentar reglas de redondeo centralizadas

### ROI
Alto: Previene bugs silenciosos en datos financieros → confiabilidad + compliance

