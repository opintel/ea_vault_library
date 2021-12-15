import hashlib
from io import BytesIO, BufferedIOBase
import os
from typing import (
    Sequence,
    Tuple,
)
from zipfile import ZipFile, ZIP_DEFLATED
from Crypto.Cipher import AES


BUFFER_SIZE = 0x10000 # 64kb
MODE = AES.MODE_CFB
FileAndName = Tuple[BytesIO, str]


def encrypt_stream(input_stream: BufferedIOBase, password: str) -> BytesIO:
    '''
    encrypt a stream (file, BytesIO, ...) with AES256 with a password
    '''
    key = bytes(hashlib.md5(password.encode()).hexdigest(), 'ascii')
    cipher_encrypt = AES.new(key, MODE)
    encrypted_stream = BytesIO()
    encrypted_stream.write(cipher_encrypt.iv) # Initially write the iv to the output
    buffer = input_stream.read(BUFFER_SIZE)
    while len(buffer):
        ciphered_bytes = cipher_encrypt.encrypt(buffer)
        encrypted_stream.write(ciphered_bytes)
        buffer = input_stream.read(BUFFER_SIZE)
    input_stream.seek(0, 0)
    encrypted_stream.seek(0, 0)
    return encrypted_stream


def decrypt_stream(encrypted_stream: BufferedIOBase, password: str) -> BytesIO:
    '''
    decrypt a stream (file, BytesIO, ...) with AES256 with a password
    '''
    key = bytes(hashlib.md5(password.encode()).hexdigest(), 'ascii')
    iv = encrypted_stream.read(16) # iv is in first 16 bytes
    cipher_decrypt = AES.new(key, MODE, iv=iv)
    decrypted_stream = BytesIO()
    buffer = encrypted_stream.read(BUFFER_SIZE)
    while len(buffer):
        decrypted_bytes = cipher_decrypt.decrypt(buffer)
        decrypted_stream.write(decrypted_bytes)
        buffer = encrypted_stream.read(BUFFER_SIZE)
    encrypted_stream.seek(0, 0)
    decrypted_stream.seek(0, 0)
    return decrypted_stream


def zip_stream(streams_with_names_list: Sequence[FileAndName]) -> BytesIO:
    '''zip a stream'''
    zipped_stream = BytesIO()
    with ZipFile(zipped_stream, 'a', ZIP_DEFLATED, False) as zip_object:
        for stream, name in streams_with_names_list:
            zip_object.writestr(name, stream.getvalue())
    return zipped_stream


def unzip_stream(stream: BufferedIOBase) -> Sequence[FileAndName]:
    '''unzip a stream'''
    buffer = []
    with ZipFile(stream) as zip_file:
        files = zip_file.filelist
        for _file in files:
            name = _file.filename
            with zip_file.open(name) as element_zip:
                unzipped_element = BytesIO(element_zip.read())
                unzipped_element.seek(0, 0)
            buffer.append((unzipped_element, name))
    return buffer


def get_hash(stream: BufferedIOBase) -> str:
    '''get a string of hex hash from a stream'''
    block_size = BUFFER_SIZE
    file_hash = hashlib.sha256()
    buffer = stream.read(block_size)
    while len(buffer):
        file_hash.update(buffer)
        buffer = stream.read(block_size)
    stream.seek(0, 0)
    return file_hash.hexdigest()


def encrypt_and_zip_streams(file_name_list: Sequence[FileAndName], password: str) -> BytesIO:
    buffer = []
    for _file, _name in file_name_list:
        encrypted_stream = encrypt_stream(_file, password)
        buffer.append((encrypted_stream, _name))
    zipped_stream = zip_stream(buffer)
    return zipped_stream


def unzip_and_decrypt_streams(zipped_and_encrypted_file: BufferedIOBase, password: str) -> Sequence[FileAndName]:
    unzipped_parts = unzip_stream(zipped_and_encrypted_file)
    buffer = []
    for stream, name in unzipped_parts:
        buffer.append((decrypt_stream(stream, password), name))
    return buffer


def save_encrypted_zip(paths: Sequence[str], password: str, full_path_name: str) -> None:
    files_and_names = []
    for path in paths:
        files_and_names.append((open(path, 'rb'), os.path.basename(path)))
    encrypted_zipped_stream = encrypt_and_zip_streams(files_and_names, password)
    encrypted_zipped_stream.seek(0, 0)
    with open(full_path_name, 'wb') as _file:
        _file.write(encrypted_zipped_stream.read())


def extract_encrypted_files(zip_path: str, password: str, output_path: str) -> None:
    with open(zip_path, 'rb') as zip_file:
        streams_names = unzip_and_decrypt_streams(zip_file, password)
        os.mkdir(output_path)
        for stream, name in streams_names:
            with open(os.path.join(output_path, name), 'wb') as _file:
                _file.write(stream.getvalue())


if __name__ == '__main__':
    input_file_path = [
        '/mnt/c/Users/desarrollo/far.txt',
        '/mnt/c/Users/desarrollo/far - copia.txt',
        '/mnt/c/Users/desarrollo/far - copia (2).txt',
        '/mnt/c/Users/desarrollo/far - copia (3).txt',
    ]
    zip_path = '/mnt/c/Users/desarrollo/todo_junto2.zip'
    output_file_path = '/mnt/c/Users/desarrollo/todo_junto2'
    password = 'hola'
    save_encrypted_zip(input_file_path, password, zip_path)
    extract_encrypted_files(zip_path, password, output_file_path)
