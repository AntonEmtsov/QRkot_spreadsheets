from sqlalchemy import Column, String, Text

from app.models.base import PreBaseCharityDonation


class CharityProject(PreBaseCharityDonation):
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)

    def __repr__(self):
        return (
            f'name: {self.name}, '
            f'description: {self.description[:20]}, '
            f'{super().__repr__()}.'
        )
