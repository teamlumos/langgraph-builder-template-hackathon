def initial_read_prompt(service_name: str):
  prompt = f"""
Here is the OAS for the connectors API. We will be implementing a connector with READ capabilities on an external API - {service_name}.

<domain-intro>
{sdk_api_spec_intro}
</domain-intro>

<read-models>
{sdk_api_spec_read_models}
</read-models>

<read-capabilities>
{sdk_api_spec_read_capabilities}
</read-capabilities>
"""

  return prompt


sdk_api_spec_intro = """openapi: 3.0.0
info:
  title: Lumos Connectors
  description: |-
    # The Lumos Connector API

    ## Introduction
    The Lumos Connector API is a standardized interface for Identity and Access Management (IAM)
    operations across various third-party systems. It enables seamless integration between Lumos
    and external applications by providing a consistent set of operations called **capabilities**.

    Each integration (referred to as a "connector") implements these capabilities to work with different third-party API providers,
    focusing primarily on:
    - User access management
    - License and cost tracking
    - User activity monitoring

    ## Core Components

    ### Connectors
    A connector is a specialized library that acts as a bridge between Lumos and third-party applications.
    It handles:
    - Translation of Lumos requests into app-specific API calls
    - Conversion of app-specific responses into standardized Lumos formats
    - Authentication and authorization flows
    - Data format transformations

    ### Capabilities
    Capabilities are standardized operations that each connector can implement. They provide:
    - Consistent interfaces across different connectors
    - Predictable behavior patterns
    - Standardized error handling
    - Unified data structures

    ## Data Model

    ### Accounts
    Accounts represent individual users or service accounts within a system.

    They serve as the primary entities for access management and support lifecycle operations such as creation, activation, deactivation, and deletion.

    Accounts can be associated with multiple entitlements and are typically identified by a unique account ID within the system.

    ### Entitlements
    Entitlements represent a permission or capability that can be granted to user accounts, such as a license or access level.

    They define specific permissions, access rights, or memberships and are always associated with a resource, which may be global or specific.

    Entitlements are categorized by `entitlement_type` (e.g., licenses, roles, permissions, group memberships) and have defined constraints for minimum and maximum assignments.

    The naming of entitlements may vary, such as using "membership" for group associations.

    ### Resources
    Resources represent entities within an application that can be accessed or managed.

    They are identified by a unique `resource_type` within each app and include a global resource (represented by an empty string) for top-level entities.

    Resources can represent hierarchical structures, such as Workspaces containing Users and Groups, and serve as the context for entitlement assignments.

    The usage of Resource IDs depends on the specific hierarchy, with an empty string for global resources and specific IDs (e.g., Workspace ID) for nested resources.

    ### Associations
    Associations define relationships from accounts to entitlements (which are resource specific).

    They follow a hierarchical structure of Account -> Entitlement -> Resource, with no direct account-to-resource associations allowed.

    Associations enable flexible access control models.

    Note: The specific structure and use of resources and entitlements may vary
    depending on the integrated system's architecture and access model.

    ## How to Use This API

    1. Discover available connectors
    2. Learn about a specific connector
    3. Configure a connector
    4. (optional) Authenticate with OAuth
    5. Read data from the connected tenant
    6. Write (update) data in the connected tenant

    ## Authenticating with a Connector

    ### Authentication Methods
    Connectors support two main authentication categories:

    ### 1. Shared Secret Authentication
    - API Keys / Tokens
    - Basic Authentication (username/password)

    ### 2. OAuth-based Authentication
    The API supports two OAuth flow types:

    #### Authorization Code Flow (3-legged OAuth)
    Requires a multi-step flow:

    1. **Authorization URL**
    - Call `get_authorization_url` to start the OAuth flow
    - Redirect user to the returned authorization URL

    2. **Handle Callback**
    - Process the OAuth callback using `handle_authorization_callback`
    - Receive access and refresh tokens

    3. **Token Management**
    - Use `refresh_access_token` to maintain valid access
    - Store refresh tokens securely

    #### Client Credentials Flow (2-legged OAuth)
    Suitable for machine-to-machine authentication:

    1. **Direct Token Request**
    - Call `handle_client_credentials_request` with client credentials
    - Receive access token (and optionally refresh token)

    2. **Token Management**
    - Use `refresh_access_token` to maintain valid access (if refresh tokens are supported)
    - Store tokens securely

    The flow type is configured in the connector settings and determines which capabilities are available. Both flows support customizable authentication methods (Basic Auth or request body) and different request formats (JSON, form data, or query parameters).

    ### Validation
    After obtaining credentials:
    1. Call `validate_credentials` to verify authentication
    2. Retrieve the unique tenant ID for the authenticated organization

    ### Authentication Schema
    Each connector's `info.authentication_schema` defines:
    - Required credential fields
    - Field formats and constraints
    - OAuth scopes (if applicable)
    ## Pagination

    Lumos connectors implement a standardized pagination mechanism to handle large datasets
    efficiently. The pagination system uses opaque tokens to maintain state across requests.

    ### How Pagination Works

    1. **Request Format**
    Every request can include an optional `page` parameter:
    ```typescript
       {
         "page": {
           "token": string,  // Optional: opaque token from previous response
           "size": number    // Optional: number of items per page
         }
       }
       ```

    2. **Response Format**
    Paginated responses include a `page` field:
    ```typescript
       {
         "response": T[],    // Array of items
         "page": {
           "token": string,  // Token for the next page
           "size": number    // Items per page
         }
       }
       ```

    ### Using Pagination

    1. **Initial Request**
    - Make the first request without a page token
    - Optionally specify a page size

    2. **Subsequent Requests**
    - Include the `token` from the previous response
    - Keep the same page size for consistency

    3. **End of Data**
    - When there's no more data, the response won't include a page token

    ### Example Flow
    ```typescript
    // First request
    POST /connectors/pagerduty/list_accounts
    {
      "page": { "size": 100 }
    }

    // Response
    {
      "response": [...],
      "page": {
        "token": "eyJwYWdlIjogMn0=",
        "size": 100
      }
    }

    // Next request
    POST /connectors/pagerduty/list_accounts
    {
      "page": {
        "token": "eyJwYWdlIjogMn0=",
        "size": 100
      }
    }
    ```

    ### Implementation Notes

    - Page tokens are opaque and should be treated as black boxes
    - Tokens may encode various information (page numbers, cursors, etc.)
    - The same page size should be used throughout a pagination sequence
    - Invalid or expired tokens will result in an error response
"""

