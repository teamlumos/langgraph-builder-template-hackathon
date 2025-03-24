def dev_req_research_prompt():
    PROMPT = """<goals>
- Identify authentication methods 
- Identify pagination structure and parameters
</goals>

<output-format>
## Authentication

...fill in

- **Scope Requirements**
...fill in

| Tenant ID |  Details (How is the tenant ID identified) |
| --- | --- |
| ...fill in | ...fill in |


## Pagination

...fill in

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

## OpenAPI Specification (OAS) URL

...fill in

</output-format>
  """

    return PROMPT
