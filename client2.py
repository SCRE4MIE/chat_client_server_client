"""Client script."""

import socket
import threading


class Client:

    def __init__(self, host, port):
        # Definicja zmiennych HOST, PORT oraz typu kodowania wiadomości
        self.host = host
        self.port = port
        self.encode = 'ascii'

        self.nickname = ''

        # Połączenie się z danym serwerem TCP
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((self.host, self.port))

        self.start()

    def start(self):
        """Metoda, która rozpoczyna wątki:
        -wątek dla metody receive,
        -wątek dla metody write
        oraz prosi użytkownika o podanie nickname.
        """

        # Wybór nazwy użytkownika
        self.nickname = input("Choose your nickname: ")

        receive_thread = threading.Thread(target=self.receive)
        receive_thread.start()

        write_thread = threading.Thread(target=self.write)
        write_thread.start()

    def receive(self):
        """Metoda, która odpowiada za otrzymywanie wiadomości z serwera."""
        while True:
            try:
                message = self.client.recv(1024).decode(self.encode)
                # Jeżeli wiadomości to: 'NICK', zostanie wysłana nazwa użytkownika
                if message == 'NICK':
                    self.client.send(self.nickname.encode(self.encode))
                else:
                    print(message)
            except:
                print("ERROR!")
                self.client.close()  # Zamknięcie połączenia z serwerem
                break

    def write(self):
        """Metoda, która odpowiada za wysyłanie wiadomości do serwera."""
        while True:
            message = input()
            if message:
                self.client.send(message.encode(self.encode))


client = Client('127.0.0.1', 5555)
