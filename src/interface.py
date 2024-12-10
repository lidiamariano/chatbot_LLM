import gradio as gr


def criar_interface(chatbot):
    """
    Cria a interface gráfica do chatbot.

    Args:
        chatbot: Instância do ChatbotSeguranca.

    Returns:
        Interface Gradio.
    """
    def interface_chat(entrada_usuario, historico):
        resposta = chatbot.gerar_resposta(entrada_usuario)
        historico.append({"role": "user", "content": entrada_usuario})
        historico.append({"role": "assistant", "content": resposta})
        return historico, ""

    with gr.Blocks(css=".gradio-container {background-color: #f7f7f7; font-family: Arial;}") as interface:
        gr.Markdown(
            """
            <div style="text-align: center; margin-top: 20px;">
                <h1 style="color: #4CAF50;">💬 Chatbot de Segurança Industrial 🦺</h1>
                <p style="font-size: 18px; color: #333;">Pergunte sobre normas de segurança e receba respostas concisas e precisas.</p>
            </div>
            """
        )

        with gr.Column():
            chat_historico = gr.Chatbot(
                label="Conversa com o Assistente",
                type="messages",
                elem_id="chatbox",
                height=500
            )
            entrada_usuario = gr.Textbox(
                label="Digite sua pergunta",
                placeholder="Exemplo: Quais EPIs são necessários para operar um torno?",
                lines=1,
            )

            with gr.Row():
                botao_enviar = gr.Button("Enviar", elem_id="botao-enviar")

        entrada_usuario.submit(interface_chat, [entrada_usuario, chat_historico], [chat_historico, entrada_usuario])
        botao_enviar.click(interface_chat, [entrada_usuario, chat_historico], [chat_historico, entrada_usuario])

    return interface
