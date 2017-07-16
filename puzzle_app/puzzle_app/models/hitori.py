from sqlalchemy import (
    Boolean,
    Column,
    Index,
    Integer,
    Text,
    ForeignKey
)


from sqlalchemy.orm import relationship


from .meta import Base


class HitoriGameBoard(Base):
    __tablename__ = 'hitori_game_boards'

    id = Column(Integer, primary_key=True)

    number_of_rows = Column(Integer, nullable=False)
    number_of_columns = Column(Integer, nullable=False)

    cells = relationship('HitoriGameBoardCell', back_populates='hitori_game_board',
                         cascade="all, delete-orphan")


class HitoriGameBoardCell(Base):
    __tablename__ = 'hitori_game_board_cells'

    id = Column(Integer, primary_key=True)

    hitori_game_board_id = Column(Integer, ForeignKey('hitori_game_boards.id', ondelete='CASCADE'), nullable=False)
    hitori_game_board = relationship('HitoriGameBoard', back_populates='cells')

    row_number = Column(Integer, nullable=False)
    column_number = Column(Integer, nullable=False)
    value = Column(Integer, nullable=False)

    included_in_solution = Column(Boolean(name="included_in_solution"))  # had to name this due to some SQLAlchemy bug
