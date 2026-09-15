import asyncio
import os
import sys
from playwright.async_api import async_playwright

async def capture_distinct_screenshots():
    output_dir = "screenshots"
    os.makedirs(output_dir, exist_ok=True)
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(channel="msedge", headless=True)
        context = await browser.new_context(viewport={"width": 1600, "height": 900}, device_scale_factor=1.5)
        page = await context.new_page()

        # Route block fonts/external trackers to ensure instant rendering
        await page.route("**/*.woff*", lambda route: route.abort())
        await page.route("https://fonts.gstatic.com/**", lambda route: route.abort())

        print("1. Loading Streamlit App at http://localhost:8501 ...")
        await page.goto("http://localhost:8501", wait_until="networkidle")
        await page.wait_for_timeout(3000)

        # Click Load Preset Sample ML Data button in sidebar
        print("2. Clicking 'Load Preset Sample ML Data'...")
        btn = page.get_by_role("button", name="Load Preset Sample ML Data")
        if await btn.count() > 0:
            await btn.click()
            await page.wait_for_timeout(3000)

        # Click 'Run Deep AI Analysis & Match' button if present to compute scores
        run_btn = page.get_by_role("button", name="Run Deep AI Analysis & Match")
        if await run_btn.count() > 0:
            print("3. Clicking 'Run Deep AI Analysis & Match'...")
            await run_btn.click()
            await page.wait_for_timeout(4000)

        # --- SC1: TOP BANNER & MATCH SCORE GAUGE ---
        sc1_path = os.path.join(output_dir, "sc1_ats_score.png")
        await page.evaluate("window.scrollTo(0, 0)")
        await page.wait_for_timeout(1000)
        await page.screenshot(path=sc1_path)
        print(f"Captured SC1 (Metrics & Score): {sc1_path}")

        # --- SC2: PLOTLY SKILL RADAR CHART ---
        sc2_path = os.path.join(output_dir, "sc2_radar_chart.png")
        # Scroll down to Plotly chart
        await page.evaluate("window.scrollTo(0, 750)")
        await page.wait_for_timeout(1500)
        # Try finding plotly chart container
        plotly_element = page.locator(".js-plotly-plot")
        if await plotly_element.count() > 0:
            await plotly_element.first.screenshot(path=sc2_path)
        else:
            await page.screenshot(path=sc2_path)
        print(f"Captured SC2 (Plotly Radar Chart): {sc2_path}")

        # --- SC3: FORMATTING AUDIT & SKILL GAP RECOMMENDATIONS ---
        sc3_path = os.path.join(output_dir, "sc3_recommendations.png")
        await page.evaluate("window.scrollTo(0, 1450)")
        await page.wait_for_timeout(1500)
        await page.screenshot(path=sc3_path)
        print(f"Captured SC3 (Format Audit & Skill Gaps): {sc3_path}")

        # --- SC4: SWITCH SIDEBAR VIEW TO EVALUATION HISTORY & DB ---
        print("4. Switching sidebar view to 'Evaluation History & Logs'...")
        radio = page.locator("label:has-text('Evaluation History & Logs')")
        if await radio.count() > 0:
            await radio.click()
            await page.wait_for_timeout(3000)

        sc4_path = os.path.join(output_dir, "sc4_batch_history.png")
        await page.evaluate("window.scrollTo(0, 0)")
        await page.wait_for_timeout(1000)
        await page.screenshot(path=sc4_path)
        print(f"Captured SC4 (SQLite Audit History Log): {sc4_path}")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(capture_distinct_screenshots())
