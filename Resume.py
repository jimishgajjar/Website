# Execute the provided code to generate the PDF resume.
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont

class OptimizedResumeBuilder:
    """Compact resume generator with justified text and tight spacing"""
    
    def __init__(self, output_path, title="Resume"):
        self.output_path = output_path
        self.doc = SimpleDocTemplate(
            output_path, pagesize=letter, title=title,
            leftMargin=25, rightMargin=25, topMargin=25, bottomMargin=25
        )
        self.width = self.doc.width
        self.story = []
        self._setup_styles()
        
    def _setup_styles(self):
        """Initialize paragraph styles with justify alignment"""
        self.styles = getSampleStyleSheet()
        
        # Base styles
        base_config = {'fontName': 'Helvetica', 'fontSize': 10, 'leading': 13, 
                       'leftIndent': 0, 'firstLineIndent': 0, 'spaceBefore': 0, 'spaceAfter': 0}
        
        style_configs = {
            'Body': {**base_config, 'alignment': TA_LEFT},
            'BodyJustify': {**base_config, 'alignment': TA_JUSTIFY},
            'BodyBold': {'fontName': 'Helvetica-Bold'},
            'BodyBoldJustify': {'fontName': 'Helvetica-Bold', 'alignment': TA_JUSTIFY},
            'BodyItalic': {'fontName': 'Helvetica-Oblique'},
            'BodyRight': {'alignment': TA_RIGHT},
            'BodyRightBold': {'fontName': 'Helvetica-Bold', 'alignment': TA_RIGHT},
            'Name': {'fontName': 'Helvetica-Bold', 'fontSize': 20, 'leading': 24, 'spaceAfter': 0}
        }
        
        for name, config in style_configs.items():
            if 'fontName' in config and name not in ['Body', 'BodyJustify', 'Name']:
                parent = self.styles['BodyJustify'] if 'Justify' in name else self.styles['Body']
                self.styles.add(ParagraphStyle(name=name, parent=parent, **config))
            else:
                self.styles.add(ParagraphStyle(name=name, **config))
        
        pdfmetrics.registerFont(UnicodeCIDFont('HeiseiKakuGo-W5'))
    
    def _table(self, data, widths, extra_style=None):
        """Create table with zero padding"""
        t = Table(data, colWidths=widths)
        base = [
            ("LEFTPADDING", (0,0), (-1,-1), 0),
            ("RIGHTPADDING", (0,0), (-1,-1), 0),
            ("TOPPADDING", (0,0), (-1,-1), 0),
            ("BOTTOMPADDING", (0,0), (-1,-1), 0),
            ("VALIGN", (0,0), (-1,-1), "TOP")
        ]
        t.setStyle(TableStyle(base + (extra_style or [])))
        return t
    
    def add_para(self, text, style_name='BodyJustify'):
        """Add full-width paragraph"""
        self.story.append(self._table(
            [[Paragraph(text, self.styles[style_name])]], 
            [self.width]
        ))
    
    def add_separator(self, space_before=-6, space_after=4):
        """Add section separator line"""
        self.story.append(Spacer(1, space_before))
        self.story.append(self._table(
            [[""]], 
            [self.width],
            [("LINEBELOW", (0,0), (-1,-1), 0.9, colors.black)]
        ))
        self.story.append(Spacer(1, space_after))
    
    def add_section_title(self, title, space_after=2):
        """Add section title"""
        self.story.append(self._table(
            [[Paragraph(title, self.styles['BodyBold']), ""]], 
            [self.width, 0]
        ))
        self.story.append(Spacer(1, space_after))
    
    def add_two_col_header(self, left_items, right_items, col_ratio=0.65):
        """Add two-column header block"""
        rows = [
            [Paragraph(left, self.styles[l_style]), Paragraph(right, self.styles[r_style])]
            for (left, l_style), (right, r_style) in zip(left_items, right_items)
        ]
        w_left = self.width * col_ratio
        w_right = self.width * (1 - col_ratio)
        self.story.append(self._table(rows, [w_left, w_right]))
    
    def add_bullets(self, bullets, space_after=3):
        """Add bullet list with optional spacing"""
        self.story.append(Spacer(1, 1))
        for bullet in bullets:
            self.add_para("• " + bullet, 'BodyJustify')
        if space_after:
            self.story.append(Spacer(1, space_after))
    
    def add_work_exp(self, company, location, role, dates, bullets, spacing=True):
        """Add work experience entry"""
        self.add_two_col_header(
            [(company, 'BodyBold'), (role, 'Body')],
            [(location, 'BodyRightBold'), (dates, 'BodyRight')]
        )
        self.add_bullets(bullets, space_after=3 if spacing else 0)
    
    def add_project(self, name, link, tech, bullets, spacing=True):
        """Add project entry"""
        self.add_two_col_header(
            [(name, 'BodyBold'), (f"<i>Tech Stack: {tech}</i>", 'BodyItalic')],
            [(link, 'BodyRight'), ("", 'BodyRight')]
        )
        self.add_bullets(bullets, space_after=3 if spacing else 0)
    
    def add_header(self, name, contact):
        """Add resume header"""
        self.add_para(name, 'Name')
        self.story.append(Spacer(1, 2))
        self.add_para(contact, 'Body')
        self.add_separator()
    
    def add_education_section(self, entries):
        """Add education entries"""
        self.add_section_title("EDUCATION")
        for idx, (school, years, degree, cgpa) in enumerate(entries):
            self.add_two_col_header(
                [(school, 'BodyBoldJustify'), (degree, 'BodyJustify')],
                [(years, 'BodyRight'), (cgpa, 'BodyRightBold')]
            )
            if idx < len(entries) - 1:
                self.story.append(Spacer(1, 2))
    
    def build(self):
        """Generate PDF"""
        self.doc.build(self.story)
        return self.output_path


