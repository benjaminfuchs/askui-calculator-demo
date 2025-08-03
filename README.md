# AskUI Test Automation Examples

This repository showcases the power of AskUI for automating user interfaces across a range of applications — from simple tools like calculators to complex industrial workflows such as FDT commissioning.

## Installation

1. Clone the repository.

2. Create a virtual environment:
```bash
python -m venv venv
```

3. Activate the virtual environment:
```bash
# Windows
.\venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Configure AskUI credentials:
Create a `.env` file in the project root:
```env
ASKUI_WORKSPACE_ID=your-workspace-id
ASKUI_TOKEN=your-token
```

⚠️ **Security Note**: Never commit the `.env` file to version control.

## Token Usage Analysis

### Calculator Tests

Each calculator test (Windows or Google) uses about 8 tokens. This includes:

- Clicking number buttons and operators
- Reading results via AI vision

### FDT Commissioning Tests

Each FDT commissioning test uses around 30 tokens. This covers:
- Navigating through the wizard
- Selecting parameters
- Checking start and end condition
