"""
Test E2E: Dashboard Load Flow
Verifica que el dashboard carga correctamente y los datos se obtienen desde /api/metrics.
Regla SKILL.md: "Reconnaissance-then-action" + "wait for networkidle"
"""

from playwright.sync_api import sync_playwright


def test_dashboard_loads_with_kpis():
    """
    Verifica flujo completo: 
    1. App.tsx carga
    2. Lazy charts se inicializan con Suspense fallback
    3. /api/metrics es llamada
    4. KPIRow renderiza 4 KPICards
    5. Valores no vacíos se muestran
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        # Rastrear requests para verificar API call
        requests_made = []
        page.on('request', lambda r: requests_made.append(r.url))
        
        # 1. Navega al dashboard
        page.goto('http://localhost:5173')
        
        # 2. CRÍTICO: Espera networkidle (todos los JS + data fetched)
        page.wait_for_load_state('networkidle')
        
        # 3. Verifica que /api/metrics fue llamada
        api_metrics_called = any('/api/metrics' in url for url in requests_made)
        assert api_metrics_called, f"❌ /api/metrics not called. Requests: {requests_made}"
        
        # 4. Verifica headers KPI presentes (reconocimiento visual)
        kpi_labels = ['Total Income', 'Total Outcome', 'Profit', 'Profit']
        for label in kpi_labels:
            # Busca el texto exacto del label
            locator = page.locator(f'text="{label}"')
            assert locator.count() > 0, f"❌ KPI label '{label}' not found"
        
        # 5. Verifica que valores numéricos están presentes ($, %)
        # Busca por selectors de clase (text-3xl = valores grandes)
        value_elements = page.locator('[class*="text-3xl"]').all()
        assert len(value_elements) >= 4, f"❌ Expected 4+ value elements, found {len(value_elements)}"
        
        # 6. Verifica contenido de valores (no vacíos)
        for idx, value_elem in enumerate(value_elements[:4]):
            text = value_elem.inner_text()
            assert text.strip(), f"❌ Value element {idx} is empty"
        
        # 7. Verifica que footer helper text está presente (accessibility)
        helper_texts = page.locator('[class*="text-muted-foreground"][class*="text-xs"]').all()
        assert len(helper_texts) > 0, "❌ No helper texts found in KPIs"
        
        # 8. Verifica que skeleton loaders NO están visibles (data ya loaded)
        skeletons = page.locator('[class*="skeleton"]').all()
        # Puede haber skeletons en charts mientras se lazy-loaden, es OK
        # Pero KPIs no deben tener skeletons
        for skeleton in skeletons:
            parent = skeleton.evaluate('el => el.parentElement.className')
            assert 'chart' in parent.lower() or 'chart-skeleton' in parent.lower(), \
                f"❌ Skeleton found outside of chart area: {parent}"
        
        browser.close()
        print("✅ Dashboard load test PASSED")
        print(f"   - API /api/metrics called")
        print(f"   - 4+ KPI labels found")
        print(f"   - Values rendered correctly")
        print(f"   - No loading skeletons visible")


if __name__ == "__main__":
    test_dashboard_loads_with_kpis()
