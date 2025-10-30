from playwright.sync_api import sync_playwright

# Example: Testing PHP application with PHP built-in server
# Use with with_server.py to automatically start and stop PHP server

# Run this with:
# python scripts/with_server.py \
#   --server "php -S localhost:8000 -t /path/to/your/php/app" \
#   --port 8000 \
#   -- python examples/php_server_testing.py

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    
    # The PHP server is already running via with_server.py
    page.goto('http://localhost:8000')
    page.wait_for_load_state('networkidle')
    
    # Test homepage
    title = page.title()
    print(f"Page title: {title}")
    
    # Get all links on the page
    links = page.locator('a[href]').all()
    print(f"\nFound {len(links)} links:")
    for link in links[:5]:
        href = link.get_attribute('href')
        text = link.inner_text().strip()
        print(f"  - {text} -> {href}")
    
    # Test navigation
    if links:
        first_link = links[0]
        print(f"\nClicking first link: {first_link.inner_text()}")
        first_link.click()
        page.wait_for_load_state('networkidle')
        print(f"Navigated to: {page.url}")
    
    # Take screenshot
    page.screenshot(path='/tmp/php_app_test.png', full_page=True)
    print("\nScreenshot saved to /tmp/php_app_test.png")
    
    browser.close()

print("PHP server testing completed!")