# ==================== Resume Data ====================
DATA = {
    'name': "Jimish Gajjar | Full Stack Developer",
    'contact': (
        "<b>Mobile:</b> +1 (437) 766-4740 | <b>Email:</b> jimish2104gajjar@gmail.com<br/>"
        "<b>LinkedIn:</b> www.linkedin.com/in/jimishgajjar | "
        "<b>Portfolio:</b> www.jimishgajjar.github.io/jimishgajjar | <b>Location:</b> Toronto, ON"
    ),
    'summary': (
        "Product-focused Front-End Engineer with 5+ years building and operating <b>large-scale</b>, <b>24x7</b> "
        "client-facing applications. Expert in <b>React</b>/<b>Redux</b>, <b>JavaScript (ES6+)</b>, <b>HTML5</b>, "
        "<b>CSS3</b>, and <b>REST</b> APIs with a deep focus on <b>cross-browser compatibility</b>, "
        "<b>progressive enhancement</b>, <b>responsive design</b>, <b>website performance</b>, and <b>accessibility</b>. "
        "Experienced shipping high-quality features with <b>unit</b> and <b>integration testing</b>, excellent "
        "documentation, and tight collaboration with design, product, and backend teams."
    ),
    'skills': (
        "<b>Languages:</b> JavaScript (ES6+), TypeScript, HTML5, CSS3, SCSS<br/>"
        "<b>Frontend:</b> React, Next.js, Angular, Tailwind CSS, MUI<br/>"
        "<b>State:</b> Redux Toolkit, Context API<br/>"
        "<b>UI/Docs:</b> Storybook, Design Systems, Documentation<br/>"
        "<b>Build & CI/CD:</b> Webpack, Vite, GitHub Actions, Azure DevOps<br/>"
        "<b>APIs & Data:</b> REST, GraphQL (Apollo)<br/>"
        "<b>Testing:</b> Jest, React Testing Library, Cypress<br/>"
        "<b>Perf & A11y:</b> Lighthouse, WCAG 2.1"
    ),
    'work': [
        {
            'company': "OpenXcell – AI Development Company (CMMI Level 3)",
            'location': "Toronto, ON",
            'role': "Software Engineer (Front-End)",
            'dates': "Jan 2023 – Dec 2023",
            'bullets': [
                "Developed modular <b>React</b> components with <b>Redux</b>, ensuring <b>cross-browser compatibility</b> and <b>accessibility</b>.",
                "Owned features end-to-end with a <b>product</b> mindset; partnered with product/design to optimize flows.",
                "Integrated <b>REST</b> APIs with graceful error states and <b>progressive enhancement</b>.",
                "Improved <b>website performance</b> via code-splitting, memoization, and image optimization.",
                "Wrote <b>unit</b>/<b>integration tests</b> (Jest, RTL) and maintained developer documentation.",
                "Contributed to <b>frontend architecture</b> decisions for scalable delivery experiences."
            ]
        },
        {
            'company': "Nexactly Solutions",
            'location': "Toronto, ON",
            'role': "Front-End Developer",
            'dates': "2022 – 2023",
            'bullets': [
                "Shipped responsive, accessible UIs in <b>React</b>/<b>TypeScript</b> aligned with WCAG 2.1.",
                "Introduced <b>Redux Toolkit</b> patterns to reduce prop-drilling and improve maintainability.",
                "Collaborated with backend to design resilient <b>REST</b> endpoints and contracts.",
                "Optimized <b>performance</b> (LCP/CLS) using preloading, lazy loading, and bundle analysis.",
                "Authored feature docs and helped establish coding standards and review checklists.",
                "Increased test coverage with <b>Jest</b> and <b>Cypress</b> and added CI gates."
            ]
        },
        {
            'company': "Letsbiz",
            'location': "Toronto, ON",
            'role': "Front-End Developer",
            'dates': "2021 – 2022",
            'bullets': [
                "Built SPA modules using <b>React</b>, <b>Redux</b>, and <b>React Router</b> with responsive layouts.",
                "Ensured <b>cross-browser</b> support through a structured test matrix and polyfills.",
                "Implemented design system components (MUI/Tailwind) for consistency and speed.",
                "Improved <b>accessibility</b> (keyboard nav, ARIA labels, focus management).",
                "Partnered with PMs to deliver high-impact product features on schedule.",
                "Instrumented metrics and dashboards to monitor 24x7 user journeys."
            ]
        },
        {
            'company': "X'Pert Infotech",
            'location': "Toronto, ON",
            'role': "Jr. Web Developer",
            'dates': "2020 – 2021",
            'bullets': [
                "Developed interactive dashboards with <b>HTML5</b>, <b>CSS3</b>, and <b>JavaScript</b>.",
                "Refactored legacy views for <b>performance</b> and maintainability.",
                "Collaborated with backend teams on API integrations (<b>REST</b>).",
                "Wrote smoke tests and simple <b>integration tests</b> to prevent regressions.",
                "Contributed to documentation and onboarding guides.",
                "Provided production support for client portals."
            ]
        }
    ],
    'projects': [
        {
            'name': "TrySpeed – AI-Integrated Crypto Payout & Analytics Platform (OpenXcell)",
            'link': "www.tryspeed.com",
            'tech': "React, Next.js, MUI, GraphQL, Highcharts, AWS",
            'bullets': [
                "Built responsive analytics dashboards in <b>React</b>/<b>MUI</b> with interactive <b>Highcharts</b>.",
                "Integrated <b>REST</b>/<b>GraphQL</b> APIs for payouts, settlements, and affiliate workflows.",
                "Improved rendering with hooks and memoization; reduced re-renders on high-traffic routes.",
                "Implemented authentication guards and ISR in <b>Next.js</b>.",
                "Added <b>unit</b>/<b>integration tests</b> (Jest, RTL) for core UI flows.",
                "Documented components and workflows in Storybook."
            ]
        },
        {
            'name': "LIMS – Laboratory Information Management System",
            'link': "N/A",
            'tech': "React, Redux, Node.js, Express, MongoDB",
            'bullets': [
                "Designed specimen tracking UI with filters, facets, and virtualized lists.",
                "Implemented role-based access controls and protected routes.",
                "Standardized <b>REST</b> error handling and empty states.",
                "Ensured <b>accessibility</b> with labels, aria-live regions, and focus trapping.",
                "Stabilized E2E with <b>Cypress</b> retries and fixtures.",
                "Wrote onboarding docs for faster team ramp-up."
            ]
        },
        {
            'name': "ShopSphere – AI-Driven E-Commerce Platform with Mobile App",
            'link': "N/A",
            'tech': "React Native, React, GraphQL, AWS, Tailwind CSS",
            'bullets': [
                "Implemented AI-based recommendations via <b>GraphQL</b> services.",
                "Built mobile-first shopping flows in <b>React Native</b>.",
                "Integrated payments and order tracking with push notifications.",
                "Optimized search with debounced queries and caching.",
                "Established Tailwind UI primitives for rapid iteration.",
                "Added testing and release notes to improve reliability."
            ]
        }
    ],
    'education': [
        ("Algonquin College, Ottawa, ON", "2024 – 2025", 
         "Post Graduate Certificate in Cloud Development and Operations", "CGPA: 3.94/4"),
        ("Conestoga College, Kitchener, ON", "2023 – 2024", 
         "Post Graduate Certificate in Computer Application Development", "CGPA: 3.72/4"),
        ("Silver Oak College of Engineering & Technology, India", "2018 – 2021", 
         "Bachelor of Engineering in Information Technology", "CGPA: 8.41/10")
    ]
}


