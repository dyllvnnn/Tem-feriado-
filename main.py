import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import tkinter.ttk as ttk
from tkinter import font as tkFont
import threading
from datetime import datetime
import os

# Colors matching the design inspiration
PRIMARY_BLUE = "#1E88E5"
DARK_BLUE = "#1565C0"
LIGHT_GRAY = "#F5F5F5"
DARK_GRAY = "#424242"
WHITE = "#FFFFFF"
SUCCESS_GREEN = "#4CAF50"
ERROR_RED = "#F44336"


class HolidayCheckerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Tem feriado aí?")
        self.root.geometry("1200x700")
        self.root.resizable(False, False)
        
        # Set minimum window size
        self.root.minsize(1000, 600)
        
        self.pdf_path = None
        self.holidays = {}
        self.found_dates = []
        self.holiday_dates = []
        
        self.setup_fonts()
        self.create_widgets()
        
    def setup_fonts(self):
        """Setup custom fonts for the application"""
        self.title_font = tkFont.Font(family="Helvetica", size=24, weight="bold")
        self.subtitle_font = tkFont.Font(family="Helvetica", size=14)
        self.body_font = tkFont.Font(family="Helvetica", size=11)
        self.small_font = tkFont.Font(family="Helvetica", size=9)
        
    def create_widgets(self):
        """Create the main UI layout"""
        # Main container with two panels
        main_frame = tk.Frame(self.root, bg=WHITE)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Left panel (blue)
        left_panel = tk.Frame(main_frame, bg=PRIMARY_BLUE, width=400)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=False)
        left_panel.pack_propagate(False)
        
        # Left panel content
        left_content = tk.Frame(left_panel, bg=PRIMARY_BLUE)
        left_content.pack(fill=tk.BOTH, expand=True, padx=30, pady=40)
        
        title = tk.Label(
            left_content, 
            text="Tem feriado aí?", 
            font=self.title_font, 
            fg=WHITE, 
            bg=PRIMARY_BLUE,
            wraplength=300,
            justify=tk.LEFT
        )
        title.pack(anchor=tk.W, pady=(0, 10))
        
        # Underline
        underline = tk.Frame(left_content, bg=WHITE, height=3)
        underline.pack(anchor=tk.W, fill=tk.X, pady=(0, 20))
        
        description = tk.Label(
            left_content,
            text="Envie um arquivo PDF contendo datas e descubra quais são feriados brasileiros. Nosso sistema verifica cada data contra o banco de dados de feriados oficial.",
            font=self.body_font,
            fg=WHITE,
            bg=PRIMARY_BLUE,
            wraplength=320,
            justify=tk.LEFT,
            pady=10
        )
        description.pack(anchor=tk.W, pady=(0, 20))
        
        status_label = tk.Label(
            left_content,
            text="Status:",
            font=self.subtitle_font,
            fg=WHITE,
            bg=PRIMARY_BLUE
        )
        status_label.pack(anchor=tk.W, pady=(20, 5))
        
        self.status_text = tk.Label(
            left_content,
            text="Pronto para analisar arquivos PDF",
            font=self.body_font,
            fg="#BBDEFB",
            bg=PRIMARY_BLUE,
            wraplength=320,
            justify=tk.LEFT
        )
        self.status_text.pack(anchor=tk.W)
        
        # Right panel (white)
        right_panel = tk.Frame(main_frame, bg=WHITE)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Right panel content
        right_content = tk.Frame(right_panel, bg=WHITE)
        right_content.pack(fill=tk.BOTH, expand=True, padx=40, pady=40)
        
        # Title
        right_title = tk.Label(
            right_content,
            text="Analisar Datas no PDF",
            font=self.subtitle_font,
            fg=DARK_GRAY,
            bg=WHITE
        )
        right_title.pack(anchor=tk.W, pady=(0, 30))
        
        # File selection frame
        file_frame = tk.Frame(right_content, bg=WHITE)
        file_frame.pack(fill=tk.X, pady=(0, 20))
        
        file_label = tk.Label(
            file_frame,
            text="Selecionar arquivo PDF",
            font=self.body_font,
            fg=DARK_GRAY,
            bg=WHITE
        )
        file_label.pack(anchor=tk.W, pady=(0, 8))
        
        file_button_frame = tk.Frame(file_frame, bg=WHITE)
        file_button_frame.pack(fill=tk.X)
        
        self.file_button = tk.Button(
            file_button_frame,
            text="Escolher arquivo",
            command=self.select_pdf,
            bg=PRIMARY_BLUE,
            fg=WHITE,
            font=self.body_font,
            padx=20,
            pady=10,
            relief=tk.FLAT,
            cursor="hand2",
            activebackground=DARK_BLUE
        )
        self.file_button.pack(side=tk.LEFT)
        
        self.file_path_label = tk.Label(
            file_button_frame,
            text="Nenhum arquivo selecionado",
            font=self.small_font,
            fg="#999",
            bg=WHITE
        )
        self.file_path_label.pack(side=tk.LEFT, padx=(15, 0))
        
        # Analyze button
        self.analyze_button = tk.Button(
            right_content,
            text="Analisar PDF",
            command=self.analyze_pdf,
            bg=PRIMARY_BLUE,
            fg=WHITE,
            font=self.subtitle_font,
            padx=30,
            pady=12,
            relief=tk.FLAT,
            cursor="hand2",
            activebackground=DARK_BLUE,
            state=tk.DISABLED
        )
        self.analyze_button.pack(pady=(0, 30))
        
        # Results frame
        results_label = tk.Label(
            right_content,
            text="Resultados",
            font=self.body_font,
            fg=DARK_GRAY,
            bg=WHITE
        )
        results_label.pack(anchor=tk.W, pady=(20, 10))
        
        # Results text area
        self.results_text = scrolledtext.ScrolledText(
            right_content,
            height=15,
            width=50,
            font=self.body_font,
            bg=LIGHT_GRAY,
            fg=DARK_GRAY,
            relief=tk.FLAT,
            padx=10,
            pady=10,
            state=tk.DISABLED
        )
        self.results_text.pack(fill=tk.BOTH, expand=True)
        
    def select_pdf(self):
        """Handle PDF file selection"""
        file_path = filedialog.askopenfilename(
            title="Selecionar arquivo PDF",
            filetypes=[("Arquivos PDF", "*.pdf"), ("Todos os arquivos", "*.*")]
        )
        
        if file_path:
            self.pdf_path = file_path
            filename = os.path.basename(file_path)
            self.file_path_label.config(text=f"✓ {filename}")
            self.analyze_button.config(state=tk.NORMAL)
            self.update_status(f"Selecionado: {filename}")
            
    def update_status(self, message):
        """Update status text in left panel"""
        self.status_text.config(text=message)
        self.root.update()
        
    def update_results(self, text):
        """Update results text area"""
        self.results_text.config(state=tk.NORMAL)
        self.results_text.insert(tk.END, text)
        self.results_text.see(tk.END)
        self.results_text.config(state=tk.DISABLED)
        
    def clear_results(self):
        """Clear results text area"""
        self.results_text.config(state=tk.NORMAL)
        self.results_text.delete(1.0, tk.END)
        self.results_text.config(state=tk.DISABLED)
        
    def analyze_pdf(self):
        """Analyze PDF in a separate thread"""
        if not self.pdf_path:
            messagebox.showerror("Erro", "Selecione um arquivo PDF primeiro")
            return
            
        self.analyze_button.config(state=tk.DISABLED)
        self.clear_results()
        self.update_status("Analisando PDF...")
        
        thread = threading.Thread(target=self._analyze_pdf_thread)
        thread.daemon = True
        thread.start()
        
    def _analyze_pdf_thread(self):
        """Background thread for PDF analysis"""
        try:
            # Import PDF reading library
            from pdf_handler import extract_dates_from_pdf
            from api_handler import fetch_holidays, check_if_holiday
            
            self.update_status("Lendo arquivo PDF...")
            self.found_dates = extract_dates_from_pdf(self.pdf_path)
            
            if not self.found_dates:
                self.update_results("Nenhuma data encontrada no arquivo PDF\n")
                self.update_status("Nenhuma data encontrada no PDF")
                self.analyze_button.config(state=tk.NORMAL)
                return
            
            self.update_results(f"Encontradas {len(self.found_dates)} data(s) no PDF:\n")
            self.update_results("-" * 40 + "\n\n")
            
            for date in self.found_dates:
                self.update_results(f"  • {date.strftime('%d/%m/%Y')}\n")
            
            self.update_results("\n" + "-" * 40 + "\n\n")
            self.update_status("Consultando feriados brasileiros...")
            
            # Fetch holidays from API
            self.holidays = fetch_holidays()
            
            if not self.holidays:
                self.update_results("Erro ao buscar dados de feriados\n")
                self.update_status("Erro ao buscar feriados")
                self.analyze_button.config(state=tk.NORMAL)
                return
            
            self.update_status("Verificando quais datas são feriados...")
            self.update_results("Análise de Feriados:\n\n")
            
            self.holiday_dates = []
            
            for date in self.found_dates:
                is_holiday, holiday_name = check_if_holiday(date, self.holidays)
                
                if is_holiday:
                    self.holiday_dates.append((date, holiday_name))
                    self.update_results(f"✅ {date.strftime('%d/%m/%Y')} - {holiday_name}\n")
                else:
                    self.update_results(f"⚪ {date.strftime('%d/%m/%Y')} - Não é feriado\n")
            
            self.update_results("\n" + "-" * 40 + "\n")
            self.update_results(f"Resumo: {len(self.holiday_dates)}/{len(self.found_dates)} datas são feriados\n")
            
            self.update_status(f"Análise concluída: {len(self.holiday_dates)} feriados encontrados")
            
        except ImportError as e:
            self.update_results(f"Erro: Módulo não encontrado - {str(e)}\n")
            self.update_results("Certifique-se de executar: pip install PyPDF2 requests\n")
            self.update_status("Erro de módulo")
        except Exception as e:
            self.update_results(f"Erro durante análise: {str(e)}\n")
            self.update_status("Erro ocorreu")
        finally:
            self.analyze_button.config(state=tk.NORMAL)


def main():
    root = tk.Tk()
    app = HolidayCheckerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
