from sqlalchemy import Column, Integer, String, DateTime, Table, ForeignKey, Float
from geoalchemy2 import Geometry
from app.database import Base
from datetime import datetime
from sqlalchemy.orm import relationship, validates, mapped_column, Mapped


user_department = Table(
    "user_department",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("department_id", Integer, ForeignKey("departments.id"), primary_key=True),
)


class User(Base):
    __tablename__ = "users"

    ROLES = ["admin", "volunteer"]

    id = Column(Integer, primary_key=True, index=True)
    firstname = Column(String, index=True)
    lastname = Column(String, index=True)
    login = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String, index=True, nullable=True)
    role = Column(String, index=True)
    created_at = Column(DateTime, default=datetime.now)
    # TODO: updated_at is not set when departments are updated
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    deleted_at = Column(DateTime, nullable=True)

    departments = relationship("Department", secondary=user_department, back_populates="users")
    clear_cuts = relationship("ClearCut", back_populates="user")

    @validates("role")
    def validate_role(self, key, value):
        if value not in User.ROLES:
            raise ValueError(f"Role must be one of: {', '.join(User.ROLES)}")
        return value


class Department(Base):
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, index=True)
    name = Column(String)
    users = relationship("User", secondary=user_department, back_populates="departments")
    cities: Mapped[list["City"]] = relationship()

    @validates("name")
    def validate_name(self, key, value):
        if key == "name" and value is None:
            raise ValueError("Name cannot be None")
        return value


class City(Base):
    __tablename__ = "cities"
    id = Column(Integer, primary_key=True, index=True)
    zip_code = Column(String, index=True)
    name = Column(String)
    department_id: Mapped[int] = mapped_column(ForeignKey("departments.id"))
    department: Mapped["Department"] = relationship(back_populates="cities")
    clear_cuts: Mapped[list["ClearCut"]] = relationship(back_populates="city")


CLEARCUT_STATUSES = [
    "to_validate",
    "waiting_for_validation",
    "legal_validated",
    "validated",
    "final_validated",
]


class ClearCut(Base):
    __tablename__ = "clear_cuts"

    id = Column(Integer, primary_key=True, index=True)
    cut_date = Column(DateTime, index=True)
    slope_percentage = Column(Float, index=True)
    location = Column(Geometry(geometry_type="Point", srid=4326))
    boundary = Column(Geometry(geometry_type="MultiPolygon", srid=4326))
    status = Column(String, index=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    natura_name = Column(String, nullable=True)
    natura_code = Column(String, nullable=True)

    city_id: Mapped[int] = mapped_column(ForeignKey("cities.id"))
    city: Mapped["City"] = relationship(back_populates="clear_cuts")

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=True)
    user: Mapped["User"] = relationship(back_populates="clear_cuts")

    @validates("status")
    def validate_status(self, key, value):
        if value not in CLEARCUT_STATUSES:
            raise ValueError(f"Status must be one of: {', '.join(CLEARCUT_STATUSES)}")
        return value
