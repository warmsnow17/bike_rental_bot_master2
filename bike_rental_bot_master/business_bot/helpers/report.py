import io
import xlsxwriter


def get_report(bookings):
    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output, {'in_memory': True})
    worksheet = workbook.add_worksheet()
    currency_format = workbook.add_format({'num_format': '#,##0'})
    header_format = workbook.add_format({'bold': True, 'bg_color': '#c9daf8'})
    worksheet.set_row(0, cell_format=header_format)
    worksheet.write(
        0, 0, 'ID'
    )
    worksheet.write(
        0, 1, 'Bike Model'
    )
    worksheet.write(
        0, 2, 'Number'
    )
    worksheet.write(
        0, 3, 'Rent Days'
    )
    worksheet.write(
        0, 4, 'From Date'
    )
    worksheet.write(
        0, 5, 'To Date'
    )
    worksheet.write(
        0, 6, 'Price'
    )
    worksheet.write(
        0, 7, 'Sum'
    )
    row = 1
    for booking in bookings:
        worksheet.write(
            row, 0, booking.offer.request.pk
        )
        worksheet.write(
            row, 1, booking.bike.model.name
        )
        worksheet.write(
            row, 2, booking.bike.number
        )
        worksheet.write(
            row, 3, (booking.to_date.date() - booking.from_date.date()).days
        )
        worksheet.write(
            row, 4, str(booking.from_date.strftime('%d.%m.%Y'))
        )
        worksheet.write(
            row, 5, str(booking.to_date.strftime('%d.%m.%Y'))
        )
        worksheet.write(
            row, 6, int(booking.offer.price), currency_format
        )
        worksheet.write(
            row, 7, int(booking.offer.total_sum), currency_format
        )
        row += 1
    worksheet.freeze_panes(1, 2)
    worksheet.set_column(0, 0, 4)
    worksheet.set_column(1, 1, 15)
    worksheet.set_column(2, 2, 10)
    worksheet.set_column(3, 3, 10)
    worksheet.set_column(4, 4, 12)
    worksheet.set_column(5, 5, 12)
    worksheet.set_column(6, 6, 12)
    worksheet.set_column(7, 7, 12)
    workbook.close()
    output.seek(0)
    return output
