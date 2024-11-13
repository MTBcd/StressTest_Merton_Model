from Port_Exposure import PortfolioImpact
import pandas as pd
import xlwings as xw
from xlwings.utils import rgb_to_int
from openpyxl.utils.cell import get_column_letter

if __name__ == '__main__':
    DF_Merton = pd.read_excel('Data.xlsx' ,engine="openpyxl")
    #print(PortfolioImpact(DF_Merton).delta_calculation())
    app = xw.App(visible=True)
    wb = app.books.add()
    ws = wb.sheets['Feuil1']
    data = PortfolioImpact(DF_Merton).delta_calculation() #.to_excel("output_data.xlsx")
    ws.range('A1').value = data

    # Assuming headers are in the first row and data starts from the second row
    # Determine the range of the data dynamically
    last_row = ws.range('A' + str(ws.cells.last_cell.row)).end('up').row
    last_column = ws.range('XFD1').end('left').column
    last_column_letter = get_column_letter(last_column)

    data_range = f'A1:{last_column_letter}{last_row}'

    # Format column widths
    ws.range(data_range).columns.autofit()

    # Format header cells
    header_range = ws.range(f'A1:{last_column_letter}1')
    header_range.color = (0, 72, 92)
    header_range.api.Font.Color = rgb_to_int((243, 122, 110))
    header_range.api.Font.Bold = True

    # Alternate row colors
    for i in range(2, last_row + 1):
        row_range = f'A{i}:{last_column_letter}{i}'
        if i % 2 == 0:
            ws.range(row_range).color = (221, 235, 247)

    # Optionally, save the workbook
    wb.save('output_dataFixedIncomeMertonLEURAGCORP_test.xlsx')
    wb.close()
    app.quit()

