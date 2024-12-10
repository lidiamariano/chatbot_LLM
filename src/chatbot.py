import google.generativeai as genai
import os
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from sentence_transformers import SentenceTransformer, util


class ChatbotSeguranca:
    def __init__(self, pdf_path):
        """
        Inicializa o chatbot e configura a API do Gemini com base no PDF.

        Args:
            pdf_path (str): Caminho para o PDF a ser utilizado como fonte de conhecimento.
        """
        self._carregar_ambiente()
        self._configurar_gemini()
        self.historico_chat = []  # Memória do chat
        self.embeddings = None
        self.textos_pdf = []

        # Carrega e processa o PDF
        self._carregar_pdf(pdf_path)

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
                "Baseie suas respostas no conteúdo do documento fornecido."
            ),
        )

    def _carregar_pdf(self, pdf_path):
        """Carrega e processa o PDF para gerar embeddings."""
        reader = PdfReader(pdf_path)
        self.textos_pdf = [page.extract_text() for page in reader.pages]

        if len(self.textos_pdf) == 0:
            raise ValueError("O PDF está vazio ou não contém texto legível.")

        # Divide o texto em frases e cria embeddings
        self.modelo_embeddings = SentenceTransformer('all-MiniLM-L6-v2')
        self.embeddings = self.modelo_embeddings.encode(self.textos_pdf, convert_to_tensor=True)

    def buscar_no_pdf(self, pergunta):
        """
        Busca os trechos mais relevantes do PDF com base na pergunta.

        Args:
            pergunta (str): Pergunta do usuário.

        Returns:
            str: Trecho mais relevante do PDF.
        """
        if self.embeddings is None or len(self.embeddings) == 0:
            return "Não foi possível encontrar informações relevantes no PDF."

        pergunta_embedding = self.modelo_embeddings.encode(pergunta, convert_to_tensor=True)
        resultados = util.cos_sim(pergunta_embedding, self.embeddings)
        indice_mais_relevante = resultados.argmax().item()
        return self.textos_pdf[indice_mais_relevante]

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
        trecho_pdf = self.buscar_no_pdf(entrada_usuario)
        historico_prompt = "\n".join(
            [f"Usuário: {entrada['usuario']}\nAssistente: {entrada['bot']}" for entrada in self.historico_chat]
        )

        prompt = (
            f"Trecho do PDF:\n{trecho_pdf}\n\n"
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