sdk_api_spec_write_capabilities = """
paths:
  /{connector_id}/activate_account:
    post:
      operationId: activate_account
      description: |-
        Activate (or reactivate) an existing user account.

        This operation allows you to activate or reactivate a user account that exists in the third-party system.
        The behavior depends on how the specific connector implements account activation/deactivation.

        Common use cases include:
        - Enabling user account access to the third-party system
        - Reactivating a previously deactivated account
        - Enabling a suspended account
        - Completing account setup after initial creation
      parameters:
        - name: connector_id
          in: path
          required: true
          schema:
            type: string
      responses:
        '200':
          description: The request has succeeded.
          content:
            application/json:
              schema:
                anyOf:
                  - $ref: '#/components/schemas/ActivateAccountResponse'
                  - $ref: '#/components/schemas/ErrorResponse'
      tags:
        - Write Capabilities
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                auth:
                  allOf:
                    - $ref: '#/components/schemas/AuthCredential'
                  description: The authentication credentials for the request.
                credentials:
                  type: array
                  items:
                    $ref: '#/components/schemas/AuthCredential'
              allOf:
                - type: object
                  required:
                    - request
                  properties:
                    request:
                      allOf:
                        - $ref: '#/components/schemas/ActivateAccount'
                      description: The main request payload.
                    include_raw_data:
                      type: boolean
                      description: Whether to include raw data in the response.
                    page:
                      allOf:
                        - $ref: '#/components/schemas/Page'
                      description: Pagination information for the request.
                    settings:
                      type: object
                      additionalProperties: {}
                      description: |-
                        Connector-specific settings for the request.

                        These are settings that are shared across all capabilities.

                        Usually contain additional required configuration options
                        not specified by the capability schema.
                  description: Generic request model.
              description: Authenticated request.
  /{connector_id}/assign_entitlement:
    post:
      operationId: assign_entitlement
      description: |-
        Assign an entitlement to an account.

        The assignment is subject to any constraints defined for the entitlement type, such as:
        - Minimum and maximum number of assignments allowed

        Common use cases include:
        - Assigning software licenses to users
        - Granting access levels to resources
        - Allocating quota or usage limits
      parameters:
        - name: connector_id
          in: path
          required: true
          schema:
            type: string
      responses:
        '200':
          description: The request has succeeded.
          content:
            application/json:
              schema:
                anyOf:
                  - $ref: '#/components/schemas/AssignEntitlementResponse'
                  - $ref: '#/components/schemas/ErrorResponse'
      tags:
        - Write Capabilities
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                auth:
                  allOf:
                    - $ref: '#/components/schemas/AuthCredential'
                  description: The authentication credentials for the request.
                credentials:
                  type: array
                  items:
                    $ref: '#/components/schemas/AuthCredential'
              allOf:
                - type: object
                  required:
                    - request
                  properties:
                    request:
                      allOf:
                        - $ref: '#/components/schemas/AssignEntitlement'
                      description: The main request payload.
                    include_raw_data:
                      type: boolean
                      description: Whether to include raw data in the response.
                    page:
                      allOf:
                        - $ref: '#/components/schemas/Page'
                      description: Pagination information for the request.
                    settings:
                      type: object
                      additionalProperties: {}
                      description: |-
                        Connector-specific settings for the request.

                        These are settings that are shared across all capabilities.

                        Usually contain additional required configuration options
                        not specified by the capability schema.
                  description: Generic request model.
              description: Authenticated request.
  /{connector_id}/create_account:
    post:
      operationId: create_account
      description: |-
        Create a new user account in the third-party system.

        This operation creates a new user account with the specified details and required entitlements.
        The account creation process may vary between integrations, but typically involves:
        - Creating the base user account with provided personal information
        - Assigning the required entitlements (permissions, licenses, etc.) that must be set during creation
        - Setting up the initial account status

        Note: Only entitlements that are required for account creation should be specified here.
        Optional entitlements should be assigned after creation using the assign_entitlement operation.
      parameters:
        - name: connector_id
          in: path
          required: true
          schema:
            type: string
      responses:
        '200':
          description: The request has succeeded.
          content:
            application/json:
              schema:
                anyOf:
                  - $ref: '#/components/schemas/CreateAccountResponse'
                  - $ref: '#/components/schemas/ErrorResponse'
      tags:
        - Write Capabilities
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                auth:
                  allOf:
                    - $ref: '#/components/schemas/AuthCredential'
                  description: The authentication credentials for the request.
                credentials:
                  type: array
                  items:
                    $ref: '#/components/schemas/AuthCredential'
              allOf:
                - type: object
                  required:
                    - request
                  properties:
                    request:
                      allOf:
                        - $ref: '#/components/schemas/CreateAccount'
                      description: The main request payload.
                    include_raw_data:
                      type: boolean
                      description: Whether to include raw data in the response.
                    page:
                      allOf:
                        - $ref: '#/components/schemas/Page'
                      description: Pagination information for the request.
                    settings:
                      type: object
                      additionalProperties: {}
                      description: |-
                        Connector-specific settings for the request.

                        These are settings that are shared across all capabilities.

                        Usually contain additional required configuration options
                        not specified by the capability schema.
                  description: Generic request model.
              description: Authenticated request.
  /{connector_id}/deactivate_account:
    post:
      operationId: deactivate_account
      description: |-
        Deactivate an existing user account in the integration system.

        This operation depends on the connector-specific concept of activation/deactivation.
        Different systems may handle deactivation differently - some may disable login,
        others may revoke permissions while preserving the account, etc.

        The account remains in the system but is made inactive according to the
        connector's capabilities.
      parameters:
        - name: connector_id
          in: path
          required: true
          schema:
            type: string
      responses:
        '200':
          description: The request has succeeded.
          content:
            application/json:
              schema:
                anyOf:
                  - $ref: '#/components/schemas/DeactivateAccountResponse'
                  - $ref: '#/components/schemas/ErrorResponse'
      tags:
        - Write Capabilities
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                auth:
                  allOf:
                    - $ref: '#/components/schemas/AuthCredential'
                  description: The authentication credentials for the request.
                credentials:
                  type: array
                  items:
                    $ref: '#/components/schemas/AuthCredential'
              allOf:
                - type: object
                  required:
                    - request
                  properties:
                    request:
                      allOf:
                        - $ref: '#/components/schemas/DeactivateAccount'
                      description: The main request payload.
                    include_raw_data:
                      type: boolean
                      description: Whether to include raw data in the response.
                    page:
                      allOf:
                        - $ref: '#/components/schemas/Page'
                      description: Pagination information for the request.
                    settings:
                      type: object
                      additionalProperties: {}
                      description: |-
                        Connector-specific settings for the request.

                        These are settings that are shared across all capabilities.

                        Usually contain additional required configuration options
                        not specified by the capability schema.
                  description: Generic request model.
              description: Authenticated request.
  /{connector_id}/delete_account:
    post:
      operationId: delete_account
      description: |-
        Delete an existing user account in an integration system. This is not a reversible operation
        and may result in data loss
      parameters:
        - name: connector_id
          in: path
          required: true
          schema:
            type: string
      responses:
        '200':
          description: The request has succeeded.
          content:
            application/json:
              schema:
                anyOf:
                  - $ref: '#/components/schemas/DeleteAccountResponse'
                  - $ref: '#/components/schemas/ErrorResponse'
      tags:
        - Write Capabilities
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                auth:
                  allOf:
                    - $ref: '#/components/schemas/AuthCredential'
                  description: The authentication credentials for the request.
                credentials:
                  type: array
                  items:
                    $ref: '#/components/schemas/AuthCredential'
              allOf:
                - type: object
                  required:
                    - request
                  properties:
                    request:
                      allOf:
                        - $ref: '#/components/schemas/DeleteAccount'
                      description: The main request payload.
                    include_raw_data:
                      type: boolean
                      description: Whether to include raw data in the response.
                    page:
                      allOf:
                        - $ref: '#/components/schemas/Page'
                      description: Pagination information for the request.
                    settings:
                      type: object
                      additionalProperties: {}
                      description: |-
                        Connector-specific settings for the request.

                        These are settings that are shared across all capabilities.

                        Usually contain additional required configuration options
                        not specified by the capability schema.
                  description: Generic request model.
              description: Authenticated request.
  /{connector_id}/unassign_entitlement:
    post:
      operationId: unassign_entitlement
      description: |-
        Unassign an Entitlement from a user account.

        Depends on the constraints (e.g. min, max) of this entitlement type.
      parameters:
        - name: connector_id
          in: path
          required: true
          schema:
            type: string
      responses:
        '200':
          description: The request has succeeded.
          content:
            application/json:
              schema:
                anyOf:
                  - $ref: '#/components/schemas/UnassignEntitlementResponse'
                  - $ref: '#/components/schemas/ErrorResponse'
      tags:
        - Write Capabilities
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                auth:
                  allOf:
                    - $ref: '#/components/schemas/AuthCredential'
                  description: The authentication credentials for the request.
                credentials:
                  type: array
                  items:
                    $ref: '#/components/schemas/AuthCredential'
              allOf:
                - type: object
                  required:
                    - request
                  properties:
                    request:
                      allOf:
                        - $ref: '#/components/schemas/UnassignEntitlement'
                      description: The main request payload.
                    include_raw_data:
                      type: boolean
                      description: Whether to include raw data in the response.
                    page:
                      allOf:
                        - $ref: '#/components/schemas/Page'
                      description: Pagination information for the request.
                    settings:
                      type: object
                      additionalProperties: {}
                      description: |-
                        Connector-specific settings for the request.

                        These are settings that are shared across all capabilities.

                        Usually contain additional required configuration options
                        not specified by the capability schema.
                  description: Generic request model.
              description: Authenticated request.

"""

