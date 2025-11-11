# Execute the provided code to generate the PDF resume.
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
output_path = "/mnt/data/Jimish Gajjar Resume - OLG.pdf"
doc = SimpleDocTemplate(output_path, pagesize=letter, title="Jimish Gajjar - Resume",
                        leftMargin=25, rightMargin=25, topMargin=25, bottomMargin=25)
W = doc.width
story = []

def fullwidth_paragraph(text, style):
    t = Table([[Paragraph(text, style)]], colWidths=[W])
    t.setStyle(TableStyle([("LEFTPADDING", (0,0), (-1,-1), 0),
                           ("RIGHTPADDING", (0,0), (-1,-1), 0),
                           ("TOPPADDING", (0,0), (-1,-1), 0),
                           ("BOTTOMPADDING", (0,0), (-1,-1), 0)]))
    story.append(t)

def sep():
    story.append(Spacer(1, -6))
    rule = Table([[""]], colWidths=[W])
    rule.setStyle(TableStyle([("LINEBELOW", (0,0), (-1,-1), 0.9, colors.black),
                              ("LEFTPADDING", (0,0), (-1,-1), 0),
                              ("RIGHTPADDING", (0,0), (-1,-1), 0)]))
    story.append(rule)
    story.append(Spacer(1, 4))

def section_title(title):
    t = Table([[Paragraph(title, styles['BodyBold'])]], colWidths=[W])
    t.setStyle(TableStyle([("LEFTPADDING", (0,0), (-1,-1), 0),
                           ("RIGHTPADDING", (0,0), (-1,-1), 0)]))
    story.append(t)
    story.append(Spacer(1, 2))

def work_experience(company, location, role, dates, bullets_list):
    t = Table([[Paragraph(company, styles['BodyBold']), Paragraph(location, styles['BodyRightBold'])],
               [Paragraph(role, styles['Body']), Paragraph(dates, styles['BodyRight'])]],
              colWidths=[W*0.65, W*0.35])
    t.setStyle(TableStyle([("LEFTPADDING", (0,0), (-1,-1), 0),
                           ("RIGHTPADDING", (0,0), (-1,-1), 0)]))
    story.append(t)
    for b in bullets_list:
        fullwidth_paragraph("• " + b, styles['BodyJustify'])
    story.append(Spacer(1, 3))

def project_block(name, link, tech, bullets):
    t = Table([[Paragraph(name, styles['BodyBold']), Paragraph(link, styles['BodyRight'])],
               [Paragraph(f"<i>Tech Stack: {tech}</i>", styles['BodyItalic']), Paragraph("", styles['BodyRight'])]],
              colWidths=[W*0.70, W*0.30])
    t.setStyle(TableStyle([("LEFTPADDING", (0,0), (-1,-1), 0),
                           ("RIGHTPADDING", (0,0), (-1,-1), 0)]))
    story.append(t)
    for b in bullets:
        fullwidth_paragraph("• " + b, styles['BodyJustify'])
    story.append(Spacer(1, 3))

# ---------- Header ----------
fullwidth_paragraph("Jimish Gajjar | Front End Developer Student", styles['Name'])
fullwidth_paragraph("<b>Mobile:</b> +1 (437) 766-4740 | <b>Email:</b> jimish2104gajjar@gmail.com<br/>"
                    "<b>LinkedIn:</b> www.linkedin.com/in/jimishgajjar | <b>Portfolio:</b> www.jimishgajjar.github.io/jimishgajjar | <b>Location:</b> Toronto, ON",
                    styles['Body'])
sep()

# ---------- Summary ----------
section_title("SUMMARY")
fullwidth_paragraph(
    "Motivated and detail-oriented <b>Front End Developer Student</b> with hands-on experience in designing and building interactive, accessible, and scalable web applications. "
    "Proficient in <b>React</b>, <b>Next.js</b>, <b>JavaScript</b>, <b>HTML</b>, and <b>CSS</b>, with a focus on usability and performance optimization. "
    "Collaborates effectively with cross-functional teams to translate <b>UX/UI designs</b> into production-ready interfaces. "
    "Strong understanding of <b>Agile</b> workflows, component-based architecture, and modern web standards. "
    "Exploring <b>AI-driven UI automation</b>, <b>AI code generation</b>, and predictive front-end testing to enhance quality and efficiency.",
    styles['BodyJustify'])
