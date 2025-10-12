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
styles.add(ParagraphStyle(name='Body', fontName='Helvetica', fontSize=10, leading=13,
                          leftIndent=0, firstLineIndent=0, spaceBefore=0, spaceAfter=0, alignment=TA_LEFT))
styles.add(ParagraphStyle(name='BodyBold', parent=styles['Body'], fontName='Helvetica-Bold'))
styles.add(ParagraphStyle(name='BodyItalic', parent=styles['Body'], fontName='Helvetica-Oblique'))
styles.add(ParagraphStyle(name='BodyRight', parent=styles['Body'], alignment=TA_RIGHT))
styles.add(ParagraphStyle(name='BodyRightBold', parent=styles['BodyBold'], alignment=TA_RIGHT))
styles.add(ParagraphStyle(name='Name', parent=styles['BodyBold'], fontSize=20, leading=24, spaceAfter=0))
styles.add(ParagraphStyle(name='BodyJustify', parent=styles['Body'], alignment=TA_JUSTIFY))
styles.add(ParagraphStyle(name='BodyBoldJustify', parent=styles['BodyBold'], alignment=TA_JUSTIFY))

# Unicode fallback
pdfmetrics.registerFont(UnicodeCIDFont('HeiseiKakuGo-W5'))

# ---------- Document ----------
output_path = "/mnt/data/Jimish Gajjar - Resume.pdf"
doc = SimpleDocTemplate(
    output_path,
    pagesize=letter,
    title="Jimish Gajjar - Resume",
    leftMargin=25, rightMargin=25, topMargin=25, bottomMargin=25
)
W = doc.width
story = []

def fullwidth_paragraph(text, style):
    t = Table([[Paragraph(text, style)]], colWidths=[W])
    t.setStyle(TableStyle([
        ("LEFTPADDING", (0,0), (-1,-1), 0),
        ("RIGHTPADDING", (0,0), (-1,-1), 0),
        ("TOPPADDING", (0,0), (-1,-1), 0),
        ("BOTTOMPADDING", (0,0), (-1,-1), 0),
    ]))
    story.append(t)

def sep():
    story.append(Spacer(1, -6))
    rule = Table([[""]], colWidths=[W])
    rule.setStyle(TableStyle([
        ("LINEBELOW", (0,0), (-1,-1), 0.9, colors.black),
        ("LEFTPADDING", (0,0), (-1,-1), 0),
        ("RIGHTPADDING", (0,0), (-1,-1), 0),
        ("TOPPADDING", (0,0), (-1,-1), 0),
        ("BOTTOMPADDING", (0,0), (-1,-1), 0),
    ]))
    story.append(rule)
    story.append(Spacer(1, 4))

def section_title(title):
    t = Table([[Paragraph(title, styles['BodyBold']), ""]], colWidths=[W, 0])
    t.setStyle(TableStyle([
        ("LEFTPADDING", (0,0), (-1,-1), 0),
        ("RIGHTPADDING", (0,0), (-1,-1), 0),
        ("TOPPADDING", (0,0), (-1,-1), 0),
        ("BOTTOMPADDING", (0,0), (-1,-1), 0),
        ("VALIGN", (0,0), (-1,-1), "TOP")
    ]))
    story.append(t)
    story.append(Spacer(1, 2))

def work_experience(company, location, role, dates, bullets_list, add_bottom_space=True):
    t = Table(
        [
            [Paragraph(company, styles['BodyBold']), Paragraph(location, styles['BodyRightBold'])],
            [Paragraph(role, styles['Body']), Paragraph(dates, styles['BodyRight'])],
        ],
        colWidths=[W*0.65, W*0.35]
    )
    t.setStyle(TableStyle([
        ("LEFTPADDING", (0,0), (-1,-1), 0),
        ("RIGHTPADDING", (0,0), (-1,-1), 0),
        ("TOPPADDING", (0,0), (-1,-1), 0),
        ("BOTTOMPADDING", (0,0), (-1,-1), 0),
        ("VALIGN", (0,0), (-1,-1), "TOP"),
    ]))
    story.append(t)
    story.append(Spacer(1, 1))
    for it in bullets_list:
        fullwidth_paragraph("• " + it, styles['BodyJustify'])
    if add_bottom_space:
        story.append(Spacer(1, 3))

