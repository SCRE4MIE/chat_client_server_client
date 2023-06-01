"""Server script."""

import threading
import socket


class Server:

    def __init__(self, host, port):

        # Definicja zmiennych HOST, PORT oraz typu kodowania wiadomości
        self.host = host
        self.port = port
        self.encode = 'ascii'

        self.clients = {}
        self.server = None

        self.start()

    def start(self):
        """Metoda, która rozpoczyna serwer."""

        # Inicjalizacja socketu
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.server.listen()  # nasłuchiwanie przez serwer
        print('Server ready...')
        self.receive()

    def broadcast(self, message):
        """
        Metoda, która rozsyła wiadomości do każdego podłączonego użytkownika
        Każdy z użytkowników, który jest podłączony do serwera,
        znajduje się w słowniku: clients
        """
        for client in self.clients.values():
            client[0].send(message)

    def handle(self, client):
        """
        Funkcja, która otrzymuje wiadomości od podłączonych użytkowników.
        Jeżeli użytkownik rozłączył się, zostanie przekazana wiadomość, do metody
        broadcast, o informacji, że dany użytkownik opuścił chat.
        """
        while True:

            try:
                message = client.recv(1024).decode(self.encode)
                if message:
                    nickname = self.clients[client][1]
                    ctx = f'{nickname} :{message}'.encode(self.encode)
                    self.broadcast(ctx)
                else:
                    nickname = self.clients[client][1]
                    self.clients.pop(client)
                    client.close()  # zamknięcie połączenia z użytkownikiem
                    self.broadcast(f'{nickname} left!'.encode(self.encode))
                    print(f'{nickname} left!')
                    break
            except:
                nickname = self.clients[client][1]
                self.clients.pop(client)
                client.close() # zamknięcie połączenia z użytkownikiem
                self.broadcast(f'{nickname} left!'.encode(self.encode))
                print(f'{nickname} left!')
                break

    def receive(self):
        """
        Metoda, która odpowiada za ustanowienie połączenia z użytkownikiem,
        pobranie nazwy użytkownika oraz za stworzenie nowego wątku, na którym
        będzie uruchomiona metoda odpowiedzialna, za otrzymywanie wiadomości
        od danego użytkownika. Każda metoda handle dla każdego użytkownika jest
        uruchamiana na nowym wątku.

        """
        while True:
            # Akceptacja połączenia
            client, address = self.server.accept()

            client.send('NICK'.encode(self.encode))
            nickname = client.recv(1024).decode(self.encode)
            self.clients[client] = (client, nickname)

            # Wysłanie wiadomości do każdego, że dany użytkownik dołączył do serwera.
            self.broadcast(f'{nickname} joined!'.encode(self.encode))
            print(f'{nickname} connected')
            # Wysłanie wiadomości do użytkownika, że dołączył do chatu.
            client.send('Connected to server!'.encode(self.encode))

            # Rozpoczęcie wątku dla użytkownika.
            thread = threading.Thread(target=self.handle, args=(client,))
            thread.start()


server = Server('127.0.0.1', 5555)
