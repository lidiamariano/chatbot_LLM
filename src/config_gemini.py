import google.generativeai as genai
import os
from dotenv import load_dotenv
import gradio as gr


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
        # Formata o histórico do chat
        historico_prompt = "\n".join(
            [f"Usuário: {entrada['usuario']}\nAssistente: {entrada['bot']}" for entrada in self.historico_chat]
        )

        # Cria o prompt para o modelo
        prompt = (
            f"Contexto:\n{self.contexto}\n\n"
            f"Histórico do chat:\n{historico_prompt}\n\n"
            f"Pergunta do usuário: {entrada_usuario}\n"
            f"Resposta:"
        )

        try:
            # Gera a resposta com o modelo configurado
            resposta = self.modelo.generate_content(prompt)
            resposta_bot = resposta.text.strip()
            self.adicionar_ao_historico(entrada_usuario, resposta_bot)  # Adiciona ao histórico
            return resposta_bot
        except Exception as e:
            return f"Erro ao processar a solicitação: {e}"


# Documento de contexto (exemplo simplificado)
documento_contexto = """
Regras e Considerações de Segurança:
- Apenas pessoal treinado e autorizado pode operar máquinas pesadas, como tornos.
- Equipamentos de proteção individual (EPIs) obrigatórios incluem óculos de segurança, protetores auriculares e luvas.
- Sempre inspecione os equipamentos antes do uso e siga os procedimentos de segurança.
"""

# Instância do chatbot
chatbot = ChatbotSeguranca(documento_contexto)


# Função para integrar com a interface gráfica
def interface_chat(entrada_usuario):
    return chatbot.gerar_resposta(entrada_usuario)


# Interface Gradio melhorada
interface = gr.Blocks()

with interface:
    gr.Markdown(
        """
        # Chatbot de Segurança Industrial 🦺
        Converse com um assistente especializado em normas de segurança industrial. 
        Pergunte sobre o uso correto de EPIs, procedimentos de segurança e mais!
        """
    )
    with gr.Row():
        entrada_usuario = gr.Textbox(
            label="Digite sua pergunta", placeholder="Exemplo: Quem pode operar um torno?"
        )
        botao_enviar = gr.Button("Enviar")
    with gr.Row():
        resposta_bot = gr.Textbox(
            label="Resposta do Chatbot",
            placeholder="A resposta aparecerá aqui...",
            interactive=False,
        )
    botao_enviar.click(fn=interface_chat, inputs=entrada_usuario, outputs=resposta_bot)

# Inicia a interface
if __name__ == "__main__":
    interface.launch()