def project_block(name, link, tech, bullets_list, add_bottom_space=True):
    t = Table(
        [
            [Paragraph(name, styles['BodyBold']), Paragraph(link, styles['BodyRight'])],
            [Paragraph(f"<i>Tech Stack: {tech}</i>", styles['BodyItalic']), Paragraph("", styles['BodyRight'])],
        ],
        colWidths=[W*0.65, W*0.35]
    )
    t.setStyle(TableStyle([
        ("LEFTPADDING", (0,0), (-1,-1), 0),
        ("RIGHTPADDING", (0,0), (-1,-1), 0),
        ("TOPPADDING", (0,0), (-1,-1), 0),
        ("BOTTOMPADDING", (0,0), (-1,-1), 0),
    ]))
    story.append(t)
    story.append(Spacer(1, 1))
    for it in bullets_list:
        fullwidth_paragraph("• " + it, styles['BodyJustify'])
    if add_bottom_space:
        story.append(Spacer(1, 3))

# ---------- Header ----------
fullwidth_paragraph("Jimish Gajjar | Full Stack Developer", styles['Name'])
story.append(Spacer(1, 2))
fullwidth_paragraph(
    "<b>Mobile:</b> +1 (437) 766-4740 | <b>Email:</b> jimish2104gajjar@gmail.com<br/>"
    "<b>LinkedIn:</b> www.linkedin.com/in/jimishgajjar | <b>Portfolio:</b> www.jimishgajjar.github.io/jimishgajjar | <b>Location:</b> Toronto, ON",
    styles['Body']
)
sep()

# ---------- Summary ----------
section_title("SUMMARY")
fullwidth_paragraph(
    "Results-driven <b>Full Stack Developer</b> with 5+ years of experience building high-performance, scalable, and secure web applications using <b>React</b>, <b>Next.js</b>, <b>Node.js</b>, and <b>TypeScript</b>. "
    "Proficient in architecting <b>end-to-end solutions</b> with microservices, REST, and GraphQL APIs, integrating <b>CI/CD pipelines</b>, and deploying to <b>AWS</b> and <b>Docker/Kubernetes</b> environments. "
    "Specialized in developing <b>blockchain-based payment platforms</b> supporting Bitcoin and stablecoin transactions via <b>Lightning Network</b>, <b>ERC20</b>, and <b>TRC20</b>. "
    "Adept at optimizing system performance, ensuring <b>cross-platform compatibility</b>, maintaining <b>clean architecture</b>, and mentoring teams to deliver high-quality, production-grade software solutions.",
    styles['BodyJustify']
)
sep()

# ---------- Technical Skills ----------
section_title("TECHNICAL SKILLS")
fullwidth_paragraph(
    "<b>Languages:</b> JavaScript (ES6+), TypeScript, C++, Java, SQL<br/>"
    "<b>Frontend:</b> React.js, Next.js, React Native, Redux Toolkit, Redux Thunk, Tailwind CSS, MUI, SASS, SCSS, Vue.js, Vuex, Formik, Storybook<br/>"
    "<b>State & Data:</b> Context API, GraphQL (Apollo, TanStack Query), RESTful APIs, Axios<br/>"
    "<b>Backend & Databases:</b> Node.js, Express.js, MongoDB, PostgreSQL, MySQL, Elasticsearch, Redis, Kafka, Strapi, Prisma, TypeORM<br/>"
    "<b>DevOps & Cloud:</b> AWS (EC2, S3, ECS, Lambda), Docker, Kubernetes, GitHub Actions, GitLab CI, Azure DevOps, Terraform, Datadog<br/>"
    "<b>Testing & QA:</b> Jest, React Testing Library, Cypress, Playwright, Mocha, Vitest, SonarQube<br/>"
    "<b>Monitoring & Tools:</b> Prometheus, Grafana, ELK Stack, Postman, LaunchDarkly, Sentry<br/>"
    "<b>Computer Science & Practices:</b> Data Structures & Algorithms, OOP, System Design, Scalability, Agile Methodologies, UI/UX Principles, Responsive Design, Cross-Platform Compatibility, Version Control (Git)",
    styles['BodyJustify']
)
sep()

