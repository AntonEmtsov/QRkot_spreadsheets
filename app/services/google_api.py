from datetime import datetime

from aiogoogle import Aiogoogle

from app.core.config import settings

FORMAT = "%Y/%m/%d %H:%M:%S"
ROW_COUNT = 100
COLUMN_COUNT = 3
LOCALE = 'ru_RU'
SPREADSHEET_BODY = dict(
    properties=dict(
        title='',
        locale=LOCALE,
    ),
    sheets=[dict(properties=dict(
        sheetType='GRID',
        sheetId=0,
        title='Лист1',
        gridProperties=dict(
            rowCount=ROW_COUNT,
            columnCount=COLUMN_COUNT,
        )
    ))]
)
SPREADSHEET_TITLE = 'Отчет от {date_time_now}'
SPREADSHEET_HEADER = [
    ['Отчет от', ''],
    ['Топ проектов по скорости закрытия'],
    ['Название проекта', 'Время сбора', 'Описание'],
]
SPREADSHEET_VALUE_ERROR = (
    'Не допустимое количество {rows_count} строк и {columns_count} столбцов'
    f'В таблице должно быть: {ROW_COUNT} строк и {COLUMN_COUNT} столбцов. '

)


async def spreadsheets_create(
    wrapper_services: Aiogoogle,
    spreadsheet_body: dict = SPREADSHEET_BODY,
) -> str:
    date_time_now = datetime.now().strftime(FORMAT)
    spreadsheet_body = spreadsheet_body.copy()
    spreadsheet_body['properties']['title'] = SPREADSHEET_TITLE.format(
        date_time_now=date_time_now,
    )
    service = await wrapper_services.discover('sheets', 'v4')
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body)
    )
    return response['spreadsheetId']


async def set_user_permissions(
        spreadsheet_id: str,
        wrapper_services: Aiogoogle,
) -> None:
    service = await wrapper_services.discover('drive', 'v3')
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheet_id,
            json={'type': 'user',
                  'role': 'writer',
                  'emailAddress': settings.email},
            fields="id",
        ))


async def spreadsheets_update_value(
        spreadsheet_id: str,
        charity_projects: list,
        wrapper_services: Aiogoogle,
) -> None:
    date_time_now = datetime.now().strftime(FORMAT)
    service = await wrapper_services.discover('sheets', 'v4')
    table_head = SPREADSHEET_HEADER.copy()
    table_head[0][1] = date_time_now
    table_values = [
        *table_head,
        *[list(map(str, [
            project.name,
            (project.close_date - project.create_date),
            project.description,
        ])) for project in charity_projects]
    ]
    rows = len(table_values)
    columns = max([len(row) for row in table_values])
    if columns > COLUMN_COUNT or rows > ROW_COUNT:
        raise ValueError(SPREADSHEET_VALUE_ERROR.format(
            rows_count=rows,
            columns_count=columns,
        ))
    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheet_id,
            range=f'R1C1:R{rows}C{columns}',
            valueInputOption='USER_ENTERED',
            json={
                'majorDimension': 'ROWS',
                'values': table_values,
            },
        )
    )
