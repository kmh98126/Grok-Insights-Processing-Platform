"""Generate a professional PDF portfolio for the Insights Platform API project."""
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm, cm
from reportlab.lib.colors import (
    HexColor, white, black, Color
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY, TA_RIGHT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable, KeepTogether, Frame, PageTemplate,
    BaseDocTemplate, NextPageTemplate
)
from reportlab.graphics.shapes import Drawing, Rect, String, Line, Circle
from reportlab.graphics import renderPDF
from reportlab.pdfgen import canvas

WIDTH, HEIGHT = A4

PRIMARY = HexColor("#1A1A2E")
SECONDARY = HexColor("#16213E")
ACCENT = HexColor("#0F3460")
HIGHLIGHT = HexColor("#E94560")
LIGHT_BG = HexColor("#F8F9FA")
DARK_TEXT = HexColor("#1A1A2E")
MEDIUM_TEXT = HexColor("#4A4A6A")
LIGHT_TEXT = HexColor("#6C757D")
CODE_BG = HexColor("#2D2D44")
SUCCESS = HexColor("#28A745")
WARNING = HexColor("#FFC107")
INFO = HexColor("#17A2B8")
CARD_BORDER = HexColor("#E0E0E8")
GRADIENT_START = HexColor("#667EEA")
GRADIENT_END = HexColor("#764BA2")

styles = getSampleStyleSheet()

TITLE_COVER = ParagraphStyle(
    "TitleCover", parent=styles["Title"],
    fontSize=38, leading=46, textColor=white,
    alignment=TA_CENTER, fontName="Helvetica-Bold",
    spaceAfter=10,
)
SUBTITLE_COVER = ParagraphStyle(
    "SubtitleCover", parent=styles["Normal"],
    fontSize=16, leading=22, textColor=HexColor("#CCCCEE"),
    alignment=TA_CENTER, fontName="Helvetica",
    spaceAfter=6,
)
SECTION_TITLE = ParagraphStyle(
    "SectionTitle", parent=styles["Heading1"],
    fontSize=22, leading=28, textColor=PRIMARY,
    fontName="Helvetica-Bold", spaceBefore=18, spaceAfter=10,
    borderPadding=(0, 0, 4, 0),
)
SUBSECTION_TITLE = ParagraphStyle(
    "SubsectionTitle", parent=styles["Heading2"],
    fontSize=15, leading=20, textColor=ACCENT,
    fontName="Helvetica-Bold", spaceBefore=14, spaceAfter=6,
)
BODY = ParagraphStyle(
    "BodyCustom", parent=styles["Normal"],
    fontSize=10.5, leading=16, textColor=DARK_TEXT,
    fontName="Helvetica", alignment=TA_JUSTIFY,
    spaceAfter=6,
)
BODY_SMALL = ParagraphStyle(
    "BodySmall", parent=BODY,
    fontSize=9.5, leading=14,
)
BULLET = ParagraphStyle(
    "BulletCustom", parent=BODY,
    fontSize=10.5, leading=16, leftIndent=20,
    bulletIndent=8, spaceAfter=4,
)
CODE_STYLE = ParagraphStyle(
    "CodeStyle", parent=styles["Code"],
    fontSize=8.5, leading=12, textColor=HexColor("#E0E0E0"),
    fontName="Courier", backColor=CODE_BG,
    leftIndent=10, rightIndent=10,
    spaceBefore=4, spaceAfter=4,
    borderPadding=(6, 6, 6, 6),
)
CODE_INLINE = ParagraphStyle(
    "CodeInline", parent=BODY,
    fontSize=9.5, fontName="Courier", textColor=HIGHLIGHT,
)
CAPTION = ParagraphStyle(
    "Caption", parent=styles["Normal"],
    fontSize=8.5, leading=12, textColor=LIGHT_TEXT,
    alignment=TA_CENTER, fontName="Helvetica-Oblique",
    spaceAfter=10,
)
FOOTER_STYLE = ParagraphStyle(
    "Footer", parent=styles["Normal"],
    fontSize=8, textColor=LIGHT_TEXT, alignment=TA_CENTER,
)
TAG_STYLE = ParagraphStyle(
    "Tag", parent=styles["Normal"],
    fontSize=9, textColor=white, fontName="Helvetica-Bold",
    alignment=TA_CENTER,
)


def draw_background(c, doc):
    """Draw page background with header/footer."""
    c.saveState()
    c.setFillColor(LIGHT_BG)
    c.rect(0, 0, WIDTH, HEIGHT, fill=1, stroke=0)
    c.setFillColor(white)
    c.rect(1.5 * cm, 1.5 * cm, WIDTH - 3 * cm, HEIGHT - 3 * cm, fill=1, stroke=0)
    c.setStrokeColor(CARD_BORDER)
    c.setLineWidth(0.5)
    c.rect(1.5 * cm, 1.5 * cm, WIDTH - 3 * cm, HEIGHT - 3 * cm, fill=0, stroke=1)
    c.setStrokeColor(HIGHLIGHT)
    c.setLineWidth(2)
    c.line(1.5 * cm, HEIGHT - 2.2 * cm, WIDTH - 1.5 * cm, HEIGHT - 2.2 * cm)
    c.setFont("Helvetica-Bold", 9)
    c.setFillColor(PRIMARY)
    c.drawString(2 * cm, HEIGHT - 2 * cm, "Insights Platform API  |  Project Portfolio")
    c.setFont("Helvetica", 8)
    c.setFillColor(LIGHT_TEXT)
    page_num = doc.page
    c.drawRightString(WIDTH - 2 * cm, 1.8 * cm, f"Page {page_num}")
    c.drawString(2 * cm, 1.8 * cm, "Insights Platform API Portfolio  |  2025")
    c.restoreState()


def draw_cover(c, doc):
    """Draw cover page background."""
    c.saveState()
    c.setFillColor(PRIMARY)
    c.rect(0, 0, WIDTH, HEIGHT, fill=1, stroke=0)
    c.setFillColor(SECONDARY)
    c.rect(0, HEIGHT * 0.35, WIDTH, HEIGHT * 0.65, fill=1, stroke=0)
    c.setStrokeColor(HIGHLIGHT)
    c.setLineWidth(4)
    c.line(WIDTH * 0.1, HEIGHT * 0.35, WIDTH * 0.9, HEIGHT * 0.35)
    for i in range(5):
        c.setStrokeColor(Color(0.06, 0.08, 0.24, 0.1 + i * 0.03))
        c.setLineWidth(0.5)
        y = HEIGHT * 0.42 + i * 25
        c.line(WIDTH * 0.05, y, WIDTH * 0.95, y)
    shapes_color = Color(0.91, 0.27, 0.38, 0.15)
    c.setFillColor(shapes_color)
    c.circle(WIDTH * 0.85, HEIGHT * 0.75, 60, fill=1, stroke=0)
    c.circle(WIDTH * 0.15, HEIGHT * 0.55, 40, fill=1, stroke=0)
    c.circle(WIDTH * 0.7, HEIGHT * 0.2, 30, fill=1, stroke=0)
    c.restoreState()


