import argparse
import pyarrow.csv as pcv
import pyarrow.parquet as ppq
import pandas as pd
import messages as msg


console_output = 'console'
file_output = 'file'
current_output = console_output     # default value


def get_schema(src_filename):
    '''Returns schema from parquet-file from filename.'''

    try: 
        file_schema = ppq.read_schema(src_filename)
    except (IOError, FileNotFoundError):
        display_message(msg.wrong_src_filename)
    
    return file_schema
  

def transform_csv2parquet(src_filename,dst_filename):
    '''Converts csv-file from the src-filename to parquet-file to dst-filename.'''

    try: 
        table = pcv.read_csv(src_filename)
    except (IOError, FileNotFoundError):
        display_message(msg.wrong_src_filename)
    
    try:
        ppq.write_table(table, dst_filename)
    except (IOError, FileNotFoundError):
        display_message(msg.wrong_dst_filename)
    
    ppq.ParquetFile(dst_filename)
 
    
def transform_parquet2csv(src_filename,dst_filename,separator=',',encoding_param='utf-8'):  
    '''
    Converts parquet-file from src-filename to csv-file to dst-filename.
    It allows to enter a separator for data (',' by default).   
    '''

    try: 
        df = ppq.read_table(src_filename).to_pandas()
    except (IOError, FileNotFoundError):
        display_message(msg.wrong_src_filename)
    
    try:
        df.to_csv(
            dst_filename,
            sep = separator,
            index = False,
            mode = 'w',
            line_terminator = '\n',
            encoding = encoding_param)
    except (IOError, FileNotFoundError):
        display_message(msg.wrong_dst_filename)


def display_message(message):
    ''' Other types of output - tbd. '''

    if current_output == console_output:
        print(message)


def modify_parser(parser):
    ''' Returns arguments of input. '''

    parser.add_argument('--csv2parquet', 
                    nargs=2,
                    help='converts csv-file from the file path:(src-filename)'
                            'to parquet-file with file path:(dst-filename)'
                            'syntax: [--csv2parquet <src-filename> <dst-filename>]')
    parser.add_argument('--parquet2csv',
                        nargs=2,
                        help='converts parquet-file from the file path:(src-filename)'
                        'to csv-file with file path:(dst-filename)'
                        'syntax: [--parquet2csv <src-filename> <dst-filename>]')
    parser.add_argument('--get-schema', 
                        help='returns schema from parquet-file from the file path (filename)'
                        'syntax: [--get-schema <filename>]')

    parser.add_argument('--disp', 
                    choices=[console_output, file_output],
                    default=console_output,  
                    type=str, 
                    help='allows to choose the way of displaying information')

    parser.add_argument('--disp-indicator', 
                    choices=[0,1,2],
                    default=1,  
                    type=int, 
                    help='allows to choose indicator to show or not the information')
    return parser


def main():

    parser = argparse.ArgumentParser()
    parser = modify_parser(parser)
    
    try:
        args = parser.parse_args()
        current_output = args.disp[0]

        if args.csv2parquet:
            transform_csv2parquet(args.csv2parquet[0],args.csv2parquet[1])
        elif args.parquet2csv:
            transform_parquet2csv(args.parquet2csv[0],args.parquet2csv[1])
        elif args.get_schema:
            schema_res = get_schema(args.get_schema)
            display_message(schema_res)
        else:
            display_message(msg.wrong_command_format)
    except:
        display_message(msg.wrong_command_format)
    

if __name__ == "__main__":
    main()
