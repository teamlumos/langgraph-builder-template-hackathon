def initial(url:str, service_name: str):
    PROMPT = f"""
<goals>
You are an expert identity security manager for {service_name}.

I want to deeply understand how {service_name} works, and common use cases people use the {service_name} for.

I also want you to identify the differences between the product tiers, specifically how it relates to features provided, as well as API access differences.

Furthermore, identify any caveats or limitations this service has for listing users, groups, roles and resources.

In order to get the most accurate information, I want you to reference the most up-to-date documentation for {service_name}.

This information will be used to build a product requirements document, I want a complete overview of what is the service used for, what does the service do, what is the relevance and usage of identities and accounts (users, groups, roles, entitlements, access), and what limitations apply to {service_name}.

Focus solely on source URLs.
</goals>

<output-format>
## Resources & Entitlement Diagram + Details

### Account

| Account type |   |
| --- | --- |
| User |  |

### **Resource Types**

| Resource Type |  |
| --- | --- |
| fill-in |  |

### **Entitlement Types**

| In Scope (Y/N) | Entitlement Label | Entitlement Type | Resource Type | Min | Max | Assignable | Standard or Custom | Documentation | Other Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Y | fill-in | fill-in | fill-in | 1 | 1 | True | Standard  | fill-in | fill-in |

### Relationship Diagram

```mermaid
graph TD
  A[X] --> |can be assigned to| B[Y]
```
</output-format>
"""
    return PROMPT