def make_section_header(title, icon_text=""):
    """Create a styled section header with colored bar."""
    elements = []
    d = Drawing(WIDTH - 4 * cm, 3)
    d.add(Rect(0, 0, 60, 3, fillColor=HIGHLIGHT, strokeColor=None))
    d.add(Rect(62, 0, WIDTH - 4 * cm - 62, 3, fillColor=CARD_BORDER, strokeColor=None))
    elements.append(d)
    elements.append(Spacer(1, 4))
    display = f"{icon_text}  {title}" if icon_text else title
    elements.append(Paragraph(display, SECTION_TITLE))
    elements.append(Spacer(1, 4))
    return elements


def make_card(content_elements, bg_color=white, border_color=CARD_BORDER):
    """Wrap content in a card-like table."""
    inner = Table(
        [[content_elements]],
        colWidths=[WIDTH - 5 * cm],
    )
    inner.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), bg_color),
        ("BOX", (0, 0), (-1, -1), 0.5, border_color),
        ("TOPPADDING", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
        ("LEFTPADDING", (0, 0), (-1, -1), 12),
        ("RIGHTPADDING", (0, 0), (-1, -1), 12),
        ("ROUNDEDCORNERS", [4, 4, 4, 4]),
    ]))
    return inner


def make_tech_badge(text, color=ACCENT):
    """Create a tech badge as a small colored table."""
    t = Table([[Paragraph(text, TAG_STYLE)]], colWidths=[None])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), color),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("ROUNDEDCORNERS", [10, 10, 10, 10]),
    ]))
    return t


def build_cover_page():
    """Build cover page elements."""
    elements = []
    elements.append(Spacer(1, HEIGHT * 0.22))
    elements.append(Paragraph("INSIGHTS PLATFORM API", TITLE_COVER))
    elements.append(Spacer(1, 8))
    elements.append(Paragraph(
        "Twitter Conversation Analysis with Grok AI",
        SUBTITLE_COVER
    ))
    elements.append(Spacer(1, 20))

    divider_style = ParagraphStyle(
        "Divider", parent=styles["Normal"],
        fontSize=14, textColor=HIGHLIGHT,
        alignment=TA_CENTER, fontName="Helvetica",
    )
    elements.append(Paragraph("______________________________", divider_style))
    elements.append(Spacer(1, 20))

    info_style = ParagraphStyle(
        "CoverInfo", parent=styles["Normal"],
        fontSize=12, leading=20, textColor=HexColor("#AAAACC"),
        alignment=TA_CENTER, fontName="Helvetica",
    )
    elements.append(Paragraph("Project Portfolio Document", info_style))
    elements.append(Spacer(1, 6))
    elements.append(Paragraph(
        "FastAPI  &bull;  Grok AI  &bull;  SQLAlchemy  &bull;  Docker",
        info_style
    ))
    elements.append(Spacer(1, 30))

    date_style = ParagraphStyle(
        "CoverDate", parent=styles["Normal"],
        fontSize=10, textColor=HexColor("#888899"),
        alignment=TA_CENTER, fontName="Helvetica",
    )
    elements.append(Paragraph("2025", date_style))
    elements.append(NextPageTemplate("content"))
    elements.append(PageBreak())
    return elements


def build_toc():
    """Build Table of Contents."""
    elements = []
    elements.extend(make_section_header("Table of Contents"))
    elements.append(Spacer(1, 10))

    toc_items = [
        ("01", "Project Overview", "Project summary and objectives"),
        ("02", "Key Features", "Core features and capabilities"),
        ("03", "System Architecture", "Architecture and data flow design"),
        ("04", "Technology Stack", "Frameworks and libraries used"),
        ("05", "API Design", "RESTful API endpoint specifications"),
        ("06", "Database Design", "Data models and schema design"),
        ("07", "Core Components", "Detailed component breakdown"),
        ("08", "Rate Limiting & Performance", "Performance optimization strategies"),
        ("09", "Deployment", "Docker containerization and deployment"),
        ("10", "Project Structure", "File and directory organization"),
        ("11", "Challenges & Solutions", "Technical decisions and problem-solving"),
    ]

    for num, title, desc in toc_items:
        num_style = ParagraphStyle("TocNum", parent=BODY, fontSize=12, textColor=HIGHLIGHT, fontName="Helvetica-Bold")
        title_style = ParagraphStyle("TocTitle", parent=BODY, fontSize=11, textColor=PRIMARY, fontName="Helvetica-Bold")
        desc_style = ParagraphStyle("TocDesc", parent=BODY, fontSize=9, textColor=LIGHT_TEXT)

        row = Table(
            [[Paragraph(num, num_style), Paragraph(title, title_style), Paragraph(desc, desc_style)]],
            colWidths=[1.2 * cm, 5 * cm, 9 * cm],
        )
        row.setStyle(TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ("LINEBELOW", (0, 0), (-1, -1), 0.3, CARD_BORDER),
        ]))
        elements.append(row)

    elements.append(PageBreak())
    return elements


def build_overview():
    """Build Project Overview section."""
    elements = []
    elements.extend(make_section_header("01  Project Overview"))

    elements.append(Paragraph(
        "Insights Platform API is a production-ready backend system designed for real-time analysis of "
        "Twitter conversations using xAI's Grok AI model. The platform receives raw conversation data through "
        "a RESTful API, processes it asynchronously using AI-powered sentiment analysis and topic clustering, "
        "and provides structured insights through queryable endpoints.",
        BODY
    ))
    elements.append(Spacer(1, 8))

    elements.append(Paragraph("Project Objectives", SUBSECTION_TITLE))
    objectives = [
        "Build a high-performance async API capable of handling 100+ requests/second",
        "Integrate Grok AI for intelligent sentiment analysis and topic categorization",
        "Implement robust rate limiting to manage both inbound traffic and external API calls",
        "Design an efficient background batch processing system for scalable data analysis",
        "Create a containerized deployment with strict resource constraints (2 CPU, 1GB RAM)",
        "Provide filtered and paginated insight retrieval with confidence-based scoring",
    ]
    for obj in objectives:
        elements.append(Paragraph(f"&bull;  {obj}", BULLET))

    elements.append(Spacer(1, 10))

    elements.append(Paragraph("Use Case Scenario", SUBSECTION_TITLE))
    elements.append(Paragraph(
        "A customer service platform collects thousands of Twitter conversations daily. The Insights Platform API "
        "ingests this data, analyzes each conversation for sentiment polarity (-1.0 to +1.0), identifies topic "
        "clusters (e.g., \"delivery_problems\", \"product_issues\", \"praise\"), and assigns a confidence score. "
        "Support teams can then query insights filtered by time range, sentiment type, and confidence threshold "
        "to prioritize responses and identify emerging trends.",
        BODY
    ))

    elements.append(Spacer(1, 10))
    summary_data = [
        ["Metric", "Value"],
        ["API Framework", "FastAPI (Python 3.11+)"],
        ["AI Engine", "Grok AI (xAI)"],
        ["Database", "SQLite (async via aiosqlite)"],
        ["Inbound Rate Limit", "100 requests/second"],
        ["Grok API Rate Limit", "10 calls/second"],
        ["Batch Size", "10 conversations per cycle"],
        ["Max Query Results", "1,000 per request"],
        ["Deployment", "Docker (2 CPU, 1GB RAM)"],
    ]
    summary_table = Table(summary_data, colWidths=[6 * cm, 10 * cm])
    summary_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), ACCENT),
        ("TEXTCOLOR", (0, 0), (-1, 0), white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("BACKGROUND", (0, 1), (-1, -1), white),
        ("GRID", (0, 0), (-1, -1), 0.5, CARD_BORDER),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [white, LIGHT_BG]),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    elements.append(summary_table)
    elements.append(PageBreak())
    return elements


