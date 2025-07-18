import requests
from bs4 import BeautifulSoup
import google.generativeai as genai


API_KEY = "AIzaSyBJeEC28vYZ-LGGqAktujdYqfnbTqgozBw"
genai.configure(api_key=API_KEY)


API_KEY = "AIzaSyBJeEC28vYZ-LGGqAktujdYqfnbTqgozBw"
genai.configure(api_key=API_KEY)


model = genai.GenerativeModel('gemini-2.5-Pró-flash-latest')


def extrair_conteudo_do_site(url):

    try:
        resposta = requests.get(url)
        resposta.raise_for_status()
        soup = BeautifulSoup(resposta.text, 'html.parser')
        textos = []

        for tag in soup.find_all(['p', 'h1', 'li']):
            texto = tag.get_text(strip=True)
            if texto and len(texto) > 2:
                textos.append(texto)

        for img in soup.find_all('img'):
            alt_text = img.get('alt')
            if alt_text:
                textos.append(alt_text)

        return "\n".join(textos)

    except Exception as e:
        return f"Erro ao acessar o site: {str(e)}"


def perguntar_ao_gemini(pergunta, contexto):

    prompt = f"""Com base no contexto abaixo, responda a pergunta:

Contexto:
{contexto}

Pergunta:
{pergunta}
"""
    try:
        resposta = model.generate_content(prompt)
        return resposta.text
    except Exception as e:
        return f"Erro ao chamar a API do Gemini: {str(e)}"


def iniciar_chat():
    """
    Função principal de execução do chatbot.
    Carrega os conteúdos dos sites e permite interações com o utilizador.
    """
    urls = [
        "https://www.jovemprogramador.com.br",
        "https://www.jovemprogramador.com.br/sobre.php",
        "http://www.jovemprogramador.com.br/apoiadores.php",
        "https://www.jovemprogramador.com.br/patrocinadores.php",
        "http://www.jovemprogramador.com.br/parceiros.php",
        "https://www.jovemprogramador.com.br/queroserprofessor/",
        "http://www.jovemprogramador.com.br/duvidas.php",
        "http://www.jovemprogramador.com.br/queroserprofessor",
        "https://www.jovemprogramador.com.br/duvidas.php#cadastro",
        "https://www.jovemprogramador.com.br/hackathon/#regulamento",
        "http://www.jovemprogramador.com.br/hackathon/",
        "http://www.jovemprogramador.com.br/aluno/",
        "http://www.jovemprogramador.com.br/vagas/",
        "https://www.jovemprogramador.com.br/precadastro/ajax"
    ]

    print("Extraindo informações dos sites...")

    contexto = ""
    for url in urls:
        conteudo = extrair_conteudo_do_site(url)
        if "Erro" in conteudo:
            print(conteudo)
            continue
        contexto += conteudo + "\n"

    if not contexto.strip():
        print("Nenhum conteúdo foi extraído.")
        return

    print("Conteúdo carregado. Pode começar a conversar. Digite 'sair' para encerrar.\n")

    while True:
        pergunta = input("Você: ")
        if pergunta.lower() in ['sair', 'exit']:
            print("Chat encerrado.")
            break

        resposta = perguntar_ao_gemini(pergunta, contexto)
        print("Bot:", resposta, "\n")


if __name__ == "__main__":
    iniciar_chat()
