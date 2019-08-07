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

def convertToAscii_script(directory, info, path):

    table_out = PrettyTable() # Setup instance

    field_names = list(directory)
    table_out.field_names = field_names

    nbr_cols = len(directory[field_names[0]])

    for col_index in range(0,nbr_cols):

        row = []

        for name in field_names:

            item = directory[name][col_index]
            row.append(str(item))
        table_out.add_row(row)
    write_ascii_file(table_out, info, path)

def write_ascii_file(ptable, other_info, file_path):
    '''
    ptable [PrettyTable] is the table that should be written to a file in ASCII format
    other_info [string]
    '''
    table_txt = ptable.get_string()
    with open(file_path,'w') as file:
            file.write(other_info)
            file.write('\n')
            file.write(table_txt)