def build_features():
    """Build Key Features section."""
    elements = []
    elements.extend(make_section_header("02  Key Features"))

    features = [
        (
            "RESTful API Design",
            "Clean, well-documented REST API built with FastAPI. Supports conversation submission (POST) "
            "and insight retrieval (GET) with comprehensive request validation using Pydantic models. "
            "Follows HTTP semantics with proper status codes (202 Accepted, 429 Too Many Requests, 400 Bad Request).",
            ACCENT
        ),
        (
            "Grok AI Integration",
            "Deep integration with xAI's Grok model for advanced NLP analysis. Each conversation is analyzed "
            "for sentiment polarity (score from -1.0 to 1.0), topic clustering (identifying categories like "
            "\"product_issues\", \"delivery_problems\", \"praise\"), and confidence scoring. Structured prompt "
            "engineering ensures consistent JSON output from the AI model.",
            HIGHLIGHT
        ),
        (
            "Asynchronous Batch Processing",
            "Background batch processor that polls for pending conversations every 5 seconds, processes them "
            "in batches of 10 with parallel execution, and manages status transitions (pending -> processing -> "
            "completed/failed). Individual failures don't affect the batch, ensuring resilience.",
            SUCCESS
        ),
        (
            "Dual Rate Limiting",
            "Two-tier rate limiting system: inbound API traffic is limited to 100 requests/second using a "
            "token bucket algorithm with sliding window, while outbound Grok API calls are throttled to "
            "10 calls/second using semaphore-based concurrency control with time-window tracking.",
            INFO
        ),
        (
            "Advanced Query Filtering",
            "Insight retrieval supports powerful filtering: time range queries (ISO8601), sentiment type "
            "filtering (positive/negative/neutral), minimum confidence thresholds (0.0-1.0), and pagination "
            "with configurable limits (up to 1,000 results). Results are ordered by timestamp descending.",
            GRADIENT_START
        ),
        (
            "Docker Containerization",
            "Production-ready Docker setup with multi-stage build, resource constraints (2 CPU cores, "
            "1GB RAM, 512MB reserved), persistent database volume mounting, and Docker Compose orchestration. "
            "Optimized for lightweight deployment on constrained infrastructure.",
            SECONDARY
        ),
    ]

    for title, desc, color in features:
        feature_title = ParagraphStyle("FeatTitle", parent=SUBSECTION_TITLE, textColor=color, fontSize=13)
        card_content = []
        card_content.append(Paragraph(title, feature_title))
        card_content.append(Paragraph(desc, BODY_SMALL))

        inner_table = Table([[c] for c in card_content], colWidths=[WIDTH - 5.5 * cm])
        inner_table.setStyle(TableStyle([
            ("TOPPADDING", (0, 0), (-1, -1), 2),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
            ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ]))

        card = Table(
            [[inner_table]],
            colWidths=[WIDTH - 4.5 * cm],
        )
        card.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), white),
            ("BOX", (0, 0), (-1, -1), 0.5, CARD_BORDER),
            ("LINEBEFOREDECL", (0, 0), (0, -1)),
            ("TOPPADDING", (0, 0), (-1, -1), 10),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
            ("LEFTPADDING", (0, 0), (-1, -1), 14),
            ("RIGHTPADDING", (0, 0), (-1, -1), 12),
        ]))
        left_bar = Table(
            [[None, card]],
            colWidths=[4, WIDTH - 4.5 * cm],
        )
        left_bar.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (0, -1), color),
            ("TOPPADDING", (0, 0), (-1, -1), 0),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
            ("LEFTPADDING", (0, 0), (-1, -1), 0),
            ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ]))
        elements.append(left_bar)
        elements.append(Spacer(1, 8))

    elements.append(PageBreak())
    return elements


def build_architecture():
    """Build System Architecture section."""
    elements = []
    elements.extend(make_section_header("03  System Architecture"))

    elements.append(Paragraph("Architecture Overview", SUBSECTION_TITLE))
    elements.append(Paragraph(
        "The system follows an event-driven, asynchronous architecture pattern. Conversations are submitted "
        "through the REST API and immediately stored with a \"pending\" status. A background batch processor "
        "continuously polls for unprocessed conversations, sends them to Grok AI for analysis, and stores "
        "the structured insights back in the database. This decoupled design ensures fast API response times "
        "(202 Accepted) while handling AI processing asynchronously.",
        BODY
    ))
    elements.append(Spacer(1, 10))

    elements.append(Paragraph("Data Flow - Conversation Submission", SUBSECTION_TITLE))
    flow1_data = [
        ["Step", "Component", "Action", "Output"],
        ["1", "Client", "POST /api/v1/conversations", "HTTP Request"],
        ["2", "Rate Limiter", "Token bucket check (100 req/s)", "Allow / 429 Reject"],
        ["3", "Pydantic Schema", "Validate request body", "ConversationRequest"],
        ["4", "SQLAlchemy ORM", "Insert to conversations table", "status: pending"],
        ["5", "FastAPI", "Return response", "202 Accepted + conv_id"],
    ]
    flow1_table = Table(flow1_data, colWidths=[1.2 * cm, 3.2 * cm, 5 * cm, 4.5 * cm])
    flow1_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), ACCENT),
        ("TEXTCOLOR", (0, 0), (-1, 0), white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("GRID", (0, 0), (-1, -1), 0.5, CARD_BORDER),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [white, LIGHT_BG]),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    elements.append(flow1_table)
    elements.append(Spacer(1, 14))

    elements.append(Paragraph("Data Flow - Background Processing", SUBSECTION_TITLE))
    flow2_data = [
        ["Step", "Component", "Action", "Output"],
        ["1", "Batch Processor", "Poll DB every 5 seconds", "Pending conversations"],
        ["2", "Batch Processor", "Update status to processing", "Batch of 10"],
        ["3", "Grok Client", "Send to Grok API (10 calls/s)", "AI Analysis JSON"],
        ["4", "Grok Client", "Parse & validate response", "Structured insight data"],
        ["5", "SQLAlchemy ORM", "Insert insight + update status", "status: completed"],
    ]
    flow2_table = Table(flow2_data, colWidths=[1.2 * cm, 3.2 * cm, 5.2 * cm, 4.3 * cm])
    flow2_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), HIGHLIGHT),
        ("TEXTCOLOR", (0, 0), (-1, 0), white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("GRID", (0, 0), (-1, -1), 0.5, CARD_BORDER),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [white, LIGHT_BG]),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    elements.append(flow2_table)
    elements.append(Spacer(1, 14))

    elements.append(Paragraph("Data Flow - Insights Retrieval", SUBSECTION_TITLE))
    flow3_data = [
        ["Step", "Component", "Action", "Output"],
        ["1", "Client", "GET /api/v1/insights?params", "HTTP Request"],
        ["2", "FastAPI", "Parse & validate query params", "Typed parameters"],
        ["3", "SQLAlchemy ORM", "Build filtered query", "SQL with WHERE clauses"],
        ["4", "Database", "Execute with indexes", "Insight records"],
        ["5", "FastAPI", "Serialize to JSON", "InsightsResponse + metadata"],
    ]
    flow3_table = Table(flow3_data, colWidths=[1.2 * cm, 3.2 * cm, 5 * cm, 4.5 * cm])
    flow3_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), SUCCESS),
        ("TEXTCOLOR", (0, 0), (-1, 0), white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("GRID", (0, 0), (-1, -1), 0.5, CARD_BORDER),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [white, LIGHT_BG]),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    elements.append(flow3_table)

    elements.append(Spacer(1, 14))
    elements.append(Paragraph("Design Principles", SUBSECTION_TITLE))
    principles = [
        "<b>Separation of Concerns</b> - API handling, data persistence, AI processing, and rate limiting "
        "are isolated into dedicated modules (main.py, models.py, grok_client.py, rate_limiter.py).",
        "<b>Async-First Design</b> - Every I/O operation uses async/await, from database queries (aiosqlite) "
        "to HTTP calls (httpx), maximizing throughput on limited CPU resources.",
        "<b>Graceful Degradation</b> - Individual conversation processing failures are isolated; the batch "
        "processor continues with remaining items. JSON parsing failures fall back to default values.",
        "<b>Resource Awareness</b> - SQLite chosen over PostgreSQL to minimize memory footprint. Batch sizes "
        "and concurrency limits are tuned for the 2-core, 1GB RAM constraint.",
    ]
    for p in principles:
        elements.append(Paragraph(f"&bull;  {p}", BULLET))

    elements.append(PageBreak())
    return elements


