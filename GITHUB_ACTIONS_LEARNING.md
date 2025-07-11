# 🚀 GitHub Actions for iOS QA Automation

## 📚 **What You'll Learn**

By the end of this guide, you'll be able to:
- ✅ Create GitHub Actions workflows 
- ✅ Write YAML configuration files
- ✅ Set up self-hosted runners for macOS
- ✅ Automate iOS testing with Appium
- ✅ Use marketplace actions
- ✅ Handle secrets and artifacts
- ✅ Optimize workflow performance

---

## 🎯 **1. GitHub Actions Basics**

### **What are GitHub Actions?**
GitHub Actions is a CI/CD platform that lets you automate workflows directly in your GitHub repository.

**Key Concepts:**
- **Workflow** = A automated process (like running tests)
- **Job** = A set of steps that run on the same runner
- **Step** = Individual task (like running a command)
- **Action** = Reusable unit of code
- **Runner** = Server that runs your workflows

### **How it Works:**
```
Code Push → Trigger → Runner → Execute Steps → Results
```

### **Why Use GitHub Actions for iOS Testing?**
- ✅ **Automatic testing** on every code change
- ✅ **Parallel execution** of multiple test suites
- ✅ **Integration** with GitHub pull requests
- ✅ **Artifact storage** for test results and screenshots
- ✅ **Notifications** when tests fail

---

## 📝 **2. YAML Syntax Essentials**

YAML (Yet Another Markup Language) is used for GitHub Actions configuration.

### **Basic YAML Rules:**
```yaml
# Comments start with #
key: value                    # String value
number: 42                   # Number value
boolean: true                # Boolean value
null_value: null             # Null value

# Lists (arrays)
fruits:
  - apple
  - banana
  - orange

# Objects (dictionaries)
person:
  name: John
  age: 30
  city: New York

# Inline lists and objects
colors: [red, green, blue]
point: {x: 10, y: 20}
```

### **YAML for GitHub Actions:**
```yaml
name: My Workflow              # Workflow name
on: [push, pull_request]      # Triggers

jobs:                         # Jobs section
  test:                       # Job name
    runs-on: ubuntu-latest    # Runner type
    steps:                    # Steps list
      - name: Checkout code   # Step name
        uses: actions/checkout@v4  # Action to use
      - name: Run tests       # Another step
        run: npm test         # Command to run
```

### **Common YAML Mistakes:**
```yaml
# ❌ Wrong indentation
jobs:
test:  # Should be indented
  runs-on: ubuntu-latest

# ✅ Correct indentation  
jobs:
  test:  # Properly indented
    runs-on: ubuntu-latest

# ❌ Missing quotes for special characters
name: My App: Tests  # Colon needs quotes

# ✅ Proper quoting
name: "My App: Tests"
```

---

## 🔧 **3. Creating Your First Workflow**

### **Workflow File Structure:**
```
your-repo/
├── .github/
│   └── workflows/
│       └── ios-tests.yml    # Your workflow file
├── src/
└── tests/
```

### **Basic Workflow Example:**
```yaml
name: iOS Tests

# When to run this workflow
on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

# Jobs to run
jobs:
  test:
    runs-on: macos-latest
    
    steps:
    - name: Checkout repository
      uses: actions/checkout@v4
      
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
        
    - name: Install dependencies
      run: |
        pip install poetry
        poetry install
        
    - name: Run tests
      run: poetry run pytest tests/
```

### **Workflow Triggers:**
```yaml
# Single event
on: push

# Multiple events
on: [push, pull_request]

# Scheduled (cron syntax)
on:
  schedule:
    - cron: '0 2 * * *'  # Daily at 2 AM

# Manual trigger
on:
  workflow_dispatch:
    inputs:
      test_type:
        description: 'Type of test to run'
        required: true
        default: 'smoke'
```

---

## 🏪 **4. GitHub Actions Marketplace**

### **Popular Actions for iOS Testing:**
```yaml
# Checkout code
- uses: actions/checkout@v4

# Setup Node.js (for Appium)
- uses: actions/setup-node@v4
  with:
    node-version: '18'

# Setup Python
- uses: actions/setup-python@v4
  with:
    python-version: '3.11'

# Cache dependencies
- uses: actions/cache@v3
  with:
    path: ~/.cache/pip
    key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}

# Upload artifacts
- uses: actions/upload-artifact@v3
  with:
    name: test-results
    path: test-results/
```

### **Finding Actions:**
- 🔍 **GitHub Marketplace**: https://github.com/marketplace?type=actions
- 🔍 **Search by category**: CI, Testing, Mobile, etc.
- 🔍 **Check ratings and usage**: Popular actions are usually better maintained

---

## 🖥️ **5. Self-Hosted Runners for macOS**

### **Why Self-Hosted for iOS?**
- ❌ **GitHub-hosted runners** don't have iOS devices
- ❌ **GitHub-hosted runners** can't run iOS simulators reliably
- ✅ **Self-hosted runners** can connect to real iOS devices
- ✅ **Self-hosted runners** give you full control

### **Setting Up Self-Hosted Runner:**

**Step 1: Go to Repository Settings**
```
Your Repo → Settings → Actions → Runners → New self-hosted runner
```

