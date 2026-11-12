"""
Olist E-Commerce: Pro Designer Executive PowerPoint Deck Generator
--------------------------------------------------------------------
Crafts a 10-slide, 16:9 widescreen boardroom presentation deck (.pptx)
designed to elite McKinsey/BCG management consulting and Silicon Valley
executive standards.

Features:
- Midnight Slate & Electric Cyan / Emerald / Coral design system (#0F172A).
- Native PowerPoint tables with custom dark cell styling and alignment.
- High-contrast hero metric blocks with large bold numbers (32-40pt).
- Action-oriented executive narrative titles on every slide.
- Strict 16:9 widescreen pixel grid with consistent 0.8" margins.
"""

import os
import sys

# Ensure stdout handles UTF-8 cleanly on Windows
if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        pass

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

def build_pro_deck():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    # -------------------------------------------------------------
    # DESIGN SYSTEM COLOR PALETTE (Modern Dark Slate / Cyber Executive)
    # -------------------------------------------------------------
    BG_DARK       = RGBColor(15, 23, 42)    # #0F172A (Deep Slate Midnight)
    SURFACE_CARD  = RGBColor(30, 41, 59)    # #1E293B (Card Slate Surface)
    SURFACE_ALT   = RGBColor(24, 33, 47)    # #18212F (Subtle Contrast Surface)
    BORDER_SUBTLE = RGBColor(51, 65, 85)    # #334155 (Subtle Divider)
    
    TEXT_PRIMARY  = RGBColor(255, 255, 255) # Pure White
    TEXT_SECONDARY= RGBColor(203, 213, 225) # Slate 300 (Readable Light)
    TEXT_MUTED    = RGBColor(148, 163, 184) # Slate 400 (Secondary Label)
    
    CYAN_ACCENT   = RGBColor(56, 189, 248)  # #38BDF8 (Electric Cyan Primary)
    EMERALD_GREEN = RGBColor(52, 211, 153)  # #34D399 (Success / Growth)
    AMBER_GOLD    = RGBColor(251, 191, 36)  # #FBBF24 (Warning / Highlight)
    CORAL_ALERT   = RGBColor(251, 113, 133) # #FB7185 (Critical / SLA Breach)
    PURPLE_ACCENT = RGBColor(168, 85, 247)  # #A855F7 (Special Feature)

    blank_layout = prs.slide_layouts[6]

    # Helper: Set Solid Dark Background
    def set_background(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
        bg.fill.solid()
        bg.fill.fore_color.rgb = BG_DARK
        bg.line.fill.background()
        return bg

    # Helper: Standard Header with Eyebrow and Action Title
    def add_slide_header(slide, eyebrow, action_title):
        tb = slide.shapes.add_textbox(Inches(0.8), Inches(0.45), Inches(11.733), Inches(0.95))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        
        # Eyebrow / Kicker
        p_eye = tf.paragraphs[0]
        p_eye.text = eyebrow.upper()
        p_eye.font.size = Pt(9.5)
        p_eye.font.bold = True
        p_eye.font.color.rgb = CYAN_ACCENT

        # Action-oriented Narrative Title
        p_title = tf.add_paragraph()
        p_title.text = action_title
        p_title.font.size = Pt(21)
        p_title.font.bold = True
        p_title.font.color.rgb = TEXT_PRIMARY

    # Helper: Stat Card Container
    def create_stat_card(slide, left, top, width, height, label, value, subtext="", badge="", accent_color=CYAN_ACCENT):
        # Card Background
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height))
        card.fill.solid()
        card.fill.fore_color.rgb = SURFACE_CARD
        card.line.color.rgb = BORDER_SUBTLE
        card.line.width = Pt(1)

        # Top Accent Strip (1-pixel style visual marker)
        accent_strip = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(left + 0.15), Inches(top), Inches(width - 0.3), Inches(0.04))
        accent_strip.fill.solid()
        accent_strip.fill.fore_color.rgb = accent_color
        accent_strip.line.fill.background()

        # Text Content
        tb = slide.shapes.add_textbox(Inches(left + 0.2), Inches(top + 0.12), Inches(width - 0.4), Inches(height - 0.2))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        # Label Row
        p_lbl = tf.paragraphs[0]
        p_lbl.text = label.upper()
        p_lbl.font.size = Pt(9)
        p_lbl.font.bold = True
        p_lbl.font.color.rgb = TEXT_MUTED

        # Huge Bold Number
        p_val = tf.add_paragraph()
        p_val.text = value
        p_val.font.size = Pt(24)
        p_val.font.bold = True
        p_val.font.color.rgb = TEXT_PRIMARY

        # Subtext / Delta
        if subtext:
            p_sub = tf.add_paragraph()
            p_sub.text = subtext
            p_sub.font.size = Pt(9)
            p_sub.font.color.rgb = accent_color

    # Helper: Content Container Box
    def create_content_panel(slide, left, top, width, height, title="", title_color=CYAN_ACCENT):
        panel = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height))
        panel.fill.solid()
        panel.fill.fore_color.rgb = SURFACE_CARD
        panel.line.color.rgb = BORDER_SUBTLE
        panel.line.width = Pt(1)

        if title:
            tb = slide.shapes.add_textbox(Inches(left + 0.25), Inches(top + 0.15), Inches(width - 0.5), Inches(0.4))
            tf = tb.text_frame
            tf.word_wrap = True
            tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
            p = tf.paragraphs[0]
            p.text = title.upper()
            p.font.size = Pt(11)
            p.font.bold = True
            p.font.color.rgb = title_color

        return panel

    # -------------------------------------------------------------
    # SLIDE 1: COVER SLIDE (Hero Modern Minimalist)
    # -------------------------------------------------------------
    s1 = prs.slides.add_slide(blank_layout)
    set_background(s1)

    # Decorative Cyan Corner Glow Line
    glow_line = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.2), Inches(1.5), Inches(0.06))
    glow_line.fill.solid()
    glow_line.fill.fore_color.rgb = CYAN_ACCENT
    glow_line.line.fill.background()

    tb1 = s1.shapes.add_textbox(Inches(0.8), Inches(1.5), Inches(11.5), Inches(4.5))
    tf1 = tb1.text_frame
    tf1.word_wrap = True
    tf1.margin_left = tf1.margin_top = tf1.margin_right = tf1.margin_bottom = 0

    p = tf1.paragraphs[0]
    p.text = "EXECUTIVE STRATEGIC BRIEFING • Q4 2026"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = CYAN_ACCENT

    p = tf1.add_paragraph()
    p.text = "Brazilian E-Commerce Growth &\nFulfillment Dynamics"
    p.font.size = Pt(40)
    p.font.bold = True
    p.font.color.rgb = TEXT_PRIMARY

    p = tf1.add_paragraph()
    p.text = "Commercial Velocity • Logistics Fulfillment SLA • Customer Retention & Sentiment Polarity"
    p.font.size = Pt(15)
    p.font.color.rgb = TEXT_SECONDARY

    # Scope Pills along the bottom of cover
    pills_data = [
        ("TRANSACTIONS", "99,941 Orders"),
        ("GROSS REVENUE", "$15.91M GMV"),
        ("PRODUCT CATALOG", "32,951 SKUs"),
        ("INFRASTRUCTURE", "Supabase + BigQuery + Power BI")
    ]
    p_left = 0.8
    for label, val in pills_data:
        pill = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(p_left), Inches(5.8), Inches(2.7), Inches(0.85))
        pill.fill.solid()
        pill.fill.fore_color.rgb = SURFACE_CARD
        pill.line.color.rgb = BORDER_SUBTLE
        pill.line.width = Pt(1)

        ptf = pill.text_frame
        ptf.word_wrap = True
        ptf.margin_top = Inches(0.12)
        ptf.margin_left = Inches(0.15)
        
        pp1 = ptf.paragraphs[0]
        pp1.text = label
        pp1.font.size = Pt(8.5)
        pp1.font.bold = True
        pp1.font.color.rgb = TEXT_MUTED

        pp2 = ptf.add_paragraph()
        pp2.text = val
        pp2.font.size = Pt(12)
        pp2.font.bold = True
        pp2.font.color.rgb = TEXT_PRIMARY

        p_left += 2.95

    # -------------------------------------------------------------
    # SLIDE 2: EXECUTIVE SCORECARD (6 Modern Cards + Verdict Bar)
    # -------------------------------------------------------------
    s2 = prs.slides.add_slide(blank_layout)
    set_background(s2)
    add_slide_header(s2, "Portfolio Health Scorecard", "Robust Revenue Growth Strained by a Leaky Retention Bucket")

    # Row 1: Commercial Pillar
    create_stat_card(s2, 0.8, 1.55, 3.65, 1.55, "Total Marketplace GMV", "$15.91M", "▲ +6.1% vs $15.0M Target", accent_color=EMERALD_GREEN)
    create_stat_card(s2, 4.84, 1.55, 3.65, 1.55, "Order Transactions", "99,941", "Steady baseline volume", accent_color=CYAN_ACCENT)
    create_stat_card(s2, 8.88, 1.55, 3.65, 1.55, "Average Order Value", "$159.33", "Stable across 3 consecutive years", accent_color=CYAN_ACCENT)

    # Row 2: Operational & Retention Pillar
    create_stat_card(s2, 0.8, 3.35, 3.65, 1.55, "On-Time Fulfillment SLA", "93.23%", "▼ -1.77% Shortfall (Target: 95.0%)", accent_color=AMBER_GOLD)
    create_stat_card(s2, 4.84, 3.35, 3.65, 1.55, "Customer Review Score", "4.09 ⭐", "4.0 Benchmark | Bimodal distribution", accent_color=CYAN_ACCENT)
    create_stat_card(s2, 8.88, 3.35, 3.65, 1.55, "Repeat Customer Rate", "3.12%", "🚨 Critical Deficit (Benchmark: 15-20%)", accent_color=CORAL_ALERT)

    # Bottom Callout: The Strategic Verdict
    verdict = create_content_panel(s2, 0.8, 5.15, 11.733, 1.75, "Executive Summary & Core Business Findings", title_color=AMBER_GOLD)
    v_tb = s2.shapes.add_textbox(Inches(1.05), Inches(5.6), Inches(11.2), Inches(1.2))
    v_tf = v_tb.text_frame
    v_tf.word_wrap = True
    v_tf.margin_left = v_tf.margin_top = v_tf.margin_right = v_tf.margin_bottom = 0

    bullets = [
        ("Commercial Scaling is Proven:", " Olist scaled to $15.91M GMV powered by 78.3% credit installment financing and stable $159 basket sizes."),
        ("Logistics Friction Threatens Brand Equity:", " Fulfillment drops to 78.6% in Northern frontier states due to 2,500km cross-country surface transit."),
        ("The Retention Emergency:", " A 3.12% repeat rate means Olist acquires 96,000 customers at high marketing CAC, but 96.9% never return.")
    ]
    for i, (b_title, b_desc) in enumerate(bullets):
        p = v_tf.paragraphs[0] if i == 0 else v_tf.add_paragraph()
        r1 = p.add_run()
        r1.text = f"{i+1}. {b_title}"
        r1.font.bold = True
        r1.font.size = Pt(10.5)
        r1.font.color.rgb = CYAN_ACCENT
        
        r2 = p.add_run()
        r2.text = b_desc
        r2.font.size = Pt(10.5)
        r2.font.color.rgb = TEXT_SECONDARY

    # -------------------------------------------------------------
    # SLIDE 3: PILLAR 1 — REVENUE VELOCITY & TIME SCALING
    # -------------------------------------------------------------
    s3 = prs.slides.add_slide(blank_layout)
    set_background(s3)
    add_slide_header(s3, "Pillar 1: Commercial Trajectory", "Revenue Scaling Driven by Volume Expansion and Credit Installments")

    # Left Panel: The 3 Growth Phases
    create_content_panel(s3, 0.8, 1.55, 6.6, 5.35, "Historical Revenue Trajectory & Seasonality", CYAN_ACCENT)
    tb_phases = s3.shapes.add_textbox(Inches(1.05), Inches(2.1), Inches(6.1), Inches(4.6))
    tf_p = tb_phases.text_frame
    tf_p.word_wrap = True
    tf_p.margin_left = tf_p.margin_top = tf_p.margin_right = tf_p.margin_bottom = 0

    phases = [
        ("Phase 1: Exploratory Beta (Late 2016)", "Operational proof-of-concept operating under $60K annual GMV; established merchant and catalog foundations."),
        ("Phase 2: Compounding Breakout (2017)", "Consistent 12-18% MoM scaling culminating in November 2017 Black Friday ($1.19M in 30 days — an all-time monthly record)."),
        ("Phase 3: Elevated Baseline (2018)", "Maintained an elevated post-holiday baseline averaging $850K - $1.05M per month through mid-2018."),
        ("Volume-Driven Engine (Zero Price Inflation)", "Average Order Value remained flat: $158.37 (2017) vs. $160.04 (2018). Scaling was 100% customer acquisition volume.")
    ]
    for i, (p_title, p_desc) in enumerate(phases):
        p = tf_p.paragraphs[0] if i == 0 else tf_p.add_paragraph()
        r = p.add_run()
        r.text = f"• {p_title}: "
        r.font.bold = True
        r.font.size = Pt(10.5)
        r.font.color.rgb = TEXT_PRIMARY
        
        r2 = p.add_run()
        r2.text = p_desc + "\n"
        r2.font.size = Pt(10)
        r2.font.color.rgb = TEXT_SECONDARY

    # Right Panel: Payment Rails & Credit Financing
    create_content_panel(s3, 7.6, 1.55, 4.933, 5.35, "Payment Tender & Credit Financing Split", EMERALD_GREEN)
    
    # 4 Payment Rail Mini Stat Strips
    rails = [
        ("CREDIT CARD", "$12.54M", "78.34%", "3.5 Avg Installments (28% use 6-10x)", CYAN_ACCENT),
        ("BOLETO BANCÁRIO", "$2.87M", "17.92%", "Essential cash rail for unbanked buyers", AMBER_GOLD),
        ("VOUCHERS", "$379K", "2.37%", "Promotional credits & dispute resolution", TEXT_MUTED),
        ("DEBIT CARDS", "$218K", "1.36%", "Instant clearance, low penetration", TEXT_MUTED)
    ]
    r_top = 2.15
    for name, gmv, share, note, col in rails:
        card = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7.85), Inches(r_top), Inches(4.433), Inches(0.95))
        card.fill.solid()
        card.fill.fore_color.rgb = SURFACE_ALT
        card.line.color.rgb = BORDER_SUBTLE
        card.line.width = Pt(1)

        ctf = card.text_frame
        ctf.word_wrap = True
        ctf.margin_top = Inches(0.1)
        ctf.margin_left = Inches(0.15)
        
        cp1 = ctf.paragraphs[0]
        cp1.text = f"{name} • {share} ({gmv})"
        cp1.font.size = Pt(10.5)
        cp1.font.bold = True
        cp1.font.color.rgb = col

        cp2 = ctf.add_paragraph()
        cp2.text = note
        cp2.font.size = Pt(9)
        cp2.font.color.rgb = TEXT_SECONDARY

        r_top += 1.15

    # -------------------------------------------------------------
    # SLIDE 4: PILLAR 1 — CATEGORY LEADERSHIP & CONCENTRATION
    # -------------------------------------------------------------
    s4 = prs.slides.add_slide(blank_layout)
    set_background(s4)
    add_slide_header(s4, "Pillar 1: Product Category Economics", "Top 10 Categories Drive 62.5% of GMV ($9.95M)")

    # Left: Native Styled Table (Top 10 Categories)
    rows = 11
    cols = 5
    tbl_shape = s4.shapes.add_table(rows, cols, Inches(0.8), Inches(1.55), Inches(7.6), Inches(5.35))
    tbl = tbl_shape.table
    tbl.columns[0].width = Inches(0.6)  # Rank
    tbl.columns[1].width = Inches(2.4)  # Category
    tbl.columns[2].width = Inches(1.5)  # GMV
    tbl.columns[3].width = Inches(1.3)  # Orders
    tbl.columns[4].width = Inches(1.8)  # Freight Drag

    headers = ["#", "Category Name (English)", "Total GMV", "Orders", "Freight Ratio"]
    for j, h in enumerate(headers):
        cell = tbl.cell(0, j)
        cell.fill.solid()
        cell.fill.fore_color.rgb = SURFACE_ALT
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.size = Pt(9.5)
        p.font.bold = True
        p.font.color.rgb = CYAN_ACCENT

    cat_data = [
        ("1", "Health & Beauty", "$1.44M", "9,670", "21.4% (Low)"),
        ("2", "Watches & Gifts", "$1.31M", "5,624", "16.8% (Premium)"),
        ("3", "Bed, Bath & Table", "$1.24M", "11,115", "29.8% (Moderate)"),
        ("4", "Sports & Leisure", "$1.16M", "8,641", "24.1% (Active)"),
        ("5", "Computers & Acc.", "$1.06M", "7,827", "18.2% (Tech)"),
        ("6", "Furniture & Decor", "$0.90M", "8,334", "38.6% (Heavy)"),
        ("7", "Housewares", "$0.78M", "6,964", "31.2% (Home)"),
        ("8", "Cool Stuff", "$0.72M", "3,999", "23.5% (Gift)"),
        ("9", "Auto Parts", "$0.69M", "4,235", "27.9% (Spares)"),
        ("10", "Garden Tools", "$0.58M", "4,347", "34.2% (Heavy)")
    ]
    for i, row in enumerate(cat_data):
        for j, val in enumerate(row):
            cell = tbl.cell(i + 1, j)
            cell.fill.solid()
            cell.fill.fore_color.rgb = SURFACE_CARD if i % 2 == 0 else SURFACE_ALT
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.font.size = Pt(9)
            p.font.color.rgb = TEXT_PRIMARY if j < 3 else TEXT_SECONDARY

    # Right: Strategic Takeaway Panels
    create_content_panel(s4, 8.6, 1.55, 3.933, 2.55, "Category Concentration Insight", CYAN_ACCENT)
    t_tb = s4.shapes.add_textbox(Inches(8.85), Inches(2.05), Inches(3.4), Inches(1.9))
    t_tf = t_tb.text_frame
    t_tf.word_wrap = True
    t_tf.margin_left = t_tf.margin_top = t_tf.margin_right = t_tf.margin_bottom = 0
    p = t_tf.paragraphs[0]
    p.text = "• Top 5 Categories generate over $6.2M (40% of national GMV).\n• Light/Compact items (beauty, watches) enjoy low shipping friction (<20%).\n• Heavy goods (furniture, housewares) suffer 30-40% freight burdens, reducing conversion."
    p.font.size = Pt(10)
    p.font.color.rgb = TEXT_SECONDARY

    create_content_panel(s4, 8.6, 4.3, 3.933, 2.6, "Geographic Concentration", AMBER_GOLD)
    g_tb = s4.shapes.add_textbox(Inches(8.85), Inches(4.8), Inches(3.4), Inches(1.9))
    g_tf = g_tb.text_frame
    g_tf.word_wrap = True
    g_tf.margin_left = g_tf.margin_top = g_tf.margin_right = g_tf.margin_bottom = 0
    p = g_tf.paragraphs[0]
    p.text = "• São Paulo (SP): $5.91M (37.1% national GMV) — The undeniable commercial hub.\n• Southeast Triangle (SP, RJ, MG): Captures 62.3% of national volume.\n• Frontier States: 18 other states share under 22% of GMV due to shipping transit friction."
    p.font.size = Pt(10)
    p.font.color.rgb = TEXT_SECONDARY

    # -------------------------------------------------------------
    # SLIDE 5: PILLAR 2 — LOGISTICS SLA & REGIONAL DIVIDE
    # -------------------------------------------------------------
    s5 = prs.slides.add_slide(blank_layout)
    set_background(s5)
    add_slide_header(s5, "Pillar 2: Logistics & Supply Chain SLA", "Regional Fulfillment Disparities: Southeastern Speed vs. Northern Drag")

    # 3 Top KPI Cards
    create_stat_card(s5, 0.8, 1.55, 3.65, 1.35, "National On-Time Rate", "93.23%", "Target: 95.0% (-1.77% gap)", accent_color=AMBER_GOLD)
    create_stat_card(s5, 4.84, 1.55, 3.65, 1.35, "Average Delivery Duration", "12.56 Days", "Target: < 10 Days (+2.56 days)", accent_color=CYAN_ACCENT)
    create_stat_card(s5, 8.88, 1.55, 3.65, 1.35, "Late Shipment Volume", "6,770 Orders", "Direct catalyst for 1-star reviews", accent_color=CORAL_ALERT)

    # Comparison Grid: South vs North/Northeast
    create_content_panel(s5, 0.8, 3.1, 5.65, 3.8, "Southeastern Logistics Hubs (Meets 95% SLA)", EMERALD_GREEN)
    se_tb = s5.shapes.add_textbox(Inches(1.05), Inches(3.6), Inches(5.15), Inches(3.1))
    se_tf = se_tb.text_frame
    se_tf.word_wrap = True
    se_tf.margin_left = se_tf.margin_top = se_tf.margin_right = se_tf.margin_bottom = 0
    se_data = [
        ("São Paulo (SP)", "8.3 Days", "96.4% On-Time", "Hub location; carrier density"),
        ("Paraná (PR)", "11.5 Days", "95.8% On-Time", "Integrated Southern highway network"),
        ("Santa Catarina (SC)", "14.1 Days", "95.1% On-Time", "Established coastal 3PL carriers"),
        ("Minas Gerais (MG)", "12.8 Days", "94.2% On-Time", "Moderate inland transit friction")
    ]
    for i, (st, days, sla, note) in enumerate(se_data):
        p = se_tf.paragraphs[0] if i == 0 else se_tf.add_paragraph()
        p.text = f"✓ {st}: {days} avg | {sla} ({note})\n"
        p.font.size = Pt(10)
        p.font.color.rgb = TEXT_SECONDARY

    create_content_panel(s5, 6.85, 3.1, 5.683, 3.8, "Northeastern Bottlenecks (Severe SLA Breaches)", CORAL_ALERT)
    ne_tb = s5.shapes.add_textbox(Inches(7.1), Inches(3.6), Inches(5.183), Inches(3.1))
    ne_tf = ne_tb.text_frame
    ne_tf.word_wrap = True
    ne_tf.margin_left = ne_tf.margin_top = ne_tf.margin_right = ne_tf.margin_bottom = 0
    ne_data = [
        ("Alagoas (AL)", "24.3 Days", "78.6% On-Time", "🚨 Worst in Brazil (-16.4% vs SLA)"),
        ("Maranhão (MA)", "21.1 Days", "82.6% On-Time", "Severe road infrastructure delay"),
        ("Sergipe (SE)", "21.0 Days", "84.8% On-Time", "Inland cross-dock bottlenecks"),
        ("Ceará (CE) / Piauí (PI)", "20.4 Days", "86.2% On-Time", "2,500km distance from SP sellers")
    ]
    for i, (st, days, sla, note) in enumerate(ne_data):
        p = ne_tf.paragraphs[0] if i == 0 else ne_tf.add_paragraph()
        p.text = f"✗ {st}: {days} avg | {sla} ({note})\n"
        p.font.size = Pt(10)
        p.font.color.rgb = TEXT_SECONDARY

    # -------------------------------------------------------------
    # SLIDE 6: PILLAR 3 — THE SMOKING GUN: TRANSIT VS REVIEWS
    # -------------------------------------------------------------
    s6 = prs.slides.add_slide(blank_layout)
    set_background(s6)
    add_slide_header(s6, "Pillar 3: The Smoking Gun Finding", "Customer Reviews are Directly Dictated by Delivery Transit Duration")

    # Big Hero Callout Card (Center Left)
    hero = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.55), Inches(4.5), Inches(5.35))
    hero.fill.solid()
    hero.fill.fore_color.rgb = SURFACE_CARD
    hero.line.color.rgb = CORAL_ALERT
    hero.line.width = Pt(2)

    h_tb = s6.shapes.add_textbox(Inches(1.05), Inches(1.85), Inches(4.0), Inches(4.7))
    h_tf = h_tb.text_frame
    h_tf.word_wrap = True
    h_tf.margin_left = h_tf.margin_top = h_tf.margin_right = h_tf.margin_bottom = 0

    p = h_tf.paragraphs[0]
    p.text = "THE ROOT CAUSE DISCOVERY"
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = CORAL_ALERT

    p = h_tf.add_paragraph()
    p.text = "+10.6 Days"
    p.font.size = Pt(40)
    p.font.bold = True
    p.font.color.rgb = TEXT_PRIMARY

    p = h_tf.add_paragraph()
    p.text = "THE 1-STAR DELIVERY PENALTY"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = AMBER_GOLD

    p = h_tf.add_paragraph()
    p.text = "\nOrders rated 1 Star take more than DOUBLE the transit time of 5-Star orders.\n\nFulfillment speed is the #1 controllable cause of customer dissatisfaction and brand churn."
    p.font.size = Pt(10.5)
    p.font.color.rgb = TEXT_SECONDARY

    # Right: Step-Down Comparison Table & Sentiment Polarity
    create_content_panel(s6, 5.6, 1.55, 6.933, 2.9, "The Transit Duration vs. Rating Step-Down", CYAN_ACCENT)
    
    # 5-Star to 1-Star Step Down Cards
    step_data = [
        ("5 ⭐ Rating", "10.7 Days", "57.1K Orders", "Fast fulfillment, customer delight", EMERALD_GREEN),
        ("4 ⭐ Rating", "12.3 Days", "19.1K Orders", "Met baseline delivery expectation", CYAN_ACCENT),
        ("3 ⭐ Rating", "14.3 Days", "8.2K Orders", "Minor delay; neutral sentiment", AMBER_GOLD),
        ("2 ⭐ Rating", "16.7 Days", "3.1K Orders", "Substantial delay; rising frustration", AMBER_GOLD),
        ("1 ⭐ Rating", "21.3 Days", "11.4K Orders", "Broken promise; catastrophic dissatisfaction", CORAL_ALERT)
    ]
    s_top = 2.05
    for rating, days, vol, note, col in step_data:
        bar = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(5.8), Inches(s_top), Inches(6.533), Inches(0.42))
        bar.fill.solid()
        bar.fill.fore_color.rgb = SURFACE_ALT
        bar.line.color.rgb = BORDER_SUBTLE
        bar.line.width = Pt(1)

        btf = bar.text_frame
        btf.word_wrap = True
        btf.margin_top = Inches(0.08)
        btf.margin_left = Inches(0.15)
        bp = btf.paragraphs[0]
        bp.text = f"{rating}:  {days} avg transit  |  {vol}  ({note})"
        bp.font.size = Pt(9.5)
        bp.font.bold = True
        bp.font.color.rgb = col

        s_top += 0.46

    # Bottom Right: The Sentiment Polarity & Retention Warning
    create_content_panel(s6, 5.6, 4.65, 6.933, 2.25, "Customer Sentiment Polarity & Bimodal Risk", AMBER_GOLD)
    sp_tb = s6.shapes.add_textbox(Inches(5.85), Inches(5.1), Inches(6.4), Inches(1.6))
    sp_tf = sp_tb.text_frame
    sp_tf.word_wrap = True
    sp_tf.margin_left = sp_tf.margin_top = sp_tf.margin_right = sp_tf.margin_bottom = 0
    p = sp_tf.paragraphs[0]
    p.text = "• Bimodal Sentiment: Reviews are polarized — 5-stars dominate (57.1K), but 1-stars form the second largest cohort (11.4K, 11.5%). Very few customers leave 2-star reviews.\n• The Verdict: Customers either experience flawless delivery or severe carrier failure; middle ground is almost nonexistent."
    p.font.size = Pt(10)
    p.font.color.rgb = TEXT_SECONDARY

    # -------------------------------------------------------------
    # SLIDE 7: PILLAR 3 — RETENTION & SELLER CONCENTRATION
    # -------------------------------------------------------------
    s7 = prs.slides.add_slide(blank_layout)
    set_background(s7)
    add_slide_header(s7, "Pillar 3: Retention Deficit & Merchant Fragility", "A 3.12% Repeat Customer Crisis Combined with High Seller Monopolization")

    # Left: The 3.12% Leaky Bucket Emergency
    create_content_panel(s7, 0.8, 1.55, 5.65, 5.35, "Customer Retention Crisis (The Leaky Bucket)", CORAL_ALERT)
    ret_tb = s7.shapes.add_textbox(Inches(1.05), Inches(2.1), Inches(5.15), Inches(4.6))
    ret_tf = ret_tb.text_frame
    ret_tf.word_wrap = True
    ret_tf.margin_left = ret_tf.margin_top = ret_tf.margin_right = ret_tf.margin_bottom = 0

    ret_points = [
        ("3.12% Repeat Customer Rate", "Out of 96,096 unique human buyers, only 2,997 returned to place a second order."),
        ("Industry Standard Deficit", "Benchmark multi-category marketplaces achieve 15% - 25% repeat purchase rates. Olist is trailing by over 12 percentage points."),
        ("High Marketing Acquisition Waste", "Olist pays full customer acquisition cost (CAC) for single-purchase transactions that never yield recurring customer lifetime value (LTV)."),
        ("Direct Churn Catalyst", "Customers who experience late delivery and leave 1-star reviews exhibit a near-zero (<0.4%) return rate.")
    ]
    for i, (title, desc) in enumerate(ret_points):
        p = ret_tf.paragraphs[0] if i == 0 else ret_tf.add_paragraph()
        r = p.add_run()
        r.text = f"• {title}: "
        r.font.bold = True
        r.font.size = Pt(10.5)
        r.font.color.rgb = TEXT_PRIMARY
        
        r2 = p.add_run()
        r2.text = desc + "\n"
        r2.font.size = Pt(10)
        r2.font.color.rgb = TEXT_SECONDARY

    # Right: Seller Pareto & Monopolization
    create_content_panel(s7, 6.85, 1.55, 5.683, 5.35, "Seller Health & The 80/20 Pareto Curve", AMBER_GOLD)
    sel_tb = s7.shapes.add_textbox(Inches(7.1), Inches(2.1), Inches(5.183), Inches(4.6))
    sel_tf = sel_tb.text_frame
    sel_tf.word_wrap = True
    sel_tf.margin_left = sel_tf.margin_top = sel_tf.margin_right = sel_tf.margin_bottom = 0

    sel_points = [
        ("Classic 80/20 Pareto Concentration", "Top 10% of merchants generate 78.4% of total marketplace GMV."),
        ("Top 20 Merchant Elite", "Just 20 sellers (0.6% of active merchant base) drive over $3.8M in revenue."),
        ("Monopolization Fragility", "Loss of a few top merchants to competitors (Mercado Livre, Amazon) poses an existential liquidity threat."),
        ("The Long-Tail Operational Overhead", "Bottom 2,000 sellers generate under 10% of revenue but produce a disproportionate share of customer service inquiries and dispatch delays.")
    ]
    for i, (title, desc) in enumerate(sel_points):
        p = sel_tf.paragraphs[0] if i == 0 else sel_tf.add_paragraph()
        r = p.add_run()
        r.text = f"• {title}: "
        r.font.bold = True
        r.font.size = Pt(10.5)
        r.font.color.rgb = TEXT_PRIMARY
        
        r2 = p.add_run()
        r2.text = desc + "\n"
        r2.font.size = Pt(10)
        r2.font.color.rgb = TEXT_SECONDARY

    # -------------------------------------------------------------
    # SLIDE 8: STRATEGIC ACTION ROADMAP & ROI MATRIX
    # -------------------------------------------------------------
    s8 = prs.slides.add_slide(blank_layout)
    set_background(s8)
    add_slide_header(s8, "Strategic Action Plan & Executive Playbook", "High-Impact Initiatives to Unlock +$2.3M in GMV and Cure Retention")

    # Native Styled Table for Strategic Action Plan
    s_rows = 5
    s_cols = 5
    s_table_shape = s8.shapes.add_table(s_rows, s_cols, Inches(0.8), Inches(1.55), Inches(11.733), Inches(5.35))
    s_table = s_table_shape.table
    s_table.columns[0].width = Inches(2.8)  # Initiative
    s_table.columns[1].width = Inches(1.5)  # Owner
    s_table.columns[2].width = Inches(1.3)  # Timeline
    s_table.columns[3].width = Inches(3.3)  # Core Action
    s_table.columns[4].width = Inches(2.833)# Projected Financial ROI

    s_headers = ["Strategic Initiative", "Owner", "Timeline", "Core Execution Action", "Projected Financial ROI"]
    for j, h in enumerate(s_headers):
        cell = s_table.cell(0, j)
        cell.fill.solid()
        cell.fill.fore_color.rgb = SURFACE_ALT
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = CYAN_ACCENT

    roadmap_data = [
        ("1. Northeast 3PL Micro-Hubs", "VP Logistics / COO", "Months 1-3", "Lease regional fulfillment staging in Recife & Salvador; pre-stock Top 50 SKUs.", "Cuts transit from 21d to 6d; lifts national SLA to 96.5% (+$680K GMV)."),
        ("2. Proactive Late-Order Credits", "Head of CX", "Months 1-2", "Automated WhatsApp alert + 15% courtesy credit if tracking exceeds 12 days.", "Recovers 25% of late detractors; lifts repeat rate to 5.5% (+$380K GMV)."),
        ("3. Algorithmic Cart Bundling", "Head of Growth", "Month 2", "Cross-sell Bed & Bath with Home Decor; 0% interest on 10x installments >$250.", "Increases items/basket from 1.13 to 1.35; lifts AOV to $185 (+$1.5M GMV)."),
        ("4. Olist Prime Seller Badges", "VP Merchants", "Months 3-4", "Fast-dispatch badge for sellers shipping <24h with fee commission discounts.", "Reduces merchant dispatch delay from 2.8d to 0.8d; de-risks Pareto concentration.")
    ]
    for i, row in enumerate(roadmap_data):
        for j, val in enumerate(row):
            cell = s_table.cell(i + 1, j)
            cell.fill.solid()
            cell.fill.fore_color.rgb = SURFACE_CARD if i % 2 == 0 else SURFACE_ALT
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.font.size = Pt(9.5)
            p.font.color.rgb = TEXT_PRIMARY if j == 0 else (EMERALD_GREEN if j == 4 else TEXT_SECONDARY)

    # -------------------------------------------------------------
    # SLIDE 9: PRODUCTION ENTERPRISE ARCHITECTURE
    # -------------------------------------------------------------
    s9 = prs.slides.add_slide(blank_layout)
    set_background(s9)
    add_slide_header(s9, "Enterprise Cloud BI Architecture", "Decoupled Multi-Cloud Modern Data Stack Verified with 100% Zero-Defect Audit")

    # 4 Architecture Tier Pillars
    tiers = [
        ("TIER 1: TRANSACTIONAL FACTS", "Supabase Cloud PostgreSQL", [
            "Hosts 99,941 orders, 113,223 items, 104,377 payments, 99,709 reviews.",
            "Composite PK constraints prevent fan-out.",
            "Dedicated IPv4 session pooling ensures sub-50ms query responses."
        ], CYAN_ACCENT),
        ("TIER 2: ENTERPRISE DIMENSIONS", "Google BigQuery Sandbox", [
            "Columnar warehouse storing 99,441 customers, 32,951 products, 3,095 sellers.",
            "Pyarrow streaming with zero latency.",
            "100% coordinates bounded within Brazil."
        ], EMERALD_GREEN),
        ("TIER 3: GOVERNANCE & LOOKUPS", "Google Sheets Live REST", [
            "Category translations (73 categories).",
            "Executive SLA KPI benchmark targets.",
            "Decoupled parameter pattern."
        ], AMBER_GOLD),
        ("TIER 4: EXECUTIVE PRESENTATION", "Power BI Desktop & VertiPaq", [
            "3-Page Widescreen Cockpit (1280x720).",
            "18 DAX measures in 5 display folders.",
            "Top-bar App Navigator with zero scrollbars."
        ], PURPLE_ACCENT)
    ]
    t_left = 0.8
    for kicker, title, items, col in tiers:
        pnl = create_content_panel(s9, t_left, 1.55, 2.75, 4.3, kicker, col)
        tb = s9.shapes.add_textbox(Inches(t_left + 0.15), Inches(2.05), Inches(2.45), Inches(3.6))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        # Subtitle
        p_sub = tf.paragraphs[0]
        p_sub.text = title
        p_sub.font.size = Pt(11)
        p_sub.font.bold = True
        p_sub.font.color.rgb = TEXT_PRIMARY

        # Bullets
        for it in items:
            p = tf.add_paragraph()
            p.text = f"• {it}\n"
            p.font.size = Pt(9)
            p.font.color.rgb = TEXT_SECONDARY

        t_left += 2.99

    # Bottom Banner: Automated Audit Certification
    audit_banner = s9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(6.05), Inches(11.733), Inches(0.85))
    audit_banner.fill.solid()
    audit_banner.fill.fore_color.rgb = SURFACE_CARD
    audit_banner.line.color.rgb = EMERALD_GREEN
    audit_banner.line.width = Pt(1.5)

    ab_tf = audit_banner.text_frame
    ab_tf.word_wrap = True
    ab_tf.margin_top = Inches(0.12)
    ab_tf.margin_left = Inches(0.2)
    ap = ab_tf.paragraphs[0]
    ap.text = "AUTOMATED PIPELINE & UNBREAKABILITY AUDIT: 27 / 27 CHECKPOINTS PASSED (100.0% PASS RATE)"
    ap.font.size = Pt(10)
    ap.font.bold = True
    ap.font.color.rgb = EMERALD_GREEN

    ap2 = ab_tf.add_paragraph()
    ap2.text = "Streaming simulation engine (simulate_new_orders.py) proved live incremental refresh in Power BI in <30s with zero schema breakage."
    ap2.font.size = Pt(9)
    ap2.font.color.rgb = TEXT_SECONDARY

    # -------------------------------------------------------------
    # SLIDE 10: CLOSING SLIDE (Minimalist Executive Sign-Off)
    # -------------------------------------------------------------
    s10 = prs.slides.add_slide(blank_layout)
    set_background(s10)

    # Decorative Cyan Line
    c_line = s10.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(2.0), Inches(1.5), Inches(0.06))
    c_line.fill.solid()
    c_line.fill.fore_color.rgb = CYAN_ACCENT
    c_line.line.fill.background()

    tb10 = s10.shapes.add_textbox(Inches(0.8), Inches(2.3), Inches(11.5), Inches(3.8))
    tf10 = tb10.text_frame
    tf10.word_wrap = True
    tf10.margin_left = tf10.margin_top = tf10.margin_right = tf10.margin_bottom = 0

    p = tf10.paragraphs[0]
    p.text = "EXECUTIVE ADVISORY COMPLETE"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = CYAN_ACCENT

    p = tf10.add_paragraph()
    p.text = "Thank You. Open for Executive Q&A."
    p.font.size = Pt(38)
    p.font.bold = True
    p.font.color.rgb = TEXT_PRIMARY

    p = tf10.add_paragraph()
    p.text = "All project assets, live cloud data pipelines, and interactive dashboards are production-verified."
    p.font.size = Pt(14)
    p.font.color.rgb = TEXT_SECONDARY

    # Deliverables Footer Pill
    f_pill = s10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(5.8), Inches(11.733), Inches(0.8))
    f_pill.fill.solid()
    f_pill.fill.fore_color.rgb = SURFACE_CARD
    f_pill.line.color.rgb = BORDER_SUBTLE

    f_tf = f_pill.text_frame
    f_tf.word_wrap = True
    f_tf.margin_top = Inches(0.18)
    f_tf.margin_left = Inches(0.2)
    fp = f_tf.paragraphs[0]
    fp.text = "DELIVERABLES: Power BI 3-Page Cockpit  |  C-Suite Advisory Report (Markdown)  |  Multi-Cloud Repository  |  ETL Engine"
    fp.font.size = Pt(9.5)
    fp.font.bold = True
    fp.font.color.rgb = CYAN_ACCENT

    # Save Deck
    output_path = os.path.join(os.path.dirname(__file__), '..', 'reports', 'executive_presentation.pptx')
    prs.save(output_path)
    print(f"🚀 Pro-Designer Boardroom Presentation generated successfully at:\n   {output_path}")

if __name__ == '__main__':
    build_pro_deck()
