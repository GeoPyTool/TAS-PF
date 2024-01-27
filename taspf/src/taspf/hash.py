import hashlib
import os

def calculate_file_hash(file_path, algorithm='sha256'):
    """
    Calculate the hash of a file

    Parameters:
    file_path (str): The path to the file
    algorithm (str): The hash algorithm to use. Default is 'sha256'.

    Returns:
    str: The hash of the file
    """
    # 获取当前文件的绝对路径
    current_file_path = os.path.abspath(__file__)

    # 获取当前文件的目录
    current_directory = os.path.dirname(current_file_path)
    # 改变当前工作目录
    os.chdir(current_directory)

    hash_func = hashlib.new(algorithm)
    with open(file_path, 'rb') as f:
        while True:
            data = f.read(8192)
            if not data:
                break
            hash_func.update(data)
    return hash_func.hexdigest()


print(calculate_file_hash('1.csv')==calculate_file_hash('2.csv'))