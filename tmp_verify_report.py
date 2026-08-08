from reports import generate_pdf_report
from types import SimpleNamespace

bookings = [
    SimpleNamespace(
        customer_name='Alice',
        table_name='T1',
        floor='Floor 1',
        booking_date='2026-08-08',
        booking_time='19:00',
        status='Reserved',
    )
]

buffer = generate_pdf_report(bookings, occupancy_rate=80)
print('generated', buffer.getbuffer().nbytes)
