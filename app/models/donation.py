from sqlalchemy import Column, ForeignKey, Integer, Text

from app.models.base import PreBaseCharityDonation


class Donation(PreBaseCharityDonation):
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    comment = Column(Text)

    def __repr__(self):
        return (
            f'user_id: {self.user_id}, '
            f'comment: {self.comment[:20]} , '
            f'{super().__repr__()}.'
        )
