import string
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import threading
import time


def obter_caracteres_especiais(teclado):
    caracteres_especiais = set()
    for char in teclado:
        if char not in string.ascii_letters and char not in string.digits and char not in string.whitespace:
            caracteres_especiais.add(char)
    return caracteres_especiais


def calcular_porcentagem_caracteres_especiais(arquivo, caracteres_especiais):
    caracteres_encontrados = set()  # Para armazenar os caracteres especiais encontrados
    with open(arquivo, 'r', encoding='utf-8') as file:  # Abre o arquivo com codificação UTF-8
        for line in file:
            for char in line:
                if char in caracteres_especiais:
                    # Adiciona o caractere especial encontrado ao conjunto
                    caracteres_encontrados.add(char)
    caracteres_especiais_usados = len(caracteres_encontrados)
    total_caracteres_especiais = len(caracteres_especiais)
    print("Caracteres especiais encontrados no arquivo:", caracteres_encontrados)
    print(f"Total de caracteres especiais no arquivo: {
          caracteres_especiais_usados}")
    print(f"Total de caracteres especiais no teclado: {
          total_caracteres_especiais}")
    return (caracteres_especiais_usados / total_caracteres_especiais) * 100


def buscar_arquivo():
    arquivo = filedialog.askopenfilename(filetypes=[("Arquivos DOC", "*.doc")])
    if arquivo:
        progress_bar.place(x=190, y=170)  # Posiciona o spinner abaixo do botão
        progress_bar.start()  # Inicia o spinner

        # Inicia uma thread para calcular a porcentagem
        threading.Thread(target=processar_arquivo, args=(arquivo,)).start()


def processar_arquivo(arquivo):
    for _ in range(101):  # Incrementa o progresso em 1% a cada 10ms
        progress_bar.step()
        root.update()
        time.sleep(0.01)
    porcentagem = calcular_porcentagem_caracteres_especiais(
        arquivo, caracteres_especiais)
    root.after(1000, lambda: mostrar_resultado(porcentagem))


def mostrar_resultado(porcentagem):
    progress_bar.stop()
    progress_bar.place_forget()  # Remove o spinner

    # Define cores fixas para diferentes faixas de porcentagem
    if porcentagem <= 50:
        color = 'red'
    else:
        color = 'green'

    label_resultado.config(
        text=f"A porcentagem de caracteres especiais utilizados no arquivo é: {
            porcentagem:.2f}%",
        wraplength=300,  # Define a largura máxima do texto antes de quebrar
        justify="center",  # Centraliza o texto verticalmente
        fg=color  # Define a cor do texto
    )
    print(f"Total de caracteres especiais: {porcentagem:.2f}%")


def main():
    global caracteres_especiais
    global label_resultado
    global root
    global progress_bar

    teclado = "áéà!'$%()-_[]{}ªãõâêôº,.;:?°íúüó"

    caracteres_especiais = obter_caracteres_especiais(teclado)

    root = tk.Tk()
    root.title("Validação de Arquivo")
    root.geometry("480x270")
    root.configure(bg='#f0f0f0')

    frame = tk.Frame(root, bg='#f0f0f0', bd=1, relief='groove',
                     borderwidth=5, padx=50, pady=20,)
    frame.pack(expand=True)

    button_buscar = tk.Button(frame, text="Buscar Arquivo", command=buscar_arquivo,
                              bg='#4CAF50', fg='white', font=('Arial', 12), relief='flat', padx=10, pady=5)
    button_buscar.pack()

    progress_bar = ttk.Progressbar(
        root, style='TProgressbar', mode='indeterminate')
    label_resultado = tk.Label(root, text="", bg='#f0f0f0', font=('Arial', 12))
    label_resultado.pack(pady=10)

    root.mainloop()


if __name__ == "__main__":
    main()
