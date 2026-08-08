from io import BytesIO
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from datetime import datetime

def _get_booking_value(booking, field, default="N/A"):
    if isinstance(booking, dict):
        return booking.get(field, default) or default
    value = getattr(booking, field, None)
    return value if value not in (None, "") else default


def generate_pdf_report(bookings_data, occupancy_rate=75):
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )
    
    elements = []
    styles = getSampleStyleSheet()

    # Custom Styles
    brand_title_style = ParagraphStyle(
        'BrandTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=24,
        textColor=colors.HexColor('#D97706'), # Gold / Amber Accent
        spaceAfter=4
    )
    
    brand_sub_style = ParagraphStyle(
        'BrandSub',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        textColor=colors.HexColor('#4B5563'),
        spaceAfter=15
    )

    header_meta_style = ParagraphStyle(
        'HeaderMeta',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        textColor=colors.HexColor('#6B7280'),
        alignment=2 # Right Align
    )

    card_label_style = ParagraphStyle(
        'CardLabel',
        fontName='Helvetica-Bold',
        fontSize=9,
        textColor=colors.HexColor('#6B7280'),
        alignment=1
    )

    card_value_style = ParagraphStyle(
        'CardValue',
        fontName='Helvetica-Bold',
        fontSize=16,
        textColor=colors.HexColor('#1F2937'),
        alignment=1
    )

    # 1. HEADER SECTION
    today_str = datetime.now().strftime('%b %d, %Y | %I:%M %p')
    header_data = [
        [
            Paragraph("<b>BELLA VISTA</b><br/><font size=9 color='#6B7280'>FINE DINING & LUXURY RESTAURANT</font>", brand_title_style),
            Paragraph(f"<b>DAILY BOOKING REPORT</b><br/>Generated: {today_str}<br/>Status: <b>CONFIDENTIAL</b>", header_meta_style)
        ]
    ]
    header_table = Table(header_data, colWidths=[300, 220])
    header_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    elements.append(header_table)
    
    elements.append(Spacer(1, 10))
    elements.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor('#D97706'), spaceAfter=15))

    # 2. EXECUTIVE SUMMARY CARDS
    total_bookings = len(bookings_data)
    confirmed = sum(
        1 for b in bookings_data
        if _get_booking_value(b, 'status', 'Available') in ['Reserved', 'Booked', 'Occupied']
    )
    
    summary_data = [
        [
            Paragraph("TOTAL BOOKINGS", card_label_style),
            Paragraph("CONFIRMED", card_label_style),
            Paragraph("OCCUPANCY RATE", card_label_style)
        ],
        [
            Paragraph(str(total_bookings), card_value_style),
            Paragraph(str(confirmed), card_value_style),
            Paragraph(f"{occupancy_rate}%", card_value_style)
        ]
    ]
    summary_table = Table(summary_data, colWidths=[170, 170, 170])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F9FAFB')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#E5E7EB')),
        ('INNERGRID', (0,0), (-1,-1), 1, colors.HexColor('#E5E7EB')),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ]))
    elements.append(summary_table)
    elements.append(Spacer(1, 20))

    # 3. BOOKINGS TABLE
    elements.append(Paragraph("<b>Detailed Booking List</b>", ParagraphStyle('SubHeading', fontName='Helvetica-Bold', fontSize=14, textColor=colors.HexColor('#1F2937'), spaceAfter=10)))

    table_data = [["#", "Customer Name", "Table No", "Floor", "Date & Time", "Status"]]
    
    for idx, b in enumerate(bookings_data, start=1):
        status = _get_booking_value(b, 'status', 'Available')
        
        # Dynamic Status Colors
        if status == 'Available':
            status_html = f"<font color='#16A34A'><b>{status}</b></font>"
        elif status == 'Reserved':
            status_html = f"<font color='#D97706'><b>{status}</b></font>"
        else:
            status_html = f"<font color='#DC2626'><b>{status}</b></font>"

        table_data.append([
            str(idx),
            _get_booking_value(b, 'customer_name', 'N/A'),
            _get_booking_value(b, 'table_name', 'N/A'),
            _get_booking_value(b, 'floor', 'Floor 1'),
            f"{_get_booking_value(b, 'booking_date', '')} {_get_booking_value(b, 'booking_time', '')}".strip(),
            Paragraph(status_html, styles['Normal'])
        ])

    data_table = Table(table_data, colWidths=[30, 140, 70, 70, 120, 80])
    data_table.setStyle(TableStyle([
        # Header Styling
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1F2937')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 10),
        ('BOTTOMPADDING', (0,0), (-1,0), 8),
        ('TOPPADDING', (0,0), (-1,0), 8),
        ('ALIGN', (0,0), (-1,0), 'LEFT'),
        
        # Row Alternating Background
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#F9FAFB')]),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E5E7EB')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
        ('FONTSIZE', (0,1), (-1,-1), 9),
        ('TOPPADDING', (0,1), (-1,-1), 6),
        ('BOTTOMPADDING', (0,1), (-1,-1), 6),
    ]))
    
    elements.append(data_table)
    elements.append(Spacer(1, 30))

    # 4. FOOTER / SIGNATURE SECTION
    footer_data = [
        [
            Paragraph("<b>Prepared By:</b><br/>Restaurant Manager", styles['Normal']),
            Paragraph("<b>Authorized Signature:</b><br/>_______________________", header_meta_style)
        ]
    ]
    footer_table = Table(footer_data, colWidths=[260, 250])
    footer_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'BOTTOM'),
    ]))
    elements.append(footer_table)

    # Build PDF
    doc.build(elements)
    buffer.seek(0)
    return buffer