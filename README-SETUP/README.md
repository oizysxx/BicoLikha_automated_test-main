# BicoLikha Automated Testing Setup

## Prerequisites

Ensure you have Mozilla Firefox installed.

## Setup Instructions

1. Start Apache and MySQL in your XAMPP Control Panel.

2. Ensure your BicoLikha Django server is running locally by running:

```bash
python manage.py runserver
```

inside:

```text
C:\Users\Justin\BicoLikha_adet
```

3. Run the following command in the terminal within this test folder:

```bash
python -m pip install pytest selenium webdriver-manager
```

## Run Test Files

Run the following commands to check all test files:

```bash
py error_handling_test.py
py test_add_record.py
py test_helper.py
py test_login.py
py test_search.py
py test_validation.py
py test_order_cod.py
```
