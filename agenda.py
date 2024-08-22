import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from datetime import datetime
from tkcalendar import DateEntry  # Importando o DateEntry

# Função para adicionar um agendamento
def adicionar_agendamento():
    nome = entry_nome.get()
    data = entry_data.get_date().strftime("%d/%m/%Y")  # Obtendo a data selecionada e formatando
    hora = f"{combo_horas.get()}:{combo_minutos.get()}"
    observacoes = text_observacoes.get("1.0", tk.END).strip()

    if nome and data and hora:
        try:
            # Tenta converter a data e hora para um objeto datetime
            agendamento_datahora = datetime.strptime(f"{data} {hora}", "%d/%m/%Y %H:%M")
        except ValueError:
            messagebox.showerror("Erro de Formato", "Formato de data ou hora inválido.")
            return

        # Adiciona o agendamento na lista
        agendamentos.append((agendamento_datahora, nome, data, hora, observacoes))

        # Ordena a lista por data e hora
        agendamentos.sort()

        # Remove todos os itens atuais da Treeview
        for item in tree.get_children():
            tree.delete(item)

        # Adiciona os itens ordenados na Treeview
        for agendamento in agendamentos:
            tree.insert("", tk.END, values=(agendamento[1], agendamento[2], agendamento[3], agendamento[4]))

        # Limpa os campos de entrada
        entry_nome.delete(0, tk.END)
        entry_data.set_date(datetime.today())  # Reseta a data para o dia atual
        combo_horas.set("00")
        combo_minutos.set("00")
        text_observacoes.delete("1.0", tk.END)
    else:
        messagebox.showwarning("Campos obrigatórios", "Por favor, preencha todos os campos.")

# Configuração da janela principal
root = tk.Tk()
root.title("Agenda")

# Lista para armazenar os agendamentos
agendamentos = []

# Labels e Entradas para Nome, Data e Hora
label_nome = tk.Label(root, text="Nome:")
label_nome.grid(row=0, column=0, padx=5, pady=5)
entry_nome = tk.Entry(root)
entry_nome.grid(row=0, column=1, padx=5, pady=5)

label_data = tk.Label(root, text="Data:")
label_data.grid(row=1, column=0, padx=5, pady=5)

# Campo de Data com DateEntry
entry_data = DateEntry(root, date_pattern="dd/mm/yyyy")  # Usando o DateEntry para selecionar datas
entry_data.grid(row=1, column=1, padx=5, pady=5)

label_hora = tk.Label(root, text="Hora:")
label_hora.grid(row=2, column=0, padx=5, pady=5)

# Combobox para selecionar horas e minutos
combo_horas = ttk.Combobox(root, values=[f"{i:02d}" for i in range(24)], width=3)
combo_horas.grid(row=2, column=1, padx=5, pady=5, sticky="w")
combo_horas.set("00")  # Valor padrão

combo_minutos = ttk.Combobox(root, values=[f"{i:02d}" for i in range(60)], width=3)
combo_minutos.grid(row=2, column=1, padx=5, pady=5, sticky="e")
combo_minutos.set("00")  # Valor padrão

label_observacoes = tk.Label(root, text="Observações:")
label_observacoes.grid(row=3, column=0, padx=5, pady=5)
text_observacoes = tk.Text(root, height=5, width=30)
text_observacoes.grid(row=3, column=1, padx=5, pady=5)

# Botão para adicionar agendamento
botao_adicionar = tk.Button(root, text="Adicionar", command=adicionar_agendamento)
botao_adicionar.grid(row=4, column=1, padx=5, pady=5, sticky="e")

# Tabela para mostrar os agendamentos
tree = ttk.Treeview(root, columns=("Nome", "Data", "Hora", "Observações"), show="headings")
tree.heading("Nome", text="Nome")
tree.heading("Data", text="Data")
tree.heading("Hora", text="Hora")
tree.heading("Observações", text="Observações")
tree.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

# Rodar a interface
root.mainloop()
