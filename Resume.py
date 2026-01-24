from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont

# ---------- Styles ----------
styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name='Body', fontName='Helvetica', fontSize=10, leading=13, alignment=TA_LEFT))
styles.add(ParagraphStyle(name='BodyBold', parent=styles['Body'], fontName='Helvetica-Bold'))
styles.add(ParagraphStyle(name='BodyItalic', parent=styles['Body'], fontName='Helvetica-Oblique'))
styles.add(ParagraphStyle(name='BodyRight', parent=styles['Body'], alignment=TA_RIGHT))
styles.add(ParagraphStyle(name='BodyRightBold', parent=styles['BodyBold'], alignment=TA_RIGHT))
styles.add(ParagraphStyle(name='Name', parent=styles['BodyBold'], fontSize=20, leading=24))
styles.add(ParagraphStyle(name='BodyJustify', parent=styles['Body'], alignment=TA_JUSTIFY))
styles.add(ParagraphStyle(name='BodyBoldJustify', parent=styles['BodyBold'], alignment=TA_JUSTIFY))

pdfmetrics.registerFont(UnicodeCIDFont('HeiseiKakuGo-W5'))

# ---------- Document ----------
output_path = "/mnt/data/Jimish Gajjar Resume.pdf"
doc = SimpleDocTemplate(
    output_path,
    pagesize=letter,
    title="Jimish Gajjar Resume",
    leftMargin=25,
    rightMargin=25,
    topMargin=25,
    bottomMargin=25
)

W = doc.width
story = []

# ---------- Helper Functions ----------
def fullwidth_paragraph(text, style):
    t = Table([[Paragraph(text, style)]], colWidths=[W])
    t.setStyle(TableStyle([
        ("LEFTPADDING", (0,0), (-1,-1), 0),
        ("RIGHTPADDING", (0,0), (-1,-1), 0),
        ("TOPPADDING", (0,0), (-1,-1), 0),
        ("BOTTOMPADDING", (0,0), (-1,-1), 0)
    ]))
    story.append(t)

def sep():
    story.append(Spacer(1, -6))
    rule = Table([[""]], colWidths=[W])
    rule.setStyle(TableStyle([
        ("LINEBELOW", (0,0), (-1,-1), 0.9, colors.black),
        ("LEFTPADDING", (0,0), (-1,-1), 0),
        ("RIGHTPADDING", (0,0), (-1,-1), 0)
    ]))
    story.append(rule)
    story.append(Spacer(1, 4))

def section_title(title):
    t = Table([[Paragraph(title, styles['BodyBold'])]], colWidths=[W])
    t.setStyle(TableStyle([
        ("LEFTPADDING", (0,0), (-1,-1), 0),
        ("RIGHTPADDING", (0,0), (-1,-1), 0)
    ]))
    story.append(t)
    story.append(Spacer(1, 2))

def work_experience(company, location, role, dates, bullets):
    t = Table([
        [Paragraph(company, styles['BodyBold']), Paragraph(location, styles['BodyRightBold'])],
        [Paragraph(role, styles['Body']), Paragraph(dates, styles['BodyRight'])]
    ], colWidths=[W*0.65, W*0.35])
    t.setStyle(TableStyle([
        ("LEFTPADDING", (0,0), (-1,-1), 0),
        ("RIGHTPADDING", (0,0), (-1,-1), 0)
    ]))
    story.append(t)

    for b in bullets:
        fullwidth_paragraph("• " + b, styles['BodyJustify'])

    story.append(Spacer(1, 3))

def project_block(name, link, tech, bullets):
    t = Table([
        [Paragraph(name, styles['BodyBold']), Paragraph(link, styles['BodyRight'])],
        [Paragraph(f"<i>Tech Stack: {tech}</i>", styles['BodyItalic']), Paragraph("", styles['BodyRight'])]
    ], colWidths=[W*0.70, W*0.30])
    t.setStyle(TableStyle([
        ("LEFTPADDING", (0,0), (-1,-1), 0),
        ("RIGHTPADDING", (0,0), (-1,-1), 0)
    ]))
    story.append(t)

    for b in bullets:
        fullwidth_paragraph("• " + b, styles['BodyJustify'])

    story.append(Spacer(1, 3))

# ---------- Header ----------
fullwidth_paragraph("Jimish Gajjar | Full Stack Engineer", styles['Name'])
fullwidth_paragraph(
    "<b>Mobile:</b> +1 (437) 766-4740 | <b>Email:</b> jimish2104gajjar@gmail.com<br/>"
    "<b>LinkedIn:</b> www.linkedin.com/in/jimishgajjar | "
    "<b>Portfolio:</b> www.jimishgajjar.github.io/jimishgajjar | "
    "<b>Location:</b> Toronto, ON",
    styles['Body']
)
sep()

# ---------- Summary ----------
section_title("SUMMARY")
fullwidth_paragraph(
    "Motivated and detail-oriented <b>Full Stac </b> with hands-on experience in building "
    "interactive, accessible, and scalable web applications using <b>React</b>, <b>Next.js</b>, "
    "<b>JavaScript</b>, <b>HTML</b>, and <b>CSS</b>. Strong understanding of Agile workflows, "
    "component-based architecture, and modern web standards.",
    styles['BodyJustify']
)
sep()