**Step 2: Choose macOS**
```bash
# Download
mkdir actions-runner && cd actions-runner
curl -o actions-runner-osx-x64-2.311.0.tar.gz -L https://github.com/actions/runner/releases/download/v2.311.0/actions-runner-osx-x64-2.311.0.tar.gz
tar xzf ./actions-runner-osx-x64-2.311.0.tar.gz

# Configure
./config.sh --url https://github.com/YOUR_USERNAME/YOUR_REPO --token YOUR_TOKEN

# Run
./run.sh
```

**Step 3: Install as Service (Optional)**
```bash
# Install
sudo ./svc.sh install

# Start
sudo ./svc.sh start

# Check status
sudo ./svc.sh status
```

### **Self-Hosted Runner Configuration:**
```yaml
jobs:
  ios-test:
    runs-on: self-hosted  # Use your macOS runner
    
    steps:
    - name: Check iOS devices
      run: idevice_id -l
      
    - name: Start Appium
      run: |
        appium &
        sleep 5
        
    - name: Run iOS tests
      run: poetry run python test_ios_real_device.py
```

---

## 📱 **6. iOS Testing Workflow**

### **Complete iOS Testing Workflow:**
```yaml
name: iOS Real Device Tests

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]
  workflow_dispatch:  # Manual trigger

jobs:
  ios-tests:
    runs-on: self-hosted
    timeout-minutes: 30
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v4
      
    - name: Check iOS device connection
      run: |
        if ! idevice_id -l; then
          echo "❌ No iOS device connected"
          exit 1
        fi
        echo "✅ iOS device connected"
        
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
        
    - name: Cache Poetry dependencies
      uses: actions/cache@v3
      with:
        path: ~/.cache/pypoetry
        key: ${{ runner.os }}-poetry-${{ hashFiles('**/poetry.lock') }}
        
    - name: Install Poetry
      run: |
        curl -sSL https://install.python-poetry.org | python3 -
        echo "$HOME/.local/bin" >> $GITHUB_PATH
        
    - name: Install dependencies
      run: poetry install
      
    - name: Start Appium server
      run: |
        pkill -f appium || true
        appium --log appium.log --log-level debug &
        sleep 5
        
    - name: Run iOS tests
      run: |
        poetry run python test_ios_real_device.py
        
    - name: Upload test results
      uses: actions/upload-artifact@v3
      if: always()
      with:
        name: test-results
        path: |
          *.png
          appium.log
          
    - name: Stop Appium server
      if: always()
      run: pkill -f appium || true
```

---

## 🔐 **7. Advanced Features**

### **Using Secrets:**
```yaml
# In workflow file
- name: Deploy to TestFlight
  env:
    APPLE_ID: ${{ secrets.APPLE_ID }}
    APP_PASSWORD: ${{ secrets.APP_PASSWORD }}
  run: |
    # Use secrets for sensitive data
```

### **Matrix Builds:**
```yaml
strategy:
  matrix:
    ios-version: [16.0, 17.0, 17.2]
    device: [iPhone-SE, iPhone-14, iPhone-15]
    
steps:
- name: Test on ${{ matrix.device }} iOS ${{ matrix.ios-version }}
  run: |
    # Run tests for each combination
```

### **Conditional Steps:**
```yaml
- name: Run only on main branch
  if: github.ref == 'refs/heads/main'
  run: echo "This runs only on main"
  
- name: Run on pull requests
  if: github.event_name == 'pull_request'
  run: echo "This runs only on PRs"
```

### **Artifacts and Reports:**
```yaml
- name: Generate test report
  run: |
    poetry run pytest --html=report.html --self-contained-html
    
- name: Upload HTML report
  uses: actions/upload-artifact@v3
  with:
    name: html-report
    path: report.html
```

---

## 🚀 **8. Performance Optimization**

### **Caching Strategies:**
```yaml
# Cache Python dependencies
- uses: actions/cache@v3
  with:
    path: ~/.cache/pip
    key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}

# Cache Node.js dependencies (for Appium)
- uses: actions/cache@v3
  with:
    path: ~/.npm
    key: ${{ runner.os }}-node-${{ hashFiles('**/package-lock.json') }}
```

### **Parallel Jobs:**
```yaml
jobs:
  unit-tests:
    runs-on: ubuntu-latest
    steps:
    - name: Run unit tests
      run: pytest tests/unit/
      
  integration-tests:
    runs-on: self-hosted
    steps:
    - name: Run integration tests
      run: pytest tests/integration/
      
  ui-tests:
    runs-on: self-hosted
    needs: [unit-tests]  # Wait for unit tests
    steps:
    - name: Run UI tests
      run: python test_ios_real_device.py
```

---

## 🎯 **Next Steps**

1. **Start Simple**: Create a basic workflow that just runs `echo "Hello World"`
2. **Add iOS Testing**: Integrate your existing Appium tests
3. **Set Up Runner**: Install self-hosted runner on your macOS
4. **Add Notifications**: Get notified when tests fail
5. **Optimize**: Add caching, parallel jobs, and better reporting

---

## 📖 **Additional Resources**

- 📚 **GitHub Actions Documentation**: https://docs.github.com/en/actions
- 📚 **YAML Syntax Guide**: https://yaml.org/spec/1.2/spec.html
- 📚 **Actions Marketplace**: https://github.com/marketplace?type=actions
- 📚 **Self-hosted Runners**: https://docs.github.com/en/actions/hosting-your-own-runners

Ready to start building your first workflow? 🚀 