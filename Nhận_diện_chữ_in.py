import cv2 
import pytesseract 
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk 
from googletrans import Translator 

# Đường dẫn đến Tesseract (nếu cần)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Tạo đối tượng Translator
translator = Translator()

# Hàm để mở hộp thoại chọn ảnh
def open_image():
    file_path = filedialog.askopenfilename(
        filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.tiff")]
    )
    if file_path:
        # Hiển thị hình ảnh trong giao diện
        load_image(file_path)

# Hàm để hiển thị hình ảnh đã chọn và nhận diện văn bản
def load_image(image_path):
    try:
        # Đọc hình ảnh
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError("Không thể đọc ảnh")

        # Chuyển đổi hình ảnh sang màu xám
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Nhận diện văn bản từ hình ảnh
        text = pytesseract.image_to_string(gray_image, lang='vie+eng')

        # In ra văn bản nhận diện được
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, text.strip())

        # Hiển thị hình ảnh trong GUI
        pil_image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        pil_image = pil_image.resize((300, 300), Image.LANCZOS)
        tk_image = ImageTk.PhotoImage(pil_image)

        image_label.config(image=tk_image)
        image_label.image = tk_image

    except Exception as e:
        messagebox.showerror("Lỗi", f"Không thể mở ảnh: {str(e)}")

# Hàm để dịch văn bản nhận diện được
def translate_text():
    try:
        # Lấy văn bản từ ô hiển thị
        original_text = result_text.get(1.0, tk.END).strip()

        if not original_text:
            messagebox.showwarning("Cảnh báo", "Không có văn bản để dịch.")
            return

        # Lấy ngôn ngữ đích từ menu thả xuống
        dest_language = language_var.get()

        # Dịch văn bản dựa trên ngôn ngữ đích đã chọn
        if dest_language == "Tiếng Việt":
            translated = translator.translate(original_text, src='en', dest='vi')
        else:
            translated = translator.translate(original_text, src='vi', dest='en')

        # Hiển thị bản dịch trong hộp thoại thông báo hoặc khu vực văn bản
        translation_text.delete(1.0, tk.END)
        translation_text.insert(tk.END, translated.text)

    except Exception as e:
        messagebox.showerror("Lỗi", f"Không thể dịch văn bản: {str(e)}")

# Tạo cửa sổ giao diện
root = tk.Tk()
root.title("Nhận diện và dịch văn bản từ hình ảnh")
root.geometry("800x600")

# Thêm khung chứa để dễ quản lý bố cục
main_frame = tk.Frame(root, bg='lightblue')
main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

# Nút chọn ảnh
btn_open = tk.Button(main_frame, text="Chọn ảnh", command=open_image, bg='lightblue', font=('Helvetica', 12))
btn_open.pack(pady=10)

# Khung hiển thị ảnh
image_frame = tk.Frame(main_frame, bg='white', bd=2, relief=tk.SUNKEN)
image_frame.pack(pady=10)
image_label = tk.Label(image_frame)
image_label.pack(padx=5, pady=5)

# Tạo menu thả xuống để chọn ngôn ngữ
language_var = tk.StringVar()
language_var.set("Tiếng Anh")  # Mặc định là dịch sang Tiếng Anh
language_label = tk.Label(main_frame, text="Chọn ngôn ngữ đích:", font=('Helvetica', 12), bg='lightblue')
language_label.pack(pady=5)
language_menu = ttk.Combobox(main_frame, textvariable=language_var, state='readonly', font=('Helvetica', 12))
language_menu['values'] = ("Tiếng Anh", "Tiếng Việt")
language_menu.pack(pady=5)

# Khung chứa để hiển thị văn bản nhận diện và bản dịch cạnh nhau
text_frame = tk.Frame(main_frame)
text_frame.pack(fill=tk.BOTH, expand=True)

# Khung hiển thị văn bản nhận diện được
result_frame = tk.Frame(text_frame, bg='white', bd=2, relief=tk.SUNKEN)
result_frame.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH, expand=True)
result_label = tk.Label(result_frame, text="Văn bản nhận diện:", font=('Helvetica', 12), bg='lightblue')
result_label.pack(anchor='w', padx=5, pady=5)
result_text = tk.Text(result_frame, height=20, font=('Helvetica', 10), bg='white', wrap=tk.WORD, padx=5, pady=5)
result_text.pack(fill=tk.BOTH, expand=True)

# Khung hiển thị văn bản đã dịch
translation_frame = tk.Frame(text_frame, bg='white', bd=2, relief=tk.SUNKEN)
translation_frame.pack(side=tk.RIGHT, padx=10, pady=10, fill=tk.BOTH, expand=True)
translation_label = tk.Label(translation_frame, text="Bản dịch:", font=('Helvetica', 12), bg='lightblue')
translation_label.pack(anchor='w', padx=5, pady=5)
translation_text = tk.Text(translation_frame, height=20, font=('Helvetica', 10), bg='white', wrap=tk.WORD, padx=5, pady=5)
translation_text.pack(fill=tk.BOTH, expand=True)

# Nút dịch văn bản ở giữa hai khung
btn_translate = tk.Button(text_frame, text="Dịch ", command=translate_text, bg='lightgreen', font=('Helvetica', 12))
btn_translate.pack(side=tk.LEFT, padx=5, pady=5)


# Chạy giao diện
root.mainloop()