def build_tech_stack():
    """Build Technology Stack section."""
    elements = []
    elements.extend(make_section_header("04  Technology Stack"))

    elements.append(Paragraph(
        "The technology stack was carefully selected to balance performance, developer productivity, "
        "and resource efficiency within the 2-core CPU and 1GB RAM constraints.",
        BODY
    ))
    elements.append(Spacer(1, 10))

    tech_data = [
        ["Category", "Technology", "Version", "Purpose"],
        ["Web Framework", "FastAPI", "0.121.3", "High-performance async API framework with auto-generated docs"],
        ["ASGI Server", "Uvicorn", "0.38.0", "Lightning-fast ASGI server for production deployment"],
        ["Validation", "Pydantic", "2.12.4", "Data validation and serialization with type hints"],
        ["ORM", "SQLAlchemy", "2.0.36", "Async ORM for database operations with 2.0 style"],
        ["Database", "SQLite + aiosqlite", "0.20.0", "Lightweight async database for resource-constrained env"],
        ["HTTP Client", "httpx", "0.27.2", "Modern async HTTP client for Grok API communication"],
        ["Rate Limiting", "Custom + slowapi", "0.1.9", "Token bucket and semaphore-based rate control"],
        ["Containerization", "Docker", "3.8", "Containerized deployment with resource limits"],
        ["Language", "Python", "3.11+", "Modern Python with async/await native support"],
    ]
    tech_table = Table(tech_data, colWidths=[2.8 * cm, 3.5 * cm, 1.8 * cm, 7.5 * cm])
    tech_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), PRIMARY),
        ("TEXTCOLOR", (0, 0), (-1, 0), white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("GRID", (0, 0), (-1, -1), 0.5, CARD_BORDER),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [white, LIGHT_BG]),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    elements.append(tech_table)
    elements.append(Spacer(1, 12))

    elements.append(Paragraph("Why FastAPI?", SUBSECTION_TITLE))
    elements.append(Paragraph(
        "FastAPI was chosen as the web framework for several critical reasons: native async/await support "
        "for high-concurrency workloads, automatic OpenAPI documentation generation, Pydantic integration "
        "for request/response validation, dependency injection system for clean database session management, "
        "and exceptional performance benchmarks that rival Node.js and Go frameworks. Its type-hint-driven "
        "development approach also reduces bugs and improves code maintainability.",
        BODY
    ))

    elements.append(Paragraph("Why SQLite over PostgreSQL?", SUBSECTION_TITLE))
    elements.append(Paragraph(
        "Given the resource constraints of 1GB RAM, SQLite was selected over PostgreSQL for several reasons: "
        "zero configuration and no separate server process required, minimal memory footprint (operates "
        "within the application process), sufficient performance for the expected workload, and simplified "
        "deployment with Docker volume mounting. The async wrapper (aiosqlite) ensures non-blocking I/O "
        "despite SQLite's inherently synchronous nature.",
        BODY
    ))

    elements.append(Paragraph("Why Grok AI?", SUBSECTION_TITLE))
    elements.append(Paragraph(
        "xAI's Grok model provides state-of-the-art natural language understanding with a focus on "
        "Twitter/X platform content. Its API follows the OpenAI-compatible chat completions format, "
        "making it straightforward to integrate. The model excels at understanding social media language "
        "patterns, informal text, and context-dependent sentiment, which is critical for accurate "
        "Twitter conversation analysis.",
        BODY
    ))

    elements.append(PageBreak())
    return elements


def build_api_design():
    """Build API Design section."""
    elements = []
    elements.extend(make_section_header("05  API Design"))

    elements.append(Paragraph(
        "The API follows RESTful design principles with clear resource naming, proper HTTP method usage, "
        "appropriate status codes, and consistent error response formats.",
        BODY
    ))
    elements.append(Spacer(1, 10))

    elements.append(Paragraph("Endpoint: POST /api/v1/conversations", SUBSECTION_TITLE))
    elements.append(Paragraph(
        "Submits a new conversation for AI-powered analysis. Returns immediately with 202 Accepted "
        "status, indicating the conversation has been queued for background processing.",
        BODY
    ))

    req_data = [
        ["Field", "Type", "Required", "Description"],
        ["text", "string", "Yes", "Conversation text content (min 1 char)"],
        ["author", "string", "No", "Author username or identifier"],
        ["timestamp", "ISO8601 datetime", "No", "Conversation timestamp (defaults to now)"],
        ["raw_data", "object", "No", "Additional metadata (stored as JSON)"],
    ]
    req_table = Table(req_data, colWidths=[2.5 * cm, 3.2 * cm, 2 * cm, 8 * cm])
    req_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), ACCENT),
        ("TEXTCOLOR", (0, 0), (-1, 0), white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("GRID", (0, 0), (-1, -1), 0.5, CARD_BORDER),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [white, LIGHT_BG]),
    ]))
    elements.append(Paragraph("<b>Request Body:</b>", BODY))
    elements.append(req_table)
    elements.append(Spacer(1, 6))

    resp_data = [
        ["Status Code", "Condition", "Response Body"],
        ["202 Accepted", "Success", '{"status": "accepted", "conversation_id": "conv_xxx", "message": "..."}'],
        ["429 Too Many Requests", "Rate limit exceeded", '{"error": "rate_limit_exceeded", "retry_after": 5}'],
        ["400 Bad Request", "Invalid schema", '{"error": "invalid_schema", "details": "..."}'],
    ]
    resp_table = Table(resp_data, colWidths=[3.8 * cm, 3.5 * cm, 8.5 * cm])
    resp_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), HIGHLIGHT),
        ("TEXTCOLOR", (0, 0), (-1, 0), white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 8.5),
        ("GRID", (0, 0), (-1, -1), 0.5, CARD_BORDER),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [white, LIGHT_BG]),
        ("FONTNAME", (0, 1), (-1, -1), "Courier"),
    ]))
    elements.append(Paragraph("<b>Response Codes:</b>", BODY))
    elements.append(resp_table)
    elements.append(Spacer(1, 14))

    elements.append(Paragraph("Endpoint: GET /api/v1/insights", SUBSECTION_TITLE))
    elements.append(Paragraph(
        "Retrieves analyzed insights with powerful filtering capabilities. Supports time-range queries, "
        "sentiment filtering, confidence thresholds, and pagination.",
        BODY
    ))

    query_data = [
        ["Parameter", "Type", "Required", "Description"],
        ["start_time", "ISO8601 datetime", "Yes", "Start of time range filter"],
        ["end_time", "ISO8601 datetime", "Yes", "End of time range filter"],
        ["limit", "integer (1-1000)", "No", "Maximum results to return (default: 100)"],
        ["min_confidence", "float (0.0-1.0)", "No", "Minimum confidence score threshold"],
        ["sentiment", "enum", "No", "Filter: positive / negative / neutral"],
    ]
    query_table = Table(query_data, colWidths=[2.8 * cm, 3.2 * cm, 2 * cm, 7.7 * cm])
    query_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), SUCCESS),
        ("TEXTCOLOR", (0, 0), (-1, 0), white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("GRID", (0, 0), (-1, -1), 0.5, CARD_BORDER),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [white, LIGHT_BG]),
    ]))
    elements.append(Paragraph("<b>Query Parameters:</b>", BODY))
    elements.append(query_table)
    elements.append(Spacer(1, 6))

    elements.append(Paragraph("<b>Response Structure:</b>", BODY))
    elements.append(Paragraph(
        "The response includes an <font face='Courier' color='#E94560'>insights</font> array containing "
        "analyzed conversations and a <font face='Courier' color='#E94560'>metadata</font> object with "
        "pagination info (total_count, returned_count, start_time, end_time). Each insight contains the "
        "original text, conversation_id, timestamp, and a nested grok_analysis object with sentiment_score, "
        "clusters array, confidence score, and reasoning text.",
        BODY
    ))

    elements.append(Spacer(1, 10))
    elements.append(Paragraph("Endpoint: GET /health", SUBSECTION_TITLE))
    elements.append(Paragraph(
        "Simple health check endpoint returning <font face='Courier' color='#E94560'>"
        "{\"status\": \"ok\"}</font>. Used for Docker health checks, load balancer probes, "
        "and monitoring systems.",
        BODY
    ))

    elements.append(PageBreak())
    return elements


