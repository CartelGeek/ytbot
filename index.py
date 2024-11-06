import os
import json
from colorama import Fore, init, Style
from youtube import getDuration, getVideoId

# Inicializa o colorama
init()

class ViewBot:
    def __init__(self):
        self.selected_email = None
        self.data_file = "data.json"
        self.durations_file = "cached_durations.json"
        self.load_data()

    def load_data(self):
        """Carrega ou cria os arquivos de dados"""
        try:
            with open(self.data_file, "r") as f:
                self.stored = json.load(f)
        except FileNotFoundError:
            self.stored = {}
            self.save_data()
            
        try:
            with open(self.durations_file, "r") as f:
                self.cached_durations = json.load(f)
        except FileNotFoundError:
            self.cached_durations = {}
            self.save_durations()

    def save_data(self):
        with open(self.data_file, "w") as f:
            json.dump(self.stored, f, indent=4)

    def save_durations(self):
        with open(self.durations_file, "w") as f:
            json.dump(self.cached_durations, f, indent=4)

    def add_account(self, email, browser):
        """Adiciona uma nova conta"""
        if browser not in ["chrome", "opera"]:
            print(f"{Fore.RED}Browser inválido. Use 'chrome' ou 'opera'{Style.RESET_ALL}")
            return False

        print(f"\n{Fore.CYAN}Configurando conta: {email}{Style.RESET_ALL}")
        print("Digite o caminho completo do executável (.exe):")
        if browser == "opera":
            print(f"{Fore.YELLOW}Exemplo: C:\\Users\\OmniKoji\\AppData\\Local\\Programs\\Opera GX\\opera.exe{Style.RESET_ALL}")
        else:
            print(f"{Fore.YELLOW}Exemplo: C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe{Style.RESET_ALL}")

        # Limpa o input do usuário
        shortcut = input("> ").strip()
        if '"' in shortcut:
            # Se o usuário colou o comando completo, extrai apenas o caminho do exe
            shortcut = shortcut.split('"')[1]
        
        if not os.path.exists(shortcut):
            print(f"{Fore.RED}Caminho inválido: {shortcut}{Style.RESET_ALL}")
            return False
            
        # Para o Opera, adiciona o diretório do perfil específico
        if browser == "opera":
            profile_num = email.split('perfil')[-1]
            shortcut = f'"{shortcut}" "--user-data-dir=C:\\Perfil-{profile_num}"'
        else:
            shortcut = f'"{shortcut}"'
                
        self.stored[email] = {
            "shortcut": shortcut,
            "watched": [],
            "browser": browser
        }
        self.save_data()
        print(f"{Fore.GREEN}[+] Conta adicionada com sucesso!{Style.RESET_ALL}")
        return True

    def delete_account(self, email):
        """Remove uma conta"""
        if email in self.stored:
            del self.stored[email]
            self.save_data()
            print(f"{Fore.GREEN}Conta {email} removida com sucesso!{Style.RESET_ALL}")
            return True
        print(f"{Fore.RED}Conta {email} não encontrada!{Style.RESET_ALL}")
        return False

    def list_accounts(self):
        """Lista todas as contas e seus tempos assistidos"""
        for index, email in enumerate(self.stored.keys()):
            total_miliseconds = 0
            for url in self.stored[email].get("watched", []):
                video_id = getVideoId(url)
                if video_id not in self.cached_durations:
                    duration = getDuration(video_id)[0]
                    self.cached_durations[video_id] = duration
                total_miliseconds += self.cached_durations[video_id]

            seconds = int(total_miliseconds / 1000)
            hours, remainder = divmod(seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            
            time_str = ""
            if hours > 0:
                time_str += f"{hours}h"
            time_str += f"{minutes}m{seconds}s"
            
            print(f"{index} {email} {time_str} < Total assistido")
            
        self.save_durations()

    def process_video(self, url, email):
        """Processa um único vídeo para uma conta"""
        target = self.stored.get(email)
        if not target:
            print(f"{Fore.RED}Conta não encontrada: {email}{Style.RESET_ALL}")
            return False

        shortcut = target.get("shortcut")
        if not shortcut:
            print(f"{Fore.RED}Atalho inválido para conta: {email}{Style.RESET_ALL}")
            return False

        # Extrai o caminho do executável (remove as aspas extras)
        exe_path = shortcut.split('" "')[0].strip('"')
        if not os.path.exists(exe_path):
            print(f"{Fore.RED}Executável não encontrado: {exe_path}{Style.RESET_ALL}")
            return False

        if url in target["watched"]:
            print(f"{Fore.YELLOW}Conta {email} já assistiu ao vídeo: {url}{Style.RESET_ALL}")
            return False

        # Usa o comando completo do shortcut + URL
        command = f'start "" {shortcut} "{url}"'
        print(f"{Fore.CYAN}Executando: {command}{Style.RESET_ALL}")
        os.system(command)
        
        target["watched"].append(url)
        self.save_data()
        print(f"{Fore.GREEN}Vídeo aberto para {email}: {url}{Style.RESET_ALL}")
        return True

    def process_video_list(self, file_path, emails=None):
        """Processa uma lista de vídeos para uma ou mais contas"""
        if not os.path.exists(file_path):
            print(f"{Fore.RED}Arquivo não encontrado: {file_path}{Style.RESET_ALL}")
            return False

        with open(file_path, "r") as f:
            urls = [url.strip() for url in f.readlines() if url.strip()]

        if not urls:
            print(f"{Fore.RED}Arquivo vazio!{Style.RESET_ALL}")
            return False

        if not emails:
            emails = [self.selected_email] if self.selected_email else []

        for email in emails:
            print(f"{Fore.CYAN}Processando conta: {email}{Style.RESET_ALL}")
            for url in urls:
                self.process_video(url, email)

        return True

    def cli(self):
        """Interface de linha de comando"""
        while True:
            try:
                cmd = input(f"{self.selected_email + ' ' if self.selected_email else ''}> ")
                
                if not cmd:
                    continue
                    
                args = cmd.split()
                command = args[0].lower()

                if command == "exit":
                    break
                    
                elif command == "add":
                    if len(args) != 3:
                        print(f"{Fore.RED}Uso: add <email> <chrome|opera>{Style.RESET_ALL}")
                        continue
                    self.add_account(args[1], args[2])

                elif command == "delete":
                    if len(args) < 2:
                        print(f"{Fore.RED}Uso: delete <email>{Style.RESET_ALL}")
                        continue
                    if args[1] == "all":
                        self.stored.clear()
                        self.save_data()
                        print(f"{Fore.GREEN}Todas as contas foram removidas!{Style.RESET_ALL}")
                    else:
                        self.delete_account(args[1])

                elif command == "list":
                    self.list_accounts()

                elif command == "select":
                    if len(args) != 2:
                        print(f"{Fore.RED}Uso: select <número>{Style.RESET_ALL}")
                        continue
                    try:
                        index = int(args[1])
                        emails = list(self.stored.keys())
                        if 0 <= index < len(emails):
                            self.selected_email = emails[index]
                            print(f"{Fore.GREEN}Conta selecionada: {self.selected_email}{Style.RESET_ALL}")
                        else:
                            print(f"{Fore.RED}Índice inválido!{Style.RESET_ALL}")
                    except ValueError:
                        print(f"{Fore.RED}Número inválido!{Style.RESET_ALL}")

                elif command == "unselect":
                    self.selected_email = None
                    print(f"{Fore.GREEN}Seleção removida{Style.RESET_ALL}")

                elif command == "vlist":
                    if len(args) < 2:
                        print(f"{Fore.RED}Uso: vlist <arquivo> [all]{Style.RESET_ALL}")
                        continue
                    
                    file_path = args[1]
                    if "all" in args:
                        emails = list(self.stored.keys())
                    else:
                        emails = [args[i] for i in range(2, len(args))]
                        if not emails and self.selected_email:
                            emails = [self.selected_email]
                            
                    self.process_video_list(file_path, emails)

                elif command == "video":
                    if len(args) < 2:
                        print(f"{Fore.RED}Uso: video <url> [all]{Style.RESET_ALL}")
                        continue
                        
                    url = args[1]
                    if "all" in args:
                        emails = list(self.stored.keys())
                    else:
                        emails = [args[i] for i in range(2, len(args))]
                        if not emails and self.selected_email:
                            emails = [self.selected_email]
                            
                    for email in emails:
                        self.process_video(url, email)

                elif command == "cls":
                    os.system("cls")

                elif command == "help":
                    self.show_help()
                    
                else:
                    print(f"{Fore.RED}Comando '{cmd}' não existe.{Style.RESET_ALL}")

            except Exception as e:
                print(f"{Fore.RED}Erro: {str(e)}{Style.RESET_ALL}")

    def show_help(self):
        """Mostra o menu de ajuda"""
        help_text = """
        ####################################################################################
        #####                              DKViews 1.4                                 #####
        #####                           https://t.me/Dk992                             #####
        ####################################################################################
        
        COMANDOS BÁSICOS:
        add <email> <chrome|opera>  - Adiciona uma nova conta
        delete <email|all>          - Remove uma conta ou todas
        list                        - Lista todas as contas
        select <número>             - Seleciona uma conta
        unselect                    - Remove a seleção atual
        cls                         - Limpa a tela
        exit                        - Sai do programa
        help                        - Mostra esta ajuda
        
        COMANDOS DE VÍDEO:
        video <url> [all]          - Abre um vídeo para conta(s)
        vlist <arquivo> [all]      - Abre lista de vídeos para conta(s)
        
        [all] - Opcional, executa para todas as contas
        """
        print(help_text)

def main():
    bot = ViewBot()
    bot.cli()

if __name__ == "__main__":
    main()
