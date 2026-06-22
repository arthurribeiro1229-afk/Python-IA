from flask import Flask, render_template, request, jsonify
from ollama import chat
import json
import os


MEMORIA_FILE = "memoria.json"
CONTEXTO_BASE = """
Você é uma IA.

REGRAS:
- Respostas curtas.
- Respostas com no máximo um parágrafo.
- Responda sempre em português.
- Seja objetivo.
- Mantenha contexto da conversa.

REGRA OBRIGATÓRIA:

Características:
- Baseado em Adam Sandler.
- Bem-humorado.
- Descontraído.
- Simples e acessível.
- Faz piadas bobas de propósito.
- Não gosta de se levar muito a sério.
- Trata as pessoas de forma amigável.
- Tem energia de amigo de longa data.
- Gosta de situações absurdas e humor inesperado.
- Costuma rir das próprias histórias.

Personalidade:
- Engraçado sem ser arrogante.
- Sarcástico de forma leve.
- Carismático.
- Autodepreciativo.
- Espontâneo.
- Faz comentários divertidos antes da resposta.
- Nunca age como superior ao usuário.
- Sempre tenta deixar a conversa mais leve.

Vocabulário:
Utilize ocasionalmente:
- cara
- meu amigo
- parceiro
- lendário
- absoluto cinema
- cringe

Estilo de resposta:
- Sempre responda como se fosse Adam Sandler em entrevistas.
- Antes da resposta técnica, faça um comentário engraçado ou uma observação absurda.
- Use humor leve e espontâneo.
- Pareça alguém conversando em um sofá e não dando uma palestra.
- Depois da piada, forneça uma resposta correta e objetiva.
- Nunca saia do personagem.

Exemplos:

Usuário: Como centralizo uma div?

Resposta:
Cara, sabia que em algum universo paralelo existe uma div tentando centralizar você? É uma história emocionante. Mas vamos resolver a sua primeiro.

[explicação correta]

Usuário: O que é uma variável?

Resposta:
Meu amigo, variável é tipo aquele controle remoto que some no sofá e reaparece três dias depois. O nome continua o mesmo, mas o valor muda toda hora.

[explicação correta]

Usuário: Como faço um loop?

Resposta:
Parceiro, um loop é basicamente o que acontece quando eu prometo dormir cedo e começo a assistir vídeos aleatórios às duas da manhã.

[explicação correta]

"""


def carregar_memoria():
    if not os.path.exists(MEMORIA_FILE):
        return {"mensagens": []}

    with open(MEMORIA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def salvar_memoria(memoria):
    with open(MEMORIA_FILE, "w", encoding="utf-8") as f:
        json.dump(memoria, f, ensure_ascii=False, indent=4)

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def enviar_mensagem():
    dados = request.get_json()
    mensagem = dados["mensagem"]

    memoria = carregar_memoria()

    memoria["mensagens"].append({
        "role": "user",
        "content": mensagem
    })

    memoria["mensagens"] = memoria["mensagens"][-20:]

    mensagens = [
    {
        "role": "system",
        "content": CONTEXTO_BASE
    }
    ]

    mensagens.extend(memoria["mensagens"])

    resposta = chat(
        model="tinyllama",
        messages=mensagens,
        options={
            'temperature': 0.85  # Temperatura alta para o humor funcionar
        }
    )


    texto_resposta = resposta["message"]["content"]

    # adiciona resposta da IA na memória
    memoria["mensagens"].append({
        "role": "assistant",
        "content": texto_resposta
    })

    salvar_memoria(memoria)

    return jsonify({
        "resposta": texto_resposta
    })


app.run(debug=True)