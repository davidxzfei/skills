# Deploying Webapp-Testing Skills to Claude Code

## Overview
The webapp-testing skill provides Claude Code with Playwright-based browser automation capabilities for testing local web applications. This guide walks through installing the `webapp-testing` skill in Claude Code and provides ready-to-run demo prompts showcasing various testing patterns.

## Prerequisites
- Access to Claude Code with plugin support enabled
- A Claude Code chat or notebook session where you can run `/plugin` commands
- Python 3.8+ with Playwright installed in your environment
- Internet access for Claude Code to pull this GitHub repository

## Install from the Claude Code Plugin Marketplace (Recommended)
1. **Add the Anthropic skills marketplace once**
   ```
   /plugin marketplace add anthropics/skills
   ```
2. **Open the plugin picker** in Claude Code and choose **Browse and install plugins**.
3. Select **anthropic-agent-skills**.
4. Choose **webapp-testing** and press **Install now**.
5. Verify the install with:
   ```
   /plugin list
   ```
   You should see `webapp-testing@anthropic-agent-skills` listed.

You can also install the skill directly from chat:
```
/plugin install webapp-testing@anthropic-agent-skills
```

## Environment Setup

After installing the plugin, ensure Playwright is set up in your environment:

```bash
# Install Playwright if not already installed
pip install playwright

# Install Chromium browser
playwright install chromium
```

## Using the webapp-testing skill inside Claude Code
- Once installed, simply reference the skill in your instruction. Claude will automatically summon it when the task matches browser testing or automation.
- Example phrasing: "Use the **webapp-testing** skill to test the login form in my local PHP application."
- For repeat work, pin the plugin in the Claude Code sidebar so you can toggle it on for any session.
- To check which skills are active in the current conversation, run `/plugin status`.

## Updating or removing the plugin
- **Update** to the latest version:
  ```
  /plugin update webapp-testing@anthropic-agent-skills
  ```
- **Remove** if no longer needed:
  ```
  /plugin uninstall webapp-testing@anthropic-agent-skills
  ```

## Step-by-Step Deployment Examples

### Example 1: Testing Static HTML Files

**Scenario**: You have a static HTML file and want to test its form functionality.

**Files Structure**:
```
project/
├── index.html
└── test_static.py
```

**Steps**:

1. **Create your test script** (`test_static.py`):
```python
from playwright.sync_api import sync_playwright
import os

html_file = os.path.abspath('index.html')
file_url = f'file://{html_file}'

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto(file_url)
    
    # Test form interactions
    page.fill('#name', 'John Doe')
    page.fill('#email', 'john@example.com')
    page.click('button[type="submit"]')
    
    # Capture result
    page.screenshot(path='/tmp/result.png', full_page=True)
    print("✅ Static HTML test completed!")
    browser.close()
```

2. **Run the test**:
```bash
python test_static.py
```

3. **Ask Claude**: "Use the webapp-testing skill to test the contact form in my index.html file and take screenshots of each step."

---

### Example 2: Testing a PHP Application with Built-in Server

**Scenario**: You have a PHP application and want to test login functionality.

**Files Structure**:
```
php-app/
├── public/
│   ├── index.php
│   ├── login.php
│   └── dashboard.php
└── test_login.py
```

**Steps**:

1. **Create your test script** (`test_login.py`):
```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    
    # Test login flow
    page.goto('http://localhost:8000/login.php')
    page.wait_for_load_state('networkidle')
    
    page.fill('#username', 'admin')
    page.fill('#password', 'password123')
    page.click('button[type="submit"]')
    
    # Wait for redirect to dashboard
    page.wait_for_url('**/dashboard.php')
    
    # Verify login success
    welcome_msg = page.locator('.welcome-message').inner_text()
    print(f"Login successful! {welcome_msg}")
    
    page.screenshot(path='/tmp/dashboard.png', full_page=True)
    browser.close()
```

2. **Run with automatic server management** (RECOMMENDED):
```bash
cd webapp-testing
python scripts/with_server.py \
  --server "php -S localhost:8000 -t ../php-app/public" \
  --port 8000 \
  -- python ../test_login.py
```

3. **Manual server approach** (if needed):
```bash
# Terminal 1: Start PHP server
php -S localhost:8000 -t php-app/public

# Terminal 2: Run test
python test_login.py
```

4. **Ask Claude**: "Use the webapp-testing skill with the with_server.py helper to test my PHP login form. Start the PHP server on port 8000 and verify the login redirects to the dashboard."

---

### Example 3: Testing a Node.js Application (React/Vue/etc)