# ---------- Technical Skills ----------
section_title("TECHNICAL SKILLS")
fullwidth_paragraph(
    "<b>Languages:</b> JavaScript, TypeScript, HTML5, CSS3, SQL<br/>"
    "<b>Frontend:</b> React.js, Next.js, Vue.js, Redux, Tailwind CSS, MUI<br/>"
    "<b>Backend:</b> Node.js, Express.js, MongoDB<br/>"
    "<b>Testing:</b> Jest, React Testing Library, Cypress<br/>"
    "<b>Cloud & Tools:</b> AWS, Docker, GitHub Actions, Postman, Figma",
    styles['BodyJustify']
)
sep()

# ---------- Education ----------
section_title("EDUCATION")
education = [
    ("Algonquin College, Ottawa, ON", "2024 - 2025",
     "Post Graduate Certificate in Cloud Development and Operations", "CGPA: 3.94/4"),
    ("Conestoga College, Milton, ON", "2023 - 2024",
     "Post Graduate Certificate in Computer Application Development", "CGPA: 3.72/4"),
    ("Silver Oak College of Engineering & Technology, India", "2018 - 2021",
     "Bachelor of Engineering in Information Technology", "CGPA: 8.41/10")
]

for school, year, degree, grade in education:
    t = Table([
        [Paragraph(school, styles['BodyBoldJustify']), Paragraph(year, styles['BodyRight'])],
        [Paragraph(degree, styles['BodyJustify']), Paragraph(grade, styles['BodyRightBold'])]
    ], colWidths=[W*0.65, W*0.35])
    story.append(t)
    story.append(Spacer(1, 2))

sep()

# ---------- Work Experience ----------
section_title("WORK EXPERIENCE")
work_experience(
    "OpenXcell - AI Development Company (CMMI Level 3)",
    "Ahmedabad, India",
    "Software Engineer (Front-End)",
    "Jan 2023 - Dec 2023",
    [
        "Built scalable UI components using React and Next.js.",
        "Integrated RESTful APIs and optimized frontend performance.",
        "Collaborated with UX teams to deliver accessible, responsive designs.",
        "Implemented Redux for efficient state management.",
        "Worked in Agile teams delivering sprint-based releases."
    ]
)

work_experience(
    "Nexactly Solutions",
    "Ahmedabad, India",
    "Front-End Developer",
    "Dec 2021 - Dec 2022",
    [
        "Developed responsive interfaces using React and TypeScript.",
        "Improved accessibility and cross-browser compatibility.",
        "Integrated APIs and implemented robust error handling.",
        "Automated frontend testing with Jest and RTL.",
        "Improved performance via code optimization."
    ]
)

sep()

# ---------- Projects ----------
section_title("PROJECTS")
project_block(
    "SharedStorage - Storage Sharing Marketplace",
    "www.sharedstorage.ca",
    "React, Node.js, MongoDB, AWS",
    [
        "Developed frontend components for storage listings.",
        "Integrated maps and geolocation features.",
        "Implemented secure authentication flows.",
        "Optimized application performance.",
        "Built admin dashboards."
    ]
)

project_block(
    "ShopSphere - E-Commerce Platform",
    "",
    "React, Next.js, Stripe, GraphQL",
    [
        "Built a full-featured e-commerce frontend.",
        "Integrated Stripe for payments.",
        "Developed reusable UI components.",
        "Optimized SEO and performance.",
        "Enhanced UX with responsive layouts."
    ]
)

# ---------- Build PDF ----------
doc.build(story)

output_path


From now on, whenever I provide you with a job description, you must automatically generate a 2-page PDF resume for me based on code. 

The rules are:

Format & Style
-Always use the exact same format, structure, and design as the fixed Python-generated PDF resume I provided earlier.
-Do not change layout, spacing, fonts, or section order.
-Resume must always be exactly 2 pages — not longer, not shorter.
-Sections to Tailor for Each Job Description
-Don’t use square, emojis, jiblishword and all.
-When I Open PDF In Google Chrome IN title it shows Jimish Gajjar Resume
-Resume name should be Jimish Gajjar Resume - (Company Name From Job Description).pdf
-Add 1 or 2 points about ai technology and ai coding in expiration and projects.
-Add proper - hyphens.
-fix it by replacing all of them with standard ASCII hyphens (-) and clean up any other invisible characters so the text renders cleanly everywhere (including Chrome, macOS Preview, and Windows).

Summary → Rewrite based on the job description.

Technical Skills → Update categories and tools to highlight skills relevant to the job description.

Work Experience → Keep companies and roles , years of expireance the same, but rewrite the 7 bullet points per job with a mix of long and short points, tailored to the job description keywords.

Projects → Keep project names and links the same, but rewrite 6.5 bullets per project to emphasize skills with a mix of long and short points, tailored to the job description keywords..

Location → If the job description specifies a location, use that in the header. Otherwise, default to Toronto, ON.

Automation Behavior

Do not ask for confirmation.

As soon as I give a job description, you must directly create and return the final 2-page PDF in the fixed format with updated content.