def build_database():
    """Build Database Design section."""
    elements = []
    elements.extend(make_section_header("06  Database Design"))

    elements.append(Paragraph(
        "The database uses two core tables with a one-to-one relationship between conversations and their "
        "analysis results. Strategic indexing ensures fast queries even as data grows.",
        BODY
    ))
    elements.append(Spacer(1, 10))

    elements.append(Paragraph("Conversations Table", SUBSECTION_TITLE))
    conv_data = [
        ["Column", "Type", "Constraints", "Description"],
        ["id", "String (PK)", "Auto-generated", "Format: conv_{uuid8} (e.g., conv_a1b2c3d4)"],
        ["text", "String", "NOT NULL", "Raw conversation text content"],
        ["author", "String", "Nullable", "Author username or identifier"],
        ["timestamp", "DateTime", "NOT NULL, Indexed", "Conversation timestamp"],
        ["raw_data", "JSON", "Nullable", "Original metadata stored as JSON"],
        ["status", "String", "Indexed", "pending | processing | completed | failed"],
        ["created_at", "DateTime", "Auto-set", "Record creation timestamp"],
    ]
    conv_table = Table(conv_data, colWidths=[2.3 * cm, 2.8 * cm, 3 * cm, 7.5 * cm])
    conv_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), PRIMARY),
        ("TEXTCOLOR", (0, 0), (-1, 0), white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 8.5),
        ("GRID", (0, 0), (-1, -1), 0.5, CARD_BORDER),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [white, LIGHT_BG]),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    elements.append(conv_table)
    elements.append(Spacer(1, 4))
    elements.append(Paragraph(
        "Indexes: idx_conv_timestamp (timestamp), idx_conv_status (status)",
        CAPTION
    ))
    elements.append(Spacer(1, 12))

    elements.append(Paragraph("Insights Table", SUBSECTION_TITLE))
    ins_data = [
        ["Column", "Type", "Constraints", "Description"],
        ["id", "Integer (PK)", "Auto-increment", "Sequential primary key"],
        ["conversation_id", "String (FK)", "NOT NULL, Indexed", "References conversations.id"],
        ["timestamp", "DateTime", "NOT NULL, Indexed", "Original conversation timestamp"],
        ["text", "String", "NOT NULL", "Conversation text (denormalized for fast access)"],
        ["sentiment_score", "Float", "Indexed", "Sentiment polarity: -1.0 to +1.0"],
        ["clusters", "JSON", "Nullable", "Topic categories array (e.g., [\"praise\", \"product\"])"],
        ["confidence", "Float", "Indexed", "Analysis confidence: 0.0 to 1.0"],
        ["reasoning", "String", "Nullable", "AI explanation of the analysis"],
        ["grok_analysis", "JSON", "Nullable", "Full Grok API response (for debugging)"],
        ["created_at", "DateTime", "Auto-set", "Record creation timestamp"],
    ]
    ins_table = Table(ins_data, colWidths=[2.5 * cm, 2.5 * cm, 3 * cm, 7.6 * cm])
    ins_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), HIGHLIGHT),
        ("TEXTCOLOR", (0, 0), (-1, 0), white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 8.5),
        ("GRID", (0, 0), (-1, -1), 0.5, CARD_BORDER),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [white, LIGHT_BG]),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    elements.append(ins_table)
    elements.append(Spacer(1, 4))
    elements.append(Paragraph(
        "Indexes: idx_insight_conversation_id, idx_insight_timestamp, idx_insight_sentiment, idx_insight_confidence",
        CAPTION
    ))

    elements.append(Spacer(1, 12))
    elements.append(Paragraph("Indexing Strategy", SUBSECTION_TITLE))
    elements.append(Paragraph(
        "Strategic indexing is applied to columns frequently used in WHERE clauses and JOIN conditions. "
        "The conversations table indexes <font face='Courier' color='#E94560'>status</font> for efficient "
        "batch processor polling and <font face='Courier' color='#E94560'>timestamp</font> for time-range "
        "queries. The insights table indexes <font face='Courier' color='#E94560'>conversation_id</font> "
        "for relationship lookups, <font face='Courier' color='#E94560'>timestamp</font> for range queries, "
        "<font face='Courier' color='#E94560'>sentiment_score</font> for sentiment filtering, and "
        "<font face='Courier' color='#E94560'>confidence</font> for threshold filtering.",
        BODY
    ))

    elements.append(PageBreak())
    return elements