**Scenario**: You have a Node.js frontend application running on npm/yarn.

**Files Structure**:
```
react-app/
├── src/
├── package.json
└── test_app.py
```

**Steps**:

1. **Create your test script** (`test_app.py`):
```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    
    # Navigate to React app
    page.goto('http://localhost:5173')
    page.wait_for_load_state('networkidle')  # Critical for SPAs!
    
    # Discover available buttons
    buttons = page.locator('button').all()
    print(f"Found {len(buttons)} buttons on page")
    
    # Test interaction
    page.click('text=Get Started')
    page.wait_for_timeout(1000)
    
    page.screenshot(path='/tmp/react_app.png', full_page=True)
    browser.close()
```

2. **Run with server management**:
```bash
cd webapp-testing
python scripts/with_server.py \
  --server "cd ../react-app && npm run dev" \
  --port 5173 \
  -- python ../test_app.py
```

3. **Ask Claude**: "Use the webapp-testing skill to test my React application. Start the dev server with npm run dev and verify all navigation buttons work correctly."

---

### Example 4: Testing Full-Stack Application (Backend + Frontend)

**Scenario**: You have a backend API and frontend that need to run together.

**Files Structure**:
```
fullstack-app/
├── backend/
│   └── server.py (Flask/FastAPI)
├── frontend/
│   └── package.json (React/Vue)
└── test_fullstack.py
```

**Steps**:

1. **Create your test script** (`test_fullstack.py`):
```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    
    # Test frontend that calls backend
    page.goto('http://localhost:5173')
    page.wait_for_load_state('networkidle')
    
    # Trigger API call
    page.click('button:has-text("Fetch Users")')
    page.wait_for_selector('.user-list')
    
    users = page.locator('.user-item').all()
    print(f"Loaded {len(users)} users from API")
    
    page.screenshot(path='/tmp/fullstack_test.png', full_page=True)
    browser.close()
```

2. **Run with multiple servers**:
```bash
cd webapp-testing
python scripts/with_server.py \
  --server "cd ../fullstack-app/backend && python server.py" \
  --port 3000 \
  --server "cd ../fullstack-app/frontend && npm run dev" \
  --port 5173 \
  -- python ../test_fullstack.py
```

3. **Ask Claude**: "Use the webapp-testing skill to test my full-stack application. Start both the Python backend on port 3000 and the frontend on port 5173, then verify the user list loads correctly."

---

### Example 5: Element Discovery and Reconnaissance

**Scenario**: You're exploring a new web application and need to discover interactive elements.

**Steps**:

1. **Use the built-in example**:
```bash
cd webapp-testing
python scripts/with_server.py \
  --server "cd ../my-app && npm start" \
  --port 3000 \
  -- python examples/element_discovery.py
```

2. **Customize for your needs**:
```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    
    page.goto('http://localhost:3000')
    page.wait_for_load_state('networkidle')
    
    # Take initial screenshot
    page.screenshot(path='/tmp/inspect.png', full_page=True)
    
    # Discover all interactive elements
    buttons = page.locator('button').all()
    links = page.locator('a[href]').all()
    inputs = page.locator('input, textarea, select').all()
    
    print(f"Found {len(buttons)} buttons")
    print(f"Found {len(links)} links")
    print(f"Found {len(inputs)} input fields")
    
    # Get page HTML for analysis
    content = page.content()
    with open('/tmp/page_source.html', 'w') as f:
        f.write(content)
    
    browser.close()
```

3. **Ask Claude**: "Use the webapp-testing skill to discover all buttons, links, and form fields on my application running at localhost:3000. Provide a summary of all interactive elements."

---

### Example 6: Capturing Console Logs and Debugging

**Scenario**: You need to debug JavaScript errors or monitor console output.

**Steps**:

1. **Use the console logging pattern**:
```python
from playwright.sync_api import sync_playwright

console_logs = []

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    
    # Capture console messages
    def handle_console(msg):
        log_entry = f"[{msg.type}] {msg.text}"
        console_logs.append(log_entry)
        print(f"Console: {log_entry}")
    
    page.on("console", handle_console)
    
    # Navigate and interact
    page.goto('http://localhost:3000')
    page.wait_for_load_state('networkidle')
    
    page.click('text=Submit')
    page.wait_for_timeout(2000)
    
    browser.close()

# Save logs
with open('/tmp/console.log', 'w') as f:
    f.write('\n'.join(console_logs))

print(f"\nCaptured {len(console_logs)} console messages")
```

2. **Ask Claude**: "Use the webapp-testing skill to test my application and capture all console logs, especially any errors that occur during form submission."

