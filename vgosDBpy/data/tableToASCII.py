from prettytable import PrettyTable

def convertToAscii(tableview):

    model = tableview.getModel() # Get model of table view
    table_out = PrettyTable() # Setup instance
    table_out.field_names = model.getHeader() # Set header

    for row_index in range(model.rowCount()):

        row = []

        for col_index in range(model.columnCount()):

            item = model.item(row_index, col_index)
            row.append(str(item))

        table_out.add_row(row)

    return table_out


def write_ascii_file(ptable, file_path):
    '''
    ptable [PrettyTable] is the table that should be written to a file in ASCII format
    '''
    table_txt = ptable.get_string()
    with open(file_path,'w') as file:
            file.write(table_txt)
