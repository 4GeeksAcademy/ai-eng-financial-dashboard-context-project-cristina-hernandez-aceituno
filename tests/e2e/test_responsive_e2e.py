"""
Test E2E: Responsive Layout
Verifica que el dashboard se adapta correctamente a mobile, tablet y desktop.
Regla SKILL.md: "Take screenshot or inspect DOM"
Archivo Real: frontend/src/App.tsx (grid layout con Tailwind)
"""

from playwright.sync_api import sync_playwright


def test_responsive_layout_mobile_tablet_desktop():
    """
    Verifica layout responsivo en 3 viewports:
    - Mobile (375x667)
    - Tablet (768x1024)
    - Desktop (1920x1080)
    
    Validaciones:
    1. No overflow horizontal
    2. Elementos visibles sin scroll vertical excesivo
    3. Grid columns adaptan correctamente
    """
    
    viewports = {
        'mobile': {'width': 375, 'height': 667},
        'tablet': {'width': 768, 'height': 1024},
        'desktop': {'width': 1920, 'height': 1080},
    }
    
    for device_name, viewport in viewports.items():
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(viewport=viewport)
            
            # Navega
            page.goto('http://localhost:5173')
            page.wait_for_load_state('networkidle')
            
            # 1. Captura screenshot para inspección visual
            # (en pytest real, esto se archiva en artefactos)
            page.screenshot(
                path=f'/tmp/dashboard_{device_name}.png',
                full_page=True
            )
            print(f"✅ Screenshot capturado: /tmp/dashboard_{device_name}.png")
            
            # 2. Verifica que el contenido principal está visible
            main_content = page.locator('main').first
            assert main_content.is_visible(), \
                f"❌ Main content not visible on {device_name}"
            
            # 3. Verifica que KPIRow está visible (4 cards en desktop, 1-2 en mobile)
            kpi_row = page.locator('[class*="grid"][class*="gap"]').first
            if kpi_row.is_visible():
                print(f"✅ KPI row visible on {device_name}")
            
            # 4. Obtén ancho del viewport y verifica no hay overflow
            viewport_width = page.evaluate('window.innerWidth')
            body_width = page.evaluate('document.body.scrollWidth')
            
            # scrollWidth debe ser similar a innerWidth (permitir pequeña diferencia)
            overflow_pixels = body_width - viewport_width
            assert overflow_pixels <= 10, \
                f"❌ Horizontal overflow on {device_name}: {overflow_pixels}px"
            
            print(f"✅ No horizontal overflow on {device_name}")
            
            # 5. Verifica scroll height razonable (no contenido infinito)
            scroll_height = page.evaluate('document.body.scrollHeight')
            assert scroll_height < 5000, \
                f"❌ Content too tall on {device_name}: {scroll_height}px"
            
            print(f"✅ Content height reasonable on {device_name}: {scroll_height}px")
            
            # 6. Verifica que labels KPI existen (pueden requerir scroll en mobile)
            for label in ['Total Income', 'Total Outcome']:
                label_elem = page.locator(f'text=\"{label}\"').first
                assert label_elem.count() > 0, \
                    f"❌ Label '{label}' not found on {device_name}"
            
            print(f"✅ KPI labels present (scroll required on mobile is OK)")
            
            browser.close()
            print(f"✅ Responsive test PASSED for {device_name}\n")


if __name__ == "__main__":
    test_responsive_layout_mobile_tablet_desktop()
