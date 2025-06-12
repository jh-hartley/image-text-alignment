from sqlalchemy.orm import Session


class CheckImageTextAlignmentService:
    """Service layer for check image text alignment operations."""

    def __init__(self, session: Session) -> None:
        self.session = session

    @staticmethod
    def from_session(session: Session) -> "CheckImageTextAlignmentService":
        return CheckImageTextAlignmentService(session)

    async def check_colour_matches_description(self, product_key: str) -> bool:
        raise NotImplementedError
