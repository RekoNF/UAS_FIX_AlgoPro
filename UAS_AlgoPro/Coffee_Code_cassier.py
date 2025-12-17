
import tkinter as tk
import tkinter.font as tkfont
from tkinter import messagebox, ttk, filedialog
from datetime import datetime
from PIL import Image, ImageTk
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image as RLImage
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
import os

class CoffeeCassierApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Coffee Code Cafe Cassier")
        self.root.geometry("700x1045")

        self.logo_img = None
        default_logo = os.path.join(os.path.dirname(__file__), "coffee ku_code shop.jpg")
        if os.path.exists(default_logo):
            try:
                img = Image.open(default_logo).convert("RGBA")
                img = img.resize((64, 64), Image.LANCZOS)
                self.logo_img = ImageTk.PhotoImage(img)
            except Exception:
                self.logo_img = None
        else:
            self.logo_img = None

        self.coffee_menu = {
            "Espresso": 40000,
            "Latte": 56000,
            "Cappuccino": 48000,
            "Mocha": 64000,
            "Americano": 32000
        }

        self.non_coffee_menu = {
            "Iced Tea": 24000,
            "Milk Tea": 48000,
            "Soda": 24000,
            "Thai Tea": 48000
        }

        self.snack_menu = {
            "Cookies & Cream": 80000,
            "French Fries": 48000,
            "Chicken Bites": 64000,
            "Croissant": 40000,
            "Waffle": 48000,
            "Cookies": 24000
        }

        self.orders = []
        self.total_revenue = 0.0

        self.create_widgets()

    def create_widgets(self):
        main_frame = ttk.Frame(self.root, padding=10)
        main_frame.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(6, weight=1)

        

        title = ttk.Label(main_frame, text="Coffee Code Cassier", font=("Poppins", 16, "bold"))
        title.grid(row=0, column=0, columnspan=3, pady=(0,10))
        if self.logo_img:
            logo_label = ttk.Label(main_frame, image=self.logo_img)
            logo_label.grid(row=0, column=0, padx=10, pady=(0,10))

        # Coffee selector
        ttk.Label(main_frame, text="Select Coffee:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.coffee_var = tk.StringVar()
        self.coffee_combobox = ttk.Combobox(main_frame, textvariable=self.coffee_var, state="readonly",
                                            values=list(self.coffee_menu.keys()))
        self.coffee_combobox.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)

        # Non-coffee selector
        ttk.Label(main_frame, text="Select non-Coffee:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.noncoffee_var = tk.StringVar()
        self.noncoffee_combobox = ttk.Combobox(main_frame, textvariable=self.noncoffee_var, state="readonly",
                                               values=list(self.non_coffee_menu.keys()))
        self.noncoffee_combobox.grid(row=2, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)

        # Snack selector
        ttk.Label(main_frame, text="Select Snack:").grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
        self.snack_var = tk.StringVar()
        self.snack_combobox = ttk.Combobox(main_frame, textvariable=self.snack_var, state="readonly",
                                           values=list(self.snack_menu.keys()))
        self.snack_combobox.grid(row=3, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)

        # Quantity
        ttk.Label(main_frame, text="Quantity:").grid(row=4, column=0, sticky=tk.W, padx=5, pady=5)
        self.qty_var = tk.IntVar(value=1)
        self.qty_spin = tk.Spinbox(main_frame, from_=1, to=100, textvariable=self.qty_var, width=6)
        self.qty_spin.grid(row=4, column=1, sticky=tk.W, padx=5, pady=5)

        # Buttons
        btn_frame = ttk.Frame(main_frame)
        btn_frame.grid(row=5, column=0, columnspan=3, pady=10)
        ttk.Button(btn_frame, text="Order", command=self.place_order).grid(row=0, column=0, padx=5)
        ttk.Button(btn_frame, text="Clear", command=self.clear_selection).grid(row=0, column=1, padx=5)
        ttk.Button(btn_frame, text="Print Receipt", command=self.print_receipt).grid(row=0, column=2, padx=5)
        ttk.Button(btn_frame, text="Export to PDF", command=self.export_pdf).grid(row=0, column=3, padx=5)
        ttk.Button(btn_frame, text="Reset All", command=self.reset_all).grid(row=0, column=4, padx=5)

        # Receipt area
        struk_frame = ttk.LabelFrame(main_frame, text="Struk Pembelian", padding=10)
        struk_frame.grid(row=6, column=0, columnspan=3, sticky=(tk.N, tk.S, tk.E, tk.W), padx=5, pady=5)
        struk_frame.columnconfigure(0, weight=1)
        struk_frame.rowconfigure(0, weight=1)

        self.receipt_text = tk.Text(struk_frame, wrap="word", height=15, font=("Courier", 10))
        self.receipt_text.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        scrollbar = ttk.Scrollbar(struk_frame, orient="vertical", command=self.receipt_text.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.receipt_text.configure(yscrollcommand=scrollbar.set)

        self.summary_var = tk.StringVar(value="Total Orders: 0 | Total Revenue: Rp0.00")
        summary_label = ttk.Label(main_frame, textvariable=self.summary_var, anchor="w", font=("Arial", 10, "bold"))
        summary_label.grid(row=7, column=0, columnspan=3, sticky=(tk.W, tk.E), padx=5, pady=(6,0))

        self.receipt_text = tk.Text(struk_frame, wrap="word", height=15, font=("Courier", 10))
        self.receipt_text.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        scrollbar = ttk.Scrollbar(struk_frame, orient="vertical", command=self.receipt_text.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.receipt_text.configure(yscrollcommand=scrollbar.set)

        # add bold tag for TOTAL REVENUE styling
        bold_font = tkfont.Font(self.receipt_text, self.receipt_text.cget("font"))
        bold_font.configure(weight="bold", size=12)
        self.receipt_text.tag_configure("bold", font=bold_font)

    def place_order(self):
        item = None
        price = None
        name = None

        if self.coffee_var.get():
            name = self.coffee_var.get()
            price = self.coffee_menu.get(name)
        elif self.noncoffee_var.get():
            name = self.noncoffee_var.get()
            price = self.non_coffee_menu.get(name)
        elif self.snack_var.get():
            name = self.snack_var.get()
            price = self.snack_menu.get(name)

        if name is None or price is None:
            messagebox.showwarning("Selection Error", "Please select an item from one of the menus.")
            return

        try:
            qty = int(self.qty_var.get())
            if qty <= 0:
                raise ValueError
        except Exception:
            messagebox.showwarning("Input Error", "Quantity harus integer > 0.")
            return

        subtotal = price * qty
        self.orders.append({"type": name, "qty": qty, "price": price, "subtotal": subtotal})
        self.total_revenue += subtotal

        receipt = f"Order #{len(self.orders)}\n"
        receipt += f"  Item : {name}\n"
        receipt += f"  Price: Rp{price:,}\n"
        receipt += f"  Qty  : {qty}\n"
        receipt += f"  Subt : Rp{subtotal:,}\n"
        receipt += "-" * 35 + "\n"

        self.receipt_text.insert(tk.END, receipt)
        self.receipt_text.see(tk.END)

        self.update_summary()
        self.clear_selection()

    def clear_selection(self):
        # Clear all selectors
        self.coffee_combobox.set("")
        self.noncoffee_combobox.set("")
        self.snack_combobox.set("")
        self.qty_var.set(1)

    def update_summary(self):
        self.summary_var.set(f"Total Orders: {len(self.orders)} | Total Revenue: Rp{self.total_revenue:,.0f}")

    def print_receipt(self):
        if not self.orders:
            messagebox.showwarning("Warning", "Tidak ada pesanan untuk dicetak.")
            return

        receipt_content = self.get_full_receipt()
        self.receipt_text.delete(1.0, tk.END)

        # insert lines and apply bold tag to TOTAL REVENUE line
        for line in receipt_content.splitlines(keepends=True):
            if line.strip().startswith("TOTAL REVENUE:"):
                self.receipt_text.insert(tk.END, line, "bold")
            else:
                self.receipt_text.insert(tk.END, line)

        self.receipt_text.see(tk.END)
        messagebox.showinfo("Print", "Struk siap dicetak. Gunakan Ctrl+P untuk print atau Export to PDF.")

    def export_pdf(self):
        if not self.orders:
            messagebox.showwarning("Warning", "Tidak ada pesanan untuk diexport.")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")],
            initialfile=f"receipt_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        )

        if not file_path:
            return

        try:
            self.create_pdf(file_path)
            messagebox.showinfo("Success", f"PDF berhasil disimpan:\n{file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Gagal membuat PDF:\n{e}")

    def create_pdf(self, file_path):
        doc = SimpleDocTemplate(file_path, pagesize=(350, 500) , topMargin=0.25*inch, bottomMargin=0.25*inch)
        elements = []
        styles = getSampleStyleSheet()

        # Tambahkan logo 
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=15,
            textColor=colors.HexColor('#304852'),
            spaceAfter=6,
            alignment=1
        )

        date_style = ParagraphStyle(
            'DateStyle',
            parent=styles['Normal'],
            fontSize=8,
            alignment=0,
            spaceAfter=4
        )

        subtitle_style = ParagraphStyle(
            'Subtitle',
            parent=styles['Normal'],
            fontSize=10,
            alignment=1,
            spaceAfter=4
        )

        subsubtitle_style = ParagraphStyle(
            'Subtitle',
            parent=styles['Normal'],
            fontSize=6,
            alignment=1,
            spaceBefore=0,
            spaceAfter=3
        )


        logo_path = os.path.join(os.path.dirname(__file__), "coffee ku_code shop.jpg")
        if os.path.exists(logo_path):
            try:
                logo = RLImage(logo_path, width=0.5*inch, height=0.5*inch)
                elements.append(logo)
                elements.append(Spacer(1, 0.2*inch))
            except Exception:
                print(f"Logo tidak dapat dimuat dari {logo_path}")

        elements.append(Paragraph("COFFEE CODE CAFE", title_style))
        elements.append(Paragraph("Bikin Harimu Menyenangkan dengan Code di kopi!", subsubtitle_style))
        elements.append(Paragraph("="*33, subtitle_style))
        elements.append(Paragraph("Receipt / Struk Pembelian", subtitle_style))
        elements.append(Spacer(1, 0.2*inch))

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        elements.append(Paragraph(f"<b>Date:</b> {timestamp}", date_style))
        elements.append(Paragraph("Jl. Kopi No.123, Jakarta", date_style))
        elements.append(Spacer(1, 0.1*inch))
        elements.append(Paragraph("="*33, subtitle_style))
        elements.append(Spacer(1, 0.2*inch))

        data = [["No.", "Item", "Price", "Qty", "Subtotal"]]
        for i, order in enumerate(self.orders, 1):
            data.append([
                str(i),
                order["type"],
                f"Rp{order['price']:,}",
                str(order['qty']),
                f"Rp{order['subtotal']:,}"
            ])

        table = Table(data, colWidths=[0.4*inch, 1.3*inch, 0.6*inch, 0.4*inch, 0.6*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#304852')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 8),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#B9DBE6')),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 6),
            ('ALIGN', (3, 1), (-1, -1), 'RIGHT'),
        ]))
        elements.append(table)
        elements.append(Spacer(1, 0.2*inch))

        total_style = ParagraphStyle(
            'TotalStyle',
            parent=styles['Heading2'],
            fontSize=12,
            textColor=colors.HexColor('#304852'),
            alignment=0,
            spaceAfter=6,
            weight='bold'
        )

        thank_you_style = ParagraphStyle(
            'ThankYouStyle',
            parent=styles['Heading2'],
            fontSize=6,
            textColor=colors.HexColor('#304852'),
            alignment=1,
            spaceBefore=6,
        )

        elements.append(Paragraph(f"<b>TOTAL: Rp{self.total_revenue:,.0f}</b>", total_style))
        elements.append(Paragraph("="*33, subtitle_style))
        elements.append(Spacer(1, 0.1*inch))
        elements.append(Paragraph("Terima kasih atas pembelian Anda! 😊", thank_you_style))

        doc.build(elements)

    def get_full_receipt(self):
        receipt = "=" * 40 + "\n"
        receipt += "           COFFEE CODE CAFE\n"
        receipt += "           Receipt / Struk\n"
        receipt += "=" * 40 + "\n"
        receipt += f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        receipt += "Alamat Cafe: Jl. Kopi No.123, Jakarta\n"
        receipt += "-" * 40 + "\n"

        for i, order in enumerate(self.orders, 1):
            receipt += f"{i}. {order['type']}\n"
            receipt += f"   Price: Rp{order['price']:,}\n"
            receipt += f"   Qty  : {order['qty']}\n"
            receipt += f"   Sub  : Rp{order['subtotal']:,}\n"
            receipt += "-" * 40 + "\n"

        receipt += f"TOTAL REVENUE: Rp{self.total_revenue:,.0f}\n" 
        receipt += "=" * 40 + "\n"
        receipt += "Thank you! 😊\n"
        return receipt

    def reset_all(self):
        if messagebox.askyesno("Confirm", "Reset semua pesanan?"):
            self.orders = []
            self.total_revenue = 0.0
            self.receipt_text.delete(1.0, tk.END)
            self.update_summary()

if __name__ == "__main__":
    root = tk.Tk()
    app = CoffeeCassierApp(root)
    root.mainloop()