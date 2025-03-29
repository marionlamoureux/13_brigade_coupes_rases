"""migration

Revision ID: 1de801c4268d
Revises:
Create Date: 2025-03-28 22:02:50.875319

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import geoalchemy2


# revision identifiers, used by Alembic.
revision: str = "1de801c4268d"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "departments",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("code", sa.String(), nullable=True),
        sa.Column("name", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_departments_code"), "departments", ["code"], unique=False)
    op.create_index(op.f("ix_departments_id"), "departments", ["id"], unique=False)
    op.create_table(
        "ecological_zonings",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("type", sa.String(), nullable=True),
        sa.Column("sub_type", sa.String(), nullable=True),
        sa.Column("name", sa.String(), nullable=True),
        sa.Column("code", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_ecological_zonings_code"), "ecological_zonings", ["code"], unique=False
    )
    op.create_index(
        op.f("ix_ecological_zonings_id"), "ecological_zonings", ["id"], unique=False
    )
    op.create_index(
        op.f("ix_ecological_zonings_name"), "ecological_zonings", ["name"], unique=False
    )
    op.create_index(
        op.f("ix_ecological_zonings_sub_type"), "ecological_zonings", ["sub_type"], unique=False
    )
    op.create_index(
        op.f("ix_ecological_zonings_type"), "ecological_zonings", ["type"], unique=False
    )
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("firstname", sa.String(), nullable=True),
        sa.Column("lastname", sa.String(), nullable=True),
        sa.Column("login", sa.String(), nullable=True),
        sa.Column("email", sa.String(), nullable=True),
        sa.Column("password", sa.String(), nullable=True),
        sa.Column("role", sa.String(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.Column("deleted_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_users_email"), "users", ["email"], unique=True)
    op.create_index(op.f("ix_users_firstname"), "users", ["firstname"], unique=False)
    op.create_index(op.f("ix_users_id"), "users", ["id"], unique=False)
    op.create_index(op.f("ix_users_lastname"), "users", ["lastname"], unique=False)
    op.create_index(op.f("ix_users_login"), "users", ["login"], unique=True)
    op.create_index(op.f("ix_users_password"), "users", ["password"], unique=False)
    op.create_index(op.f("ix_users_role"), "users", ["role"], unique=False)
    op.create_table(
        "cities",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("zip_code", sa.String(), nullable=True),
        sa.Column("name", sa.String(), nullable=True),
        sa.Column("department_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["department_id"],
            ["departments.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_cities_id"), "cities", ["id"], unique=False)
    op.create_index(op.f("ix_cities_zip_code"), "cities", ["zip_code"], unique=False)
    op.create_table(
        "clear_cuts",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("cut_date", sa.DateTime(), nullable=True),
        sa.Column("slope_percentage", sa.Float(), nullable=True),
        sa.Column("area_hectare", sa.Float(), nullable=True),
        sa.Column(
            "location",
            geoalchemy2.types.Geometry(
                geometry_type="POINT", srid=4326, from_text="ST_GeomFromEWKT", name="geometry"
            ),
            nullable=True,
        ),
        sa.Column(
            "boundary",
            geoalchemy2.types.Geometry(
                geometry_type="MULTIPOLYGON",
                srid=4326,
                from_text="ST_GeomFromEWKT",
                name="geometry",
            ),
            nullable=True,
        ),
        sa.Column("status", sa.String(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.Column("natura_name", sa.String(), nullable=True),
        sa.Column("natura_code", sa.String(), nullable=True),
        sa.Column("user_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_clear_cuts_area_hectare"), "clear_cuts", ["area_hectare"], unique=False
    )
    op.create_index(op.f("ix_clear_cuts_cut_date"), "clear_cuts", ["cut_date"], unique=False)
    op.create_index(op.f("ix_clear_cuts_id"), "clear_cuts", ["id"], unique=False)
    op.create_index(
        op.f("ix_clear_cuts_slope_percentage"), "clear_cuts", ["slope_percentage"], unique=False
    )
    op.create_index(op.f("ix_clear_cuts_status"), "clear_cuts", ["status"], unique=False)
    op.create_table(
        "user_department",
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("department_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["department_id"],
            ["departments.id"],
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("user_id", "department_id"),
    )
    op.create_table(
        "ecological_zoning_clear_cut",
        sa.Column("ecological_zoning_id", sa.Integer(), nullable=False),
        sa.Column("clear_cut_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["clear_cut_id"],
            ["clear_cuts.id"],
        ),
        sa.ForeignKeyConstraint(
            ["ecological_zoning_id"],
            ["ecological_zonings.id"],
        ),
        sa.PrimaryKeyConstraint("ecological_zoning_id", "clear_cut_id"),
    )
    op.create_table(
        "registries",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("number", sa.String(), nullable=True),
        sa.Column("sheet", sa.Integer(), nullable=True),
        sa.Column("section", sa.String(), nullable=True),
        sa.Column("district_code", sa.String(), nullable=True),
        sa.Column("city_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["city_id"],
            ["cities.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_registries_district_code"), "registries", ["district_code"], unique=False
    )
    op.create_index(op.f("ix_registries_id"), "registries", ["id"], unique=False)
    op.create_index(op.f("ix_registries_number"), "registries", ["number"], unique=False)
    op.create_index(op.f("ix_registries_section"), "registries", ["section"], unique=False)
    op.create_index(op.f("ix_registries_sheet"), "registries", ["sheet"], unique=False)
    op.create_table(
        "registry_clear_cut",
        sa.Column("registry_id", sa.Integer(), nullable=False),
        sa.Column("clear_cut_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["clear_cut_id"],
            ["clear_cuts.id"],
        ),
        sa.ForeignKeyConstraint(
            ["registry_id"],
            ["registries.id"],
        ),
        sa.PrimaryKeyConstraint("registry_id", "clear_cut_id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("registry_clear_cut")
    op.drop_index(op.f("ix_registries_sheet"), table_name="registries")
    op.drop_index(op.f("ix_registries_section"), table_name="registries")
    op.drop_index(op.f("ix_registries_number"), table_name="registries")
    op.drop_index(op.f("ix_registries_id"), table_name="registries")
    op.drop_index(op.f("ix_registries_district_code"), table_name="registries")
    op.drop_table("registries")
    op.drop_table("ecological_zoning_clear_cut")
    op.drop_table("user_department")
    op.drop_index(op.f("ix_clear_cuts_status"), table_name="clear_cuts")
    op.drop_index(op.f("ix_clear_cuts_slope_percentage"), table_name="clear_cuts")
    op.drop_index(op.f("ix_clear_cuts_id"), table_name="clear_cuts")
    op.drop_index(op.f("ix_clear_cuts_cut_date"), table_name="clear_cuts")
    op.drop_index(op.f("ix_clear_cuts_area_hectare"), table_name="clear_cuts")
    op.drop_table("clear_cuts")
    op.drop_index(op.f("ix_cities_zip_code"), table_name="cities")
    op.drop_index(op.f("ix_cities_id"), table_name="cities")
    op.drop_table("cities")
    op.drop_index(op.f("ix_users_role"), table_name="users")
    op.drop_index(op.f("ix_users_password"), table_name="users")
    op.drop_index(op.f("ix_users_login"), table_name="users")
    op.drop_index(op.f("ix_users_lastname"), table_name="users")
    op.drop_index(op.f("ix_users_id"), table_name="users")
    op.drop_index(op.f("ix_users_firstname"), table_name="users")
    op.drop_index(op.f("ix_users_email"), table_name="users")
    op.drop_table("users")
    op.drop_index(op.f("ix_ecological_zonings_type"), table_name="ecological_zonings")
    op.drop_index(op.f("ix_ecological_zonings_sub_type"), table_name="ecological_zonings")
    op.drop_index(op.f("ix_ecological_zonings_name"), table_name="ecological_zonings")
    op.drop_index(op.f("ix_ecological_zonings_id"), table_name="ecological_zonings")
    op.drop_index(op.f("ix_ecological_zonings_code"), table_name="ecological_zonings")
    op.drop_table("ecological_zonings")
    op.drop_index(op.f("ix_departments_id"), table_name="departments")
    op.drop_index(op.f("ix_departments_code"), table_name="departments")
    op.drop_table("departments")
    # ### end Alembic commands ###
