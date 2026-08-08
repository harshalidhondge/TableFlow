from utils.extensions import db


class Table(db.Model):
    __tablename__ = "tables"

    id = db.Column(db.Integer, primary_key=True)

    # Table Details
    table_name = db.Column(db.String(100), nullable=False)

    capacity = db.Column(db.Integer, nullable=False, default=4)

    floor = db.Column(db.String(30), nullable=False, default="Floor 1")

    location = db.Column(db.String(100), nullable=False, default="Main Hall")

    table_type = db.Column(db.String(50), nullable=False, default="Regular")

    # Booking Details
    customer_name = db.Column(db.String(100))

    description = db.Column(db.String(255))

    booking_date = db.Column(db.Date)

    booking_time = db.Column(db.Time)

    status = db.Column(
        db.String(30),
        default="Available"
    )

    # Owner
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id")
    )