sep()

# ---------- Technical Skills ----------
section_title("TECHNICAL SKILLS")
fullwidth_paragraph(
    "<b>Languages:</b> JavaScript (ES6+), TypeScript, HTML5, CSS3, SQL<br/>"
    "<b>Frontend:</b> React.js, Next.js, Vue.js, Redux Toolkit, Tailwind CSS, MUI, Accessibility (WCAG 2.1), Responsive Design<br/>"
    "<b>Backend:</b> Node.js, Express.js, RESTful APIs, MongoDB<br/>"
    "<b>Testing:</b> Jest, React Testing Library, Cypress<br/>"
    "<b>Cloud & DevOps:</b> AWS (S3, Lambda), Docker, GitHub Actions, Postman, Figma, VS Code<br/>"
    "<b>AI & Automation:</b> OpenAI API, AI-powered code analysis, intelligent UI testing, analytics dashboards<br/>"
    "<b>Soft Skills:</b> Communication, Team Collaboration, Agile, Time Management, Creative Problem Solving",
    styles['BodyJustify'])
sep()

# ---------- Work Experience ----------
section_title("WORK EXPERIENCE")
work_experience("OpenXcell - AI Development Company (CMMI Level 3)", "Ahmedabad, India",
                "Software Engineer (Front-End)", "Jan 2023 - Dec 2023",
                [
                    "Built scalable UI components using <b>React</b> and <b>Next.js</b>, improving rendering efficiency by 25%.",
                    "Implemented <b>RESTful APIs</b> and integrated microservices for dynamic data-driven modules.",
                    "Collaborated with UI/UX teams to ensure accessible, responsive, and pixel-perfect designs.",
                    "Applied <b>Redux</b> and context APIs to optimize state management and reduce data redundancy.",
                    "Introduced <b>AI-based UI validation</b> to automate visual regression testing and consistency checks.",
                    "Worked with <b>Agile teams</b> to deliver sprint-ready, production-grade releases on schedule.",
                    "Automated deployments via <b>Docker</b> and <b>AWS ECS</b>, maintaining high reliability."
                ])
work_experience("Nexactly Solutions", "Ahmedabad, India",
                "Front-End Developer", "Dec 2021 - Dec 2022",
                [
                    "Developed dynamic interfaces using <b>React</b>, <b>TypeScript</b>, and <b>CSS</b> for cross-browser compatibility.",
                    "Collaborated on UX improvements and ensured adherence to <b>WCAG 2.1</b> accessibility standards.",
                    "Integrated <b>REST APIs</b> and validated data synchronization using robust error handling.",
                    "Automated unit testing pipelines using <b>Jest</b> and <b>React Testing Library</b>.",
                    "Implemented <b>CI/CD pipelines</b> for front-end deployments and reduced downtime by 30%.",
                    "Enhanced application performance with lazy loading, image optimization, and caching.",
                    "Contributed to <b>AI-powered usage analytics</b> for performance dashboards."
                ])
work_experience("Letsbiz", "Ahmedabad, India",
                "Front-End Developer", "Jun 2021 - Nov 2021",
                [
                    "Created reusable <b>React</b> components and improved design consistency with <b>Storybook</b> documentation.",
                    "Integrated <b>GraphQL</b> APIs for real-time data updates and efficient query handling.",
                    "Collaborated with design and QA teams to deliver fully responsive UIs for production.",
                    "Enhanced SEO and accessibility compliance using semantic HTML and ARIA roles.",
                    "Implemented <b>AI-driven testing scripts</b> for front-end validation across devices.",
                    "Improved app performance by 18% through code refactoring and dependency optimization.",
                    "Developed developer onboarding docs and reusable hooks for internal teams."
                ])
work_experience("X'Pert Infotech", "Ahmedabad, India",
                "Jr. Web Developer", "Jan 2020 - May 2021",
                [
                    "Developed modular <b>HTML5/CSS3</b> layouts and <b>JavaScript</b> components for enterprise clients.",
                    "Assisted in developing <b>Node.js</b> APIs and handled secure user authentication flows.",
                    "Applied responsive design principles to support both web and mobile users.",
                    "Conducted <b>cross-browser testing</b> and resolved rendering issues efficiently.",
                    "Collaborated with QA and design teams for bug tracking and feature refinements.",
                    "Integrated <b>AI-based analytics widgets</b> for user activity visualization.",
                    "Documented APIs and workflows for knowledge transfer."
                ])
