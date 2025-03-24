def oas_retrieval_prompt():
    return """
<goals>
- Discover OpenAPI Specification (OAS/Swagger) links or references
- Discover Postman Collection links or references
</goals>

<output-format>
## OpenAPI Specification (OAS/Swagger)

...fill in

## Postman Collection

...fill in

</output-format>
"""
