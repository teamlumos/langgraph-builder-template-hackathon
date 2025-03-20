

def compose_prompt(
        pre_research: str, 
        sdk_prompt: str, 
        product_req_prompt: str | None = None,
        dev_req_prompt: str | None = None
    ) -> str:
    """
    Compose a prompt for a research agent.
    """
    if product_req_prompt:
        return f"{product_req_prompt}\n\n{pre_research}\n\n{sdk_prompt}"
    elif dev_req_prompt:
        return f"{dev_req_prompt}\n\n{pre_research}\n\n{sdk_prompt}"
    else:
        return f"{pre_research}\n\n{sdk_prompt}"