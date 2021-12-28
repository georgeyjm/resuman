import calendar
import subprocess

from resuman.models import Resume


def _friendly_time(year: int, month: int) -> str:
    if month is not None:
        month_name = calendar.month_name[month]
        return f'{month_name} {year}'
    if year is not None:
        return str(year)
    return ''


def render_resume(resume_id):
    resume = Resume.query.get(resume_id)

    with open('assets/template.tex', encoding='utf-8') as f:
        template_text = f.read()

    body_text = ''
    for section in resume.sections:
        section_text = rf'\section[{section.type}]{{{section.name}}}' + '\n'
        for entry in section.entries:
            title = entry.title or ''
            subtitle = entry.subtitle or ''
            start = _friendly_time(entry.start_year, entry.start_month)
            entry_text = rf'\sectionitem{{{title}}}{{{subtitle}}}{{{start}}}'
            if not entry.is_ongoing:
                entry_text += f'{{{_friendly_time(entry.end_year, entry.end_month)}}}'
            entry_text += '\n' + r'\begin{description}' + '\n'
            entry_text += '\n'.join([r'\item ' + desc.content for desc in entry.descriptions])
            entry_text += '\n' + r'\end{description}' + '\n'
        
            section_text += entry_text
        body_text += '\n' + section_text
    
    template_text = template_text.replace('<<RESUMAN:BODY>>', body_text)
    with open('assets/test.tex', 'w', encoding='utf-8') as f:
        f.write(template_text)

    subprocess.run(['pdflatex', 'test.tex'], cwd='assets/')
