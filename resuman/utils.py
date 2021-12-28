import subprocess

from resuman.models import Resume


def render_resume(resume_id):
    resume = Resume.query.get(resume_id)
    print(resume)
    print(resume.sections)
    print(resume.sections[1].entries)
    print(resume.sections[1].entries[1].descriptions)

    # subprocess.run(['pdflatex', 'XX'])