sdk_api_spec_common_models = """
    AuthCredential:
      type: object
      properties:
        id:
          type: string
          description: The ID of the authentication schema.
          example: some_unique_id
        oauth:
          allOf:
            - $ref: '#/components/schemas/OAuthCredential'
          description: OAuth credentials, if using OAuth.
        oauth_client_credentials:
          allOf:
            - $ref: '#/components/schemas/OAuthClientCredential'
          description: OAuth client credentials, if using OAuth Client Credentials flow.
        oauth1:
          allOf:
            - $ref: '#/components/schemas/OAuth1Credential'
          description: OAuth 1.0a credentials, if using OAuth 1.0a.
        basic:
          allOf:
            - $ref: '#/components/schemas/BasicCredential'
          description: Basic auth credentials, if using basic auth.
        token:
          allOf:
            - $ref: '#/components/schemas/TokenCredential'
          description: Token credentials, if using token-based auth.
        jwt:
          allOf:
            - $ref: '#/components/schemas/JWTCredential'
          description: JWT credentials, if using JWT.
      description: Authentication credentials, which can be one of several types.
    AuthModel:
      type: string
      enum:
        - oauth
        - oauth_client_credentials
        - oauth1
        - basic
        - token
        - jwt
      description: Enum representing different authentication models.
    AuthorizationUrl:
      type: object
      required:
        - authorization_url
      properties:
        authorization_url:
          type: string
          description: The authorization URL to redirect the user to.
        code_verifier:
          type: string
          description: |-
            A code verifier for PKCE.
            This is the challenge that was sent in the authorization URL when using PKCE.
      description: OAuth authorization URL details.
    BasicAuthentication:
      type: object
      required:
        - username
        - password
      properties:
        username:
          type: string
          description: The username for basic auth.
        password:
          type: string
          description: The password for basic auth.
          x-secret: true
          x-field_type: SECRET
      description: |-
        Basic authentication model.
        This is a model exclusively used by standard capabilities.
      x-credential-type: basic
    BasicCredential:
      type: object
      required:
        - username
        - password
      properties:
        username:
          type: string
          description: The username for basic auth.
        password:
          type: string
          description: The password for basic auth.
          x-secret: true
          x-field_type: SECRET
      description: Basic authentication credentials.
      x-credential-type: basic
    CapabilitySchema:
      type: object
      required:
        - argument
        - output
      properties:
        argument:
          type: object
          additionalProperties: {}
          description: JSON schema for the input arguments of the capability.
        output:
          type: object
          additionalProperties: {}
          description: JSON schema for the output of the capability.
        display_name:
          type: string
          description: An optional text to display for the integration capability, in place of the default behavior, which is to use the capability name.
        description:
          type: string
          description: An optional 1-2 sentence description of any unusual behaviors of the capability, rendered for the end user.
      description: The schema for a capability, including its input arguments and output.
    EmptyButCreateAnyway:
      type: object
      description: |-
        This is a hack to force creation of types that extend this model, that
        otherwise don't have any properties but we still want the Python types for.
    Error:
      type: object
      required:
        - message
        - error_code
        - app_id
      properties:
        message:
          type: string
          description: A human-readable string explaining what went wrong.
          example: Authentication credentials didn't work
        status_code:
          type: integer
          description: |-
            An http status code (if applicable) corresponding to the
            underlying app's HTTP response that triggered this error.
          example: 401
        app_error_code:
          type: string
          description: |-
            An application-specific code string that can tell us more details
            about the underlying application code or request that triggered
            the error.
          example: my_integration.token_expired
        error_code:
          allOf:
            - $ref: '#/components/schemas/ErrorCode'
          description: A standard error code used by Lumos callers to respond to this error.
          example: unauthenticated
        app_id:
          type: string
          description: The ID of the app where the error occurred.
          example: pagerduty
        raised_by:
          type: string
          description: What type of exception triggered this error (if any)
          example: ConnectorError
        raised_in:
          type: string
          description: Where the exception was raised
          example: my_integration.integration:list_accounts
      description: An error that occurred during an operation.
    ErrorCode:
      type: string
      enum:
        - not_found
        - internal_error
        - api_error
        - unauthorized
        - bad_request
        - permission_denied
        - not_implemented
        - unexpected_error
        - unsupported_operation
        - unknown_value
        - invalid_value
        - unauthenticated
        - request_timeout
        - connection_timeout
        - connection_rejected
        - rate_limit
        - authentication_expired
        - service_error
        - invalid_response
        - client_call_error
        - connection_closed
        - creds_revoked
        - invalid_page_token
        - integration_missing_parameter
      description: Enum representing various error codes that can be returned by the connector.
    ErrorResponse:
      type: object
      required:
        - is_error
        - error
      properties:
        is_error:
          type: boolean
          description: Always true for error responses.
          default: true
        error:
          allOf:
            - $ref: '#/components/schemas/Error'
          description: The error details.
        raw_data:
          type: object
          additionalProperties: {}
          description: Raw data associated with the error, if any.
        page:
          allOf:
            - $ref: '#/components/schemas/Page'
          description: Pagination information, if applicable.
      description: Error details and metadata returned when an operation fails.
    GetAuthorizationUrl:
      type: object
      required:
        - client_id
        - scopes
        - redirect_uri
        - state
      properties:
        credential_id:
          type: string
          description: The credential ID assigned to these credentials.
        client_id:
          type: string
          description: OAuth client ID provided by the third-party service.
        scopes:
          type: array
          items:
            type: string
          description: List of OAuth scopes to request.
        redirect_uri:
          type: string
          description: URL where the user will be redirected after authorization. Must match the connector settings.
        state:
          type: string
          description: State parameter for security validation.
        form_data:
          type: object
          additionalProperties:
            type: string
          description: Form data to include in the authorization request.
      description: Parameters for generating an OAuth authorization URL.
      x-capability-category: authorization
    GetAuthorizationUrlRequest:
      type: object
      allOf:
        - type: object
          required:
            - request
          properties:
            request:
              allOf:
                - $ref: '#/components/schemas/GetAuthorizationUrl'
              description: The main request payload.
            include_raw_data:
              type: boolean
              description: Whether to include raw data in the response.
            page:
              allOf:
                - $ref: '#/components/schemas/Page'
              description: Pagination information for the request.
            settings:
              type: object
              additionalProperties: {}
              description: |-
                Connector-specific settings for the request.

                These are settings that are shared across all capabilities.

                Usually contain additional required configuration options
                not specified by the capability schema.
          description: Generic request model.
    GetAuthorizationUrlResponse:
      type: object
      allOf:
        - type: object
          required:
            - response
          properties:
            response:
              $ref: '#/components/schemas/AuthorizationUrl'
            raw_data: {}
            page:
              $ref: '#/components/schemas/Page'
          description: Response containing the main response payload, raw data, and pagination information.
      description: Response containing the OAuth authorization URL and related data.
    GetLastActivity:
      type: object
      required:
        - account_ids
      properties:
        account_ids:
          type: array
          items:
            type: string
          description: List of account identifiers to fetch activity data for
      description: Request parameters for retrieving last activity data
      x-capability-level: read
    GetLastActivityResponse:
      type: object
      allOf:
        - type: object
          required:
            - response
          properties:
            response:
              type: array
              items:
                $ref: '#/components/schemas/LastActivityData'
            raw_data: {}
            page:
              $ref: '#/components/schemas/Page'
          description: Response containing the main response payload, raw data, and pagination information.
      description: Response containing last activity data for requested accounts
    HandleAuthorizationCallback:
      type: object
      required:
        - client_id
        - client_secret
        - redirect_uri_with_code
      properties:
        credential_id:
          type: string
          description: The credential ID assigned to these credentials.
        client_id:
          type: string
          description: The OAuth client ID provided by the third-party service.
        client_secret:
          type: string
          description: The OAuth client secret associated with the client ID.
        redirect_uri_with_code:
          type: string
          description: The redirect URI containing the authorization code returned by the OAuth provider.
        state:
          type: string
          description: (Optional) A state parameter for security validation.
        code_verifier:
          type: string
          description: |-
            A code verifier for PKCE.
            This is returned from the get_authorization_url operation if PKCE is enabled.
      description: Parameters for handling an OAuth2 authorization callback.
      x-capability-category: authorization
    HandleAuthorizationCallbackRequest:
      type: object
      allOf:
        - type: object
          required:
            - request
          properties:
            request:
              allOf:
                - $ref: '#/components/schemas/HandleAuthorizationCallback'
              description: The main request payload.
            include_raw_data:
              type: boolean
              description: Whether to include raw data in the response.
            page:
              allOf:
                - $ref: '#/components/schemas/Page'
              description: Pagination information for the request.
            settings:
              type: object
              additionalProperties: {}
              description: |-
                Connector-specific settings for the request.

                These are settings that are shared across all capabilities.

                Usually contain additional required configuration options
                not specified by the capability schema.
          description: Generic request model.
    HandleAuthorizationCallbackResponse:
      type: object
      allOf:
        - type: object
          required:
            - response
          properties:
            response:
              $ref: '#/components/schemas/OauthCredentials'
            raw_data: {}
            page:
              $ref: '#/components/schemas/Page'
          description: Response containing the main response payload, raw data, and pagination information.
      description: Response containing the OAuth credentials after handling an authorization callback.
    HandleClientCredentials:
      type: object
      required:
        - client_id
        - client_secret
        - scopes
      properties:
        credential_id:
          type: string
          description: The credential ID assigned to these credentials.
        client_id:
          type: string
          description: The OAuth client ID provided by the third-party service, used to identify the application.
        client_secret:
          type: string
          description: The OAuth client secret associated with the client ID, used to authenticate the application.
        scopes:
          type: array
          items:
            type: string
          description: An array of strings representing the OAuth scopes to request, defining the access level.
      description: Parameters for handling a client credentials request.
      x-capability-category: authorization
    HandleClientCredentialsRequest:
      type: object
      allOf:
        - type: object
          required:
            - request
          properties:
            request:
              allOf:
                - $ref: '#/components/schemas/HandleClientCredentials'
              description: The main request payload.
            include_raw_data:
              type: boolean
              description: Whether to include raw data in the response.
            page:
              allOf:
                - $ref: '#/components/schemas/Page'
              description: Pagination information for the request.
            settings:
              type: object
              additionalProperties: {}
              description: |-
                Connector-specific settings for the request.

                These are settings that are shared across all capabilities.

                Usually contain additional required configuration options
                not specified by the capability schema.
          description: Generic request model.
    HandleClientCredentialsResponse:
      type: object
      allOf:
        - type: object
          required:
            - response
          properties:
            response:
              $ref: '#/components/schemas/OauthCredentials'
            raw_data: {}
            page:
              $ref: '#/components/schemas/Page'
          description: Response containing the main response payload, raw data, and pagination information.
      description: Response containing the OAuth credentials after handling a client credentials request.
    JWTClaims:
      type: object
      required:
        - iss
        - sub
        - aud
        - exp
        - nbf
        - iat
        - jti
        - act
        - scope
        - client_id
        - may_act
      properties:
        iss:
          type: string
          description: The issuer of the JWT.
        sub:
          type: string
          description: The subject of the JWT.
        aud:
          type: string
          description: The audience of the JWT.
        exp:
          type: integer
          format: int64
          description: The expiration time of the JWT in seconds since the Unix epoch.
        nbf:
          type: integer
          format: int64
          description: The not before time of the JWT in seconds since the Unix epoch.
        iat:
          type: integer
          format: int64
          description: The issue time of the JWT in seconds since the Unix epoch.
        jti:
          type: string
          description: The JWT ID.
        act:
          type: string
          description: The Actor of the JWT.
        scope:
          type: array
          items:
            type: string
          description: Scopes granted to the JWT.
        client_id:
          type: string
          description: The client ID of the JWT.
        may_act:
          type: string
          description: The may_act of the JWT.
      description: JWT payload model representing the claims in the JWT.
    JWTCredential:
      type: object
      required:
        - headers
        - claims
        - secret
      properties:
        headers:
          allOf:
            - $ref: '#/components/schemas/JWTHeaders'
          description: The JWT headers.
        claims:
          allOf:
            - $ref: '#/components/schemas/JWTClaims'
          description: The JWT claims.
        secret:
          type: string
          description: The JWT secret.
      description: JWT credential model.
      x-credential-type: jwt
    JWTHeaders:
      type: object
      required:
        - alg
        - jku
        - jwk
        - typ
        - kid
        - x5u
        - x5c
        - x5t
        - x5t#S256
        - cty
        - crit
      properties:
        alg:
          type: string
          description: The JWT algorithm.
        jku:
          type: string
          description: JWK Set URL.
        jwk:
          type: string
          description: JWK.
        typ:
          type: string
          description: The JWT type.
        kid:
          type: string
          description: The JWT key ID.
        x5u:
          type: string
          description: The X509 URL.
        x5c:
          type: string
          description: The X509 certificate chain.
        x5t:
          type: string
          description: The X509 certificate SHA-1 thumbprint.
        x5t#S256:
          type: string
          description: The X509 certificate SHA-256 thumbprint.
        cty:
          type: string
          description: The content type of the JWT.
        crit:
          type: array
          items:
            type: string
          description: The JWT critical extension.
      description: JWT headers model.
    OAuth1Credential:
      type: object
      required:
        - consumer_key
        - consumer_secret
        - token_id
        - token_secret
      properties:
        consumer_key:
          type: string
        consumer_secret:
          type: string
        token_id:
          type: string
        token_secret:
          type: string
      description: |-
        OAuth 1.0a credential model.
        This auth type is not used much, handling is done per-connector.
      x-credential-type: oauth1
    OAuthAuthentication:
      type: object
      required:
        - access_token
      properties:
        access_token:
          type: string
          description: The OAuth access token.
          x-field_type: HIDDEN
      description: |-
        OAuth authentication model.
        This is a model exclusively used by standard capabilities.
      x-credential-type: oauth
    OAuthAuthorization:
      type: object
      required:
        - client_id
        - client_secret
        - scopes
      properties:
        client_id:
          type: string
          description: The OAuth client id.
        client_secret:
          type: string
          description: The OAuth client secret.
        state:
          type: string
          description: The OAuth state variable.
        scopes:
          type: array
          items:
            type: string
          description: The OAuth scopes list.
      description: |-
        OAuth authorization model.
        This is a model exclusively used by authorization capabilities.
      x-credential-type: oauth
    OAuthClientCredential:
      type: object
      required:
        - access_token
        - client_id
        - client_secret
        - scopes
      properties:
        access_token:
          type: string
          description: The OAuth access token.
          x-field_type: HIDDEN
        client_id:
          type: string
          description: The OAuth client id.
        client_secret:
          type: string
          description: The OAuth client secret.
          x-secret: true
          x-field_type: SECRET
        scopes:
          type: array
          items:
            type: string
          description: The OAuth scopes list.
      description: OAuth Client Credentials
      x-credential-type: oauth_client_credentials
    OAuthClientCredentialAuthentication:
      type: object
      required:
        - access_token
      properties:
        access_token:
          type: string
          description: The OAuth access token.
          x-field_type: HIDDEN
      description: |-
        OAuth Client Credential Authentication model.
        This is a model exclusively used by standard capabilities.
      x-credential-type: oauth_client_credentials
    OAuthClientCredentialAuthorization:
      type: object
      required:
        - client_id
        - client_secret
        - scopes
      properties:
        client_id:
          type: string
          description: The OAuth client id.
          x-field_type: HIDDEN
        client_secret:
          type: string
          description: The OAuth client secret.
          x-secret: true
          x-field_type: SECRET
        scopes:
          type: array
          items:
            type: string
          description: The OAuth scopes list.
      description: |-
        OAuth Client Credential Authorization model.
        This is a model exclusively used by authorization capabilities.
      x-credential-type: oauth_client_credentials
    OAuthCredential:
      type: object
      required:
        - access_token
      properties:
        access_token:
          type: string
          description: The OAuth access token.
          x-field_type: HIDDEN
      allOf:
        - $ref: '#/components/schemas/OAuthAuthentication'
      description: OAuth access token and related authentication data.
      x-credential-type: oauth
    OAuthScopes:
      type: object
      properties:
        activate_account:
          type: string
        assign_entitlement:
          type: string
        create_account:
          type: string
        deactivate_account:
          type: string
        delete_account:
          type: string
        find_entitlement_associations:
          type: string
        get_last_activity:
          type: string
        list_accounts:
          type: string
        list_custom_attributes_schema:
          type: string
        list_entitlements:
          type: string
        list_resources:
          type: string
        unassign_entitlement:
          type: string
        validate_credentials:
          type: string
      description: |-
        Map of capabilities to OAuth scopes.

        This is used to determine the OAuth scopes required for a given capability.

        If a capability is not listed, it is assumed to not require any OAuth scopes.

        Scopes are a space-delimited list of scope names.
    OauthCredentials:
      type: object
      required:
        - access_token
        - token_type
      properties:
        access_token:
          type: string
          description: The token used for authenticating API requests, providing access to the API.
        refresh_token:
          type: string
          description: (Optional) A token used to refresh the access token, extending the session without re-authentication.
        token_type:
          allOf:
            - $ref: '#/components/schemas/TokenType'
          description: The type of token, usually "bearer", indicating how the token should be used.
        state:
          type: string
          description: (Optional) A state parameter for security validation, ensuring the response matches the request.
      description: |-
        OAuth credentials model.

        Enough authentication material to enable a capability, e.g. List Accounts, for an OAuth-based connector.
    Page:
      type: object
      properties:
        token:
          type: string
          description: |-
            Opaque token representing the next page of results.
            Include this token in subsequent requests to retrieve the next page.
        size:
          type: integer
          format: int32
          description: |-
            Number of items to return per page.
            This should remain consistent throughout a pagination sequence.
      description: Pagination parameters for requests and responses.
    RefreshAccessToken:
      type: object
      required:
        - client_id
        - client_secret
        - refresh_token
      properties:
        credential_id:
          type: string
          description: The credential ID assigned to these credentials.
        client_id:
          type: string
          description: The OAuth client ID provided by the third-party service.
        client_secret:
          type: string
          description: The OAuth client secret associated with the client ID.
        refresh_token:
          type: string
          description: The token used to obtain a new access token, extending the session.
        state:
          type: string
          description: (Optional) A state parameter for security validation.
      description: RefreshAccessToken Model
      x-capability-category: authorization
    RefreshAccessTokenResponse:
      type: object
      allOf:
        - type: object
          required:
            - response
          properties:
            response:
              $ref: '#/components/schemas/OauthCredentials'
            raw_data: {}
            page:
              $ref: '#/components/schemas/Page'
          description: Response containing the main response payload, raw data, and pagination information.
      description: Response containing the OAuth credentials after refreshing an access token.
    StandardCapabilityName:
      type: string
      enum:
        - app_info
        - info
        - connected_info
        - activate_account
        - assign_entitlement
        - create_account
        - update_account
        - deactivate_account
        - delete_account
        - find_entitlement_associations
        - get_authorization_url
        - get_last_activity
        - handle_authorization_callback
        - handle_client_credentials_request
        - list_accounts
        - list_custom_attributes_schema
        - list_entitlements
        - list_expenses
        - list_resources
        - refresh_access_token
        - unassign_entitlement
        - validate_credentials
      description: Enum representing the standard capabilities we expect most connectors to provide.
    TimeRange:
      type: object
      properties:
        start_date:
          type: string
        end_date:
          type: string
      description: A period of time
    TokenAuthentication:
      type: object
      required:
        - token
      properties:
        token:
          type: string
          description: The token for token-based auth.
          x-secret: true
          x-field_type: SECRET
      description: |-
        Token-based authentication model.
        This is a model exclusively used by standard capabilities.
      x-credential-type: token
    TokenCredential:
      type: object
      required:
        - token
      properties:
        token:
          type: string
          description: The token for token-based auth.
          x-secret: true
          x-field_type: SECRET
      description: Token-based authentication credentials.
      x-credential-type: token
    TokenType:
      type: string
      enum:
        - bearer

"""

