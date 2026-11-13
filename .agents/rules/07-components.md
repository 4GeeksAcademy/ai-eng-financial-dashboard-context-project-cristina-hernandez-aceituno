# 🎨 Reglas de Componentes

Reglas sobre estructura y patrones de componentes React.

---

## REGLA-COMP-001: Record<> para Type-Safe Variants

**Norma**: Componentes con múltiples variantes usan `Record<>`.

**Hecho citado**: `frontend/src/components/dashboard/kpi-card.tsx:12-25` (CONCRETE_FINDINGS.md, línea 130)

```typescript
const variantStyles: Record<KPICardProps['variant'], { badge: string; icon: string }> = {
  income: { badge: 'bg-[var(--income-badge)]', icon: 'text-[var(--income-badge-fg)]' },
  outcome: { badge: 'bg-[var(--outcome-badge)]', icon: 'text-[var(--outcome-badge-fg)]' },
  profit: { badge: 'bg-[var(--profit-badge)]', icon: 'text-[var(--profit-badge-fg)]' },
  profitPercent: { badge: 'bg-[var(--profit-badge)]', icon: 'text-[var(--profit-badge-fg)]' },
}
```

**Por qué**: 
- TypeScript previene falta de keys
- Claridad visual
- Type-safe y exhaustivo

**Aplicación**: Usar para componentes con 2+ variantes.

---

## REGLA-COMP-002: Aria Labels para Accesibilidad

**Norma**: Secciones principales tienen `aria-label`.

**Hecho citado**: `frontend/src/App.tsx:48-52` (CONCRETE_FINDINGS.md, línea 140)

```typescript
<section aria-label="Key performance indicators">
  <KPIRow metrics={metrics} loading={loading} />
</section>

<section aria-label="Financial charts">
  ...
</section>
```

**Por qué**: 
- Accesibilidad para screen readers
- Semántica clara
- Inclusividad

**Aplicación**: Secciones principales deben tener aria-label.

---

## REGLA-COMP-003: Funciones Puras sin Side Effects

**Norma**: Lógica de cálculo (KPIs, datos) en funciones puras.

**Hecho citado**: `frontend/src/lib/financial-utils.ts` (CONCRETE_FINDINGS.md, línea 146)

```typescript
export function computeKPIs(movements: FinancialMovement[]): KPIMetrics {
  const totalIncome = movements
    .filter((m) => m.operation_type === "income")
    .reduce((sum, m) => sum + m.amount, 0);
  
  return { totalIncome, totalOutcome, profit, profitPercent };
}
```

**Por qué**: 
- Testeable
- Predecible
- Reutilizable

**Aplicación**: Mover lógica de componentes a utils cuando sea posible.

---

## 📚 Referencias

- [PROJECT_RULES.md](../../PROJECT_RULES.md) - Documento maestro de reglas

**Volver al índice**: [index.md](./index.md)
