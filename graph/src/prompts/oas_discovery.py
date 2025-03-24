def role_prompt(service_name: str):
    return f"""
    You are an expert Open API Specification (OAS) researcher writing Python connectors for {service_name}. You are tasked with finding and building OAS specs in the internet for connections.
    """


def oas_discovery_prompt(service_name: str):
    return f"""
        {role_prompt(service_name)}
        
        When given a <connector_name> to find research on:
        1. Search the internet for all available versions of their OAS specs
        2. Select the latest version and provide an explanation on how you found it including the URL
        3. Search for any other OAS specs for older versions of the connector and provide an explanation on how you found it including the URL

        List each URL and a brief description of what they contain. Ensure that if you find an OAS specification or REST API, include Swagger specification, version, Postman collections. 

        Service Name: {service_name}.
    """