---

### Example 7: Testing WordPress Site

**Scenario**: You want to test a local WordPress installation.

**Steps**:

1. **Create WordPress test script**:
```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    
    # Test WordPress admin login
    page.goto('http://localhost:8000/wp-admin')
    page.wait_for_load_state('networkidle')
    
    page.fill('#user_login', 'admin')
    page.fill('#user_pass', 'password')
    page.click('#wp-submit')
    
    # Verify logged in
    page.wait_for_url('**/wp-admin/**')
    page.screenshot(path='/tmp/wp_dashboard.png', full_page=True)
    print("✅ WordPress login successful!")
    
    browser.close()
```

2. **Run with PHP server** (if using built-in server):
```bash
cd webapp-testing
python scripts/with_server.py \
  --server "php -S localhost:8000 -t /path/to/wordpress" \
  --port 8000 \
  -- python ../test_wordpress.py
```

3. **Ask Claude**: "Use the webapp-testing skill to test my WordPress site. Login to wp-admin and verify the dashboard loads correctly."

---

### Example 8: Testing Laravel Application

**Scenario**: Testing a Laravel PHP application with Artisan serve.

**Steps**:

1. **Create Laravel test script**:
```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    
    # Test Laravel homepage
    page.goto('http://localhost:8000')
    page.wait_for_load_state('networkidle')
    
    assert 'Laravel' in page.title()
    print("✅ Laravel homepage loaded")
    
    # Test authentication
    page.goto('http://localhost:8000/login')
    page.fill('input[name="email"]', 'test@example.com')
    page.fill('input[name="password"]', 'password')
    page.click('button[type="submit"]')
    
    page.wait_for_url('**/dashboard')
    page.screenshot(path='/tmp/laravel_dashboard.png', full_page=True)
    print("✅ Laravel authentication successful!")
    
    browser.close()
```

2. **Run with Artisan serve**:
```bash
cd webapp-testing
python scripts/with_server.py \
  --server "cd ../my-laravel-app && php artisan serve" \
  --port 8000 \
  -- python ../test_laravel.py
```

3. **Ask Claude**: "Use the webapp-testing skill to test my Laravel application. Start the server with artisan serve and test the login flow."

---

## Ten Demo Prompts to Showcase the Webapp-Testing Skill

Use these prompts inside Claude Code after enabling the plugin. Adjust paths and URLs to match your project structure.

| # | Testing Pattern | Demo Prompt | What it Exercises |
|---|-----------------|-------------|-------------------|
| 1 | Static HTML | "Use the webapp-testing skill to test the contact form in `website/index.html`. Fill in all fields and verify the submission shows a success message." | File:// URL testing, form interactions |
| 2 | PHP Login | "Use the webapp-testing skill with with_server.py to start my PHP app on port 8000 and test the login form at `/login.php`. Use credentials admin/password123." | PHP server management, authentication testing |
| 3 | React SPA | "Use the webapp-testing skill to test my React app. Start npm run dev on port 5173 and verify all navigation buttons work correctly." | SPA testing with networkidle wait |
| 4 | Element Discovery | "Use the webapp-testing skill to discover all buttons, links, and input fields on my app running at localhost:3000. Provide a detailed inventory." | DOM inspection and reconnaissance |
| 5 | Console Logging | "Use the webapp-testing skill to run my app and capture all console logs, especially any errors. Save them to a file for debugging." | Browser console monitoring |
| 6 | Full-Stack Test | "Use the webapp-testing skill with multiple servers: start my FastAPI backend on port 8000 and Vue frontend on port 5173, then test the user registration flow." | Multi-server orchestration |
| 7 | WordPress Admin | "Use the webapp-testing skill to test my local WordPress installation. Login to wp-admin and verify the dashboard loads without errors." | WordPress-specific testing |
| 8 | Laravel Auth | "Use the webapp-testing skill to start my Laravel app with artisan serve and test the entire authentication flow from login to profile page." | Laravel testing patterns |
| 9 | Form Validation | "Use the webapp-testing skill to test form validation on my PHP contact form. Try invalid inputs first, then valid ones, and verify error messages appear correctly." | Validation testing workflow |
| 10 | Screenshot Comparison | "Use the webapp-testing skill to take full-page screenshots of my app at different screen sizes (mobile, tablet, desktop) for visual regression testing." | Responsive design testing |

**Tip**: After each run, ask Claude to describe the steps it took and show you the test script it created. This helps you understand the testing patterns and customize them for your needs.

---

## Common Patterns and Best Practices

