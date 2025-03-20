def pre_research_prompt():
    return """<goal>
- First, scan the entire API documentation
- Identify both nested and general identity-related endpoints before deciding the most relevant path
- Be aware of nested resources and do not include them unless they are tenant or organization related
- Find API endpoints for relevant resources and be precise and explicit regarding URLs for API endpoints
- Include explicit URLs for API endpoints in the output.
</goal>

<relevant-identity-resources>
- Users
- Groups (teams/user groups/organizations/etc.)
- Roles (permissions/entitlements/policies)
</relevant-identity-resources>

<examples>
    <1> 
    - we look through documentation and find /assets/user-groups/ as well as /groups endpoints
    - we decide to include only the /groups endpoint
    </1>
</examples>

<output-format>
- <endpoint-name>
- <endpoint-description>
- <endpoint-url>
- <endpoint-method>
- <endpoint-parameters>
- <endpoint-response>
</output-format>
"""
