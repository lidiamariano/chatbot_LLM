import google.generativeai as genai
import os
from dotenv import load_dotenv


class ChatbotSeguranca:
    def __init__(self, documento_contexto):
        """
        Inicializa o chatbot com o contexto fornecido e configura a API do Gemini.

        Args:
            documento_contexto (str): Texto do documento de normas de segurança.
        """
        self._carregar_ambiente()
        self._configurar_gemini()
        self.contexto = documento_contexto
        self.historico_chat = []  # Memória do chat

    def _carregar_ambiente(self):
        """Carrega as variáveis de ambiente do arquivo .env."""
        load_dotenv()
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("A variável de ambiente GEMINI_API_KEY não foi encontrada. Verifique o arquivo .env.")

    def _configurar_gemini(self):
        """Configura a API do Google Gemini com uma instrução personalizada."""
        genai.configure(api_key=self.api_key)
        self.modelo = genai.GenerativeModel(
            "models/gemini-1.5-flash",
            system_instruction=(
                "Você é um assistente especializado em normas de segurança industrial. "
                "Seu papel é fornecer respostas precisas e concisas às perguntas dos usuários. "
                "Sempre baseie suas respostas no documento de segurança fornecido."
            ),
        )

    def adicionar_ao_historico(self, mensagem_usuario, resposta_bot):
        """Adiciona a interação ao histórico do chat."""
        self.historico_chat.append({"usuario": mensagem_usuario, "bot": resposta_bot})

    def gerar_resposta(self, entrada_usuario):
        """
        Gera uma resposta contextualizada baseada na entrada do usuário.

        Args:
            entrada_usuario (str): Pergunta ou consulta do usuário.

        Returns:
            str: Resposta gerada pelo modelo.
        """
        historico_prompt = "\n".join(
            [f"Usuário: {entrada['usuario']}\nAssistente: {entrada['bot']}" for entrada in self.historico_chat]
        )

        prompt = (
            f"Contexto:\n{self.contexto}\n\n"
            f"Histórico do chat:\n{historico_prompt}\n\n"
            f"Pergunta do usuário: {entrada_usuario}\n"
            f"Resposta:"
        )

        try:
            resposta = self.modelo.generate_content(prompt)
            resposta_bot = resposta.text.strip()
            self.adicionar_ao_historico(entrada_usuario, resposta_bot)  # Adiciona ao histórico
            return resposta_bot
        except Exception as e:
            return f"Erro ao processar a solicitação: {e}"
