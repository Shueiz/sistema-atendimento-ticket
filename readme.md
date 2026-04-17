# 🏦 Sistema de Atendimento Bancário (Fila FIFO)

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white)
![CustomTkinter](https://img.shields.io/badge/GUI-CustomTkinter-darkgreen)
![Estrutura de Dados](https://img.shields.io/badge/Estrutura-Fila%20(Queue)-orange)

Um sistema interativo de gerenciamento de senhas bancárias desenvolvido com **Python** e **CustomTkinter**. Este projeto foi criado como aplicação prática para a disciplina de Estruturas de Dados, demonstrando como uma estrutura clássica de *ArrayList* pode ser adaptada para se comportar como uma **Fila (FIFO - First-In, First-Out)**.

---

## 🚀 Funcionalidades

* **Emissão de Tickets:** Adiciona novos clientes ao final da fila (`enfileirar`).
* **Chamada de Clientes:** Remove e atende sempre o primeiro cliente da fila (`desenfileirar`).
* **Redimensionamento Dinâmico:** O array interno dobra de tamanho automaticamente quando atinge sua capacidade máxima (`_resize_memory()`).
* **Interface Gráfica Moderna:** Desenvolvida com `CustomTkinter`, incluindo modo escuro nativo e design responsivo.
* **Monitoramento de Memória:** Um painel em tempo real no rodapé que exibe o tamanho atual, a capacidade máxima e a porcentagem de ocupação do array na memória.
* **Tratamento de Exceções:** Prevenção de quebras no sistema ao tentar chamar clientes com a fila vazia (captura de `IndexError`).

---

## 🧠 Sob o Capô: Estrutura de Dados

O diferencial deste projeto é que **não utilizamos os métodos nativos de lista do Python** (como `.append()` ou `.pop(0)`). A lógica de negócio foi implementada do zero utilizando um array de tamanho fixo inicial, manipulando os índices manualmente:

1. **Shift Left (`_shift_left`):** Ao atender o cliente do índice `0`, todos os elementos subsequentes são realocados uma posição para a esquerda através de um laço de repetição, cobrindo o espaço vazio.
2. **Garbage Collection:** O último espaço do array, após o deslocamento, tem sua referência explicitamente limpa (`self._array[self._tamanho] = None`) para otimização de memória.

---

## 🛠️ Como executar o projeto na sua máquina

**Pré-requisitos:**
* Python 3.x instalado.
* Sistema Operacional: Windows, macOS ou Linux (requer `python3-tk` em distros baseadas em Debian/Ubuntu).

**Passo a passo:**

1. Clone este repositório:
   ```bash
   git clone [https://github.com/Shueiz/sistema-atendimento-ticket.git](https://github.com/Shueiz/sistema-atendimento-ticket.git)

2. Entre na pasta do projeto:
    ```bash
    cd sistema_tickets

3. Instale a biblioteca gráfica:
    ```bash
    pip install customtkinter

4. Execute o sistema:
    ```bash
    python sistema_tickets.py

## 👨‍💻 Autor

Desenvolvido por Matheus Concesso Araujo Pereira

LinkedIn: https://www.linkedin.com/in/matheus-concesso-095870301/

Apresentação do Projeto (Vídeo): [Link em breve - Gravando...]

Projeto desenvolvido para a disciplina de Estruturas de Dados.
