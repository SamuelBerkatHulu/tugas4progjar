import socket
import json
import base64
import logging

server_address = ('0.0.0.0', 9999)

def send_command(command_str=""):
    global server_address
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect(server_address)
        logging.warning(f"connecting to {server_address}")
        logging.warning(f"sending message ")
        sock.sendall(command_str.encode())
        data_received = ""
        while True:
            data = sock.recv(16)
            if data:
                data_received += data.decode()
                if "\r\n\r\n" in data_received:
                    break
            else:
                break
        hasil = json.loads(data_received)
        logging.warning("data received from server:")
        return hasil
    except socket.error as e:
        logging.warning(f"socket error: {e}")
        return False
    except json.JSONDecodeError as e:
        logging.warning(f"JSON decode error: {e}")
        return False
    finally:
        sock.close()

def remote_list():
    command_str = f"LIST"
    hasil = send_command(command_str)
    if hasil and hasil['status'] == 'OK':
        print("daftar file : ")
        for nmfile in hasil['data']:
            print(f"- {nmfile}")
        return True
    else:
        print("Gagal")
        return False

def remote_get(filename=""):
    command_str = f"GET {filename}"
    hasil = send_command(command_str)
    if hasil and hasil['status'] == 'OK':
        namafile = hasil['data_namafile']
        isifile = base64.b64decode(hasil['data_file'])
        with open(namafile, 'wb+') as fp:
            fp.write(isifile)
        return True
    else:
        print("Gagal")
        return False

def x_upload(filename=""):
    try:
        with open(filename, 'rb') as f:
            file_content = base64.b64encode(f.read()).decode()
        command_str = f"UPLOAD {filename} {file_content}"
        hasil = send_command(command_str)
        if hasil and hasil['status'] == 'OK':
            print(hasil['data'])
            return True
        else:
            print("Gagal")
            return False
    except FileNotFoundError:
        print(f"File {filename} tidak ditemukan")
        return False

def y_delete(filename=""):
    command_str = f"DELETE {filename}"
    hasil = send_command(command_str)
    if hasil and hasil['status'] == 'OK':
        print(hasil['data'])
        return True
    else:
        print("Gagal")
        return False

def print_menu():
    print("File Client Menu:")
    print("1. Daftar files")
    print("2. Dapatkan file")
    print("3. Unggah file")
    print("4. Hapus file")
    print("5. Keluar")

def main():
    global server_address

    while True:
        print_menu()
        choice = input("Enter your choice: ")

        if choice == "1":
            remote_list()
        elif choice == "2":
            filename = input("Enter the filename to get: ")
            remote_get(filename)
        elif choice == "3":
            filename = input("Enter the filename to upload: ")
            if x_upload(filename):
                print(f"File {filename} uploaded successfully.")
        elif choice == "4":
            filename = input("Enter the filename to delete: ")
            if y_delete(filename):
                print(f"File {filename} deleted successfully.")
        elif choice == "5":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == '__main__':
    server_address = ('0.0.0.0', 9999)
    main()
