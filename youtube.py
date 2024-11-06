def getVideoId(url):
    """Extrai o ID do vídeo de uma URL do YouTube"""
    if not url:
        return None
    if "youtu.be" in url:
        return url.split("/")[-1].split("?")[0]
    elif "youtube.com" in url:
        if "v=" in url:
            return url.split("v=")[1].split("&")[0]
    return url.strip()

def getDuration(video_id):
    """Retorna a duração do vídeo em milissegundos"""
    return [0]  # valor padrão