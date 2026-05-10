import json
import os
from django.conf import settings

_MAHARASHTRA_PINCODES = None

def get_maharashtra_pincodes():
    global _MAHARASHTRA_PINCODES
    if _MAHARASHTRA_PINCODES is None:
        json_path = os.path.join(settings.BASE_DIR, 'orders', 'data', 'maharashtra_pincodes.json')
        try:
            with open(json_path, 'r') as f:
                pincode_list = json.load(f)
                _MAHARASHTRA_PINCODES = set(str(p) for p in pincode_list)
        except Exception as e:
            print(f"Error loading Maharashtra pincodes: {e}")
            _MAHARASHTRA_PINCODES = set()
    return _MAHARASHTRA_PINCODES

def is_maharashtra_pincode(pincode):
    if not pincode:
        return False
    valid_set = get_maharashtra_pincodes()
    return str(pincode).strip() in valid_set

def generate_invoice_pdf(order):
    from reportlab.lib.pagesizes import A4
    from reportlab.lib import colors
    from reportlab.lib.units import cm
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet
    import io

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=2*cm, leftMargin=2*cm, topMargin=2*cm, bottomMargin=2*cm)
    styles = getSampleStyleSheet()
    elements = []

    # Title
    elements.append(Paragraph(f"INVOICE", styles['Title']))
    elements.append(Spacer(1, 0.5*cm))

    # Header Info (Company & Customer)
    header_data = [
        [Paragraph(f"<b>From:</b><br/>Soham Gift Ltd<br/>Maharashtra, India", styles['Normal']),
         Paragraph(f"<b>To:</b><br/>{order.user.get_full_name() or order.user.username}<br/>{order.address.street_address}<br/>{order.address.city}, {order.address.pincode}", styles['Normal'])]
    ]
    header_table = Table(header_data, colWidths=[9*cm, 9*cm])
    elements.append(header_table)
    elements.append(Spacer(1, 0.5*cm))

    # Order Info
    elements.append(Paragraph(f"<b>Order ID:</b> {order.id}", styles['Normal']))
    elements.append(Paragraph(f"<b>Date:</b> {order.created_at.strftime('%Y-%m-%d %H:%M')}", styles['Normal']))
    if order.gst_number:
        elements.append(Paragraph(f"<b>GST:</b> {order.gst_number}", styles['Normal']))
    elements.append(Spacer(1, 1*cm))

    # Items Table
    data = [['Product', 'Qty', 'Unit Price', 'Subtotal']]
    for item in order.items.all():
        data.append([item.product.name, str(item.quantity), f"₹{item.price}", f"₹{item.price * item.quantity}"])
    
    # Summary rows
    data.append(['', '', 'Subtotal:', f"₹{sum(i.price * i.quantity for i in order.items.all())}"])
    data.append(['', '', 'Shipping:', f"₹{order.shipping_charges}"])
    data.append(['', '', 'Tax (18%):', f"₹{order.tax_amount}"])
    if order.coupon:
        discount = (order.total_amount * order.coupon.discount_percent / 100) # Simplified
        data.append(['', '', 'Discount:', f"-₹{discount}"])
    data.append(['', '', 'Total:', f"₹{order.total_amount}"])

    table = Table(data, colWidths=[8*cm, 2*cm, 4*cm, 4*cm])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ALIGN', (2, 0), (3, -1), 'RIGHT'),
    ]))
    elements.append(table)
    
    doc.build(elements)
    buffer.seek(0)
    return buffer