### Pattern 1: Reconnaissance-Then-Action
Always inspect before acting on dynamic applications:

```python
# Step 1: Inspect
page.goto('http://localhost:3000')
page.wait_for_load_state('networkidle')
page.screenshot(path='/tmp/inspect.png', full_page=True)

# Step 2: Discover selectors
buttons = page.locator('button').all()
for btn in buttons:
    print(btn.inner_text())

# Step 3: Act with discovered selectors
page.click('button:has-text("Submit")')
```

### Pattern 2: Server Lifecycle Management
Always use `with_server.py` for automatic server management:

```bash
# Good: Automatic cleanup
python scripts/with_server.py \
  --server "npm run dev" \
  --port 5173 \
  -- python test.py

# Avoid: Manual server management (can leave orphan processes)
npm run dev &
python test.py
```

### Pattern 3: Wait Strategies
Use appropriate waits for different scenarios:

```python
# For SPAs: Wait for network idle
page.wait_for_load_state('networkidle')

# For specific elements
page.wait_for_selector('.data-loaded')

# For URL changes
page.wait_for_url('**/dashboard')

# For timeouts (use sparingly)
page.wait_for_timeout(1000)
```

### Pattern 4: Error Handling
Always include proper error handling:

```python
from playwright.sync_api import sync_playwright

try:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        page.goto('http://localhost:3000')
        page.wait_for_load_state('networkidle')
        
        # Your test logic here
        
        browser.close()
except Exception as e:
    print(f"Test failed: {e}")
    raise
```

---

## Troubleshooting

### Issue 1: "Browser executable not found"
**Solution**: Install Chromium browser:
```bash
playwright install chromium
```

### Issue 2: "Page didn't load in time"
**Solution**: Increase timeout or check if server is running:
```python
page.goto('http://localhost:3000', timeout=60000)  # 60 seconds
```

### Issue 3: "Element not found"
**Solution**: Use reconnaissance first:
```python
# See what's actually on the page
page.screenshot(path='/tmp/debug.png', full_page=True)
content = page.content()
print(content)
```

### Issue 4: "Server port already in use"
**Solution**: Kill existing process or use different port:
```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9

# Or use a different port
python scripts/with_server.py --server "..." --port 8001 -- ...
```

### Issue 5: "JavaScript not executing"
**Solution**: Always wait for networkidle on SPAs:
```python
page.goto('http://localhost:3000')
page.wait_for_load_state('networkidle')  # Critical!
```

---

## Advanced Usage

### Testing with Authentication Tokens
```python
# Set cookies/localStorage before testing
page.goto('http://localhost:3000')
page.evaluate("""
    localStorage.setItem('auth_token', 'your-token-here');
""")
page.reload()
```

### Testing API Responses
```python
# Intercept network requests
page.on("response", lambda response: 
    print(f"Response: {response.url} - {response.status}")
)

page.goto('http://localhost:3000')
```

### Mobile Testing
```python
# Emulate mobile device
iphone_13 = p.devices['iPhone 13']
browser = p.chromium.launch(headless=True)
page = browser.new_page(**iphone_13)
```

### Performance Monitoring
```python
# Measure page load time
import time
start = time.time()
page.goto('http://localhost:3000')
page.wait_for_load_state('networkidle')
load_time = time.time() - start
print(f"Page loaded in {load_time:.2f} seconds")
```

---

## Integration with Claude Code Workflows

### Workflow 1: Test-Driven Development
1. Ask Claude to create a test script for your feature
2. Run the test (it should fail initially)
3. Implement the feature
4. Run the test again to verify

### Workflow 2: Regression Testing
1. Ask Claude to create comprehensive test scripts
2. Run tests before making changes
3. Make your changes
4. Run tests again to catch regressions

### Workflow 3: Documentation Generation
1. Ask Claude to test your application
2. Request it generates documentation based on discovered elements
3. Keep documentation updated as features change

---

## Resources

- **SKILL.md** - Complete skill reference and decision tree
- **examples/** - Working examples for common patterns
- **scripts/with_server.py** - Server lifecycle management helper
- **WEBAPP_TESTING_VS_CHROME_DEVTOOLS_MCP.md** - Comparison with alternative approaches

---

## Getting Help

If you encounter issues:
1. Run `python scripts/with_server.py --help` to see usage
2. Check the examples directory for similar patterns
3. Use the reconnaissance pattern to inspect the actual page state
4. Ask Claude to explain the test script it generated

Remember: The webapp-testing skill is designed to be used as a black box. Start with `--help` on scripts before reading source code to keep your context window clean.