# ---------- Work Experience ----------
section_title("WORK EXPERIENCE")
work_experience("OpenXcell – AI Development Company (CMMI Level 3)", "Ahmedabad, India.",
                "Software Engineer (Front-End)", "Jan 2023 – Dec 2023",
                [
                    "Led end-to-end development of a <b>cryptocurrency payment platform</b> enabling businesses to accept <b>Bitcoin</b> and <b>stablecoins</b> (BTC, USDT, USDC) via <b>Lightning Network</b>, <b>ERC20</b>, and <b>TRC20</b>.",
                    "Developed and deployed <b>automated backend workflows</b>, boosting transaction efficiency by <b>40%</b> and reducing manual work by <b>50%</b> through asynchronous processing.",
                    "Designed and implemented <b>RESTful APIs</b> and <b>microservices architecture</b> for merchant onboarding and seamless third-party integration.",
                    "Enhanced <b>system uptime</b> and scalability by optimizing blockchain node configurations and fault-tolerant queue mechanisms.",
                    "Integrated <b>Prometheus</b>, <b>Grafana</b>, and <b>ELK Stack</b> for observability, metrics tracking, and real-time monitoring.",
                    "Mentored junior developers and enforced <b>clean code practices</b>, improving delivery timelines and developer productivity.",
                    "Collaborated cross-functionally to deliver a <b>Stripe-style developer experience</b> with standardized API documentation and test environments.",
                    "Partnered with QA and DevOps teams to ensure <b>secure deployments</b> and continuous integration using <b>Docker</b> and <b>AWS ECS</b>."
                ], add_bottom_space=True)
work_experience("Nexactly Solutions", "Ahmedabad, India.",
                "Front-End Developer", "Dec 2021 - Dec 2022",
                [
                    "Developed responsive, accessible UIs using <b>React</b>, <b>Next.js</b>, and <b>TypeScript</b>, optimized for multiple browsers and devices.",
                    "Implemented <b>Redux Toolkit</b> and modular architecture to improve scalability and reduce prop-drilling.",
                    "Collaborated with backend teams to design and integrate <b>RESTful APIs</b> with secure error handling and validation.",
                    "Improved performance metrics by leveraging <b>lazy loading</b>, <b>memoization</b>, and <b>dynamic imports</b>.",
                    "Automated <b>CI/CD pipelines</b> with <b>GitHub Actions</b> and improved build times and deployment reliability.",
                    "Wrote <b>unit</b> and <b>integration tests</b> using <b>Jest</b> and <b>React Testing Library</b>, improving coverage by 40%.",
                    "Partnered with QA and design teams to maintain UI consistency and <b>WCAG 2.1 accessibility</b> compliance.",
                    "Supported agile sprint planning and release coordination with the product management team."
                ], add_bottom_space=True)
work_experience("Letsbiz", "Ahmedabad, India.",
                "Front-End Developer", "Jun 2021 - Nov 2021",
                [
                    "Built modular, reusable <b>React</b> components and UI frameworks using <b>Redux</b> and <b>Tailwind CSS</b>.",
                    "Developed <b>Storybook</b> component libraries to streamline design and development workflows.",
                    "Integrated <b>GraphQL</b> APIs for real-time data updates and reduced over-fetching across client modules.",
                    "Optimized application performance through <b>code-splitting</b> and asset preloading, improving load times by 20%.",
                    "Implemented <b>responsive design</b> principles ensuring pixel-perfect UIs on mobile and desktop devices.",
                    "Collaborated in <b>Agile sprints</b> to deliver prioritized product features and resolve production issues efficiently.",
                    "Improved <b>SEO</b> and <b>Lighthouse</b> performance scores via bundle optimization and accessibility improvements.",
                    "Documented front-end architecture decisions and mentored new developers during onboarding."
                ], add_bottom_space=True)
work_experience("X’Pert Infotech", "Ahmedabad, India.",
                "Jr. Web Developer", "Jan 2020 - May 2021",
                [
                    "Developed dynamic web interfaces using <b>HTML5</b>, <b>CSS3</b>, and <b>JavaScript</b> for enterprise client dashboards.",
                    "Assisted in developing <b>REST APIs</b> with <b>Node.js</b> and <b>Express.js</b> for backend data exchange.",
                    "Refactored SQL queries and improved database indexing, enhancing <b>performance</b> by 25%.",
                    "Implemented <b>JWT-based authentication</b> and role-based authorization to enhance security.",
                    "Created <b>technical documentation</b> for APIs, user flows, and new feature integration.",
                    "Performed <b>regression testing</b> and supported post-release issue resolution in production.",
                    "Collaborated with backend developers and QA engineers to improve bug detection and code quality.",
                    "Maintained <b>continuous improvement</b> through feedback loops and iterative deployment cycles."
                ], add_bottom_space=False)
sep()

