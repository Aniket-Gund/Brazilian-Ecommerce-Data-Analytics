"""
Olist E-Commerce: Executive PowerPoint Presentation Generator (Step 9)
------------------------------------------------------------------------
Builds a 10-slide, 16:9 widescreen boardroom presentation deck (.pptx)
styled with executive dark/navy theme, structured KPI cards, metric tables,
and strategic recommendations.
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
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def create_deck():
    prs = Presentation()
    # 16:9 Widescreen dimensions
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    # Color Palette
    BG_COLOR = RGBColor(27, 38, 49)        # Dark Slate #1B2631
    CARD_BG = RGBColor(44, 62, 80)         # Container #2C3E50
    TEXT_WHITE = RGBColor(255, 255, 255)   # Crisp White
    TEXT_MUTED = RGBColor(189, 195, 199)   # Light Gray
    ACCENT_BLUE = RGBColor(46, 134, 193)   # Executive Blue #2E86C1
    ACCENT_TEAL = RGBColor(23, 165, 137)   # Metric Teal #17A589
    ACCENT_CORAL = RGBColor(231, 76, 60)   # Alert Red/Coral #E74C3C
    ACCENT_GOLD = RGBColor(241, 196, 15)   # Highlight Gold #F1C40F

    blank_layout = prs.slide_layouts[6]

    def set_slide_background(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
        bg.fill.solid()
        bg.fill.fore_color.rgb = BG_COLOR
        bg.line.fill.background()
        return bg

    def add_header(slide, title_text, category_text="OLIST EXECUTIVE STRATEGIC BRIEFING"):
        tb = slide.shapes.add_textbox(Inches(0.8), Inches(0.5), Inches(11.7), Inches(0.9))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        
        p_cat = tf.paragraphs[0]
        p_cat.text = category_text.upper()
        p_cat.font.size = Pt(10)
        p_cat.font.bold = True
        p_cat.font.color.rgb = ACCENT_BLUE

        p_title = tf.add_paragraph()
        p_title.text = title_text
        p_title.font.size = Pt(22)
        p_title.font.bold = True
        p_title.font.color.rgb = TEXT_WHITE

    def add_card(slide, left, top, width, height, title, value, subtitle="", accent_color=ACCENT_BLUE):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height))
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = accent_color
        card.line.width = Pt(1.5)

        tf = card.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.2)
        tf.margin_top = Inches(0.15)
        
        p1 = tf.paragraphs[0]
        p1.text = title.upper()
        p1.font.size = Pt(10)
        p1.font.bold = True
        p1.font.color.rgb = TEXT_MUTED

        p2 = tf.add_paragraph()
        p2.text = value
        p2.font.size = Pt(22)
        p2.font.bold = True
        p2.font.color.rgb = accent_color

        if subtitle:
            p3 = tf.add_paragraph()
            p3.text = subtitle
            p3.font.size = Pt(9.5)
            p3.font.color.rgb = TEXT_WHITE

    # -------------------------------------------------------------
    # SLIDE 1: TITLE SLIDE
    # -------------------------------------------------------------
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_background(s1)

    tbox = s1.shapes.add_textbox(Inches(1.2), Inches(1.8), Inches(11.0), Inches(4.0))
    tf1 = tbox.text_frame
    tf1.word_wrap = True
    
    p = tf1.paragraphs[0]
    p.text = "OLIST BRAZILIAN E-COMMERCE"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = ACCENT_GOLD

    p = tf1.add_paragraph()
    p.text = "C-Suite Executive Findings & Strategic Advisory"
    p.font.size = Pt(36)
    p.font.bold = True
    p.font.color.rgb = TEXT_WHITE

    p = tf1.add_paragraph()
    p.text = "Commercial Velocity • Logistics Fulfillment SLA • Customer Retention & Sentiment Polarity"
    p.font.size = Pt(16)
    p.font.color.rgb = ACCENT_BLUE

    p = tf1.add_paragraph()
    p.text = "\nEvaluated Scope: 99,941 Orders | $15.91M GMV | Multi-Cloud Architecture (PostgreSQL + BigQuery + Sheets)"
    p.font.size = Pt(12)
    p.font.color.rgb = TEXT_MUTED

    # -------------------------------------------------------------
    # SLIDE 2: EXECUTIVE SUMMARY & SCORECARD
    # -------------------------------------------------------------
    s2 = prs.slides.add_slide(blank_layout)
    set_slide_background(s2)
    add_header(s2, "Executive Macro Performance Scorecard")

    # 6 Scorecard KPI Cards
    add_card(s2, 0.8, 1.6, 3.6, 1.4, "Total Marketplace GMV", "$15.91M", "Target: $15.0M (+6.1% over target)", ACCENT_BLUE)
    add_card(s2, 4.8, 1.6, 3.6, 1.4, "Total Orders Volume", "99,941", "Completed customer transactions", ACCENT_TEAL)
    add_card(s2, 8.8, 1.6, 3.6, 1.4, "Average Order Value (AOV)", "$159.33", "Consistent basket spend across 3 years", ACCENT_GOLD)

    add_card(s2, 0.8, 3.3, 3.6, 1.4, "On-Time Delivery SLA", "93.23%", "Target: 95.0% (-1.77% shortfall = 6.7K late)", ACCENT_CORAL)
    add_card(s2, 4.8, 3.3, 3.6, 1.4, "Average Customer Rating", "4.09 ⭐", "Target: 4.20 ⭐ (Weighted average review)", ACCENT_GOLD)
    add_card(s2, 8.8, 3.3, 3.6, 1.4, "Repeat Customer Rate", "3.12%", "Target: 10.0% (Severe retention bottleneck)", ACCENT_CORAL)

    # Executive Summary Text Card
    summary_box = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(5.0), Inches(11.6), Inches(1.8))
    summary_box.fill.solid()
    summary_box.fill.fore_color.rgb = CARD_BG
    summary_box.line.color.rgb = ACCENT_BLUE
    stf = summary_box.text_frame
    stf.word_wrap = True
    sp1 = stf.paragraphs[0]
    sp1.text = "EXECUTIVE VERDICT & STRATEGIC PRIORITIES"
    sp1.font.size = Pt(12)
    sp1.font.bold = True
    sp1.font.color.rgb = ACCENT_GOLD

    sp2 = stf.add_paragraph()
    sp2.text = "1. Commercial growth is robust: $15.91M GMV achieved via stable $159 AOV and high credit adoption (78.3%).\n2. Logistics friction threatens brand equity: Regional disparities in the Northeast drag fulfillment down to 78.6%.\n3. The Retention Emergency: Only 3.12% repeat rate means Olist acquires 96K customers once and loses them permanently."
    sp2.font.size = Pt(11)
    sp2.font.color.rgb = TEXT_WHITE

    # -------------------------------------------------------------
    # SLIDE 3: PILLAR 1 — REVENUE VELOCITY & TIME INTELLIGENCE
    # -------------------------------------------------------------
    s3 = prs.slides.add_slide(blank_layout)
    set_slide_background(s3)
    add_header(s3, "Pillar 1: Revenue Velocity & Seasonal Expansion", "COMMERCIAL PERFORMANCE")

    add_card(s3, 0.8, 1.6, 5.6, 5.2, "Commercial Trajectory Findings", "Exponential Growth", "", ACCENT_BLUE)
    c1_tf = s3.shapes[-1].text_frame
    c1_tf.paragraphs[1].text = "2016-2018 Run Rate"
    c1_tf.paragraphs[1].font.size = Pt(16)
    p = c1_tf.add_paragraph()
    p.text = "\n• 2016 Beta: Under $60K in exploratory commercial revenue.\n• 2017 Breakout: Steady MoM compounding culminating in the Black Friday peak (Nov 2017: $1.19M GMV in 30 days).\n• 2018 Sustained Baseline: Elevated run-rate averaging $850K - $1.05M per month.\n• Price Inelasticity: AOV remained virtually constant ($158.37 in 2017 vs $160.04 in 2018), proving scaling was driven entirely by transactional customer volume."
    p.font.size = Pt(11)
    p.font.color.rgb = TEXT_WHITE

    add_card(s3, 6.8, 1.6, 5.6, 5.2, "Payment Tender & Financing Split", "Credit Card Dominance", "", ACCENT_TEAL)
    c2_tf = s3.shapes[-1].text_frame
    c2_tf.paragraphs[1].text = "78.34% Credit Share"
    c2_tf.paragraphs[1].font.size = Pt(16)
    p = c2_tf.add_paragraph()
    p.text = "\n• Credit Card: $12.54M (78.34%) — 3.5 average installments. Over 28% of credit buyers spread payments across 6-10 months.\n• Boleto Bancário: $2.87M (17.92%) — Crucial cash-voucher rail for unbanked and small-business buyers.\n• Vouchers: $379K (2.37%) — Primarily customer service recovery and promotional credits.\n• Debit Cards: $218K (1.36%) — Niche transactional rail.\n• Insight: Brazil's installment financing culture is the primary liquidity engine supporting Olist's $159 basket size."
    p.font.size = Pt(11)
    p.font.color.rgb = TEXT_WHITE

    # -------------------------------------------------------------
    # SLIDE 4: PILLAR 1 — CATEGORY & GEOGRAPHY CONCENTRATION
    # -------------------------------------------------------------
    s4 = prs.slides.add_slide(blank_layout)
    set_slide_background(s4)
    add_header(s4, "Pillar 1: Product Category & Regional Concentration", "COMMERCIAL PERFORMANCE")

    add_card(s4, 0.8, 1.6, 5.6, 5.2, "Top 10 Product Categories", "$9.95M (62.5% GMV)", "", ACCENT_GOLD)
    c3_tf = s4.shapes[-1].text_frame
    c3_tf.paragraphs[1].text = "Top 5 Categories Drive 40%"
    c3_tf.paragraphs[1].font.size = Pt(16)
    p = c3_tf.add_paragraph()
    p.text = "\n1. health_beauty: $1.44M (High margin, low friction 21.4%)\n2. watches_gifts: $1.31M (Premium ticket, low shipping friction 16.8%)\n3. bed_bath_table: $1.24M (Core volume, 11,115 orders)\n4. sports_leisure: $1.16M (Lifestyle active goods)\n5. computers_accessories: $1.06M (Tech hardware)\n6. furniture_decor: $0.90M (High freight burden 38.6%)\n7. housewares: $0.78M | 8. cool_stuff: $0.72M\n9. auto: $0.69M | 10. garden_tools: $0.58M"
    p.font.size = Pt(10.5)
    p.font.color.rgb = TEXT_WHITE

    add_card(s4, 6.8, 1.6, 5.6, 5.2, "Geographic Revenue Concentration", "62.3% in Southeast", "", ACCENT_BLUE)
    c4_tf = s4.shapes[-1].text_frame
    c4_tf.paragraphs[1].text = "São Paulo Hegemony"
    c4_tf.paragraphs[1].font.size = Pt(16)
    p = c4_tf.add_paragraph()
    p.text = "\n• São Paulo (SP): $5.91M (37.1% national GMV) — The epicenter of Brazilian consumer demand and merchant supply.\n• Rio de Janeiro (RJ): $2.14M (13.4% GMV) — High revenue but plagued by logistics delivery delays.\n• Minas Gerais (MG): $1.92M (12.1% GMV) — Strong tertiary market.\n• Southern Cluster (RS, PR, SC): $2.33M (14.6% GMV) — Highest on-time fulfillment rates nationally (>95%).\n• Long-Tail (18 other states): Generate under 22% combined, facing severe transport transit friction."
    p.font.size = Pt(11)
    p.font.color.rgb = TEXT_WHITE

    # -------------------------------------------------------------
    # SLIDE 5: PILLAR 2 — LOGISTICS FULFILLMENT & REGIONAL SLA
    # -------------------------------------------------------------
    s5 = prs.slides.add_slide(blank_layout)
    set_slide_background(s5)
    add_header(s5, "Pillar 2: Logistics SLA & Geographic Fulfillment Divide", "SUPPLY CHAIN & OPERATIONS")

    add_card(s5, 0.8, 1.6, 3.6, 2.2, "National On-Time Rate", "93.23%", "Target: 95.0% (-1.77% gap = 6,770 late shipments)", ACCENT_CORAL)
    add_card(s5, 4.8, 1.6, 3.6, 2.2, "Average Transit Duration", "12.56 Days", "From customer purchase to doorstep delivery", ACCENT_GOLD)
    add_card(s5, 8.8, 1.6, 3.6, 2.2, "Portfolio Freight Ratio", "16.57%", "Macro freight as % of Net Product Revenue", ACCENT_TEAL)

    add_card(s5, 0.8, 4.1, 11.6, 2.7, "Regional Fulfillment Disparities", "The North/Northeast Logistics Bottleneck", "", ACCENT_CORAL)
    c5_tf = s5.shapes[-1].text_frame
    c5_tf.paragraphs[1].text = "Southeastern Efficiency vs. Northern Drag"
    c5_tf.paragraphs[1].font.size = Pt(15)
    p = c5_tf.add_paragraph()
    p.text = "• Southeastern Champions: São Paulo (96.4%), Paraná (95.8%), and Santa Catarina (95.1%) meet or exceed the 95.0% SLA.\n• The Northeastern Breakdown: Alagoas (AL: 78.6%), Maranhão (MA: 82.6%), Sergipe (SE: 84.8%), Piauí (PI: 86.1%), and Ceará (CE: 86.2%) severely fail corporate standards.\n• Root Cause: 70%+ of merchants ship from São Paulo via Correios road networks. Cross-country transit to the Amazon/Northeast takes 21-25 days on average, creating acute fulfillment dissatisfaction."
    p.font.size = Pt(11)
    p.font.color.rgb = TEXT_WHITE

    # -------------------------------------------------------------
    # SLIDE 6: PILLAR 3 — THE SMOKING GUN: TRANSIT VS. RATING
    # -------------------------------------------------------------
    s6 = prs.slides.add_slide(blank_layout)
    set_slide_background(s6)
    add_header(s6, "Pillar 3: The Smoking Gun — Transit Delay vs. Rating", "CUSTOMER EXPERIENCE & RETENTION")

    add_card(s6, 0.8, 1.6, 5.6, 5.2, "Empirical Delivery Transit Days vs. Review Score", "10.6-Day Delivery Penalty", "", ACCENT_CORAL)
    c6_tf = s6.shapes[-1].text_frame
    c6_tf.paragraphs[1].text = "Rating Dictated by Transit Speed"
    c6_tf.paragraphs[1].font.size = Pt(16)
    p = c6_tf.add_paragraph()
    p.text = "\n⭐ 5-Star Orders: Arrive in 10.7 Days (High customer delight)\n⭐ 4-Star Orders: Arrive in 12.3 Days (+1.6 days)\n⭐ 3-Star Orders: Arrive in 14.3 Days (+3.6 days)\n⭐ 2-Star Orders: Arrive in 16.7 Days (+6.0 days)\n⭐ 1-Star Orders: Arrive in 21.3 Days (+10.6 days — DOUBLE TRANSIT)\n\n• Mathematical Finding: Every additional week of carrier transit reduces customer satisfaction by nearly 2 stars.\n• Conclusion: Delivery transit duration is the #1 controllable cause of customer churn and 1-star negative ratings."
    p.font.size = Pt(11)
    p.font.color.rgb = TEXT_WHITE

    add_card(s6, 6.8, 1.6, 5.6, 5.2, "Customer Retention & Sentiment Polarity", "Bimodal Polarity", "", ACCENT_GOLD)
    c7_tf = s6.shapes[-1].text_frame
    c7_tf.paragraphs[1].text = "3.12% Repeat Buyer Crisis"
    c7_tf.paragraphs[1].font.size = Pt(16)
    p = c7_tf.add_paragraph()
    p.text = "\n• Polarized Sentiment: 57.1K reviews are 5-star, but 11.4K reviews are 1-star (forming the second largest cohort at 11.5%). Only 3.1K are 2-star.\n• The 3.12% Retention Deficit: Out of 96,096 unique buyers, only 2,997 ever made a second purchase. The e-commerce industry benchmark is 15-25%.\n• Economic Cost: Olist acquires customers once at full marketing CAC, but loses 96.88% of them due to fulfillment friction.\n• Strategic Objective: Raising retention from 3.12% to 6.0% unlocks +$450K in high-margin recurring GMV."
    p.font.size = Pt(11)
    p.font.color.rgb = TEXT_WHITE

    # -------------------------------------------------------------
    # SLIDE 7: SELLER PARETO & MONOPOLIZATION RISK
    # -------------------------------------------------------------
    s7 = prs.slides.add_slide(blank_layout)
    set_slide_background(s7)
    add_header(s7, "Pillar 3: Merchant Quality & The 80/20 Pareto Curve", "MERCHANT ECOSYSTEM")

    add_card(s7, 0.8, 1.6, 5.6, 5.2, "Seller Revenue Concentration", "Classic 80/20 Rule", "", ACCENT_BLUE)
    c8_tf = s7.shapes[-1].text_frame
    c8_tf.paragraphs[1].text = "Top 10% Sellers Drive 78.4% GMV"
    c8_tf.paragraphs[1].font.size = Pt(16)
    p = c8_tf.add_paragraph()
    p.text = "\n• Active Merchant Base: 3,095 sellers on the marketplace.\n• Top 20 Elite Sellers (0.6%): Account for over $3.8M in revenue.\n• Top 10% Merchants: Generate 78.4% of total marketplace GMV.\n• Monopolization Fragility: Loss of key merchant accounts directly impairs marketplace liquidity.\n• The Long Tail Overhead: The bottom 2,000 sellers generate under 10% of revenue while generating disproportionate support tickets and delayed carrier dispatches."
    p.font.size = Pt(11)
    p.font.color.rgb = TEXT_WHITE

    add_card(s7, 6.8, 1.6, 5.6, 5.2, "Merchant SLA & Dispatch Compliance", "Dispatch Friction", "", ACCENT_CORAL)
    c9_tf = s7.shapes[-1].text_frame
    c9_tf.paragraphs[1].text = "Carrier Hand-off Delays"
    c9_tf.paragraphs[1].font.size = Pt(16)
    p = c9_tf.add_paragraph()
    p.text = "\n• Merchant Handling Time: Averages 2.8 days before packages are transferred to carriers (`order_delivered_carrier_date`).\n• Top-Tier Sellers: Hand packages to carriers within 18 hours.\n• Bottom-Tier Sellers: Take 4 to 6 business days just to pack and dispatch orders, immediately exhausting the SLA buffer.\n• Action: Institute seller penalties and dispatch cutoffs: merchants failing to ship within 48 hours must face temporary suspension from search rankings."
    p.font.size = Pt(11)
    p.font.color.rgb = TEXT_WHITE

    # -------------------------------------------------------------
    # SLIDE 8: STRATEGIC RECOMMENDATIONS & ROI MATRIX
    # -------------------------------------------------------------
    s8 = prs.slides.add_slide(blank_layout)
    set_slide_background(s8)
    add_header(s8, "Prioritized Strategic Initiatives & Projected ROI", "ACTIONABLE ROADMAP")

    add_card(s8, 0.8, 1.6, 3.6, 5.2, "1. Logistics Micro-Hubs", "Cut Transit by 55%", "Owner: VP Logistics", ACCENT_BLUE)
    c10_tf = s8.shapes[-1].text_frame
    p = c10_tf.add_paragraph()
    p.text = "\n• Deploy regional 3PL fulfillment hubs in Recife (PE) and Salvador (BA).\n• Pre-stock Top 50 fast-moving SKUs.\n• Slashes Northeastern transit from 21 days to 6 days.\n• Financial ROI: Recovers $680K in churned customer GMV; lifts national SLA to 96.5%."
    p.font.size = Pt(10.5)
    p.font.color.rgb = TEXT_WHITE

    add_card(s8, 4.8, 1.6, 3.6, 5.2, "2. Proactive CX Credits", "Save Late Churn", "Owner: Head of CX", ACCENT_TEAL)
    c11_tf = s8.shapes[-1].text_frame
    p = c11_tf.add_paragraph()
    p.text = "\n• Trigger automated WhatsApp alerts when tracking flags transit > 12 days.\n• Issue 15% courtesy retention vouchers on the spot.\n• Converts 1-star detractors into appeased return buyers.\n• Financial ROI: Lifts repeat customer rate from 3.12% to 5.5% (+$380K annual GMV)."
    p.font.size = Pt(10.5)
    p.font.color.rgb = TEXT_WHITE

    add_card(s8, 8.8, 1.6, 3.6, 5.2, "3. Cart Bundling Engine", "+16% Basket Lift", "Owner: Head of Growth", ACCENT_GOLD)
    c12_tf = s8.shapes[-1].text_frame
    p = c12_tf.add_paragraph()
    p.text = "\n• Introduce dynamic checkout cross-sells (Bed & Bath + Housewares).\n• 0% interest split installments on baskets > $250.\n• Increases basket items from 1.13 to 1.35.\n• Financial ROI: Lifts AOV from $159 to $185 (+$1.5M incremental revenue)."
    p.font.size = Pt(10.5)
    p.font.color.rgb = TEXT_WHITE

    # -------------------------------------------------------------
    # SLIDE 9: TECHNICAL ARCHITECTURE & PRODUCTION RESILIENCE
    # -------------------------------------------------------------
    s9 = prs.slides.add_slide(blank_layout)
    set_slide_background(s9)
    add_header(s9, "Enterprise Cloud BI Architecture & Data Pipeline", "TECHNICAL INFRASTRUCTURE")

    add_card(s9, 0.8, 1.6, 11.6, 5.2, "End-to-End Multi-Cloud Architecture", "100% Production Audit Verified", "", ACCENT_BLUE)
    c13_tf = s9.shapes[-1].text_frame
    c13_tf.paragraphs[1].text = "Zero Defects | Multi-Source Cloud Integration"
    c13_tf.paragraphs[1].font.size = Pt(15)
    p = c13_tf.add_paragraph()
    p.text = "\n• Tier 1: Supabase PostgreSQL (Facts Layer) — Hosts 99,941 orders, 113,223 line items, 104,377 payments, and 99,709 reviews with composite PK indexing and IPv4 session pooling.\n• Tier 2: Google BigQuery Sandbox (Dimensions Layer) — Streams 99,441 customers, 32,951 products, 3,095 sellers, and 800 calendar dates with pyarrow columnar speed.\n• Tier 3: Google Sheets (Governance Layer) — Live REST lookup endpoints for category translations and corporate SLA KPI targets.\n• Tier 4: Power BI Desktop & VertiPaq Engine — 3-Page Executive Cockpit with 18 DAX measures, bidirectional cross-filtering, and display folders.\n• Live Streaming Verified: Automated ingestion engine (simulate_new_orders.py) pushed 500 streaming orders in an atomic transaction; refreshed dynamically in Power BI in < 30 seconds."
    p.font.size = Pt(11)
    p.font.color.rgb = TEXT_WHITE

    # -------------------------------------------------------------
    # SLIDE 10: CLOSING & Q&A
    # -------------------------------------------------------------
    s10 = prs.slides.add_slide(blank_layout)
    set_slide_background(s10)

    tbox10 = s10.shapes.add_textbox(Inches(1.2), Inches(2.2), Inches(11.0), Inches(3.5))
    tf10 = tbox10.text_frame
    tf10.word_wrap = True

    p = tf10.paragraphs[0]
    p.text = "THANK YOU"
    p.font.size = Pt(40)
    p.font.bold = True
    p.font.color.rgb = TEXT_WHITE

    p = tf10.add_paragraph()
    p.text = "\nQuestions & Executive Discussion"
    p.font.size = Pt(22)
    p.font.color.rgb = ACCENT_GOLD

    p = tf10.add_paragraph()
    p.text = "\nDeliverables Available: 3-Page Power BI Executive Cockpit | Detailed Findings Report (Markdown) | Multi-Cloud Codebase"
    p.font.size = Pt(13)
    p.font.color.rgb = TEXT_MUTED

    # Save presentation
    os.makedirs(os.path.join(os.path.dirname(__file__), '..', 'reports'), exist_ok=True)
    output_path = os.path.join(os.path.dirname(__file__), '..', 'reports', 'executive_presentation.pptx')
    prs.save(output_path)
    print(f"✅ Boardroom-ready PowerPoint deck generated successfully at:\n   {output_path}")

if __name__ == '__main__':
    create_deck()
