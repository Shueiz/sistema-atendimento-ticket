"""
Sistema de Atendimento Bancário
Desenvolvido com CustomTkinter para interface moderna.
"""

import customtkinter as ctk
from tkinter import messagebox
import time


class Ticket:
    def __init__(self, numero: int, cliente: str):
        self.numero = numero
        self.cliente = cliente

    def __str__(self):
        return f"[Ticket #{self.numero:03d} - {self.cliente}]"


class FilaAtendimento:
    def __init__(self, capacidade_inicial: int = 5):
        #"Inicia a fila com uma capacidade fixa padrão, no caso 5, para demonstrar o array enchendo."
        self._capacidade = capacidade_inicial
        self._tamanho = 0
        self._array = [None] * self._capacidade

    def enfileirar(self, ticket: Ticket):
        #"Na regra FIFO, os itens entram no final. Se o tamanho atingir a capacidade, chamamos o método de redimensionar."
        if self._tamanho == self.capacity():
            self._resize_memory()
        self._array[self._tamanho] = ticket
        self._tamanho += 1

    def desenfileirar(self) -> Ticket:
        #"Aqui é o coração da Fila. O atendimento sempre acontece no índice zero. Depois de atender, deslocamos o array para a esquerda."
        if self._tamanho == 0:
            raise IndexError("A fila está vazia. Nenhum ticket para atender.")
        ticket_atendido = self._array[0]
        self._shift_left(0, self._tamanho - 1)
        #"O _shift_left puxa quem estava na posição 1 para a 0, a 2 para a 1, e assim por diante."
        self._tamanho -= 1
        self._array[self._tamanho] = None # Libera memória do último espaço que ficou duplicado
        return ticket_atendido 

    def capacity(self) -> int:
        return len(self._array)

    def size(self) -> int:
        return self._tamanho

    def __str__(self) -> str:
        if self._tamanho == 0:
            return "Fila vazia."
        itens = [str(self._array[i]) for i in range(self._tamanho)]
        return " → ".join(itens)

    def _shift_left(self, start: int, end: int):
        # "Este é o método adaptado da lista original que percorre o array reorganizando os espaços."
        for index in range(start, end):
            self._array[index] = self._array[index + 1]

    def _resize_memory(self):
        # "Quando a capacidade esgota, criamos um novo array com o dobro do tamanho (10) e copiamos os dados."
        new_capacity = self.capacity() * 2
        new_capacity = self.capacity() * 2
        new_array = [None] * new_capacity
        for position in range(self._tamanho):
            new_array[position] = self._array[position]
        self._array = new_array


# ─────────────────────────────────────────────
#  INTERFACE GRÁFICA
# ─────────────────────────────────────────────

