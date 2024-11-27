system_prompt = """Analyze the content from the input log information.\n"""
user_prompt = """<Analysis rules>
- Classify and list all analyzed system exceptions, resource overloads and error information. The more listed, the better
- Resource overload includes nearly overload or insufficient resources. Resources include CPU, disk, memory and other resources.
- Error messages indicate error messages other than system exceptions and do not include resource overload.
- System exception indicates execution error
- Do not include other content or additional information
- Do not include duplicate messages
- Answer in Traditional Chinese
</Analysis rules>

<Output example>
    [System exception]
        1. Time, Log message
        2. ...
    [Error message]
        1. Time, Log message
        2. ...
    [resource overload]
        1. Time, Log message
        2. ...
</Example output>

Based on the "log_data" system log data, analyze the log messages expressing system exceptions, resource overloads and error information during the incident. The analysis follows the "Analysis Rules" and the analysis results are output according to the "Output Example"."""
