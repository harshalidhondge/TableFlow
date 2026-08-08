import unittest
from types import SimpleNamespace

from reports import generate_pdf_report


class GeneratePdfReportTests(unittest.TestCase):
    def test_generate_pdf_report_accepts_model_like_objects(self):
        bookings = [
            SimpleNamespace(
                customer_name="Alice",
                table_name="T1",
                floor="Floor 1",
                booking_date="2026-08-08",
                booking_time="19:00",
                status="Reserved",
            )
        ]

        buffer = generate_pdf_report(bookings, occupancy_rate=80)

        self.assertIsNotNone(buffer)
        self.assertGreater(buffer.getbuffer().nbytes, 0)


if __name__ == "__main__":
    unittest.main()
