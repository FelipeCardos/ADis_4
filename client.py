import requests
import sys

class Client:
    def __init__(self, base):
        self.base = base
        
        
    def __check_command(self, command):
        match command:
            
            case ["CREATE", "UTILIZADOR", x, y] if (len(x) | len(y) != 0): return (True,"C1")
            
            case ["CREATE", "ARTISTA"|"MUSICA", x] if len(x) != 0: return (True, "C2")
            
            case ["CREATE", x, y, z]:
                try:
                    int(x) and int(y)
                    if len(z) != 0: return (True, "C3")
                except:
                    return (False, None)
            
            case ["READ"|"DELETE","UTILIZADOR"|"MUSICA"|"ARTISTA", x]:
                try:
                    int(x)
                    return (True, "C4")
                except:
                    return (False, None)
            
            case ["READ"|"DELETE","ALL", "UTILIZADORES"|"ARTISTAS"|"MUSICAS"]: return (True, "C5")
                
            case ["READ"|"DELETE","ALL","MUSICAS_A"|"MUSICAS_U", x]:
                try:
                    int(x)
                    return (True, "C6")
                except:
                    return (False, None)
                
            case ["READ"|"DELETE","ALL","MUSICAS", x] if len(x) != 0: return (True, "C7")
            
            case ["UPDATE", "MUSICA", x, y, z]:
                    try:
                        int(x) and int(z)
                        if len(y) != 0: return (True, "C8")
                    except:
                        return (False, None)
                    
            case ["UPDATE", "UTILIZADOR", x, y]:
                try:
                    int(x)
                    if len(y) != 0: return (True, "C9")
                except:
                    return (False, None)
            
            case _:
                return (False, None)
        
        
    def __help(self):
        print("""
        HELP:
            CREATE:
            
                UTILIZADOR <nome> <senha>
                ARTISTA <id_spotify>
                MUSICA <id_spotify>
                <id_user> <id_musica> <avaliacao>
                
            READ or DELETE:
            
                UTILIZADOR <id_user>
                ARTISTA <id_artista>
                MUSICA <id_musica>
                ALL < UTILIZADORES | ARTISTAS | MUSICAS>
                ALL MUSICAS_A <id_artista>
                ALL MUSICAS_U <id_user>
                ALL MUSICAS <avaliacao>
                
            UPDATE:
            
                MUSICA <id_musica> <avaliacao> <id_user>
                UTILIZADOR <id_user> <password>
        """)
        
        
    def start(self, command):
        if command == "EXIT":
            sys.exit(1)
        if command == "HELP":
            self.__help()
            return (False, None)
        else:
            splited_command = command.split(" ")
            return self.__check_command(splited_command)
        
        
    def send_request(self, command, checked_type):
        if checked_type == "C1":
            return requests.post(self.base + "utilizadores", {'nome': command[2], 'senha': command[3]})
        
        
        
        if checked_type == "C2":
            if command[1] == "ARTISTA":
                return requests.post(self.base + "artistas", {'id_spotify': command[2]})
            else:
                return requests.post(self.base + "musicas", {'id_spotify': command[2]})
            
            
        if checked_type == "C3":
            return requests.post(self.base + "utilizadores/" + str(command[1]) + "/playlist", {'id_musica': command[2], 'avaliacao': command[3]})
        
        
        if checked_type == "C4":
            if command[0] == "READ":
                if command[1] == "UTILIZADOR":
                    return requests.get(self.base + "utilizadores/" + str(command[2]))
                if command[1] == "ARTISTA":
                    return requests.get(self.base + "artistas/" + str(command[2]))
                if command[1] == "MUSICA":
                    return requests.get(self.base + "musicas/" + str(command[2]))
            if command[0] == "DELETE":
                if command[1] == "UTILIZADOR":
                    return requests.delete(self.base + "utilizadores/" + str(command[2]))
                if command[1] == "ARTISTA":
                    return requests.delete(self.base + "artistas/" + str(command[2]))
                if command[1] == "MUSICA":
                    return requests.delete(self.base + "musicas/" + str(command[2]))
        
        
        if checked_type == "C5":
            if command[0] == "READ":
                if command[2] == "UTILIZADORES":
                    return requests.get(self.base + "utilizadores")
                if command[2] == "ARTISTAS":
                    return requests.get(self.base + "artistas")
                if command[2] == "MUSICAS":
                    return requests.get(self.base + "musicas")
            if command[0] == "DELETE":
                if command[2] == "UTILIZADORES":
                    return requests.delete(self.base + "utilizadores")
                if command[2] == "ARTISTAS":
                    return requests.delete(self.base + "artistas")
                if command[2] == "MUSICAS":
                    return requests.delete(self.base + "musicas")
        
        
        if checked_type == "C6":
            if command[0] == "READ":
                if command[2] == "MUSICAS_A":
                    return requests.get(self.base + "artistas/" + str(command[3]) + "/playlist")
                if command[2] == "MUSICAS_U":
                    return requests.get(self.base + "utilizadores/" + str(command[3]) + "/playlist")
            if command[0] == "DELETE":
                if command[2] == "MUSICAS_A":
                    return requests.delete(self.base + "artistas/" + str(command[3]) + "/playlist")
                if command[2] == "MUSICAS_U":
                    return requests.delete(self.base + "utilizadores/" + str(command[3]) + "/playlist")
        
        
        if checked_type == "C7":
            if command[0] == "READ":
                return requests.get(self.base + "musicas/playlist/" + str(command[3]))
            if command[0] == "DELETE":
                return requests.delete(self.base + "musicas/playlist/" + str(command[3]))
        
        
        if checked_type == "C8":
            return requests.put(self.base + "utilizadores/" + str(command[4])+ "/playlist/" + str(command[2]), {"avaliacao": command[3]})
        
        
        if checked_type == "C9":
            return requests.put(self.base + "utilizadores/" + str(command[2]), {"senha": command[3]})
        
        
    def receive_request(self, request):
        print(f"\nResposta recebida: \n Código: {request.status_code} \n Corpo: {request.text} \n")
        
        
def main() -> None:
    base = "http://127.0.0.1:5000/"
    check = Client(base)
    
    while True:
        asked_command = input("Digite o comando: ")
        (checked, checked_type) = check.start(asked_command)
        if checked:
            request = check.send_request(asked_command.split(" "), checked_type)
            check.receive_request(request)
        else:
            print("Comando inválido")
        
    
if __name__ == "__main__":
    main()
