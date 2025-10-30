from playwright.sync_api import sync_playwright

# Example: Testing a PHP web application using Playwright
# This demonstrates testing a typical PHP application (e.g., LAMP stack)

# Assumptions:
# - PHP development server running on localhost:8000
# - Or use with_server.py to start the PHP server automatically

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={'width': 1920, 'height': 1080})
    
    # Example 1: Testing a PHP login form
    page.goto('http://localhost:8000/login.php')
    page.wait_for_load_state('networkidle')
    
    # Take initial screenshot
    page.screenshot(path='/tmp/php_login_page.png', full_page=True)
    
    # Fill in login form
    page.fill('#username', 'testuser')
    page.fill('#password', 'testpass123')
    
    # Submit form and wait for navigation
    page.click('button[type="submit"]')
    page.wait_for_url('**/dashboard.php')  # Wait for redirect
    
    # Verify successful login
    welcome_message = page.locator('.welcome-message').inner_text()
    print(f"Login successful! Message: {welcome_message}")
    
    # Example 2: Testing a PHP AJAX endpoint
    page.goto('http://localhost:8000/api/users.php')
    page.wait_for_load_state('networkidle')
    
    # Get the JSON response displayed on page
    content = page.content()
    print(f"API Response: {content}")
    
    # Example 3: Testing PHP form submission with validation
    page.goto('http://localhost:8000/register.php')
    page.wait_for_load_state('networkidle')
    
    # Test form validation
    page.fill('#email', 'invalid-email')
    page.click('button[type="submit"]')
    page.wait_for_timeout(500)
    
    # Check for validation error
    error = page.locator('.error-message').inner_text()
    print(f"Validation error displayed: {error}")
    
    # Fill valid data
    page.fill('#email', 'user@example.com')
    page.fill('#username', 'newuser')
    page.fill('#password', 'SecurePass123!')
    page.click('button[type="submit"]')
    
    # Wait for success message
    page.wait_for_selector('.success-message')
    success = page.locator('.success-message').inner_text()
    print(f"Registration successful: {success}")
    
    # Example 4: Capture console logs (useful for debugging PHP JavaScript)
    console_logs = []
    
    def handle_console(msg):
        console_logs.append(f"[{msg.type}] {msg.text}")
    
    page.on("console", handle_console)
    page.goto('http://localhost:8000/dashboard.php')
    page.wait_for_load_state('networkidle')
    
    print(f"\nCaptured {len(console_logs)} console messages:")
    for log in console_logs:
        print(f"  {log}")
    
    # Example 5: Testing PHP session persistence
    # Navigate to different pages and verify session is maintained
    page.goto('http://localhost:8000/profile.php')
    page.wait_for_load_state('networkidle')
    
    # Check if still logged in
    if page.locator('.logout-button').is_visible():
        print("Session maintained - user still logged in")
    else:
        print("Session lost - user logged out")
    
    # Take final screenshot
    page.screenshot(path='/tmp/php_profile_page.png', full_page=True)
    
    browser.close()

print("\nPHP application testing completed!")
