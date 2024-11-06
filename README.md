# DKViews 1.4

Um bot para automatizar visualizações de vídeos do YouTube usando múltiplos perfis do Opera GX.

## Instalação

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/DKViews.git
cd DKViews
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

## Uso

1. Execute o programa:
```bash
python index.py
```

2. Comandos disponíveis:
- `add <email> <chrome|opera>` - Adiciona uma nova conta
- `delete <email|all>` - Remove uma conta ou todas
- `list` - Lista todas as contas
- `select <número>` - Seleciona uma conta
- `unselect` - Remove a seleção atual
- `cls` - Limpa a tela
- `exit` - Sai do programa
- `video <url> [all]` - Abre um vídeo para conta(s)
- `vlist <arquivo> [all]` - Abre lista de vídeos para conta(s)

## Configuração

1. Adicione uma conta:
```
add perfil1 opera
```

2. Digite o caminho do Opera GX:
```
C:\Users\SeuUsuario\AppData\Local\Programs\Opera GX\opera.exe
```

3. Execute vídeos:
```
vlist videos.txt all
```

## Contribuindo

Pull requests são bem-vindos. Para mudanças maiores, abra uma issue primeiro para discutir o que você gostaria de mudar.

## Licença

[MIT](https://choosealicense.com/licenses/mit/) 