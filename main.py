from db_manager import process_files
from graph_loader import load_data_into_graph

if __name__ == '__main__':
    directory = 'Dataset'
    process_files(directory)
    load_data_into_graph(directory)
