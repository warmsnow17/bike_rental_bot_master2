import io
import os
import xlsxwriter
from fastapi import Depends, HTTPException
from starlette.requests import Request
from starlette.responses import StreamingResponse
from starlette.status import HTTP_404_NOT_FOUND
from fastapi_admin.app import app
from fastapi_admin.depends import get_resources, get_current_admin
from fastapi_admin.template import templates
from database.models import Bike, BikePhoto
from business_bot import dp
import mimetypes


@app.get('/')
async def home(
    request: Request,
    resources=Depends(get_resources),
    admin=Depends(get_current_admin),
):
    return templates.TemplateResponse(
        'dashboard.html',
        context={
            'request': request,
            'resources': resources,
            'resource_label': 'Dashboard',
            'page_pre_title': 'overview',
            'page_title': 'Dashboard',
        },
    )

@app.get('/bikes/export')
async def export_bikes(
    request: Request,
    resources=Depends(get_resources),
    admin=Depends(get_current_admin)
):
    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output, {'in_memory': True})
    worksheet = workbook.add_worksheet()
    currency_format = workbook.add_format({'num_format': '#,##0'})
    header_format = workbook.add_format({'bold': True, 'bg_color': '#c9daf8'})
    worksheet.set_row(0, cell_format=header_format)
    worksheet.write(
        0, 0, 'ID'
    )
    worksheet.set_column(0, 0, 5)
    worksheet.write(
        0, 1, 'Bike Model'
    )
    worksheet.set_column(1, 1, 15)
    worksheet.write(
        0, 2, 'Creation Date'
    )
    worksheet.set_column(2, 2, 15)
    worksheet.write(
        0, 3, 'Status'
    )
    worksheet.set_column(3, 3, 10)
    worksheet.write(
        0, 4, 'Year'
    )
    worksheet.set_column(4, 4, 10)
    worksheet.write(
        0, 5, 'Mileage'
    )
    worksheet.set_column(5, 5, 12)
    worksheet.write(
        0, 6, 'Color'
    )
    worksheet.set_column(7, 6, 12)
    worksheet.write(
        0, 7, 'Owner'
    )
    worksheet.set_column(7, 7, 12)
    worksheet.write(
        0, 8, 'Keyless'
    )
    worksheet.set_column(8, 8, 10)
    worksheet.write(
        0, 9, 'ABS'
    )
    worksheet.set_column(9, 9, 5)
    worksheet.write(
        0, 10, 'Daily price'
    )
    worksheet.set_column(10, 10, 12)
    worksheet.write(
        0, 11, 'Weekly price'
    )
    worksheet.set_column(11, 11, 15)
    worksheet.write(
        0, 12, 'Price per two weeks'
    )
    worksheet.set_column(12, 12, 20)
    worksheet.write(
        0, 13, 'Monthly price'
    )
    worksheet.set_column(13, 13, 15)
    worksheet.write(
        0, 14, 'Garage Longitude'
    )
    worksheet.set_column(14, 14, 20)
    worksheet.write(
        0, 15, 'Garage Latitude'
    )
    worksheet.set_column(15, 15, 20)
    worksheet.write(
        0, 16, 'Photo'
    )
    worksheet.set_column(16, 16, 25)
    row = 1
    async for bike in Bike.all().select_related('model', 'user').prefetch_related('user__garages', 'photos'):
        worksheet.write(
            row, 0, bike.pk
        )
        worksheet.write(
            row, 1, bike.model.name
        )
        worksheet.write(
            row, 2, bike.created_at.strftime('%d.%m.%Y %H:%M')
        )
        worksheet.write(
            row, 3, await bike.get_bike_status()
        )
        worksheet.write(
            row, 4, bike.year
        )
        worksheet.write(
            row, 5, bike.mileage
        )
        worksheet.write(
            row, 6, bike.color
        )
        worksheet.write(
            row, 7, bike.user.username
        )
        worksheet.write(
            row, 8, 'Yes' if bike.keyless else 'No'
        )
        worksheet.write(
            row, 9, 'Yes' if bike.abs else 'No'
        )
        worksheet.write(
            row, 10, int(bike.price), currency_format
        )
        worksheet.write(
            row, 11, int(bike.weekly_price), currency_format
        )
        worksheet.write(
            row, 12, int(bike.biweekly_price), currency_format
        )
        worksheet.write(
            row, 13, int(bike.monthly_price), currency_format
        )
        if len(bike.user.garages) > 0:
            worksheet.write(
                row, 14, bike.user.garages[0].lon
            )
            worksheet.write(
                row, 15, bike.user.garages[0].lat
            )
        
        if len(bike.photos) > 0:
            photo = bike.photos[0]
            worksheet.write(
                row, 16, f'https://{request.url.hostname}/administrator/bikephoto/{photo.pk}'
            )
        row += 1
    worksheet.freeze_panes(1, 1)
    workbook.close()
    output.seek(0)
    return StreamingResponse(
        output,
        media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        headers={'Content-Disposition': 'inline; filename=bikes.xlsx'}
    )


@app.get('/bikephoto/{photo_id}')
async def export_bikes(
    photo_id,
    request: Request,
    resources=Depends(get_resources),
    admin=Depends(get_current_admin)
):
    photo = await BikePhoto.get_or_none(pk=photo_id)
    if not photo:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail='Not found')
    file = await dp.bot.get_file(photo.telegram_id)
    filename = os.path.basename(file.file_path)
    mt, _ = mimetypes.guess_type(file.file_path)
    if not mt:
        mt = os.path.splitext(filename)[-1]
    file_content = await dp.bot.download_file_by_id(photo.telegram_id)
    return StreamingResponse(
        file_content,
        media_type=mt
    )
