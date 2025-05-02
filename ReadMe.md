# Failed Mutations Processing Tool

## Overview

This tool is designed to process failed GraphQL mutations from the OneMainFinancial consumer communications system logs. Specifically, it focuses on the `updatePhoneNumberConsents` mutations that have failed with the error "Unresolved custom parameters found in header."

## Purpose

The main purpose of this tool is to:
1. Process extract failed GraphQL mutation data from CloudWatch Log Insights JSON exports
2. Transform this data into a structured CSV format for analysis
3. Enable easier debugging and troubleshooting of failed consent update operations

## Files in this Project

- **logs-insights-results.json**: Raw CloudWatch Logs Insights export containing log entries of failed mutations
- **Failed_Mutations.csv**: Generated CSV file containing structured data extracted from the logs
- **mutation-csv-maker.py**: Python script that processes the logs and generates the CSV file

## How It Works

The `mutation-csv-maker.py` script:

1. Reads the CloudWatch Logs Insights export (`logs-insights-results.json` manually exported from CloudWatch)
2. Parses each log entry looking for `updatePhoneNumberConsents` operations
3. Extracts the following information:
   - The original GraphQL mutation and variables
   - The error response
   - Timestamps
4. Generates a CSV file with columns:
   - UNIQUE_TRACKING_CODE
   - REQUEST_BODY (contains the GraphQL mutation and input variables)
   - RESPONSE_BODY (contains the error details)
   - ADD_TIMESTAMP
   - CHG_TIMESTAMP

## How to Use

### Prerequisites

- Python 3.x
- Required Python libraries: 
  - json
  - csv
  - re
  - datetime
  - dateutil

### Running the Script

```bash
# Navigate to the project directory
cd /path/to/Failed-Mutations

# Run the script
python mutation-csv-maker.py
```

By default, the script will:
1. Read from `logs-insights-results.json`
2. Generate `Failed_Mutations.csv`

### Customizing the Process

You can modify the script to use different input/output files by changing the parameters in the function call at the bottom of the script:

```python
process_cloudwatch_insights_export("your-input-file.json", "your-output-file.csv")
```

## Error Pattern

The failed mutations being tracked have the following characteristics:

- GraphQL operation: `updatePhoneNumberConsents`
- Error message: "Unresolved custom parameters found in header"
- Service: "postPreferenceData"
- Program: "LSEPCONSSP"

## Data Structure

### Input Logs Structure

The logs contain entries with `updatePhoneNumberConsents` input objects including:
- Phone number and type
- Consent settings for different business functions (PROMOTIONAL, SERVICING)
- Communication channels (DIALER, SMS)
- Metadata (source channel, customer name, etc.)

### Output CSV Structure

The generated CSV contains:
- UNIQUE_TRACKING_CODE: An empty placeholder column for tracking
- REQUEST_BODY: JSON string containing the GraphQL mutation and input variables
- RESPONSE_BODY: JSON string containing the error details
- ADD_TIMESTAMP: Timestamp from the log entry's "timestamp" field
- CHG_TIMESTAMP: Timestamp from the log entry's "@timestamp" field

## Additional Notes

This tool is designed specifically for the consumer communications subgraph in the OneMainFinancial system to help diagnose issues with the updatePhoneNumberConsents mutation. The error "Unresolved custom parameters found in header" suggests there might be an issue with the headers or parameters being sent to the underlying service.