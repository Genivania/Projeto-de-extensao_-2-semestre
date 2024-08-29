import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from datetime import datetime
from tkcalendar import DateEntry


# Função para adicionar ou salvar edição de um agendamento
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

        if botao_adicionar['text'] == "Salvar":
            # Editando o agendamento existente
            excluir_agendamento(atualizar_tree=False)  # Exclui o agendamento atual sem confirmação
            botao_adicionar.config(text="Adicionar")  # Muda o texto do botão de volta para "Adicionar"

        # Adiciona o agendamento na lista
        agendamentos.append((agendamento_datahora, nome, data, hora, observacoes))

        # Ordena a lista por data e hora
        agendamentos.sort()

        # Atualiza a exibição da Treeview
        atualizar_treeview()

        # Limpa os campos de entrada
        entry_nome.delete(0, tk.END)
        entry_data.set_date(datetime.today())  # Reseta a data para o dia atual
        combo_horas.set("00")
        combo_minutos.set("00")
        text_observacoes.delete("1.0", tk.END)
    else:
        messagebox.showwarning("Campos obrigatórios", "Por favor, preencha todos os campos.")


# Função para excluir um agendamento
def excluir_agendamento(atualizar_tree=True):
    # Obtém o item selecionado na Treeview
    selecionado = tree.selection()
    if selecionado:
        if atualizar_tree:  # Só pergunta confirmação se for realmente excluir, não editar
            confirmacao = messagebox.askyesno("Confirmar Exclusão",
                                              "Você tem certeza que deseja excluir este agendamento?")
            if not confirmacao:
                return

        # Obtém os valores do item selecionado
        item = tree.item(selecionado)
        agendamento = item["values"]

        # Remove o agendamento da lista
        for i, a in enumerate(agendamentos):
            if (a[1], a[2], a[3], a[4]) == tuple(agendamento):
                del agendamentos[i]
                break

        # Atualiza a exibição da Treeview
        if atualizar_tree:
            atualizar_treeview()
    else:
        messagebox.showwarning("Seleção", "Por favor, selecione um agendamento para excluir.")


# Função para editar um agendamento
def editar_agendamento():
    selecionado = tree.selection()
    if selecionado:
        # Obtém os valores do item selecionado
        item = tree.item(selecionado)
        agendamento = item["values"]

        # Preenche os campos com os dados do agendamento
        entry_nome.delete(0, tk.END)
        entry_nome.insert(0, agendamento[0])
        entry_data.set_date(datetime.strptime(agendamento[1], "%d/%m/%Y"))
        combo_horas.set(agendamento[2].split(":")[0])
        combo_minutos.set(agendamento[2].split(":")[1])
        text_observacoes.delete("1.0", tk.END)
        text_observacoes.insert(tk.END, agendamento[3])

        # Muda o texto do botão "Adicionar" para "Salvar"
        botao_adicionar.config(text="Salvar")
    else:
        messagebox.showwarning("Seleção", "Por favor, selecione um agendamento para editar.")


# Função para atualizar a Treeview
def atualizar_treeview():
    # Remove todos os itens atuais da Treeview
    for item in tree.get_children():
        tree.delete(item)

    # Adiciona os itens ordenados na Treeview
    for agendamento in agendamentos:
        tree.insert("", tk.END, values=(agendamento[1], agendamento[2], agendamento[3], agendamento[4]))


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

# Botão para adicionar ou salvar edição de agendamento
botao_adicionar = tk.Button(root, text="Adicionar", command=adicionar_agendamento)
botao_adicionar.grid(row=4, column=1, padx=5, pady=5, sticky="e")

# Botão para excluir agendamento
botao_excluir = tk.Button(root, text="Excluir", command=lambda: excluir_agendamento(atualizar_tree=True))
botao_excluir.grid(row=4, column=0, padx=5, pady=5, sticky="w")

# Botão para editar agendamento
botao_editar = tk.Button(root, text="Editar", command=editar_agendamento)
botao_editar.grid(row=4, column=1, padx=5, pady=5, sticky="w")

# Tabela para mostrar os agendamentos
tree = ttk.Treeview(root, columns=("Nome", "Data", "Hora", "Observações"), show="headings")
tree.heading("Nome", text="Nome")
tree.heading("Data", text="Data")
tree.heading("Hora", text="Hora")
tree.heading("Observações", text="Observações")
tree.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

# Rodar a interface
root.mainloop()
