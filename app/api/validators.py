from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charityproject import charityproject_crud
from app.models import CharityProject

PROJECT_NAME_ALREADY_EXISTS = 'Проект с таким именем уже существует!'
PROJECT_NOT_FOUND = 'Проект не найден'
PROJECT_CANNOT_DELETED = (
    'В проект были внесены средства, не подлежит удалению!'
)
CLOSED_PROJECT_CANNOT_EDITED = 'Закрытый проект нельзя редактировать!'
THE_AMOUNT_IS_LESS_THAN_THE_INVESTED_AMOUNT = (
    'Нельзя установить требуемую сумму меньше уже вложенной'
)


async def check_name_duplicate(
    project_name: str,
    session: AsyncSession,
) -> None:
    project = await charityproject_crud.get_project_id_by_name(
        project_name,
        session,
    )
    if project:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=PROJECT_NAME_ALREADY_EXISTS,
        )


async def check_charityproject_exists(
    charityproject_id: int,
    session: AsyncSession,
) -> CharityProject:
    project = await charityproject_crud.get(charityproject_id, session)
    if not project:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=PROJECT_NOT_FOUND,
        )
    return project


async def check_project_invested(
    project_id: int,
    session: AsyncSession,
) -> None:
    project = await charityproject_crud.get(
        project_id,
        session,
    )
    if project.invested_amount:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=PROJECT_CANNOT_DELETED,
        )


async def charity_project_closed(
    project_id: int,
    session: AsyncSession,
) -> None:
    project = await charityproject_crud.get(
        project_id,
        session,
    )
    if project.fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=CLOSED_PROJECT_CANNOT_EDITED,
        )


async def check_updating_full_amount(
    project_id: int,
    updating_full_amount: int,
    session: AsyncSession,
) -> None:
    project = await charityproject_crud.get(
        project_id,
        session,
    )
    if project.invested_amount > updating_full_amount:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail=THE_AMOUNT_IS_LESS_THAN_THE_INVESTED_AMOUNT,
        )
