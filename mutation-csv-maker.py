import json
import csv
import re
import datetime
from dateutil import parser

def extract_log_data(log_entry):
    """Extract relevant data from a log entry"""
    try:
        # Parse the log entry if it's a string
        if isinstance(log_entry, str):
            log_data = json.loads(log_entry)
        else:
            log_data = log_entry
        
        # Extract timestamp information
        add_timestamp = None
        if "timestamp" in log_data:
            add_timestamp = parser.parse(log_data["timestamp"])
        
        chg_timestamp = None
        if "@timestamp" in log_data:
            chg_timestamp = parser.parse(log_data["@timestamp"])
        
        # Extract the input object JSON string using regex
        message = log_data.get("message", "")
        match = re.search(r'updatePhoneNumberConsents input object: (\{.*\})', message)
        if not match:
            return None
        
        input_json_str = match.group(1)
        input_object = json.loads(input_json_str)
        
        # Construct the request body in the desired format
        request_body = {
            "query": "mutation UpdatePhoneNumberConsents($input: ConsumerCommunicationsUpdatePhoneNumberConsentsInput!) {systems {capabilities {consumerCommunications {updatePhoneNumberConsents(input: $input) {successOrFailure message error {code message}}}}}}",
            "variables": {
                "input": input_object
            }
        }
        
        # Static response body
        response_body = {
            "program": "LSEPCONSSP",
            "service": "postPreferenceData",
            "error": "Unresolved custom parameters found in header."
        }
        
        return {
            "UNIQUE_TRACKING_CODE": "",
            "REQUEST_BODY": json.dumps(request_body),
            "RESPONSE_BODY": json.dumps(response_body),
            "ADD_TIMESTAMP": add_timestamp.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3] if add_timestamp else "",
            "CHG_TIMESTAMP": chg_timestamp.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3] if chg_timestamp else ""
        }
    except Exception as e:
        print(f"Error processing log entry: {str(e)}")
        return None

def process_logs_to_csv(input_file, output_file):
    """Process logs from input file and write to CSV"""
    try:
        # Read the input file
        with open(input_file, 'r') as f:
            logs_data = json.load(f)
        
        # Process each log entry
        processed_data = []
        for log in logs_data:
            result = extract_log_data(log)
            if result:
                processed_data.append(result)
        
        # Write to CSV
        with open(output_file, 'w', newline='') as csvfile:
            fieldnames = ['UNIQUE_TRACKING_CODE', 'REQUEST_BODY', 'RESPONSE_BODY', 'ADD_TIMESTAMP', 'CHG_TIMESTAMP']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for row in processed_data:
                writer.writerow(row)
        
        print(f"Successfully processed {len(processed_data)} log entries to {output_file}")
    except Exception as e:
        print(f"Error processing logs to CSV: {str(e)}")

def process_single_log_entry(log_entry):
    """Process a single log entry for demonstration"""
    result = extract_log_data(log_entry)
    if result:
        print(json.dumps(result, indent=2))
    else:
        print("Failed to process log entry")

# If you have a raw log entry to test with
sample_log = """
{
  "@timestamp": "2025-04-30T17:31:10.948Z",
  "@message": {"level":"DEBUG","message":"updatePhoneNumberConsents input object: {\\\"phoneNumber\\\":\\\"8125847848\\\",\\\"phoneType\\\":\\\"CELL\\\",\\\"consents\\\":[{\\\"businessFunction\\\":\\\"PROMOTIONAL\\\",\\\"channels\\\":[{\\\"communicationsChannel\\\":\\\"DIALER\\\",\\\"hasConsented\\\":false,\\\"updatedAt\\\":\\\"2025-04-30T12:31:10-05:00\\\"},{\\\"communicationsChannel\\\":\\\"SMS\\\",\\\"hasConsented\\\":false,\\\"updatedAt\\\":\\\"2025-04-30T12:31:10-05:00\\\"}],\\\"hasConsented\\\":false},{\\\"businessFunction\\\":\\\"SERVICING\\\",\\\"channels\\\":[{\\\"communicationsChannel\\\":\\\"DIALER\\\",\\\"hasConsented\\\":true,\\\"updatedAt\\\":\\\"2025-04-30T12:31:10-05:00\\\"},{\\\"communicationsChannel\\\":\\\"SMS\\\",\\\"hasConsented\\\":true,\\\"updatedAt\\\":\\\"2025-04-30T12:31:10-05:00\\\"}],\\\"hasConsented\\\":true}],\\\"metadata\\\":{\\\"sourceChannel\\\":\\\"WEB\\\",\\\"ipAddress\\\":\\\"127.0.0.1\\\",\\\"customerName\\\":\\\"AMANDA COOLEY\\\",\\\"appId\\\":\\\"367040268\\\"},\\\"updatedAt\\\":\\\"2025-04-30T12:31:10-05:00\\\"}","metadata":{"_interactionId":"y65pxe8qz3prydp5w72ajhgx","_serverName":"consumer-communication-subgraph","_userId":null},"timestamp":"2025-04-30T17:31:10.947Z"}
}
"""

# Function to handle CloudWatch Logs Insights export format
def process_cloudwatch_insights_export(input_file, output_file):
    """Process CloudWatch Logs Insights export file and write to CSV"""
    try:
        # Read the input file - adjust based on your export format
        with open(input_file, 'r') as f:
            # For JSON export
            logs_data = json.load(f)
        
        # Process each log entry
        processed_data = []
        for log in logs_data:
            # CloudWatch Logs Insights export might have a different structure
            # Adjust this based on your actual export format
            message = log.get("@message", log)
            
            # If @message is a string that contains a JSON object
            if isinstance(message, str) and message.startswith("{"):
                try:
                    message = json.loads(message)
                except:
                    pass
            
            # Create a combined log entry with both timestamp fields
            combined_log = {
                "@timestamp": log.get("@timestamp"),
                "timestamp": message.get("timestamp") if isinstance(message, dict) else None,
                "message": message.get("message") if isinstance(message, dict) else message
            }
            
            result = extract_log_data(combined_log)
            if result:
                processed_data.append(result)
        
        # Write to CSV
        with open(output_file, 'w', newline='') as csvfile:
            fieldnames = ['UNIQUE_TRACKING_CODE', 'REQUEST_BODY', 'RESPONSE_BODY', 'ADD_TIMESTAMP', 'CHG_TIMESTAMP']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for row in processed_data:
                writer.writerow(row)
        
        print(f"Successfully processed {len(processed_data)} log entries to {output_file}")
    except Exception as e:
        print(f"Error processing CloudWatch Insights export to CSV: {str(e)}")

if __name__ == "__main__":
    # Example usage:
    # For testing with a single log entry
    # process_single_log_entry(json.loads(sample_log))
    
    # For processing a file of logs
    # process_logs_to_csv("input_logs.json", "output.csv")
    
    # For processing CloudWatch Logs Insights export
    process_cloudwatch_insights_export("logs-insights-results.json", "Failed_Mutations.csv")