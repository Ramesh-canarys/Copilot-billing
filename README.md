# GitHub Custom Action for Copilot Billing

This project provides a GitHub custom action that retrieves billing seat information from the GitHub API, calculates billing based on active days, and writes the results to a CSV file.

## Project Structure

```
github-custom-action
├── .github
│   └── workflows
│       └── action.yml
├── src
│   └── main.py
├── Dockerfile
├── requirements.txt
└── README.md
```

## Files Overview

- **src/main.py**: Contains the main script for the custom action, including functions to interact with the GitHub API and process billing information.
- **.github/workflows/action.yml**: Defines the GitHub Actions workflow for the custom action, specifying inputs, outputs, and the entry point.
- **Dockerfile**: Used to create a Docker image for the custom action, installing required dependencies.
- **requirements.txt**: Lists the Python dependencies required for the project.

## Usage

1. **Setup**: Ensure you have the necessary permissions and tokens to access the GitHub API.
2. **Configure**: Update the `ENTERPRISE_SLUG` and `AUTH_TOKEN` in `src/main.py` with your enterprise slug and authentication token.
3. **Deploy**: Use the GitHub Actions workflow defined in `.github/workflows/action.yml` to deploy the custom action.

## Functions

- **get_copilot_billing_seats**: Retrieves billing seat information from the GitHub API.
- **calculate_daily_rate**: Calculates the daily rate based on the current month.
- **calculate_billing**: Calculates the billing for each seat based on active days.
- **write_to_csv**: Writes the billing information to a CSV file.

## Requirements

- Python 3.x
- Dependencies listed in `requirements.txt`:
  - requests==2.32.0
  - python-csv==0.0.13
  - urllib3==1.26.15
  - python-dateutil==2.9.0

## License

This project is licensed under the MIT License. See the LICENSE file for details.