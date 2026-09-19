import os
from playwright.sync_api import sync_playwright

# Configuration for screenshot dimensions and high-DPI scale
VARIATIONS = {
    "variation1": {"width": 402, "height": 874, "scale": 3},
    "variation2": {"width": 2560, "height": 1664, "scale": 2},
}

OUTPUT_DIR = "screenshots"

def generate_screenshots():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    with sync_playwright() as p:
        browser = p.chromium.launch()
        
        for i in range(1, 9):
            filename = f"{i:03d}.html"
            if not os.path.exists(filename):
                print(f"Skipping {filename}: File not found.")
                continue
            
            filepath = os.path.abspath(filename)
            file_url = f"file://{filepath}"
            
            for var_name, config in VARIATIONS.items():
                context = browser.new_context(
                    viewport={"width": config["width"], "height": config["height"]},
                    device_scale_factor=config["scale"]
                )
                page = context.new_page()
                page.goto(file_url, wait_until="networkidle")
                
                output_path = os.path.join(OUTPUT_DIR, f"{i:03d}_{var_name}.png")
                page.screenshot(path=output_path, full_page=False)
                print(f"Captured: {output_path}")
                
                context.close()
                
        browser.close()

if __name__ == "__main__":
    generate_screenshots()