def build_components():
    """Build Core Components section."""
    elements = []
    elements.extend(make_section_header("07  Core Components"))

    components = [
        {
            "name": "main.py - FastAPI Application",
            "lines": "248 lines",
            "desc": (
                "The application entry point that initializes FastAPI, defines all API endpoints, manages "
                "the application lifecycle (startup/shutdown events), and coordinates between rate limiting, "
                "database, and batch processing components. Uses FastAPI's dependency injection for database "
                "session management and implements comprehensive error handling with proper HTTP status codes."
            ),
            "highlights": [
                "Lifecycle management: Database initialization and batch processor start/stop",
                "Rate limiting integration at the endpoint level",
                "Pydantic model-based request/response validation",
                "Dynamic query building with SQLAlchemy for filtered insights retrieval",
                "Comprehensive error handling with rollback support",
            ],
        },
        {
            "name": "grok_client.py - Grok AI Client",
            "lines": "139 lines",
            "desc": (
                "Handles all communication with xAI's Grok API. Implements structured prompt engineering "
                "for consistent JSON output, semaphore-based rate limiting (10 calls/second), retry logic "
                "with exponential backoff, and robust response parsing that handles markdown code block "
                "wrapping from the AI model."
            ),
            "highlights": [
                "Prompt engineering for structured sentiment analysis and topic clustering",
                "Semaphore + sliding window rate limiting (10 calls/second)",
                "Markdown code block stripping from Grok responses",
                "Exponential backoff retry (3 attempts) for transient failures",
                "Graceful fallback with default values on JSON parsing errors",
                "429 rate limit response handling with Retry-After header support",
            ],
        },
        {
            "name": "batch_processor.py - Background Processor",
            "lines": "115 lines",
            "desc": (
                "An asyncio-based background task that continuously processes pending conversations. "
                "Uses asyncio.create_task for non-blocking execution, asyncio.gather for parallel batch "
                "processing, and proper status state machine management."
            ),
            "highlights": [
                "Polling loop: checks for pending conversations every 5 seconds",
                "Batch processing: 10 conversations per cycle with parallel execution",
                "Status state machine: pending -> processing -> completed/failed",
                "Error isolation: individual failures don't affect the batch",
                "Graceful shutdown with task cancellation support",
            ],
        },
        {
            "name": "rate_limiter.py - Rate Limiting Engine",
            "lines": "57 lines",
            "desc": (
                "Implements a token bucket algorithm with sliding window for precise rate limiting. "
                "Uses asyncio.Lock for thread-safe token management and deque for efficient "
                "time-window tracking. Provides Retry-After calculation for 429 responses."
            ),
            "highlights": [
                "Token bucket algorithm with sliding time window",
                "Async lock for safe concurrent access",
                "Configurable max_requests and time_window parameters",
                "Retry-After header value calculation",
                "Global inbound_limiter instance (100 req/s)",
            ],
        },
        {
            "name": "models.py - Database Models",
            "lines": "55 lines",
            "desc": (
                "SQLAlchemy 2.0 declarative models defining the database schema. Uses Column definitions "
                "with proper types, constraints, and strategic indexes for query performance."
            ),
            "highlights": [
                "UUID-based conversation IDs (conv_{hex8} format)",
                "JSON columns for flexible metadata storage",
                "Strategic composite indexes on frequently queried columns",
                "Default value generators for timestamps and IDs",
            ],
        },
        {
            "name": "schemas.py - Pydantic Schemas",
            "lines": "66 lines",
            "desc": (
                "Request/response validation schemas using Pydantic v2. Defines strict type validation, "
                "value ranges, and custom validators. Supports ORM mode for direct model serialization."
            ),
            "highlights": [
                "ConversationRequest with custom text validator (non-empty, trimmed)",
                "GrokAnalysis with bounded float fields (-1.0 to 1.0, 0.0 to 1.0)",
                "SentimentFilter enum for type-safe query parameters",
                "InsightItem with from_attributes config for ORM compatibility",
            ],
        },
    ]

    for comp in components:
        elements.append(Paragraph(comp["name"], SUBSECTION_TITLE))
        meta_style = ParagraphStyle("CompMeta", parent=BODY_SMALL, textColor=LIGHT_TEXT, fontName="Helvetica-Oblique")
        elements.append(Paragraph(comp["lines"], meta_style))
        elements.append(Paragraph(comp["desc"], BODY))
        elements.append(Paragraph("<b>Key Implementation Details:</b>", BODY))
        for h in comp["highlights"]:
            elements.append(Paragraph(f"&bull;  {h}", BULLET))
        elements.append(Spacer(1, 8))

    elements.append(PageBreak())
    return elements


def build_rate_limiting():
    """Build Rate Limiting & Performance section."""
    elements = []
    elements.extend(make_section_header("08  Rate Limiting & Performance"))

    elements.append(Paragraph(
        "The system implements a dual-layer rate limiting strategy to protect both the API server "
        "and the external Grok AI service from overload.",
        BODY
    ))
    elements.append(Spacer(1, 10))

    elements.append(Paragraph("Inbound Rate Limiter (Token Bucket)", SUBSECTION_TITLE))
    elements.append(Paragraph(
        "The inbound rate limiter uses a <b>token bucket algorithm</b> with a sliding time window. "
        "It maintains a deque of request timestamps and removes entries older than the configured "
        "time window (1 second). If the deque length equals the max capacity (100), the request is "
        "rejected with a 429 status code and a calculated Retry-After header.",
        BODY
    ))

    inbound_data = [
        ["Parameter", "Value", "Description"],
        ["Algorithm", "Token Bucket", "Sliding window with timestamp deque"],
        ["Max Requests", "100 / second", "Maximum inbound API requests"],
        ["Time Window", "1.0 second", "Sliding window duration"],
        ["Concurrency", "asyncio.Lock", "Thread-safe async access"],
        ["Rejection", "HTTP 429", "Includes Retry-After header"],
    ]
    inbound_table = Table(inbound_data, colWidths=[3 * cm, 3.5 * cm, 9 * cm])
    inbound_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), ACCENT),
        ("TEXTCOLOR", (0, 0), (-1, 0), white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("GRID", (0, 0), (-1, -1), 0.5, CARD_BORDER),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [white, LIGHT_BG]),
    ]))
    elements.append(inbound_table)
    elements.append(Spacer(1, 14))

    elements.append(Paragraph("Grok API Rate Limiter (Semaphore + Window)", SUBSECTION_TITLE))
    elements.append(Paragraph(
        "The Grok API rate limiter combines an <b>asyncio.Semaphore</b> (limiting to 10 concurrent calls) "
        "with a <b>time-window tracker</b> that maintains a list of recent call timestamps. If 10 calls "
        "have been made within the last second, the system calculates the precise wait time and sleeps "
        "before proceeding. This dual approach prevents both burst overload and sustained rate violation.",
        BODY
    ))

    grok_data = [
        ["Parameter", "Value", "Description"],
        ["Concurrency Limit", "10 simultaneous", "asyncio.Semaphore(10)"],
        ["Rate Limit", "10 calls / second", "Time-window based throttling"],
        ["Call Interval", "100ms minimum", "Effective spacing between calls"],
        ["Retry Strategy", "Exponential backoff", "2^attempt seconds (max 3 retries)"],
        ["429 Handling", "Retry-After header", "Respects server-specified wait time"],
    ]
    grok_table = Table(grok_data, colWidths=[3 * cm, 3.5 * cm, 9 * cm])
    grok_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), HIGHLIGHT),
        ("TEXTCOLOR", (0, 0), (-1, 0), white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("GRID", (0, 0), (-1, -1), 0.5, CARD_BORDER),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [white, LIGHT_BG]),
    ]))
    elements.append(grok_table)
    elements.append(Spacer(1, 14))

    elements.append(Paragraph("Performance Optimization Strategies", SUBSECTION_TITLE))
    optimizations = [
        "<b>Async I/O Everywhere</b> - All database operations use async SQLAlchemy with aiosqlite. "
        "All HTTP calls use async httpx. This maximizes CPU utilization during I/O wait times.",
        "<b>Batch Processing</b> - Instead of processing each conversation immediately, the system batches "
        "10 at a time and processes them in parallel using asyncio.gather, reducing overhead.",
        "<b>Database Indexing</b> - Strategic indexes on timestamp, status, sentiment_score, and confidence "
        "columns ensure O(log n) query performance for filtered insight retrieval.",
        "<b>Connection Pooling</b> - SQLAlchemy's async engine manages a connection pool, avoiding the "
        "overhead of creating new database connections for each request.",
        "<b>Lightweight Stack</b> - SQLite eliminates the overhead of a separate database server process, "
        "keeping the total memory footprint well within the 1GB constraint.",
        "<b>Low-Temperature AI Calls</b> - Grok API calls use temperature=0.3 for more deterministic, "
        "consistent analysis results, reducing the need for retries due to inconsistent output.",
    ]
    for opt in optimizations:
        elements.append(Paragraph(f"&bull;  {opt}", BULLET))

    elements.append(PageBreak())
    return elements


