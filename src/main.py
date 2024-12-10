from chatbot import ChatbotSeguranca
from interface import criar_interface

# Documento de contexto
documento_contexto = """
Regras e Considerações de Segurança:
- Apenas pessoal treinado e autorizado pode operar máquinas pesadas, como tornos.
- Equipamentos de proteção individual (EPIs) obrigatórios incluem óculos de segurança, protetores auriculares e luvas.
- Sempre inspecione os equipamentos antes do uso e siga os procedimentos de segurança.
"""

# Instância do chatbot
chatbot = ChatbotSeguranca(documento_contexto)

# Cria a interface e inicia o programa
if __name__ == "__main__":
    interface = criar_interface(chatbot)
    interface.launch()
