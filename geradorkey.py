import tkinter as tk
from tkinter import ttk
import secrets
import string

class SecureKeyGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Secure Key Generator")
        self.root.geometry("700x600")
        self.root.configure(bg="#f0f0f0")
        
        self.generated_keys = []
        
        # Title
        title = ttk.Label(root, text="🔐 Secure Key Generator", 
                         font=("Arial", 18, "bold"))
        title.pack(pady=15)
        
        # Control Frame
        control_frame = ttk.LabelFrame(root, text="Opções de Geração", padding=10)
        control_frame.pack(pady=10, padx=10, fill="x")
        
        # Key Type
        ttk.Label(control_frame, text="Tipo de Chave:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.key_type = tk.StringVar(value="urlsafe")
        key_types = ttk.Combobox(control_frame, textvariable=self.key_type, 
                                state="readonly", width=20)
        key_types['values'] = ('URL Safe (Base64)', 'Hexadecimal', 'Aleatória Complexa')
        key_types.grid(row=0, column=1, sticky="ew", padx=5, pady=5)
        
        # Key Length
        ttk.Label(control_frame, text="Comprimento (bytes):").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.length_var = tk.StringVar(value="32")
        length_spinbox = ttk.Spinbox(control_frame, from_=16, to=128, 
                                     textvariable=self.length_var, width=20)
        length_spinbox.grid(row=1, column=1, sticky="ew", padx=5, pady=5)
        
        # Quantity
        ttk.Label(control_frame, text="Quantidade de Chaves:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.quantity_var = tk.StringVar(value="1")
        quantity_spinbox = ttk.Spinbox(control_frame, from_=1, to=50, 
                                       textvariable=self.quantity_var, width=20)
        quantity_spinbox.grid(row=2, column=1, sticky="ew", padx=5, pady=5)
        
        # Buttons Frame
        button_frame = ttk.Frame(control_frame)
        button_frame.grid(row=3, column=0, columnspan=2, sticky="ew", padx=5, pady=10)
        
        gen_btn = ttk.Button(button_frame, text="Gerar Chaves",
                            command=self.generate_keys)
        gen_btn.pack(side="left", padx=5)
        
        copy_btn = ttk.Button(button_frame, text="Copiar Selecionada",
                             command=self.copy_selected)
        copy_btn.pack(side="left", padx=5)
        
        clear_btn = ttk.Button(button_frame, text="Limpar",
                              command=self.clear_keys)
        clear_btn.pack(side="left", padx=5)
        
        control_frame.columnconfigure(1, weight=1)
        
        # Results Frame
        results_frame = ttk.LabelFrame(root, text="Chaves Geradas", padding=10)
        results_frame.pack(pady=10, padx=10, fill="both", expand=True)
        
        # Scrollbar and Listbox
        scrollbar = ttk.Scrollbar(results_frame)
        scrollbar.pack(side="right", fill="y")
        
        self.listbox = tk.Listbox(results_frame, yscrollcommand=scrollbar.set,
                                  font=("Courier", 9), bg="white", height=15)
        self.listbox.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.listbox.yview)
        
        # Info Frame
        info_frame = ttk.Frame(root)
        info_frame.pack(pady=5, padx=10, fill="x")
        
        self.info_label = ttk.Label(info_frame, text="", font=("Arial", 9), foreground="green")
        self.info_label.pack(side="left")
        
        self.status_label = ttk.Label(info_frame, text="Pronto para gerar", font=("Arial", 9), foreground="blue")
        self.status_label.pack(side="right")
    
    def generate_keys(self):
        try:
            key_type = self.key_type.get()
            length = int(self.length_var.get())
            quantity = int(self.quantity_var.get())
            
            if length < 16:
                length = 16
            if quantity < 1:
                quantity = 1
            
            self.generated_keys = []
            
            for _ in range(quantity):
                if key_type == "URL Safe (Base64)":
                    key = secrets.token_urlsafe(length)
                elif key_type == "Hexadecimal":
                    key = secrets.token_hex(length)
                else:  # Aleatória Complexa
                    chars = string.ascii_letters + string.digits + string.punctuation
                    key = ''.join(secrets.choice(chars) for _ in range(length * 2))
                
                self.generated_keys.append(key)
            
            self.display_keys()
            self.status_label.config(text=f"✓ {quantity} chave(s) gerada(s) com sucesso!")
            
        except ValueError:
            self.status_label.config(text="Erro: Verifique os valores inseridos", foreground="red")
    
    def display_keys(self):
        self.listbox.delete(0, tk.END)
        for key in self.generated_keys:
            self.listbox.insert(tk.END, key)
        
        total = len(self.generated_keys)
        avg_length = len(self.generated_keys[0]) if self.generated_keys else 0
        self.info_label.config(
            text=f"Total: {total} | Comprimento médio: {avg_length} caracteres"
        )
    
    def copy_selected(self):
        selection = self.listbox.curselection()
        if selection:
            key = self.generated_keys[selection[0]]
            self.root.clipboard_clear()
            self.root.clipboard_append(key)
            self.status_label.config(text="✓ Chave copiada para a área de transferência!", foreground="green")
        else:
            self.status_label.config(text="Selecione uma chave primeiro", foreground="red")
    
    def clear_keys(self):
        self.generated_keys = []
        self.listbox.delete(0, tk.END)
        self.info_label.config(text="")
        self.status_label.config(text="Pronto para gerar", foreground="blue")

if __name__ == "__main__":
    root = tk.Tk()
    app = SecureKeyGenerator(root)
    root.mainloop()