sep()

# ---------- Projects ----------
section_title("PROJECTS")

project_block("SharedStorage - Storage Sharing Marketplace Platform", "www.sharedstorage.ca",
              "Flutter, React, Node.js, MongoDB, AWS S3, Docker, Google Maps API",
              [
                  "Created peer-to-peer storage sharing app with <b>Flutter</b> and <b>React</b> frontends.",
                  "Integrated <b>Google Maps API</b> for dynamic geolocation and listing mapping.",
                  "Implemented secure authentication and <b>AWS S3</b> image upload flows.",
                  "Built <b>AI-based search recommendations</b> to enhance discoverability.",
                  "Configured Dockerized environments for seamless local and cloud builds.",
                  "Designed admin dashboards for rental analytics and activity monitoring."
              ])
              
project_block("TrySpeed - AI-Integrated Crypto Payout & Analytics Platform", "www.tryspeed.com",
              "React, Next.js, Node.js, Lightning Network, GraphQL, Prisma, AWS, Docker",
              [
                  "Developed secure crypto transaction modules with <b>Lightning Network</b> and <b>ERC20</b> integration.",
                  "Built admin dashboards in <b>React</b> for merchant onboarding and settlement analytics.",
                  "Integrated <b>GraphQL APIs</b> and <b>Prisma ORM</b> for optimized database performance.",
                  "Configured <b>AWS ECS</b> and Docker containers for deployment automation.",
                  "Implemented <b>AI-driven transaction insights</b> improving uptime and data accuracy.",
                  "Collaborated with teams to maintain scalable microservice architecture."
              ])

project_block("LIMS - Laboratory Information Management System", "",
              "React, Redux, Node.js, Express, MongoDB, AWS",
              [
                  "Built secure role-based dashboards and analytics features for lab operations.",
                  "Developed REST endpoints for sample workflows with authentication.",
                  "Created data visualization panels using <b>React</b> and <b>Redux</b>.",
                  "Automated test coverage using <b>Jest</b> and <b>Cypress</b> frameworks.",
                  "Deployed on AWS with load-balanced configuration and S3 integration.",
                  "Implemented <b>AI-based data analysis</b> to detect workflow anomalies."
              ])

project_block("ShopSphere - AI-Driven E-Commerce Platform", "",
              "React, Next.js, GraphQL, Stripe API, AWS, Tailwind CSS",
              [
                  "Developed full-featured e-commerce platform with <b>Next.js</b> and <b>React Hooks</b>.",
                  "Integrated <b>Stripe API</b> for secure payments and refund automation.",
                  "Built <b>AI recommendation engine</b> to enhance user shopping experience.",
                  "Designed responsive pages using <b>Tailwind CSS</b> improving Lighthouse scores.",
                  "Implemented <b>GraphQL</b> queries for performance optimization.",
                  "Led UI review cycles improving customer conversion by 17%."
              ])
sep()

# ---------- Education ----------
section_title("EDUCATION")
edu = [
    ("Algonquin College, Ottawa, ON", "2024 - 2025", "Post Graduate Certificate in Cloud Development and Operations", "CGPA: 3.94/4"),
    ("Conestoga College, Milton, ON", "2023 - 2024", "Post Graduate Certificate in Computer Application Development", "CGPA: 3.72/4"),
    ("Silver Oak College of Engineering & Technology, India", "2018 - 2021", "Bachelor of Engineering in Information Technology", "CGPA: 8.41/10"),
]
for s, y, d, c in edu:
    t = Table([[Paragraph(s, styles['BodyBoldJustify']), Paragraph(y, styles['BodyRight'])],
               [Paragraph(d, styles['BodyJustify']), Paragraph(c, styles['BodyRightBold'])]],
              colWidths=[W*0.65, W*0.35])
    story.append(t)
    story.append(Spacer(1, 2))

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
-When I Open PDF In Google Chrome IN title it shows Jimish Gajjar - Resume
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
