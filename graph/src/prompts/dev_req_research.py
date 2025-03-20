def dev_req_research_prompt(service_name: str, context: str, open_api_spec: str):
    PROMPT = f"""<goals>
- Understand the context: what is the account, what are the resources, what are the entitlements, what are the relationships between them.
- Follow the context to research the API endpoints.
- Identify authentication methods and implementation details.
- Analyze pagination structure and parameters.
- Locate OpenAPI Specification (OAS) references or documentation links.
- Provide the OpenAPI Specification (OAS) URL in the output.
- Follow the output-format to generate the output.
</goals>

<domain-context>
{open_api_spec}
</domain-context>

<context>
{context}
</context>

<output-format>
## Authentication

...fill in

- **Scope Requirements**
...fill in

| Tenant ID |  Details (How is the tenant ID identified) |
| --- | --- |
| ...fill in | ...fill in |


## API Endpoints

...fill in

**Milestone 1: Read Capabilities** 

## List user accounts, resources, and entitlements

...fill in

**Milestone 2: Write Capabilities** 

### Deprovisioning

...fill in

### Provisioning

...fill in

### OpenAPI Specification (OAS) URL

...fill in

</output-format>
  """

    return PROMPT