# Paleta de cores
COLORS = {
    "bg_dark":       "#0D1117",
    "bg_card":       "#161B22",
    "bg_input":      "#1C2128",
    "border":        "#30363D",
    "accent_blue":   "#1F6FEB",
    "accent_green":  "#238636",
    "accent_gold":   "#D29922",
    "accent_red":    "#DA3633",
    "text_primary":  "#E6EDF3",
    "text_secondary":"#8B949E",
    "text_muted":    "#484F58",
    "highlight":     "#388BFD",
    "card_hover":    "#1C2128",
}

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Estado
        self._fila = FilaAtendimento(capacidade_inicial=5)
        self._contador_ticket = 0
        self._ultimo_ticket: Ticket | None = None

        # Janela
        self.title("Sistema de Atendimento Bancário")
        self.geometry("820x760")
        self.minsize(720, 680)
        self.configure(fg_color=COLORS["bg_dark"])

        self._build_ui()
        self._atualizar_ui()

    # ──────────────────────────────────────────
    #  Construção da UI
    # ──────────────────────────────────────────

    def _build_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)

        self._build_header()
        self._build_call_panel()
        self._build_input_section()
        self._build_queue_panel()
        self._build_footer()

    # -- Cabeçalho --------------------------------
    def _build_header(self):
        header = ctk.CTkFrame(self, fg_color=COLORS["bg_card"],
                              corner_radius=0, border_width=0)
        header.grid(row=0, column=0, sticky="ew", padx=0, pady=0)
        header.grid_columnconfigure(1, weight=1)

        # Ícone / logotipo textual
        icon_lbl = ctk.CTkLabel(
            header,
            text="🏦",
            font=ctk.CTkFont(size=36),
            text_color=COLORS["accent_gold"],
        )
        icon_lbl.grid(row=0, column=0, padx=(24, 12), pady=18)

        title_frame = ctk.CTkFrame(header, fg_color="transparent")
        title_frame.grid(row=0, column=1, sticky="w")

        ctk.CTkLabel(
            title_frame,
            text="Sistema de Atendimento Bancário",
            font=ctk.CTkFont(family="Segoe UI", size=22, weight="bold"),
            text_color=COLORS["text_primary"],
        ).pack(anchor="w")

        ctk.CTkLabel(
            title_frame,
            text="Estrutura de Dados · Fila FIFO com ArrayList Dinâmico",
            font=ctk.CTkFont(family="Segoe UI", size=11),
            text_color=COLORS["text_secondary"],
        ).pack(anchor="w")

        # Separador
        sep = ctk.CTkFrame(self, height=2, fg_color=COLORS["accent_blue"],
                           corner_radius=0)
        sep.grid(row=1, column=0, sticky="ew")

    # -- Painel de chamada -------------------------
    def _build_call_panel(self):
        outer = ctk.CTkFrame(self, fg_color="transparent")
        outer.grid(row=2, column=0, sticky="ew", padx=24, pady=(20, 0))
        outer.grid_columnconfigure(0, weight=1)

        card = ctk.CTkFrame(outer, fg_color=COLORS["bg_card"],
                            corner_radius=12,
                            border_width=1, border_color=COLORS["border"])
        card.grid(row=0, column=0, sticky="ew")
        card.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            card,
            text="ATENDENDO AGORA",
            font=ctk.CTkFont(family="Segoe UI", size=10, weight="bold"),
            text_color=COLORS["text_muted"],
        ).grid(row=0, column=0, padx=20, pady=(16, 4))

        self._lbl_chamada = ctk.CTkLabel(
            card,
            text="Aguardando primeiro atendimento...",
            font=ctk.CTkFont(family="Segoe UI", size=20, weight="bold"),
            text_color=COLORS["text_secondary"],
            wraplength=700,
        )
        self._lbl_chamada.grid(row=1, column=0, padx=20, pady=(0, 18))

    # -- Seção de entrada + botões ----------------
    def _build_input_section(self):
        outer = ctk.CTkFrame(self, fg_color="transparent")
        outer.grid(row=3, column=0, sticky="nsew", padx=24, pady=16)
        outer.grid_columnconfigure(0, weight=1)
        outer.grid_columnconfigure(1, weight=0)
        outer.grid_columnconfigure(2, weight=0)
        outer.grid_rowconfigure(0, weight=0)

        # Campo de texto
        self._entry_nome = ctk.CTkEntry(
            outer,
            placeholder_text="Digite o nome do cliente...",
            font=ctk.CTkFont(family="Segoe UI", size=14),
            fg_color=COLORS["bg_input"],
            border_color=COLORS["border"],
            border_width=1,
            text_color=COLORS["text_primary"],
            placeholder_text_color=COLORS["text_muted"],
            height=46,
            corner_radius=8,
        )
        self._entry_nome.grid(row=0, column=0, sticky="ew", padx=(0, 12))
        self._entry_nome.bind("<Return>", lambda e: self._emitir_ticket())

        # Botão enfileirar
        self._btn_emitir = ctk.CTkButton(
            outer,
            text="＋  Emitir Ticket",
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            fg_color=COLORS["accent_green"],
            hover_color="#2EA043",
            text_color="#FFFFFF",
            height=46,
            width=160,
            corner_radius=8,
            command=self._emitir_ticket,
        )
        self._btn_emitir.grid(row=0, column=1, padx=(0, 12))

        # Botão desenfileirar
        self._btn_chamar = ctk.CTkButton(
            outer,
            text="▶  Chamar Próximo",
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            fg_color=COLORS["accent_blue"],
            hover_color=COLORS["highlight"],
            text_color="#FFFFFF",
            height=46,
            width=180,
            corner_radius=8,
            command=self._chamar_proximo,
        )
        self._btn_chamar.grid(row=0, column=2)

        # Painel da fila (abaixo dos inputs)
        self._build_queue_panel_inside(outer)

    def _build_queue_panel_inside(self, parent):
        """Painel de visualização da fila dentro da seção de entrada."""
        label_title = ctk.CTkLabel(
            parent,
            text="FILA DE ESPERA",
            font=ctk.CTkFont(family="Segoe UI", size=10, weight="bold"),
            text_color=COLORS["text_muted"],
        )
        label_title.grid(row=1, column=0, columnspan=3, sticky="w",
                         pady=(20, 6))

        card = ctk.CTkFrame(parent, fg_color=COLORS["bg_card"],
                            corner_radius=12,
                            border_width=1, border_color=COLORS["border"])
        card.grid(row=2, column=0, columnspan=3, sticky="nsew")
        card.grid_columnconfigure(0, weight=1)
        parent.grid_rowconfigure(2, weight=1)

        self._txt_fila = ctk.CTkTextbox(
            card,
            font=ctk.CTkFont(family="Consolas", size=13),
            fg_color="transparent",
            text_color=COLORS["text_primary"],
            border_width=0,
            state="disabled",
            wrap="word",
            height=180,
        )
        self._txt_fila.grid(row=0, column=0, sticky="nsew",
                            padx=16, pady=12)

    def _build_queue_panel(self):
        """Placeholder — o painel real é criado em _build_queue_panel_inside."""
        pass

    # -- Rodapé / monitor de memória --------------
    def _build_footer(self):
        footer = ctk.CTkFrame(self, fg_color=COLORS["bg_card"],
                              corner_radius=0,
                              border_width=0)
        footer.grid(row=4, column=0, sticky="ew")
        footer.grid_columnconfigure(0, weight=1)
        footer.grid_columnconfigure(1, weight=0)

        # Separador topo footer
        sep = ctk.CTkFrame(self, height=1, fg_color=COLORS["border"],
                           corner_radius=0)
        sep.grid(row=4, column=0, sticky="new")

        self._lbl_memoria = ctk.CTkLabel(
            footer,
            text="",
            font=ctk.CTkFont(family="Consolas", size=11),
            text_color=COLORS["text_secondary"],
        )
        self._lbl_memoria.grid(row=0, column=0, sticky="w", padx=20, pady=12)

        ctk.CTkLabel(
            footer,
            text="Estrutura: ArrayList Dinâmico (FIFO)",
            font=ctk.CTkFont(family="Segoe UI", size=10),
            text_color=COLORS["text_muted"],
        ).grid(row=0, column=1, sticky="e", padx=20)

    # ──────────────────────────────────────────
    #  Ações
    # ──────────────────────────────────────────

    def _emitir_ticket(self):
        #"Quando clico em Emitir Ticket, a interface captura o nome, cria um objeto Ticket e chama o método enfileirar da nossa estrutura de dados."
        nome = self._entry_nome.get().strip()
        if not nome:
            self._flash_entry()
            return

        self._contador_ticket += 1
        ticket = Ticket(self._contador_ticket, nome)
        self._fila.enfileirar(ticket)

        self._entry_nome.delete(0, "end")
        self._entry_nome.focus()
        self._atualizar_ui()

    def _chamar_proximo(self):
        #"O botão de Chamar aciona o desenfileirar. O bloco try/except garante que, se a fila estiver vazia, o sistema não quebra e exibe um aviso."
        try:
            ticket = self._fila.desenfileirar()
            self._ultimo_ticket = ticket
            self._lbl_chamada.configure(
                text=f"✅  {ticket.cliente}  —  Ticket #{ticket.numero:03d}",
                text_color=COLORS["accent_green"],
            )
        except IndexError:
            self._lbl_chamada.configure(
                text="⚠️  A fila está vazia. Nenhum cliente aguardando.",
                text_color=COLORS["accent_red"],
            )
        self._atualizar_ui()

    # ──────────────────────────────────────────
    #  Atualização de estado
    # ──────────────────────────────────────────

    def _atualizar_ui(self):
        # Visualização da fila
        self._txt_fila.configure(state="normal")
        self._txt_fila.delete("1.0", "end")

        if self._fila.size() == 0:
            self._txt_fila.insert("end", "  [ Fila vazia — nenhum cliente aguardando ]")
        else:
            # Exibe cada ticket em linha separada para maior legibilidade
            for i in range(self._fila.size()):
                t = self._fila._array[i]
                posicao = "🔜 PRÓXIMO" if i == 0 else f"   #{i + 1:02d}     "
                linha = f"  {posicao}   {t}\n"
                self._txt_fila.insert("end", linha)

            self._txt_fila.insert(
                "end",
                f"\n  ─── Representação __str__: ───\n  {str(self._fila)}\n"
            )

        self._txt_fila.configure(state="disabled")

        # Monitor de memória
        tamanho = self._fila.size()
        capacidade = self._fila.capacity()
        ocupacao = (tamanho / capacidade * 100) if capacidade > 0 else 0
        barra = self._barra_progresso(tamanho, capacidade, largura=20)

        self._lbl_memoria.configure(
            text=(
                f"🗃  Tamanho Atual: {tamanho}  │  "
                f"Capacidade do Array: {capacidade}  │  "
                f"Ocupação: {ocupacao:.0f}%  {barra}  │  "
                f"Tickets Emitidos: {self._contador_ticket}"
            )
        )

    def _barra_progresso(self, atual: int, total: int, largura: int = 20) -> str:
        """Retorna uma mini barra de progresso em texto."""
        if total == 0:
            return "─" * largura
        preenchido = int((atual / total) * largura)
        return "█" * preenchido + "░" * (largura - preenchido)

    def _flash_entry(self):
        """Pisca a borda do campo de entrada para indicar erro."""
        original = COLORS["border"]
        self._entry_nome.configure(border_color=COLORS["accent_red"])
        self.after(400, lambda: self._entry_nome.configure(border_color=original))


# ─────────────────────────────────────────────
#  Entry point
# ─────────────────────────────────────────────

if __name__ == "__main__":
    app = App()
    app.mainloop()