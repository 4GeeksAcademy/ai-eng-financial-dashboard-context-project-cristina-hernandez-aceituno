---
name: financial-data-contract-specification
description: Establish and maintain a centralized, versioned data contract for financial values (decimal precision, rounding rules, validation ranges, currency) between frontend and backend. Use when implementing new financial metrics, fixing precision bugs, ensuring API type-safety, or preventing data format mismatches.
license: MIT
keywords:
  - financial-data
  - api-contract
  - type-safety
  - precision-decimal
  - currency-validation
  - data-contract
---

# Financial Data Contract Specification

## 🎯 Objective

**Eliminate silent data format mismatches** between backend calculations and frontend display of financial values by establishing a single, versioned, executable data contract.

**Problem**: The Financial Dashboard backend uses 2 decimal precision (1234.57) but frontend displays 0 decimals ($1,235) with no documented contract. Changes in backend precision/format silently break frontend without validation.

**Solution**: Create a centralized financial data contract that:
- ✅ Specifies exact decimal precision per field type
- ✅ Defines rounding behavior (banker's rounding)
- ✅ Validates ranges (amounts > 0, percentages 0-100)
- ✅ Enforces type safety (Pydantic backend, Zod frontend)
- ✅ Versions API changes (`/api/v1/` vs `/api/v2/`)
- ✅ Prevents silent data corruption

---

## 📋 When to Use

Invoke this skill when:

1. **Implementing new financial metrics** — Adding numeric fields to API
2. **Fixing display bugs** — Currency shows wrong decimals/rounding
3. **Adding new currencies** — Extending from USD to EUR/GBP
4. **Type safety concerns** — Frontend lacks validation of API responses
5. **Backend refactoring** — Changing precision, adding validation, versioning API
6. **Data quality issues** — Seeing inconsistent calculations between endpoints
7. **Multi-team coordination** — Need executable contract between backend & frontend teams

---

## 📥 Input Requirements

### Context You Must Gather

1. **Financial fields audit**
   - List all numeric financial fields in codebase
   - What is their semantic meaning? (currency, percentage, ratio)
   - Current storage and display precision

2. **Current behavior analysis**
   - Backend: How are values calculated and rounded?
   - Frontend: How are values formatted for display?
   - Where do they diverge? (discovered gaps)

3. **Business rules**
   - Min/max valid ranges for each field
   - Currency support (USD only? Multi-currency?)
   - Decimal precision per field type
   - Rounding strategy (banker's vs standard)

4. **Code inventory**
   - Backend calculation points (where `round()` is used)
   - Backend models and validators (Pydantic, SQLAlchemy)
   - Frontend types (TypeScript interfaces)
   - Frontend formatters and display components
   - Existing test expectations

5. **Tooling & dependencies**
   - Is Zod or TypeBox available? (for frontend validation)
   - Is Pydantic used? (for backend validation)
   - Testing framework available?

### Key Files to Examine

**Backend**:
- `app/routes.py` (search for `round(`)
- `app/main.py`
- Type models/schemas

**Frontend**:
- `src/lib/financial-types.ts`
- `src/lib/financial-utils.ts`
- `src/lib/financial-utils.test.ts`
- `src/App.tsx` (API fetch)

**Documentation**:
- README.md, API docs (if any)
- Existing validation patterns

---

## 📤 Expected Outputs

### 1. Data Contract Definition Document
**File**: `./.agents/skills/financial-data-contract/CONTRACT_v1.md` (or add to API docs)

Contains:
- Contract version and date
- Each financial field with: name, type, precision, rounding rule, min/max, currency, examples
- Validation rules (what's invalid, error responses)
- Rounding behavior documented with examples
- Versioning strategy
- Change log template

### 2. Backend Implementation
**Files**: 
- `backend/app/financial_validation.py` (new centralized module)
- Updated `app/routes.py` (using centralized validators)
- Updated type models (Pydantic with field validators)

**What's added**:
- Functions: `round_currency()`, `round_percent()`, `round_ratio()`
- Pydantic models with range/precision validators
- Centralized rounding rules (no more scattered `round()` calls)
- Contract version endpoint (GET `/api/contract`)

### 3. Frontend Implementation
**Files**:
- Updated `src/lib/financial-types.ts` (JSDoc + types)
- Updated `src/lib/financial-utils.ts` (matches backend precision)
- New `src/lib/financial-contract-validation.ts` (Zod schema)
- Updated `src/App.tsx` (validate API responses)

**What's added**:
- Zod schema validating API responses
- Updated formatters matching backend precision
- JSDoc comments on types (precision, range, currency)
- Runtime validation on fetch

### 4. Contract Tests
**Files**: `frontend/src/lib/financial-utils.test.ts`, `backend/tests/test_financial_contract.py`

**What's tested**:
- Backend precision: `round_currency(1234.567)` → exactly `Decimal('1234.57')`
- Rounding rules: banker's rounding behavior
- Range validation: amounts > 0, percentages 0-100
- Frontend formatters: match backend precision
- Round-trip test: Backend → API → Frontend → Display consistency

### 5. Documentation
**Files**: 
- `API_CONTRACT.md` (versioned contract spec)
- `MIGRATION_v1_to_v2.md` (if upgrading contract version)
- Comments in code (JSDoc, inline)
- Skill output saved to memory-bank

---

## ✅ Acceptance Criteria

Task is complete when:

### Backend
- [ ] `financial_validation.py` exists with centralized rounding functions
- [ ] All `round()` calls in `routes.py` use centralized functions
- [ ] Models have Pydantic validators for ranges (amounts > 0, percentages 0-100)
- [ ] No hardcoded decimal precision in route handlers
- [ ] Contract endpoint exists: `GET /api/contract` returns versioned spec
- [ ] Linting passes (`pylint`, `flake8`)
- [ ] Tests pass (15+ tests covering rounding, ranges, edge cases)

### Frontend
- [ ] Zod schema created to validate API responses
- [ ] `App.tsx` uses schema validation on fetch (not `response.json()` directly)
- [ ] `formatCurrency()` and `formatPercent()` match backend precision exactly
- [ ] JSDoc comments on types specify precision, range, currency
- [ ] Tests added/updated: 5+ tests for precision, formatters, validation
- [ ] TypeScript compiles with 0 errors
- [ ] ESLint passes

### Documentation
- [ ] `API_CONTRACT.md` exists and specifies v1.0 exactly
- [ ] Each field documented: type, precision, range, currency, examples, notes
- [ ] Versioning strategy documented (how to upgrade v1.0 → v1.1)
- [ ] Invalid examples shown (what NOT to send)
- [ ] Contract linked in README or API docs

### Validation
- [ ] All 5 E2E tests pass (dashboard still loads, displays correctly)
- [ ] No breaking changes to existing endpoints
- [ ] Contract version queryable: `GET /api/contract` → `{ version: "1.0", ... }`
- [ ] One real refactoring completed: centralize redondeo in `routes.py`

---

## 🛠️ Implementation Steps

### PHASE 1: Audit & Discovery (20 min)

**Step 1.1**: Scan codebase for financial fields

```bash
# Find all numeric financial fields
grep -r "amount\|income\|outcome\|profit\|percent\|ratio" \
  backend/app/ frontend/src/ \
  --include="*.py" --include="*.ts" \
  | grep -E ":\s*(number|float|Decimal)" | head -20
```

**Step 1.2**: Create discovery table (temporary)

Document current behavior:

| Field | Backend Type | Backend Rounding | Frontend Format | Display Decimals | Currency | Valid Range | Gaps |
|-------|--------------|------------------|-----------------|------------------|----------|-------------|------|
| `amount` | `float` | `round(..., 2)` | `formatCurrency()` | 0 | USD | > 0 | Display loses precision |
| `profitPercent` | `float` | `round(..., 2)` | `formatPercent()` | 1 | No | 0–100 | ✓ OK |
| `increase_ratio` | `float` | `round(..., 4)` | None | 4 | No | Any | ⚠️ Inconsistent with others |

**Step 1.3**: Review existing tests for precision expectations

```bash
# Check what precision tests expect
grep -A2 "formatCurrency\|formatPercent" frontend/src/lib/financial-utils.test.ts

# Check backend rounding
grep -B2 -A2 "round(" backend/app/routes.py | head -30
```

**Deliverable**: Discovery table saved as temporary notes

---

### PHASE 2: Define the Contract (15 min)

**Step 2.1**: Create contract definition

**File**: `./.agents/skills/financial-data-contract/CONTRACT_v1.md`

```markdown
# Financial Data Contract v1.0

Established: 2026-11-18
Status: ACTIVE

## Overview

All financial values in the Financial Dashboard API v1 follow these rules:
- Decimal precision: Exact specification per field
- Rounding: Banker's rounding (round half to even)
- Currency: USD only in v1
- Validation: Ranges enforced at API boundary

## Field Specification

### Currency Fields (amounts, totals)

| Field | Precision | Min | Max | Display Decimals | Example |
|-------|-----------|-----|-----|------------------|---------|
| `amount` | 2 decimals | 0.01 | 999,999.99 | 0 | 1250.47 → "$1,250" |
| `totalIncome` | 2 decimals | 0.00 | 999,999.99 | 0 | 15000.00 → "$15,000" |
| `totalOutcome` | 2 decimals | 0.00 | 999,999.99 | 0 | 8750.50 → "$8,751" |
| `profit` | 2 decimals | -999,999.99 | 999,999.99 | 0 | 6249.50 → "$6,250" |

### Percentage Fields

| Field | Precision | Min | Max | Display Decimals | Example |
|-------|-----------|-----|-----|------------------|---------|
| `profitPercent` | 2 decimals | 0 | 100 | 1 | 15.235 → "15.2%" |

### Ratio Fields (internal)

| Field | Precision | Min | Max | Display Decimals | Example |
|-------|-----------|-----|-----|------------------|---------|
| `increase_ratio` | 4 decimals | 0 | 1 | 4 | 0.1234 (not user-visible) |

## Rounding Behavior

All calculations use banker's rounding (round half to even):
- 1.5 → 2 (2 is even)
- 2.5 → 2 (2 is even)
- 1.235 → 1.24 (4 is even)

## API Validation

Invalid responses (should return 422):
- `amount` with 3+ decimals (must be exactly 2)
- `profitPercent` > 100 or < 0
- `totalOutcome` < 0
- Any field NULL when required

## Transport Format

All values are decimal numbers in JSON (no strings):

```json
{
  "amount": 1250.47,
  "totalIncome": 15000.00,
  "profitPercent": 15.24,
  "increase_ratio": 0.1234
}
```
```

---

### PHASE 3: Implement Backend (30 min)

**Step 3.1**: Create centralized validation module

**File**: `backend/app/financial_validation.py` (NEW)

```python
"""
Financial data validation and rounding rules.
Implements Financial Data Contract v1.0
"""

from decimal import Decimal, ROUND_HALF_EVEN
from pydantic import BaseModel, Field, validator

def round_currency(value, decimals=2):
    """Round currency using banker's rounding to N decimals."""
    d = Decimal(str(value))
    quantize_exp = Decimal(10) ** -decimals
    return d.quantize(quantize_exp, rounding=ROUND_HALF_EVEN)

def round_percent(value, decimals=2):
    """Round percentage using banker's rounding to N decimals."""
    if value is None:
        return None
    d = Decimal(str(value))
    quantize_exp = Decimal(10) ** -decimals
    return d.quantize(quantize_exp, rounding=ROUND_HALF_EVEN)

class CurrencyAmount(BaseModel):
    """Currency field validator (2 decimals, 0.01-999,999.99)"""
    value: Decimal = Field(..., ge=Decimal("0.01"), le=Decimal("999999.99"))

class PercentageValue(BaseModel):
    """Percentage field validator (2 decimals, 0-100)"""
    value: Decimal = Field(..., ge=0, le=100)
```

**Step 3.2**: Update routes to use centralized rounding

**File**: `backend/app/routes.py` - Replace 12 `round()` calls:

Before:
```python
amount = round(random.uniform(800, 12000), 2)      # Scattered
net = round(income - outcome, 2)                   # Scattered
increase_ratio = round(increase_ratio, 4)          # Scattered
```

After:
```python
from app.financial_validation import round_currency, round_percent

amount = round_currency(random.uniform(800, 12000))  # Centralized
net = round_currency(income - outcome)                # Centralized
increase_ratio = round_percent(increase_ratio, 4)    # Centralized
```

**Step 3.3**: Add contract endpoint

```python
@app.get("/api/contract")
def get_contract():
    """Return current financial data contract version."""
    return {
        "version": "1.0",
        "established": "2026-11-18",
        "currency": "USD",
        "fields": {
            "amount": {"precision": 2, "min": 0.01, "max": 999999.99},
            "profitPercent": {"precision": 2, "min": 0, "max": 100},
            "increase_ratio": {"precision": 4, "min": 0, "max": 1},
        }
    }
```

**Step 3.4**: Test backend

```bash
cd backend
python -m pytest tests/test_financial_contract.py -v

# Should see all tests PASS:
# - test_round_currency_banker's_rounding
# - test_round_percent_validation
# - test_range_validation_amounts
# - test_contract_endpoint_returns_version
```

---

### PHASE 4: Implement Frontend (30 min)

**Step 4.1**: Create Zod validation schema

**File**: `frontend/src/lib/financial-contract-validation.ts` (NEW)

```typescript
import { z } from 'zod';

export const FinancialContractV1 = z.object({
  amount: z.number().positive().multipleOf(0.01),
  totalIncome: z.number().nonnegative().multipleOf(0.01),
  totalOutcome: z.number().nonnegative().multipleOf(0.01),
  profit: z.number().multipleOf(0.01),
  profitPercent: z.number().min(0).max(100).multipleOf(0.01),
  increase_ratio: z.number().min(0).max(1).optional(),
});

export function validateFinancialData(data: unknown) {
  return FinancialContractV1.parse(data);
}
```

**Step 4.2**: Update App.tsx to validate

Before:
```typescript
const data = await response.json();  // ❌ No validation
```

After:
```typescript
const rawData = await response.json();
const data = validateFinancialData(rawData);  // ✅ Validates contract
```

**Step 4.3**: Update formatters to match contract

**File**: `frontend/src/lib/financial-utils.ts`

```typescript
// Matches backend precision exactly
const currencyFormatter = new Intl.NumberFormat("en-US", {
  style: "currency",
  currency: "USD",
  minimumFractionDigits: 0,  // ✓ Documented (backend: 2, display: 0)
  maximumFractionDigits: 0,
});

export function formatCurrency(value: number): string {
  return currencyFormatter.format(value);
}

export function formatPercent(value: number): string {
  return (Math.round(value * 10) / 10).toFixed(1) + "%";  // 1 decimal
}
```

**Step 4.4**: Test frontend

```bash
cd frontend
npm run test -- financial-utils.test.ts

# Should see:
# ✓ formatCurrency(1234.56) → "$1,235" (0 decimals)
# ✓ formatPercent(15.235) → "15.2%" (1 decimal)
```

---

### PHASE 5: Documentation & Validation (15 min)

**Step 5.1**: Document in README or API docs

Add to README:

```markdown
## Financial Data Contract

The Financial Dashboard implements a versioned data contract for financial values.

**Current Version**: v1.0

**Key Rules**:
- Currency amounts: 2 decimals precision, displayed as 0 decimals
- Percentages: 2 decimals precision, displayed as 1 decimal
- All values use banker's rounding
- Contract queryable at: `GET /api/contract`

See [API_CONTRACT.md](docs/API_CONTRACT.md) for full specification.
```

**Step 5.2**: Run full validation

```bash
# Backend tests
cd backend && python -m pytest tests/test_financial_contract.py -v

# Frontend tests & lint
cd frontend && npm run test && npm run lint && npm run build

# E2E tests
npm run test:e2e
```

**Step 5.3**: Verify contract is queryable

```bash
curl http://localhost:8000/api/contract
# Should return contract v1.0 JSON
```

---

## 📊 Real Example: Centralizing Redondeo in routes.py

### Before (12 scattered round calls)

```python
# Line 80
amount = round(random.uniform(800, 12000), 2)

# Line 83  
profit_percent = round((profit / income) * 100, 2)

# Line 236 (INCONSISTENT: 4 decimals)
increase_ratio = round(increase_ratio, 4)

# ... 9 more scattered round() calls
```

**Problem**: 
- ❌ Hardcoded 2, 4 decimals in 12 places
- ❌ No centralized rounding rule
- ❌ Changed one place? Bug silently introduced

### After (Centralized)

```python
from app.financial_validation import round_currency, round_percent, round_ratio

# Line 80
amount = round_currency(random.uniform(800, 12000))  # Always 2 decimals

# Line 83
profit_percent = round_percent((profit / income) * 100)  # Always 2 decimals

# Line 236
increase_ratio = round_ratio(increase_ratio)  # Always 4 decimals
```

**Benefits**:
- ✅ Single source of truth for rounding rules
- ✅ Consistent precision everywhere
- ✅ Easy to test: test functions once, all 12 places use same logic
- ✅ Easy to change: update function, all 12 places updated

---

## 🎓 Summary

**What you've accomplished**:

✅ Identified all financial fields  
✅ Created centralized rounding functions  
✅ Documented contract v1.0 (fields, precision, ranges)  
✅ Added Zod validation to frontend  
✅ Validated API responses on fetch  
✅ Replaced 12 scattered `round()` with centralized functions  
✅ Tested contract compliance (backend + frontend)  
✅ Documented contract in API docs  

**Result**: 🟢 Backend and frontend now have a **single executable contract**. Changes to precision/rounding are centralized, tested, and documented.

---

## 🔗 References

**Financial Data Standards**:
- [ISO 4217 - Currency codes](https://en.wikipedia.org/wiki/ISO_4217)
- [Banker's Rounding (ROUND_HALF_EVEN)](https://en.wikipedia.org/wiki/Rounding#Round_half_to_even)
- [Stripe API Precision](https://stripe.com/docs/currencies#zero-decimal)

**Validation Libraries**:
- [Pydantic (Python)](https://docs.pydantic.dev/)
- [Zod (TypeScript)](https://zod.dev/)

**Related Skills**:
- `accessibility` - Ensuring formatted numbers are screen-reader accessible
- `webapp-testing` - E2E tests for contract compliance
- `vercel-react-best-practices` - Performance of number formatters (caching Intl)