sdk_api_spec_write_models = """
    ActivateAccount:
      type: object
      required:
        - account_id
      properties:
        account_id:
          type: string
          description: The unique identifier for the account in the third-party system that should be activated
      description: Request payload for activating an account
      x-capability-level: write
    ActivateAccountResponse:
      type: object
      allOf:
        - type: object
          required:
            - response
          properties:
            response:
              $ref: '#/components/schemas/ActivatedAccount'
            raw_data: {}
            page:
              $ref: '#/components/schemas/Page'
          description: Response containing the main response payload, raw data, and pagination information.
      description: Response containing the status of the activated account.
    ActivatedAccount:
      type: object
      required:
        - status
        - activated
      properties:
        status:
          allOf:
            - $ref: '#/components/schemas/AccountStatus'
          description: The current status of the account after the activation attempt
        activated:
          type: boolean
          description: Whether the account was successfully activated
          deprecated: true
      description: Details about the activated account
    AssignEntitlement:
      type: object
      required:
        - account_integration_specific_id
        - resource_integration_specific_id
        - resource_type
        - entitlement_type
        - entitlement_integration_specific_id
      properties:
        account_integration_specific_id:
          type: string
          description: The unique identifier for the account in the third-party system
          x-semantic: account-id
        resource_integration_specific_id:
          type: string
          description: The unique identifier for the resource in the third-party system that the entitlement will be assigned to
        resource_type:
          type: string
          description: The type of resource being assigned the entitlement (e.g. "user", "team", "project")
          x-resource-type: true
        entitlement_type:
          type: string
          description: The type of entitlement being assigned (e.g. "license", "permission", "quota")
          x-entitlement-type: true
        entitlement_integration_specific_id:
          type: string
          description: The unique identifier for the specific entitlement in the third-party system
      description: Request payload for assigning an entitlement
      x-capability-level: write
    AssignEntitlementResponse:
      type: object
      allOf:
        - type: object
          required:
            - response
          properties:
            response:
              $ref: '#/components/schemas/AssignedEntitlement'
            raw_data: {}
            page:
              $ref: '#/components/schemas/Page'
          description: Response containing the main response payload, raw data, and pagination information.
      description: Response containing the result of the entitlement assignment
    AssignedEntitlement:
      type: object
      required:
        - assigned
      properties:
        assigned:
          type: boolean
          description: This should only ever be true. If the assignment can't happen we expect an error.
      description: Details about the entitlement assignment result
    CreateAccount:
      type: object
      required:
        - entitlements
      properties:
        email:
          type: string
          description: The email address for the new account
        username:
          type: string
          description: The username for the new account
        given_name:
          type: string
          description: The user's first/given name
        family_name:
          type: string
          description: The user's last/family name
        user_status:
          type: string
          description: Initial status for the account (e.g. "active", "pending")
        extra_data:
          type: object
          additionalProperties: {}
          description: Additional connector-specific data needed for account creation
        entitlements:
          type: array
          items:
            $ref: '#/components/schemas/CreateAccountEntitlement'
          description: |-
            List of _required_ entitlements that must be set when an account is created.
            This list is all entitlement types with a min > 0
      description: Request payload for creating a new user account
      x-capability-level: write
    CreateAccountEntitlement:
      type: object
      required:
        - entitlement_type
        - integration_specific_id
      properties:
        integration_specific_resource_id:
          type: string
          description: |-
            The unique identifier for the resource in the third-party system that the entitlement will be assigned to.
            For global resources (e.g. global roles), this should be an empty string or leave blank.
            For scoped resources (e.g. workspace-specific roles), this should be the resource ID (e.g. workspace ID).
        entitlement_type:
          type: string
          description: Should match an entitlement type returned by this connector's info response
          x-entitlement-type: true
        integration_specific_id:
          type: string
          description: The unique identifier for the specific required entitlement in the third-party system
      description: Required entitlement configuration for assigning permissions during account creation
    CreateAccountResponse:
      type: object
      allOf:
        - type: object
          required:
            - response
          properties:
            response:
              $ref: '#/components/schemas/CreatedAccount'
            raw_data: {}
            page:
              $ref: '#/components/schemas/Page'
          description: Response containing the main response payload, raw data, and pagination information.
      description: Response containing the result of the account creation
    CreatedAccount:
      type: object
      required:
        - status
        - created
      properties:
        id:
          type: string
          description: The ID of the created account
          x-semantic: account-id
        status:
          allOf:
            - $ref: '#/components/schemas/AccountStatus'
          description: The current status of the created account
        created:
          type: boolean
          enum:
            - true
          description: Legacy flag indicating successful account creation
          deprecated: true
      description: Details about the created account
    DeactivateAccount:
      type: object
      required:
        - account_id
      properties:
        account_id:
          type: string
          description: The unique identifier of the account to deactivate in the integration system
          x-semantic: account-id
      description: Request parameters for deactivating an account
      x-capability-level: write
    DeactivateAccountResponse:
      type: object
      allOf:
        - type: object
          required:
            - response
          properties:
            response:
              $ref: '#/components/schemas/DeactivatedAccount'
            raw_data: {}
            page:
              $ref: '#/components/schemas/Page'
          description: Response containing the main response payload, raw data, and pagination information.
      description: Response containing the result of the account deactivation
    DeactivatedAccount:
      type: object
      required:
        - status
        - deactivated
      properties:
        status:
          allOf:
            - $ref: '#/components/schemas/AccountStatus'
          description: The current status of the account after deactivation
        deactivated:
          type: boolean
          description: Legacy flag indicating successful account deactivation
          deprecated: true
      description: Details about the deactivated account
    DeleteAccount:
      type: object
      required:
        - account_id
      properties:
        account_id:
          type: string
          description: The unique identifier of the account to delete in the integration system
          x-semantic: account-id
      description: Request parameters for deleting an account
      x-capability-level: write
    DeleteAccountResponse:
      type: object
      allOf:
        - type: object
          required:
            - response
          properties:
            response:
              $ref: '#/components/schemas/DeletedAccount'
            raw_data: {}
            page:
              $ref: '#/components/schemas/Page'
          description: Response containing the main response payload, raw data, and pagination information.
      description: Response containing the result of the account deletion
    DeletedAccount:
      type: object
      required:
        - status
        - deleted
      properties:
        status:
          allOf:
            - $ref: '#/components/schemas/AccountStatus'
          description: The current status of the account after deletion
        deleted:
          type: boolean
          description: Legacy flag indicating successful account deletion
          deprecated: true
      description: Details about the deleted account
    UnassignEntitlement:
      type: object
      required:
        - account_integration_specific_id
        - resource_type
        - resource_integration_specific_id
        - entitlement_type
        - entitlement_integration_specific_id
      properties:
        account_integration_specific_id:
          type: string
          description: The integration-specific identifier for the user account
        resource_type:
          type: string
          description: Should match a previously declared resource type from this connector
          x-resource-type: true
        resource_integration_specific_id:
          type: string
          description: The integration-specific identifier for the resource
        entitlement_type:
          type: string
          description: Should match a previously declared entitlement type from this connector
          x-entitlement-type: true
        entitlement_integration_specific_id:
          type: string
          description: The integration-specific identifier for the entitlement
      description: Parameters required to unassign an entitlement from a user account
      x-capability-level: write
    UnassignEntitlementResponse:
      type: object
      allOf:
        - type: object
          required:
            - response
          properties:
            response:
              $ref: '#/components/schemas/UnassignedEntitlement'
            raw_data: {}
            page:
              $ref: '#/components/schemas/Page'
          description: Response containing the main response payload, raw data, and pagination information.
      description: Response containing the result of the unassign entitlement operation
    UnassignedEntitlement:
      type: object
      required:
        - unassigned
      properties:
        unassigned:
          type: boolean
          description: Indicates whether the entitlement was successfully unassigned
      description: Result of the unassign entitlement operation
    UpdateAccountResponse:
      type: object
      allOf:
        - type: object
          required:
            - response
          properties:
            response:
              $ref: '#/components/schemas/UpdateableAccount'
            raw_data: {}
            page:
              $ref: '#/components/schemas/Page'
          description: Response containing the main response payload, raw data, and pagination information.
      description: |-
        Response containing the result of the account update.

        The returned type should be the same as the input.
    UpdateableAccount:
      type: object
      required:
        - id
      properties:
        id:
          type: string
          description: The value previously supplied by the integration as this account's Unique ID.
          x-semantic: account-id
      description: Request payload for updating a user account
"""

