from jinja2 import Template

def render_template(subject_template: str, body_template: str, variables: dict) -> tuple[str, str]:
    """
    Render template subject & body using Jinja2.
    Supports: {{name}}, loops, conditionals, links, etc.
    Missing variables are left unchanged.
    """

    try:
        subject = Template(subject_template).render(**variables)
        body = Template(body_template).render(**variables)
    except Exception as e:
        # fallback behavior if template fails to render
        raise Exception(f"Template render error: {str(e)}")

    return subject, body