# ==================== Generate Resume ====================
def generate_compact_resume():
    """Generate optimized 2-page resume without highlights section"""
    builder = OptimizedResumeBuilder(
        "/mnt/data/Jimish Gajjar - Resume (Optimized Compact).pdf",
        "Jimish Gajjar - Resume"
    )
    
    # Header
    builder.add_header(DATA['name'], DATA['contact'])
    
    # Summary
    builder.add_section_title("SUMMARY")
    builder.add_para(DATA['summary'], 'BodyJustify')
    builder.add_separator()
    
    # Skills
    builder.add_section_title("TECHNICAL SKILLS")
    builder.add_para(DATA['skills'], 'BodyJustify')
    builder.add_separator()
    
    # Work Experience
    builder.add_section_title("WORK EXPERIENCE")
    for idx, exp in enumerate(DATA['work']):
        is_last = idx == len(DATA['work']) - 1
        builder.add_work_exp(
            exp['company'], exp['location'], exp['role'],
            exp['dates'], exp['bullets'], spacing=not is_last
        )
    builder.add_separator()
    
    # Projects
    builder.add_section_title("PROJECTS")
    for idx, proj in enumerate(DATA['projects']):
        is_last = idx == len(DATA['projects']) - 1
        builder.add_project(
            proj['name'], proj['link'], proj['tech'],
            proj['bullets'], spacing=not is_last
        )
    builder.add_separator()
    
    # Education (no separator after)
    builder.add_education_section(DATA['education'])
    
    return builder.build()


# Execute
output = generate_compact_resume()
output
