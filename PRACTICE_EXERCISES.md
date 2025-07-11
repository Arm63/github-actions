# 🏋️ GitHub Actions Practice Exercises

## 🎯 **Exercise 1: Basic Workflow Creation**

**Task**: Create a workflow that runs on every push and prints system information.

**Requirements**:
- Name the workflow "System Info"
- Trigger on push to any branch
- Run on Ubuntu
- Print OS, date, and current user

**Your turn**: Create `.github/workflows/system-info.yml`

<details>
<summary>💡 Hint</summary>

```yaml
name: System Info
on: push
jobs:
  info:
    runs-on: ubuntu-latest
    steps:
    - name: Print system info
      run: |
        echo "OS: $(uname -s)"
        echo "Date: $(date)"
        echo "User: $(whoami)"
```
</details>

---

## 🎯 **Exercise 2: Multi-Job Workflow**

**Task**: Create a workflow with 2 jobs that run in sequence.

**Requirements**:
- Job 1: "prepare" - runs on Ubuntu, prints "Preparing..."
- Job 2: "execute" - runs on Ubuntu, depends on "prepare", prints "Executing..."
- Both jobs should checkout code

**Your turn**: Create `.github/workflows/multi-job.yml`

<details>
<summary>💡 Hint</summary>

```yaml
name: Multi Job Example
on: workflow_dispatch
jobs:
  prepare:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    - run: echo "Preparing..."
  
  execute:
    runs-on: ubuntu-latest
    needs: prepare
    steps:
    - uses: actions/checkout@v4
    - run: echo "Executing..."
```
</details>

---

## 🎯 **Exercise 3: Matrix Strategy**

**Task**: Create a workflow that tests multiple Python versions.

**Requirements**:
- Test Python versions: 3.9, 3.10, 3.11
- Run on Ubuntu
- Install Poetry and dependencies
- Print Python version

**Your turn**: Create `.github/workflows/matrix-test.yml`

<details>
<summary>💡 Hint</summary>

```yaml
name: Matrix Test
on: workflow_dispatch
jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.9, 3.10, 3.11]
    steps:
    - uses: actions/checkout@v4
    - uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    - run: python --version
```
</details>

---

## 🎯 **Exercise 4: Conditional Execution**

**Task**: Create a workflow with conditional steps.

**Requirements**:
- Run on push and pull_request
- Step 1: Always runs, prints "Starting..."
- Step 2: Only runs on main branch, prints "Main branch detected"
- Step 3: Only runs on pull requests, prints "Pull request detected"

**Your turn**: Create `.github/workflows/conditional.yml`

<details>
<summary>💡 Hint</summary>

```yaml
name: Conditional Steps
on: [push, pull_request]
jobs:
  conditional:
    runs-on: ubuntu-latest
    steps:
    - run: echo "Starting..."
    - if: github.ref == 'refs/heads/main'
      run: echo "Main branch detected"
    - if: github.event_name == 'pull_request'
      run: echo "Pull request detected"
```
</details>

---

## 🎯 **Exercise 5: Using Marketplace Actions**

**Task**: Create a workflow that uses popular marketplace actions.

**Requirements**:
- Checkout code
- Setup Node.js version 18
- Cache node_modules
- Run `npm --version`

**Your turn**: Create `.github/workflows/marketplace.yml`

<details>
<summary>💡 Hint</summary>

```yaml
name: Marketplace Actions
on: workflow_dispatch
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    - uses: actions/setup-node@v4
      with:
        node-version: '18'
    - uses: actions/cache@v3
      with:
        path: ~/.npm
        key: ${{ runner.os }}-node-${{ hashFiles('**/package-lock.json') }}
    - run: npm --version
```
</details>

---

## 🎯 **Exercise 6: Artifacts and Outputs**

**Task**: Create a workflow that generates and uploads artifacts.

**Requirements**:
- Create a text file with current date
- Upload the file as an artifact
- Name the artifact "date-file"

**Your turn**: Create `.github/workflows/artifacts.yml`

<details>
<summary>💡 Hint</summary>

```yaml
name: Artifacts Example
on: workflow_dispatch
jobs:
  create-artifact:
    runs-on: ubuntu-latest
    steps:
    - run: echo "Current date: $(date)" > date.txt
    - uses: actions/upload-artifact@v4
  with:
    name: date-file
    path: date.txt
```
</details>

---

## 🎯 **Exercise 7: Environment Variables**

**Task**: Create a workflow that uses environment variables.

**Requirements**:
- Set global env var: `APP_NAME=MyApp`
- Set job-level env var: `JOB_NAME=test-job`
- Set step-level env var: `STEP_NAME=print-info`
- Print all three variables

**Your turn**: Create `.github/workflows/env-vars.yml`

<details>
<summary>💡 Hint</summary>