sdk_api_spec_read_models = """
    AccountStatus:
      type: string
      enum:
        - ACTIVE
        - INACTIVE
        - SUSPENDED
        - DEPROVISIONED
        - PENDING
        - DELETED
      description: Enum representing the possible statuses of an account.
    AccountType:
      type: string
      enum:
        - service
        - user
      description: Enum representing the types of accounts.
    ActivityEventType:
      type: string
      enum:
        - last_login
        - last_activity
      description: Enum representing types of activity events.
    EntitlementType:
      type: object
      required:
        - type_id
        - type_label
        - resource_type_id
        - min
      properties:
        type_id:
          type: string
          description: A unique identifier for this entitlement type.
        type_label:
          type: string
          description: A human-readable label for this entitlement type.
        resource_type_id:
          type: string
          description: This must be the same string as a type_id from the declared resource types
        min:
          type: integer
          format: uint32
          description: |-
            How many of this type of entitlement must be assigned?
            If 1: all accounts must have have one.
            If 0: this can be removed from an active account.
        max:
          type: integer
          format: uint32
          description: |-
            How many of this type of entitlement can be assigned?
            If 1: an account can only have one.
            Otherwise, accounts can have many (up to the specified max, if there is one)
      description: All the things we need to know about an entitlement type in this app.
      example:
        type_id: role
        type_label: IAM role
        resource_type_id: aws_account
        min: 0
    FindEntitlementAssociations:
      type: object
      allOf:
        - $ref: '#/components/schemas/EmptyButCreateAnyway'
      description: |-
        Request parameters for finding entitlement associations.
        Currently accepts empty input.
      x-capability-level: read
    FindEntitlementAssociationsResponse:
      type: object
      allOf:
        - type: object
          required:
            - response
          properties:
            response:
              type: array
              items:
                $ref: '#/components/schemas/FoundEntitlementAssociation'
            raw_data: {}
            page:
              $ref: '#/components/schemas/Page'
          description: Response containing the main response payload, raw data, and pagination information.
      description: Response containing the found entitlement associations
    FoundAccountData:
      type: object
      required:
        - integration_specific_id
      properties:
        integration_specific_id:
          type: string
          description: Integration specific identifier that uniquely identifies an account.
          x-semantic: account-id
        email:
          type: string
          description: The email address associated with the account.
        given_name:
          type: string
          description: The given name (first name) of the account holder.
        family_name:
          type: string
          description: The family name (last name) of the account holder.
        username:
          type: string
          description: The username associated with the account.
        user_status:
          allOf:
            - $ref: '#/components/schemas/AccountStatus'
          description: The current status of the account.
        extra_data:
          type: object
          additionalProperties: {}
          description: Additional data specific to the connector that doesn't fit into the standard fields.
        custom_attributes:
          type: object
          additionalProperties:
            type: string
          description: Custom attributes associated with the account. See the list_custom_attributes_schema capability.
        account_type:
          allOf:
            - $ref: '#/components/schemas/AccountType'
          description: The type of the account (e.g., service account or user account).
      description: |-
        A representation of a user within a connector. The fields provided here
        are the most commonly occurring across all connectors.
        For a complete list of fields specific to your connector, please
        refer to the [info endpoint](#tag/Describe/operation/info).
    FoundEntitlementAssociation:
      type: object
      required:
        - account_id
        - integration_specific_entitlement_id
        - integration_specific_resource_id
      properties:
        account_id:
          type: string
          description: The ID of the account that has been granted the entitlement.
          x-semantic: account-id
        integration_specific_entitlement_id:
          type: string
          description: The ID of the entitlement that has been granted.
        integration_specific_resource_id:
          type: string
          description: The ID of the resource to which the entitlement applies.
      description: A link between a user account and their granted entitlement.
    FoundEntitlementData:
      type: object
      required:
        - entitlement_type
        - integration_specific_id
        - integration_specific_resource_id
        - label
      properties:
        entitlement_type:
          type: string
          description: Should match a previously declared entitlement type from this connector.
          x-entitlement-type: true
        extra_data:
          type: object
          additionalProperties: {}
          description: Additional data specific to the entitlement that doesn't fit into the standard fields.
        integration_specific_id:
          type: string
          description: |-
            The unique ID within this application of an entitlement.

            May only be unique within the tenant and the entitlement type.
        integration_specific_resource_id:
          type: string
          description: |-
            The unique ID within this application of the resource this entitlement
            is for.

            See `FoundResourceData.integration_specific_resource_id`
        is_assignable:
          type: boolean
          description: Indicates whether this entitlement can be assigned to users.
        label:
          type: string
          description: A human-readable label for the entitlement.
        custom_attributes:
          type: object
          additionalProperties:
            type: string
          description: Custom attributes associated with the entitlement. See the list_custom_attributes_schema capability.
      description: An entitlement representing an authorization or permission that can be granted to users within the connector.
      example:
        entitlement_type: org_role
        integration_specific_id: member
        integration_specific_resource_id: ''
        label: Org Member
    FoundResourceData:
      type: object
      required:
        - integration_specific_id
        - label
        - resource_type
      properties:
        integration_specific_id:
          type: string
          description: |-
            The unique ID within this application of a resource.

            May only be unique within the tenant and the resource type.

            There will always be a global "account" (i.e. tenant) resource
            for things like tenant-wide roles.
        label:
          type: string
          description: A human-readable label for the resource.
        resource_type:
          type: string
          description: Should match a previously declared resource type from this connector.
          x-resource-type: true
        extra_data:
          type: object
          additionalProperties:
            type: string
          description: Additional data specific to the resource that doesn't fit into the standard fields.
      description: Resource data describing a resource within the connector.
    LastActivityData:
      type: object
      required:
        - account_id
        - event_type
        - happened_at
      properties:
        account_id:
          type: string
          description: The ID of the account.
        event_type:
          type: string
          description: The type of activity event.
        happened_at:
          type: string
          description: The timestamp when the activity occurred.
      description: Last known activity data for a user account.
    ListAccounts:
      type: object
      properties:
        custom_attributes:
          type: array
          items:
            type: string
          description: |-
            Optional array of custom attribute names to include in the account data.
            Each string in this array represents a specific custom attribute to retrieve.
      description: Request parameters for listing accounts.
      x-capability-level: read
    ListAccountsResponse:
      type: object
      allOf:
        - type: object
          required:
            - response
          properties:
            response:
              type: array
              items:
                $ref: '#/components/schemas/FoundAccountData'
            raw_data: {}
            page:
              $ref: '#/components/schemas/Page'
          description: Response containing the main response payload, raw data, and pagination information.
      description: Response containing information about the accounts
    ListCustomAttributesSchema:
      type: object
      allOf:
        - $ref: '#/components/schemas/EmptyButCreateAnyway'
      description: Request parameters for listing custom attribute schemas.
      x-capability-level: read
    ListCustomAttributesSchemaResponse:
      type: object
      allOf:
        - type: object
          required:
            - response
          properties:
            response:
              type: array
              items:
                $ref: '#/components/schemas/CustomAttributeSchema'
            raw_data: {}
            page:
              $ref: '#/components/schemas/Page'
          description: Response containing the main response payload, raw data, and pagination information.
      description: Response containing the schema definitions for all supported custom attributes
    ListEntitlements:
      type: object
      properties:
        custom_attributes:
          type: array
          items:
            type: string
          description: |-
            Optional array of custom attribute names to include in the entitlement data.
            Each string in this array represents a specific custom attribute to retrieve.
            You can get these attributes from `list_custom_attributes_schema`
      description: Request parameters for listing entitlements.
      x-capability-level: read
    ListEntitlementsResponse:
      type: object
      allOf:
        - type: object
          required:
            - response
          properties:
            response:
              type: array
              items:
                $ref: '#/components/schemas/FoundEntitlementData'
            raw_data: {}
            page:
              $ref: '#/components/schemas/Page'
          description: Response containing the main response payload, raw data, and pagination information.
      description: Response containing the list of available entitlements and their details
    ListExpenses:
      type: object
      required:
        - filters
      properties:
        filters:
          $ref: '#/components/schemas/ExpenseFilters'
      description: Request parameters for listing expenses.
    ListExpensesResponse:
      type: object
      allOf:
        - type: object
          required:
            - response
          properties:
            response:
              type: array
              items:
                $ref: '#/components/schemas/Expense'
            raw_data: {}
            page:
              $ref: '#/components/schemas/Page'
          description: Response containing the main response payload, raw data, and pagination information.
      description: Response containing information about the expenses
    ListResources:
      type: object
      allOf:
        - $ref: '#/components/schemas/EmptyButCreateAnyway'
      description: Request parameters for listing resources.
      x-capability-level: read
    ListResourcesResponse:
      type: object
      allOf:
        - type: object
          required:
            - response
          properties:
            response:
              type: array
              items:
                $ref: '#/components/schemas/FoundResourceData'
            raw_data: {}
            page:
              $ref: '#/components/schemas/Page'
          description: Response containing the main response payload, raw data, and pagination information.
      description: Response containing the list of available resources and their details
    ResourceType:
      type: object
      required:
        - type_id
        - type_label
      properties:
        type_id:
          type: string
          description: A unique identifier for this resource type.
        type_label:
          type: string
          description: A human-readable label for this resource type.
      description: A type of resource in the connector.
      example:
        type_id: aws_account
        type_label: AWS Account
    ValidateCredentials:
      type: object
      allOf:
        - $ref: '#/components/schemas/EmptyButCreateAnyway'
      description: Parameters for validating credentials.
      x-capability-level: read
    ValidateCredentialsResponse:
      type: object
      allOf:
        - type: object
          required:
            - response
          properties:
            response:
              $ref: '#/components/schemas/ValidatedCredentials'
            raw_data: {}
            page:
              $ref: '#/components/schemas/Page'
          description: Response containing the main response payload, raw data, and pagination information.
      description: Response containing the result of credential validation.
    ValidatedCredentials:
      type: object
      required:
        - valid
        - unique_tenant_id
      properties:
        valid:
          type: boolean
          description: |-
            Indicates whether the provided credentials are valid and active.

            - true: Credentials are valid and can be used for API operations
            - false: Credentials are invalid, expired, or revoked
        unique_tenant_id:
          type: string
          description: |-
            The unique identifier for the customer's tenant/organization in the integrated application.
            This ID is used to scope operations and resources to the correct tenant.

            The format varies by connector:
            - AWS: Account ID
            - GitHub: Organization name
            - PagerDuty: Subdomain
            - Azure: Tenant ID
            - Google Workspace: Domain name

            This ID should be stable and not change for the lifetime of the tenant.
      description: Result of credential validation containing validity and tenant information
"""

