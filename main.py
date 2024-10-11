import streamlit as st
import markdown2
import pdfkit
import openai  
import os

# OpenAI GPT API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

# Function to call GPT API and generate markdown resume
def generate_resume(role, name, email, mobile, linkedin, github, about, education, experience, projects, certificates, links):
    prompt = f"""
    Directly start with the resume, also dont add any emojis or special characters.
    No need to add any headers or titles, just the content.
    No need to add 'Sure, here is your resume formatted in Markdown' at the beginning.
    Only return the markdown content.
    Use H1 for the name and role, H2 for the sections (About, Education, Work Experience, Projects, Certificates, Additional Links), and bullet points for the details.
    Also use --- to separate sections.
    Use ATS friendly resume format with keywords.
    I am applying for the role of {role}. Here is my information:

    Name: {name}
    Email: {email}
    Mobile: {mobile}
    LinkedIn: {linkedin}
    GitHub: {github}

    About me: {about}

    Education: {education}

    Work Experience: {experience}

    Projects: {projects}

    Certificates: {certificates}

    Additional Links: {links}

    Please format this as a resume in Markdown, optimized for the role of {role}, and include appropriate sections.
    """

    # Call GPT API with the user's prompt
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ], 
        temperature=0.25
    )

    return response.choices[0].message['content']

# Function to call GPT-4 for resume feedback
def get_resume_feedback(role, resume_content):
    prompt = f"""
    You are an expert career advisor. Please review the following resume for the role of {role} and provide a score out of 100.
    Include detailed feedback on the following areas:
    - Relevance of skills and experience for the role.
    - Areas for improvement.
    - Missing components that are commonly expected in resumes for this role.

    Resume content:
    {resume_content}
    """

    # Call GPT API for feedback
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ], 
        temperature=0.25
    )

    return response.choices[0].message['content']

# Function to convert markdown to PDF
def convert_markdown_to_pdf(markdown_content, output_filename):
    try:
        # Convert markdown to HTML
        html_content = markdown2.markdown(markdown_content)

        # Custom CSS for styling
        custom_css = """
        <style>
            body {
                font-family: Arial, sans-serif;
                letter-spacing: 0.1em; /* Slightly increase letter-spacing */
            }
            h1, h2, h3, h4 {
                margin-top: 20px;
            }
            p, li {
                letter-spacing: 0.1em; /* Adjust for readability */
            }
        </style>
        """

        # Add CSS to HTML content
        html_content = f"{custom_css}{html_content}"

        # Save HTML content to a temporary file
        temp_html = "resume.html"
        with open(temp_html, 'w') as f:
            f.write(html_content)

        # Convert the HTML file to PDF using pdfkit
        pdfkit.from_file(temp_html, output_filename)
        os.remove(temp_html)  # Clean up the temporary HTML file
        return True
    except Exception as e:
        st.error(f"Error converting Markdown to PDF: {e}")
        return False

# Streamlit UI for user input
st.title("AI-Powered Resume Generator")

# Role the user is applying for
role = st.text_input("Role you're applying for", "Data Engineer")

# User information
name = st.text_input("Full Name", "Souradip Pal")
email = st.text_input("Email", "example@email.com")
mobile = st.text_input("Mobile Number", "+91 9876543210")
linkedin = st.text_input("LinkedIn Profile URL", "https://linkedin.com/in/yourprofile")
github = st.text_input("GitHub Profile URL", "https://github.com/yourprofile")

# About section (user's description about themselves)
about = st.text_area("Tell us about yourself", "I am a passionate data engineer with expertise in data pipelines, etc.")

# Education, Experience, Projects, Certificates, and Links
education = st.text_area("Education", "Master of Computer Applications, Vellore Institute of Technology, GPA: 8.06")
experience = st.text_area("Work Experience", "Business Analyst Intern at WS (Jan 2024 - Mar 2024)")
projects = st.text_area("Projects", "Student Performance Prediction, achieving 96% accuracy.")
certificates = st.text_area("Certificates", "Programming in Python (Meta), March 2023")
links = st.text_area("Additional Links", "https://portfolio.com")

# Button to generate resume
if st.button("Generate Resume"):
    # Generate the Markdown resume using GPT
    resume_markdown = generate_resume(
        role, name, email, mobile, linkedin, github, about, education, experience, projects, certificates, links
    )
    
    # Display the generated markdown
    #st.subheader("Generated Markdown")
    #st.code(resume_markdown, language="markdown")


 # Get resume feedback
    feedback = get_resume_feedback(role, resume_markdown)
    st.subheader("Resume Feedback and Score")
    st.text(feedback)   
    # Convert markdown to PDF
    output_pdf_path = "resume_generated.pdf"
    if convert_markdown_to_pdf(resume_markdown, output_pdf_path):
        st.success("Resume PDF generated successfully!")
        with open(output_pdf_path, "rb") as f:
            st.download_button("Download Resume PDF", f, file_name="resume_generated.pdf")