```yaml
name: Environment Variables
on: workflow_dispatch
env:
  APP_NAME: MyApp
jobs:
  test:
    runs-on: ubuntu-latest
    env:
      JOB_NAME: test-job
    steps:
    - env:
        STEP_NAME: print-info
      run: |
        echo "App: $APP_NAME"
        echo "Job: $JOB_NAME"
        echo "Step: $STEP_NAME"
```
</details>

---

## 🎯 **Exercise 8: iOS Specific Workflow**

**Task**: Create a workflow for iOS testing (without real device).

**Requirements**:
- Run on macOS
- Check if Xcode is available
- Install Poetry
- Install your project dependencies
- Run a simple Python test

**Your turn**: Create `.github/workflows/ios-practice.yml`

<details>
<summary>💡 Hint</summary>

```yaml
name: iOS Practice
on: workflow_dispatch
jobs:
  ios-test:
    runs-on: macos-latest
    steps:
    - uses: actions/checkout@v4
    - run: xcode-select --version
    - uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    - run: |
        curl -sSL https://install.python-poetry.org | python3 -
        echo "$HOME/.local/bin" >> $GITHUB_PATH
    - run: poetry install
    - run: poetry run python -c "print('iOS workflow test passed!')"
```
</details>

---

## 🎯 **Exercise 9: Workflow with Inputs**

**Task**: Create a manually triggered workflow with inputs.

**Requirements**:
- Manual trigger only (`workflow_dispatch`)
- Input 1: `environment` (choice: dev, staging, prod)
- Input 2: `run_tests` (boolean, default: true)
- Input 3: `message` (string, default: "Hello World")
- Print all inputs

**Your turn**: Create `.github/workflows/inputs.yml`

<details>
<summary>💡 Hint</summary>

```yaml
name: Workflow with Inputs
on:
  workflow_dispatch:
    inputs:
      environment:
        type: choice
        options: [dev, staging, prod]
      run_tests:
        type: boolean
        default: true
      message:
        type: string
        default: "Hello World"
jobs:
  process:
    runs-on: ubuntu-latest
    steps:
    - run: |
        echo "Environment: ${{ github.event.inputs.environment }}"
        echo "Run tests: ${{ github.event.inputs.run_tests }}"
        echo "Message: ${{ github.event.inputs.message }}"
```
</details>

---

## 🎯 **Exercise 10: Complete iOS Testing Pipeline**

**Task**: Create a comprehensive iOS testing workflow.

**Requirements**:
- Run on macOS
- Multiple jobs: setup, test, report
- Use caching for dependencies
- Upload test results as artifacts
- Only run on main branch or manual trigger

**Your turn**: Create `.github/workflows/ios-pipeline.yml`

<details>
<summary>💡 Hint</summary>

```yaml
name: iOS Testing Pipeline
on:
  push:
    branches: [main]
  workflow_dispatch:

jobs:
  setup:
    runs-on: macos-latest
    steps:
    - uses: actions/checkout@v4
    - uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    - uses: actions/cache@v3
      with:
        path: ~/.cache/pypoetry
        key: ${{ runner.os }}-poetry-${{ hashFiles('**/poetry.lock') }}
    - run: |
        curl -sSL https://install.python-poetry.org | python3 -
        echo "$HOME/.local/bin" >> $GITHUB_PATH
    - run: poetry install

  test:
    runs-on: macos-latest
    needs: setup
    steps:
    - uses: actions/checkout@v4
    - uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    - run: |
        curl -sSL https://install.python-poetry.org | python3 -
        echo "$HOME/.local/bin" >> $GITHUB_PATH
    - run: poetry install
    - run: |
        echo "Test completed at $(date)" > test-results.txt
        echo "Status: PASSED" >> test-results.txt
         - uses: actions/upload-artifact@v4
       with:
         name: test-results
         path: test-results.txt
```
</details>

---

## 🏆 **Bonus Challenge: Self-Hosted Runner Setup**

**Task**: Set up a self-hosted runner on your macOS machine.

**Requirements**:
1. Go to your GitHub repository
2. Settings → Actions → Runners
3. Click "New self-hosted runner"
4. Follow the macOS setup instructions
5. Create a workflow that uses `runs-on: self-hosted`

**Benefits**:
- Can access your iOS devices
- Full control over the environment
- Faster builds (no queue time)

---

## 📝 **Practice Tips**

1. **Start Simple**: Begin with Exercise 1 and work your way up
2. **Test Often**: Use `workflow_dispatch` to test manually
3. **Read Logs**: Check the Actions tab for detailed logs
4. **Use Marketplace**: Explore actions at https://github.com/marketplace
5. **Validate YAML**: Use online YAML validators if syntax errors occur

## 🎯 **Next Steps After Exercises**

1. **Create a real iOS testing workflow** for your project
2. **Set up notifications** for failed tests
3. **Add secrets** for sensitive data
4. **Implement deployment** workflows
5. **Optimize performance** with caching and parallel jobs

Ready to start practicing? Pick an exercise and create your first workflow! 🚀 