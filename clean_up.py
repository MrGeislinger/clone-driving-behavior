import argparse
import pandas as pd

def clean_image_paths(filepath, remove_substr, img_columns, replace_str=''):
    '''Read in a log file (CSV) by removing substring from image paths.
    '''
    df = pd.read_csv(filepath)
    # Remove substring specified for each specified column
    for col in img_columns:
        df.iloc[:,col] = df.iloc[:,col].str.replace(remove_substr, replace_str)
    # Overwrite the file originally given
    # Don't write the header or index to the CSV
    df.to_csv(filepath, header=False, index=False)


if __name__ == '__main__':    
    parser = argparse.ArgumentParser(description='Cleaning Driving Log')
    parser.add_argument(
        'log_filepath',
        type=str,
        help='Path to CSV log file'
    )
    parser.add_argument(
        'substring',
        type=str,
        help='Substring to remove'
    )
    # Optionally decide what columns are the image paths
    parser.add_argument(
        'columns',
        type=list,
        default=[0,1,2],
        nargs='?',
        help='List of columns for image paths (column position)'
    )    

    args = parser.parse_args()
    
    print(f'Removing following substring from `{args.log_filepath}`:')
    print(f'\t"{args.substring}"')
    clean_image_paths(
        args.log_filepath, 
        args.substring,
        img_columns=args.columns
    )
    print('')