def build_deployment():
    """Build Deployment section."""
    elements = []
    elements.extend(make_section_header("09  Deployment"))

    elements.append(Paragraph(
        "The application is containerized with Docker for consistent deployment across environments. "
        "Docker Compose provides orchestration with resource constraints matching production requirements.",
        BODY
    ))
    elements.append(Spacer(1, 10))

    elements.append(Paragraph("Dockerfile Configuration", SUBSECTION_TITLE))
    docker_steps = [
        ["Stage", "Command", "Purpose"],
        ["Base Image", "FROM python:3.11-slim", "Minimal Python image for small footprint"],
        ["System Deps", "apt-get install gcc", "C compiler for native Python extensions"],
        ["Dependencies", "pip install -r requirements.txt", "Install Python packages (cached layer)"],
        ["Application", "COPY . .", "Copy application source code"],
        ["Expose", "EXPOSE 8000", "Declare API port"],
        ["Run", "uvicorn main:app --host 0.0.0.0 --port 8000", "Start ASGI server"],
    ]
    docker_table = Table(docker_steps, colWidths=[2.5 * cm, 5.5 * cm, 7.6 * cm])
    docker_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), PRIMARY),
        ("TEXTCOLOR", (0, 0), (-1, 0), white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("GRID", (0, 0), (-1, -1), 0.5, CARD_BORDER),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [white, LIGHT_BG]),
        ("FONTNAME", (1, 1), (1, -1), "Courier"),
        ("FONTSIZE", (1, 1), (1, -1), 8),
    ]))
    elements.append(docker_table)
    elements.append(Spacer(1, 14))

    elements.append(Paragraph("Docker Compose - Resource Constraints", SUBSECTION_TITLE))
    resource_data = [
        ["Resource", "Limit", "Reservation", "Notes"],
        ["CPU", "2 cores", "1 core", "Sufficient for async workload + batch processing"],
        ["Memory", "1 GB", "512 MB", "SQLite in-process, no separate DB server"],
        ["Storage", "10 GB", "-", "Database file + application code"],
        ["Port", "8000:8000", "-", "Host-to-container port mapping"],
        ["Restart", "unless-stopped", "-", "Auto-restart on crash"],
    ]
    resource_table = Table(resource_data, colWidths=[2 * cm, 2.5 * cm, 2.5 * cm, 8.6 * cm])
    resource_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), SUCCESS),
        ("TEXTCOLOR", (0, 0), (-1, 0), white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("GRID", (0, 0), (-1, -1), 0.5, CARD_BORDER),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [white, LIGHT_BG]),
    ]))
    elements.append(resource_table)
    elements.append(Spacer(1, 14))

    elements.append(Paragraph("Environment Variables", SUBSECTION_TITLE))
    env_data = [
        ["Variable", "Required", "Default", "Description"],
        ["GROK_KEY", "Yes", "-", "xAI Grok API authentication key"],
        ["DATABASE_URL", "No", "sqlite+aiosqlite:///./insights.db", "Database connection string"],
        ["API_URL", "No", "http://localhost:8000", "Base URL for data ingestion script"],
    ]
    env_table = Table(env_data, colWidths=[2.8 * cm, 1.8 * cm, 5.5 * cm, 5.5 * cm])
    env_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), INFO),
        ("TEXTCOLOR", (0, 0), (-1, 0), white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("GRID", (0, 0), (-1, -1), 0.5, CARD_BORDER),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [white, LIGHT_BG]),
        ("FONTNAME", (0, 1), (0, -1), "Courier"),
        ("FONTNAME", (2, 1), (2, -1), "Courier"),
        ("FONTSIZE", (2, 1), (2, -1), 7.5),
    ]))
    elements.append(env_table)

    elements.append(PageBreak())
    return elements


def build_project_structure():
    """Build Project Structure section."""
    elements = []
    elements.extend(make_section_header("10  Project Structure"))

    elements.append(Paragraph(
        "The project follows a flat, modular structure where each file has a single, well-defined "
        "responsibility. This design simplifies navigation and testing.",
        BODY
    ))
    elements.append(Spacer(1, 10))

    structure_data = [
        ["File", "Lines", "Category", "Responsibility"],
        ["main.py", "248", "Application", "FastAPI app, endpoints, lifecycle management"],
        ["models.py", "55", "Data Layer", "SQLAlchemy ORM models (Conversation, Insight)"],
        ["schemas.py", "66", "Validation", "Pydantic request/response schemas"],
        ["database.py", "37", "Data Layer", "Async engine, session factory, initialization"],
        ["grok_client.py", "139", "AI Integration", "Grok API client, prompt engineering, rate limiting"],
        ["rate_limiter.py", "57", "Middleware", "Token bucket rate limiter implementation"],
        ["batch_processor.py", "115", "Processing", "Background batch processing system"],
        ["ingest_data.py", "~100", "Utility", "Data ingestion script (sample + CSV)"],
        ["requirements.txt", "16", "Config", "Python dependency declarations"],
        ["Dockerfile", "24", "DevOps", "Container image build instructions"],
        ["docker-compose.yml", "24", "DevOps", "Container orchestration with resource limits"],
        ["test_api.sh", "~50", "Testing", "Shell-based API endpoint tests"],
        ["README.md", "241", "Docs", "Setup, API docs, usage, troubleshooting"],
        ["ARCHITECTURE.md", "208", "Docs", "Architecture documentation and design decisions"],
        ["TESTING.md", "-", "Docs", "Testing guide with scenarios and checklist"],
    ]
    struct_table = Table(structure_data, colWidths=[3.2 * cm, 1.2 * cm, 2.5 * cm, 8.7 * cm])
    struct_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), PRIMARY),
        ("TEXTCOLOR", (0, 0), (-1, 0), white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 8.5),
        ("GRID", (0, 0), (-1, -1), 0.5, CARD_BORDER),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [white, LIGHT_BG]),
        ("FONTNAME", (0, 1), (0, -1), "Courier"),
        ("FONTSIZE", (0, 1), (0, -1), 8),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    elements.append(struct_table)
    elements.append(Spacer(1, 6))
    elements.append(Paragraph(
        "Total: ~8 Python source files, ~720+ lines of application code, 3 documentation files, 3 config/DevOps files",
        CAPTION
    ))

    elements.append(Spacer(1, 14))
    elements.append(Paragraph("Module Dependency Graph", SUBSECTION_TITLE))
    dep_data = [
        ["Module", "Depends On"],
        ["main.py", "database, models, schemas, rate_limiter, batch_processor"],
        ["batch_processor.py", "models, grok_client, database"],
        ["grok_client.py", "(external: httpx, asyncio)"],
        ["rate_limiter.py", "(standalone: asyncio, collections)"],
        ["models.py", "(standalone: SQLAlchemy)"],
        ["schemas.py", "(standalone: Pydantic)"],
        ["database.py", "models"],
    ]
    dep_table = Table(dep_data, colWidths=[3.5 * cm, 12 * cm])
    dep_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), ACCENT),
        ("TEXTCOLOR", (0, 0), (-1, 0), white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("GRID", (0, 0), (-1, -1), 0.5, CARD_BORDER),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [white, LIGHT_BG]),
        ("FONTNAME", (0, 1), (0, -1), "Courier"),
        ("FONTSIZE", (0, 1), (0, -1), 8.5),
    ]))
    elements.append(dep_table)

    elements.append(PageBreak())
    return elements


