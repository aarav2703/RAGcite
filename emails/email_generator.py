# emails/email_generator.py

from embeddings.deepseek_client import generate_response


def generate_cold_email(
    professor_name: str,
    university: str,
    user_interest: str,
    paper_title: str = "",
    include_paper: bool = False,
    student_name: str = "",
    student_uni: str = "",
    student_email: str = "",
    contact_line: str = "",
) -> str:
    """
    Generate a cold email to a professor using DeepSeek V3 with personalization.

    Parameters:
        professor_name (str): Name of the professor
        university (str): Professor's institution
        user_interest (str): Student's research topic
        paper_title (str): Optional paper title
        include_paper (bool): Whether to reference the paper
        student_name (str): Student's name
        student_uni (str): Student's university
        student_email (str): Student's email address
        contact_line (str): Optional contact (LinkedIn, phone, etc.)

    Returns:
        str: Generated cold email
    """
    system_prompt = "You are an academic assistant helping a graduate student write a polite and concise email to a professor for research collaboration."

    paper_mention = (
        f" I found your paper titled '{paper_title}' very insightful."
        if include_paper and paper_title
        else ""
    )

    user_prompt = f"""
Write a cold email to Professor {professor_name} from {university}.
The student, {student_name} from {student_uni}, is interested in the following topic: "{user_interest}".
{paper_mention}
Please end the email with a polite sign-off including:
- {student_name}
- {student_uni}
- {student_email}
- {contact_line if contact_line else ""}
The email should be polite, short, and express interest in collaboration or guidance.
"""

    return generate_response(system_prompt, user_prompt, temperature=1.0)