# ---------- Projects ----------
section_title("PROJECTS")
project_block("TrySpeed – AI-Integrated Crypto Payout & Analytics Platform (OpenXcell)", "www.tryspeed.com",
              "React, Next.js, Node.js, Lightning Network, GraphQL, Prisma, AWS, Docker",
              [
                "Developed a unified crypto payment processor enabling businesses to accept <b>Bitcoin</b> and <b>stablecoins</b> (BTC, USDT, USDC) via <b>Lightning Network</b>, <b>ERC20</b>, and <b>TRC20</b>.",
                "Built and deployed <b>automated backend pipelines</b>, improving throughput by 40% and reducing manual tasks by 50%.",
                "Architected <b>Stripe-like RESTful APIs</b> for merchant onboarding and developer integrations.",
                "Implemented <b>real-time dashboards</b> in <b>React</b>/<b>Next.js</b> for tracking settlements, withdrawals, and transactions.",
                "Developed <b>microservices</b> architecture using <b>Node.js</b>, <b>GraphQL</b>, and <b>Prisma ORM</b> to scale concurrent transactions.",
                "Improved uptime and fault tolerance via <b>asynchronous queues</b> and <b>redundant blockchain nodes</b>.",
                "Deployed services on <b>AWS ECS</b> with <b>Docker</b> and automated <b>CI/CD</b> via <b>GitHub Actions</b>.",
                "Mentored developers on <b>code optimization</b>, <b>scalability</b>, and <b>CI/CD best practices</b> to maintain production reliability."
            ], add_bottom_space=True)
project_block("LIMS – Laboratory Information Management System", "",
              "React, Redux, Node.js, Express, MongoDB, AWS",
              [
                "Designed and built secure, role-based modules for <b>sample tracking</b> and laboratory workflows.",
                "Integrated <b>REST APIs</b> with backend systems, ensuring consistent data synchronization across services.",
                "Developed <b>real-time analytics dashboards</b> using <b>React</b> and <b>Redux</b> for data visualization.",
                "Optimized database schema and query performance, improving response times and scalability.",
                "Implemented <b>data validation</b> and <b>error handling</b> layers for reliable backend communication.",
                "Automated QA testing using <b>Jest</b> and <b>Cypress</b>, reducing manual regression testing cycles.",
                "Deployed system infrastructure on <b>AWS</b> with secure S3 data storage and load-balanced instances.",
                "Created developer documentation for API endpoints, versioning, and environment setup."
            ], add_bottom_space=True)
project_block("ShopSphere – AI-Driven E-Commerce Platform with Mobile App", "",
              "React Native, Next.js, GraphQL, AWS, Tailwind CSS",
              [
                "Built an <b>AI-powered e-commerce platform</b> with real-time product recommendations and dynamic user experiences.",
                "Developed mobile-first interfaces using <b>React Native</b> and <b>Next.js</b> for web and mobile platforms.",
                "Integrated <b>Stripe</b> payments, <b>order tracking</b>, and push notifications for enhanced user engagement.",
                "Built scalable <b>GraphQL APIs</b> and optimized them for low latency and high traffic volumes.",
                "Automated deployment and CI/CD workflows using <b>GitHub Actions</b> and <b>Docker</b> containers.",
                "Created <b>real-time analytics dashboards</b> for sales and inventory tracking with visual data insights.",
                "Collaborated with UI/UX teams to optimize user flow and increase conversion rates by 18%.",
                "Documented architecture, APIs, and infrastructure setup to support multi-developer environments."
            ], add_bottom_space=False)
sep()

# ---------- Education ----------
section_title("EDUCATION")
edu_blocks = [
    ("Algonquin College, Ottawa, ON", "2024 – 2025", "Post Graduate Certificate in Cloud Development and Operations", "CGPA: 3.94/4"),
    ("Conestoga College, Milton, ON", "2023 – 2024", "Post Graduate Certificate in Computer Application Development", "CGPA: 3.72/4"),
    ("Silver Oak College of Engineering & Technology, India", "2018 – 2021", "Bachelor of Engineering in Information Technology", "CGPA: 8.41/10"),
]
for idx, (school, years, degree, cgpa) in enumerate(edu_blocks):
    t = Table(
        [
            [Paragraph(school, styles['BodyBoldJustify']), Paragraph(years, styles['BodyRight'])],
            [Paragraph(degree, styles['BodyJustify']), Paragraph(cgpa, styles['BodyRightBold'])],
        ],
        colWidths=[W*0.65, W*0.35]
    )
    t.setStyle(TableStyle([
        ("LEFTPADDING", (0,0), (-1,-1), 0),
        ("RIGHTPADDING", (0,0), (-1,-1), 0),
        ("TOPPADDING", (0,0), (-1,-1), 0),
        ("BOTTOMPADDING", (0,0), (-1,-1), 0),
        ("VALIGN", (0,0), (-1,-1), "TOP"),
    ]))
    story.append(t)
    if idx < len(edu_blocks) - 1:
        story.append(Spacer(1, 2))

# ---------- Build ----------
doc.build(story)
output_path
