from chatbot import ChatbotSeguranca
from interface import criar_interface

# Caminho para o PDF
caminho_pdf = "./data/document.pdf"

# Instância do chatbot
chatbot = ChatbotSeguranca(caminho_pdf)

# Cria a interface e inicia o programa
if __name__ == "__main__":
    interface = criar_interface(chatbot)
    interface.launch()