sdk_api_spec_read_capabilities = """
paths:
  /{connector_id}/validate_credentials:
    post:
      operationId: validate_credentials
      description: |-
        Validate the customer's credentials and retrieve tenant information.

        This operation verifies that the credentials provided by the customer are valid and active.
        It also retrieves identifying information about the customer's tenant/organization in the
        integrated application.

        The credentials could have been obtained through various means, such as:
        - OAuth flow
        - API keys
        - Username/password
        - Service account credentials

        This endpoint should be called:
        - After obtaining new credentials to verify they work
        - Before performing other operations to ensure credentials are still valid
        - To get the tenant identifier needed for other operations
      parameters:
        - name: connector_id
          in: path
          required: true
          schema:
            type: string
      responses:
        '200':
          description: The request has succeeded.
          content:
            application/json:
              schema:
                anyOf:
                  - $ref: '#/components/schemas/ValidateCredentialsResponse'
                  - $ref: '#/components/schemas/ErrorResponse'
      tags:
        - Read Capabilities
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                auth:
                  allOf:
                    - $ref: '#/components/schemas/AuthCredential'
                  description: The authentication credentials for the request.
                credentials:
                  type: array
                  items:
                    $ref: '#/components/schemas/AuthCredential'
              allOf:
                - type: object
                  required:
                    - request
                  properties:
                    request:
                      allOf:
                        - $ref: '#/components/schemas/ValidateCredentials'
                      description: The main request payload.
                    include_raw_data:
                      type: boolean
                      description: Whether to include raw data in the response.
                    page:
                      allOf:
                        - $ref: '#/components/schemas/Page'
                      description: Pagination information for the request.
                    settings:
                      type: object
                      additionalProperties: {}
                      description: |-
                        Connector-specific settings for the request.

                        These are settings that are shared across all capabilities.

                        Usually contain additional required configuration options
                        not specified by the capability schema.
                  description: Generic request model.
              description: Authenticated request.
  /{connector_id}/find_entitlement_associations:
    post:
      operationId: find_entitlement_associations
      description: |-
        Find associations between entitlements and resources in an integration system.

        This operation retrieves the relationships between entitlements and their associated resources
        in the third-party system. An entitlement represents a relationship that can be associated
        with a user account, such as group memberships, role assignments, or workspace access.

        The resource context helps identify the specific entity (like workspace, organization, etc.)
        under which the entitlement exists. For global entitlements, the resource ID should be empty.
      parameters:
        - name: connector_id
          in: path
          required: true
          schema:
            type: string
      responses:
        '200':
          description: The request has succeeded.
          content:
            application/json:
              schema:
                anyOf:
                  - $ref: '#/components/schemas/FindEntitlementAssociationsResponse'
                  - $ref: '#/components/schemas/ErrorResponse'
      tags:
        - Read Capabilities
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                auth:
                  allOf:
                    - $ref: '#/components/schemas/AuthCredential'
                  description: The authentication credentials for the request.
                credentials:
                  type: array
                  items:
                    $ref: '#/components/schemas/AuthCredential'
              allOf:
                - type: object
                  required:
                    - request
                  properties:
                    request:
                      allOf:
                        - $ref: '#/components/schemas/FindEntitlementAssociations'
                      description: The main request payload.
                    include_raw_data:
                      type: boolean
                      description: Whether to include raw data in the response.
                    page:
                      allOf:
                        - $ref: '#/components/schemas/Page'
                      description: Pagination information for the request.
                    settings:
                      type: object
                      additionalProperties: {}
                      description: |-
                        Connector-specific settings for the request.

                        These are settings that are shared across all capabilities.

                        Usually contain additional required configuration options
                        not specified by the capability schema.
                  description: Generic request model.
              description: Authenticated request.
  /{connector_id}/get_authorization_url:
    post:
      operationId: get_authorization_url
      description: |-
        Get OAuth authorization URL for a connector.

        Constructs and returns the OAuth 2.0 authorization URL for the specified connector.
        This URL can be used to direct users to the authorization page where they can grant
        access to their account. Upon authorization completion, users will be redirected to
        the specified callback URL.
      parameters:
        - name: connector_id
          in: path
          required: true
          schema:
            type: string
      responses:
        '200':
          description: The request has succeeded.
          content:
            application/json:
              schema:
                anyOf:
                  - $ref: '#/components/schemas/GetAuthorizationUrlResponse'
                  - $ref: '#/components/schemas/ErrorResponse'
      tags:
        - OAuth Capabilities
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/GetAuthorizationUrlRequest'
  /{connector_id}/get_last_activity:
    post:
      operationId: get_last_activity
      description: |-
        Retrieve the last activity information for specified user accounts.

        Activity data may include last login or last usage.

        This can be useful for:
        - Identifying inactive accounts
        - Tracking last login dates and methods
      parameters:
        - name: connector_id
          in: path
          required: true
          schema:
            type: string
      responses:
        '200':
          description: The request has succeeded.
          content:
            application/json:
              schema:
                anyOf:
                  - $ref: '#/components/schemas/GetLastActivityResponse'
                  - $ref: '#/components/schemas/ErrorResponse'
      tags:
        - Read Capabilities
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                auth:
                  allOf:
                    - $ref: '#/components/schemas/AuthCredential'
                  description: The authentication credentials for the request.
                credentials:
                  type: array
                  items:
                    $ref: '#/components/schemas/AuthCredential'
              allOf:
                - type: object
                  required:
                    - request
                  properties:
                    request:
                      allOf:
                        - $ref: '#/components/schemas/GetLastActivity'
                      description: The main request payload.
                    include_raw_data:
                      type: boolean
                      description: Whether to include raw data in the response.
                    page:
                      allOf:
                        - $ref: '#/components/schemas/Page'
                      description: Pagination information for the request.
                    settings:
                      type: object
                      additionalProperties: {}
                      description: |-
                        Connector-specific settings for the request.

                        These are settings that are shared across all capabilities.

                        Usually contain additional required configuration options
                        not specified by the capability schema.
                  description: Generic request model.
              description: Authenticated request.
  /{connector_id}/list_accounts:
    post:
      operationId: list_accounts
      description: |-
        Retrieve a list of accounts associated with the specified credentials. Response will include only active and suspended account.

        Common use cases include:
        - Auditing connected accounts
        - Account discovery and synchronization

        The request body allows for optional specification of custom attributes to include in the response.
      parameters:
        - name: connector_id
          in: path
          required: true
          schema:
            type: string
      responses:
        '200':
          description: The request has succeeded.
          content:
            application/json:
              schema:
                anyOf:
                  - $ref: '#/components/schemas/ListAccountsResponse'
                  - $ref: '#/components/schemas/ErrorResponse'
      tags:
        - Read Capabilities
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                auth:
                  allOf:
                    - $ref: '#/components/schemas/AuthCredential'
                  description: The authentication credentials for the request.
                credentials:
                  type: array
                  items:
                    $ref: '#/components/schemas/AuthCredential'
              allOf:
                - type: object
                  required:
                    - request
                  properties:
                    request:
                      allOf:
                        - $ref: '#/components/schemas/ListAccounts'
                      description: The main request payload.
                    include_raw_data:
                      type: boolean
                      description: Whether to include raw data in the response.
                    page:
                      allOf:
                        - $ref: '#/components/schemas/Page'
                      description: Pagination information for the request.
                    settings:
                      type: object
                      additionalProperties: {}
                      description: |-
                        Connector-specific settings for the request.

                        These are settings that are shared across all capabilities.

                        Usually contain additional required configuration options
                        not specified by the capability schema.
                  description: Generic request model.
              description: Authenticated request.
  /{connector_id}/list_entitlements:
    post:
      operationId: list_entitlements
      description: |-
        List all entitlements available in the connected system.

        The response includes details about each entitlement including:
        - The type of entitlement (e.g. group, role, workspace)
        - The resource it applies to (empty string for global resource)
        - Integration-specific identifiers
      parameters:
        - name: connector_id
          in: path
          required: true
          schema:
            type: string
      responses:
        '200':
          description: The request has succeeded.
          content:
            application/json:
              schema:
                anyOf:
                  - $ref: '#/components/schemas/ListEntitlementsResponse'
                  - $ref: '#/components/schemas/ErrorResponse'
      tags:
        - Read Capabilities
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                auth:
                  allOf:
                    - $ref: '#/components/schemas/AuthCredential'
                  description: The authentication credentials for the request.
                credentials:
                  type: array
                  items:
                    $ref: '#/components/schemas/AuthCredential'
              allOf:
                - type: object
                  required:
                    - request
                  properties:
                    request:
                      allOf:
                        - $ref: '#/components/schemas/ListEntitlements'
                      description: The main request payload.
                    include_raw_data:
                      type: boolean
                      description: Whether to include raw data in the response.
                    page:
                      allOf:
                        - $ref: '#/components/schemas/Page'
                      description: Pagination information for the request.
                    settings:
                      type: object
                      additionalProperties: {}
                      description: |-
                        Connector-specific settings for the request.

                        These are settings that are shared across all capabilities.

                        Usually contain additional required configuration options
                        not specified by the capability schema.
                  description: Generic request model.
              description: Authenticated request.
  /{connector_id}/list_resources:
    post:
      operationId: list_resources
      description: |-
        List all resources available in the connected system.

        The response includes details about each resource including:
        - The type of resource (e.g. workspace, team, repository)
        - Integration-specific identifier
        - Human readable label

        Resources help establish the contextual hierarchy for entitlements, showing which entities
        can contain or be assigned different types of access controls.
      parameters:
        - name: connector_id
          in: path
          required: true
          schema:
            type: string
      responses:
        '200':
          description: The request has succeeded.
          content:
            application/json:
              schema:
                anyOf:
                  - $ref: '#/components/schemas/ListResourcesResponse'
                  - $ref: '#/components/schemas/ErrorResponse'
      tags:
        - Read Capabilities
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                auth:
                  allOf:
                    - $ref: '#/components/schemas/AuthCredential'
                  description: The authentication credentials for the request.
                credentials:
                  type: array
                  items:
                    $ref: '#/components/schemas/AuthCredential'
              allOf:
                - type: object
                  required:
                    - request
                  properties:
                    request:
                      allOf:
                        - $ref: '#/components/schemas/ListResources'
                      description: The main request payload.
                    include_raw_data:
                      type: boolean
                      description: Whether to include raw data in the response.
                    page:
                      allOf:
                        - $ref: '#/components/schemas/Page'
                      description: Pagination information for the request.
                    settings:
                      type: object
                      additionalProperties: {}
                      description: |-
                        Connector-specific settings for the request.

                        These are settings that are shared across all capabilities.

                        Usually contain additional required configuration options
                        not specified by the capability schema.
                  description: Generic request model.
              description: Authenticated request.
"""