def build_challenges():
    """Build Challenges & Solutions section."""
    elements = []
    elements.extend(make_section_header("11  Challenges & Solutions"))

    challenges = [
        {
            "challenge": "Grok API Response Inconsistency",
            "problem": (
                "Grok AI sometimes wraps JSON responses in markdown code blocks (```json...```) "
                "and occasionally returns malformed JSON, causing parsing failures."
            ),
            "solution": (
                "Implemented a robust response parser that strips markdown code block wrappers "
                "(```json and ```) before JSON parsing. Added a 3-retry mechanism with exponential "
                "backoff (1s, 2s, 4s) and a graceful fallback that returns default values "
                "(sentiment_score=0.0, confidence=0.0, clusters=[\"unknown\"]) when all retries fail."
            ),
        },
        {
            "challenge": "Dual Rate Limiting Coordination",
            "problem": (
                "Needed to limit inbound API traffic (100 req/s) and outbound Grok calls (10 calls/s) "
                "with different strategies, while keeping the system responsive."
            ),
            "solution": (
                "Implemented two separate rate limiting mechanisms: a token bucket algorithm with "
                "asyncio.Lock for inbound traffic (synchronous check on each request), and a "
                "semaphore + time-window tracker for Grok API calls (asynchronous wait with precise "
                "sleep calculation). The separation ensures neither limiter blocks the other."
            ),
        },
        {
            "challenge": "Resource-Constrained Deployment",
            "problem": (
                "The application must run within 2 CPU cores and 1GB RAM, ruling out heavy "
                "database servers like PostgreSQL and limiting concurrency options."
            ),
            "solution": (
                "Selected SQLite with async wrapper (aiosqlite) to eliminate separate database "
                "process overhead. Tuned batch sizes to 10 conversations and Grok concurrency to "
                "10 calls to balance throughput with memory usage. Used Python 3.11-slim Docker "
                "image to minimize container size."
            ),
        },
        {
            "challenge": "Asynchronous Background Processing",
            "problem": (
                "Background batch processing must run continuously without blocking API request "
                "handling, while sharing the same database and respecting rate limits."
            ),
            "solution": (
                "Used asyncio.create_task to spawn the batch processor as a non-blocking background "
                "task. Each batch creates its own database session (AsyncSessionLocal) to avoid "
                "session conflicts. The processor uses asyncio.gather for parallel conversation "
                "processing within each batch, and individual failures are caught without "
                "affecting other conversations in the batch."
            ),
        },
        {
            "challenge": "Graceful Error Isolation",
            "problem": (
                "A single Grok API failure or malformed response could potentially crash the "
                "entire batch processing pipeline, leaving conversations in a stuck state."
            ),
            "solution": (
                "Implemented per-conversation error handling within _process_single. Failed "
                "conversations are marked with status=\"failed\" while the batch continues. "
                "The batch processor's main loop also catches exceptions at the batch level "
                "and waits 5 seconds before retrying. This multi-level error handling ensures "
                "the system remains operational even under partial failure conditions."
            ),
        },
    ]

    for ch in challenges:
        elements.append(Paragraph(ch["challenge"], SUBSECTION_TITLE))

        prob_style = ParagraphStyle("Problem", parent=BODY, textColor=HIGHLIGHT)
        elements.append(Paragraph(f"<b>Problem:</b> {ch['problem']}", BODY))
        elements.append(Paragraph(f"<b>Solution:</b> {ch['solution']}", BODY))
        elements.append(Spacer(1, 6))

        d = Drawing(WIDTH - 4 * cm, 1)
        d.add(Rect(0, 0, WIDTH - 4 * cm, 0.5, fillColor=CARD_BORDER, strokeColor=None))
        elements.append(d)
        elements.append(Spacer(1, 6))

    elements.append(Spacer(1, 14))
    elements.append(Paragraph("Summary", SUBSECTION_TITLE))
    elements.append(Paragraph(
        "The Insights Platform API demonstrates a production-grade approach to building AI-powered "
        "data analysis pipelines. By combining FastAPI's async capabilities with Grok AI's NLP power, "
        "the system achieves high throughput within strict resource constraints. The modular architecture, "
        "comprehensive error handling, and dual rate limiting strategy make it resilient and maintainable. "
        "This project showcases skills in API design, async programming, AI integration, database design, "
        "rate limiting algorithms, and containerized deployment.",
        BODY
    ))

    return elements


def generate_pdf(output_path="Insights_Platform_API_Portfolio.pdf"):
    """Generate the complete portfolio PDF."""

    doc = BaseDocTemplate(
        output_path,
        pagesize=A4,
        leftMargin=2 * cm,
        rightMargin=2 * cm,
        topMargin=2.5 * cm,
        bottomMargin=2.5 * cm,
        title="Insights Platform API - Project Portfolio",
        author="Developer Portfolio",
        subject="FastAPI + Grok AI Twitter Analysis Platform",
    )

    cover_frame = Frame(
        0, 0, WIDTH, HEIGHT,
        leftPadding=3 * cm, rightPadding=3 * cm,
        topPadding=2 * cm, bottomPadding=2 * cm,
        id="cover"
    )
    content_frame = Frame(
        2 * cm, 2.5 * cm, WIDTH - 4 * cm, HEIGHT - 5 * cm,
        leftPadding=0, rightPadding=0,
        topPadding=0, bottomPadding=0,
        id="content"
    )

    cover_template = PageTemplate(id="cover", frames=[cover_frame], onPage=draw_cover)
    content_template = PageTemplate(id="content", frames=[content_frame], onPage=draw_background)

    doc.addPageTemplates([cover_template, content_template])

    elements = []
    elements.extend(build_cover_page())
    elements.extend(build_toc())
    elements.extend(build_overview())
    elements.extend(build_features())
    elements.extend(build_architecture())
    elements.extend(build_tech_stack())
    elements.extend(build_api_design())
    elements.extend(build_database())
    elements.extend(build_components())
    elements.extend(build_rate_limiting())
    elements.extend(build_deployment())
    elements.extend(build_project_structure())
    elements.extend(build_challenges())

    doc.build(elements)
    print(f"Portfolio PDF generated: {output_path}")
    print(f"File size: {os.path.getsize(output_path) / 1024:.1f} KB")


if __name__ == "__main__":
    generate_pdf()
