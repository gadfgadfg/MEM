import tkinter as tk
from tkinter import filedialog, messagebox, colorchooser, ttk
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter, ImageTk

class MemeGeneratorApp:
    def __init__(self, master):
        self.master = master
        master.title("Генератор Мемов")

        self.top_text = tk.StringVar()
        self.bottom_text = tk.StringVar()
        self.image_path = None
        self.original_image = None
        self.temp_image = None
        self.modified_image = None
        self.font_size = 50

        self.top_text_color = "white"
        self.top_text_italic = tk.BooleanVar()
        self.top_text_bold = tk.BooleanVar()
        self.top_letter_spacing = tk.DoubleVar(value=0.0)
        self.top_line_spacing = tk.DoubleVar(value=1.0)
        self.top_stroke_color = "black"
        self.top_stroke_width = 2
        self.top_shadow_color = "gray"
        self.top_shadow_offset_x = 2
        self.top_shadow_offset_y = 2
        self.top_text_position = tk.StringVar(value="сверху_по_центру")

        self.bottom_text_color = "white"
        self.bottom_text_italic = tk.BooleanVar()
        self.bottom_text_bold = tk.BooleanVar()
        self.bottom_letter_spacing = tk.DoubleVar(value=0.0)
        self.bottom_line_spacing = tk.DoubleVar(value=1.0)
        self.bottom_stroke_color = "black"
        self.bottom_stroke_width = 2
        self.bottom_shadow_color = "gray"
        self.bottom_shadow_offset_x = 2
        self.bottom_shadow_offset_y = 2
        self.bottom_text_position = tk.StringVar(value="снизу_по_центру")

        self.input_frame = tk.Frame(master)
        self.input_frame.pack(pady=10, fill=tk.X)

        tk.Label(self.input_frame, text="Текст сверху:").grid(row=0, column=0, sticky="w")
        self.top_text_entry = tk.Entry(self.input_frame, textvariable=self.top_text)
        self.top_text_entry.grid(row=0, column=1, padx=5, sticky="ew")
        self.input_frame.columnconfigure(1, weight=1)

        tk.Label(self.input_frame, text="Текст снизу:").grid(row=1, column=0, sticky="w")
        self.bottom_text_entry = tk.Entry(self.input_frame, textvariable=self.bottom_text)
        self.bottom_text_entry.grid(row=1, column=1, padx=5, sticky="ew")

        self.edit_image_button = tk.Button(self.input_frame, text="Редактировать изображение", command=self.open_image_editor)
        self.edit_image_button.grid(row=0, column=2, rowspan=1, padx=5, sticky="ew")

        self.settings_button = tk.Button(self.input_frame, text="Настройки", command=self.open_settings_window)
        self.settings_button.grid(row=1, column=2, rowspan=1, padx=5, sticky="ew")

        self.preview_frame = tk.Frame(master)
        self.preview_frame.pack(pady=10, fill=tk.BOTH, expand=True)

        self.preview_image_label = tk.Label(self.preview_frame)
        self.preview_image_label.pack(fill=tk.BOTH, expand=True)

        self.action_frame = tk.Frame(master)
        self.action_frame.pack(pady=10, fill=tk.X)

        self.select_image_button = tk.Button(self.action_frame, text="Выбрать изображение", command=self.select_image)
        self.select_image_button.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

        self.preview_button = tk.Button(self.action_frame, text="Предпросмотр", command=self.update_preview)
        self.preview_button.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

        self.save_meme_button = tk.Button(self.action_frame, text="Сохранить мем", command=self.save_meme)
        self.save_meme_button.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

        self.action_frame.columnconfigure(0, weight=1)
        self.action_frame.columnconfigure(1, weight=1)
        self.action_frame.columnconfigure(2, weight=1)

    def open_image_editor(self):
        if not self.image_path:
            messagebox.showerror("Ошибка", "Сначала выберите изображение!")
            return

        editor_window = tk.Toplevel(self.master)
        editor_window.title("Редактор изображений")

        self.brightness = tk.DoubleVar(value=1.0)
        self.contrast = tk.DoubleVar(value=1.0)
        self.saturation = tk.DoubleVar(value=1.0)

        settings_frame = tk.Frame(editor_window)
        settings_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        row = 0

        brightness_label = tk.Label(settings_frame, text="Яркость:")
        brightness_label.grid(row=row, column=0, sticky="w", padx=5, pady=5)
        brightness_scale = tk.Scale(settings_frame, from_=0.1, to=3.0, resolution=0.1, orient=tk.HORIZONTAL,
                                     variable=self.brightness)
        brightness_scale.grid(row=row, column=1, padx=5, pady=5, sticky="ew")
        row += 1

        contrast_label = tk.Label(settings_frame, text="Контрастность:")
        contrast_label.grid(row=row, column=0, sticky="w", padx=5, pady=5)
        contrast_scale = tk.Scale(settings_frame, from_=0.1, to=3.0, resolution=0.1, orient=tk.HORIZONTAL,
                                   variable=self.contrast)
        contrast_scale.grid(row=row, column=1, padx=5, pady=5, sticky="ew")
        row += 1

        saturation_label = tk.Label(settings_frame, text="Насыщенность:")
        saturation_label.grid(row=row, column=0, sticky="w", padx=5, pady=5)
        saturation_scale = tk.Scale(settings_frame, from_=0.1, to=3.0, resolution=0.1, orient=tk.HORIZONTAL,
                                   variable=self.saturation)
        saturation_scale.grid(row=row, column=1, padx=5, pady=5, sticky="ew")
        row += 1

        filter_label = tk.Label(settings_frame, text="Фильтры:")
        filter_label.grid(row=row, column=0, sticky="w", padx=5, pady=5)
        filter_options = ["Нет", "Черно-белый", "Сепия", "Размытие"]
        self.selected_filter = tk.StringVar(value="Нет")
        filter_dropdown = tk.OptionMenu(settings_frame, self.selected_filter, *filter_options)
        filter_dropdown.grid(row=row, column=1, padx=5, pady=5, sticky="ew")
        row += 1

        settings_frame.columnconfigure(1, weight=1)

        button_frame = tk.Frame(editor_window)
        button_frame.pack(pady=10, fill=tk.X)

        apply_button = tk.Button(button_frame, text="Применить", command=self.apply_image_changes)
        apply_button.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

        reset_button = tk.Button(button_frame, text="Сбросить", command=self.reset_image)
        reset_button.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(1, weight=1)

        editor_window.columnconfigure(0, weight=1)
        editor_window.rowconfigure(0, weight=1)

    def apply_image_changes(self):
        if not self.image_path:
            return

        try:
            img = self.original_image.copy()

            enhancer = ImageEnhance.Brightness(img)
            img = enhancer.enhance(self.brightness.get())

            enhancer = ImageEnhance.Contrast(img)
            img = enhancer.enhance(self.contrast.get())

            enhancer = ImageEnhance.Color(img)
            img = enhancer.enhance(self.saturation.get())

            selected_filter = self.selected_filter.get()
            if selected_filter == "Черно-белый":
                img = img.convert("L")
            elif selected_filter == "Сепия":
                img = self.apply_sepia(img)
            elif selected_filter == "Размытие":
                img = img.filter(ImageFilter.BLUR)

            self.temp_image = img
            self.modified_image = img

            messagebox.showinfo("Успех", "Изменения применены!")
            self.update_preview()

        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при изменении изображения: {e}")

    def reset_image(self):
        if not self.image_path:
            return

        self.brightness.set(1.0)
        self.contrast.set(1.0)
        self.saturation.set(1.0)
        self.selected_filter.set("Нет")

        self.modified_image = self.original_image.copy()
        self.temp_image = self.original_image.copy()
        self.update_preview()

    def apply_sepia(self, img):
        sepia_depth = 20
        sepia_intensity = 0.5
        width, height = img.size
        sepia = Image.new('RGB', (width, height), (0, 0, 0))
        draw = ImageDraw.Draw(sepia)

        for x in range(width):
            for y in range(height):
                r, g, b = img.getpixel((x, y))

                gray = int(0.299 * r + 0.587 * g + 0.114 * b)

                new_r = int(gray + sepia_depth * 2)
                new_g = int(gray + sepia_depth)
                new_b = gray

                new_r = min(255, int(new_r * sepia_intensity))
                new_g = min(255, int(new_g * sepia_intensity))
                new_b = min(255, int(new_b * sepia_intensity))

                draw.point((x, y), (new_r, new_g, new_b))

        return sepia

    def open_settings_window(self):
        settings_window = tk.Toplevel(self.master)
        settings_window.title("Настройки текста")

        notebook = ttk.Notebook(settings_window)
        notebook.pack(expand=True, fill="both", padx=10, pady=10)

        top_text_tab = tk.Frame(notebook)
        bottom_text_tab = tk.Frame(notebook)
        notebook.add(top_text_tab, text="Верхний текст")
        notebook.add(bottom_text_tab, text="Нижний текст")

        self.create_text_settings_tab(top_text_tab, "top")
        self.create_text_settings_tab(bottom_text_tab, "bottom")

        apply_button = tk.Button(settings_window, text="Применить", command=self.apply_settings)
        apply_button.pack(pady=10)

    def create_text_settings_tab(self, tab, text_position):
        settings_frame = tk.Frame(tab)
        settings_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        row = 0

        tk.Label(settings_frame, text="Размер шрифта:").grid(row=row, column=0, sticky="w", padx=5, pady=5)
        self.font_size_entry = tk.Entry(settings_frame)
        self.font_size_entry.insert(0, str(self.font_size))
        self.font_size_entry.grid(row=row, column=1, padx=5, pady=5, sticky="ew")
        settings_frame.columnconfigure(1, weight=1)
        row += 1

        color_label = tk.Label(settings_frame, text="Цвет текста:")
        color_label.grid(row=row, column=0, sticky="w", padx=5, pady=5)
        color_button = tk.Button(settings_frame, text="Выбрать цвет", command=lambda pos=text_position: self.choose_color(pos))
        color_button.grid(row=row, column=1, padx=5, pady=5, sticky="ew")
        row += 1

        italic_check = tk.Checkbutton(settings_frame, text="Курсив", variable=getattr(self, f"{text_position}_text_italic"))
        italic_check.grid(row=row, column=0, sticky="w", padx=5, pady=5)
        bold_check = tk.Checkbutton(settings_frame, text="Полужирный", variable=getattr(self, f"{text_position}_text_bold"))
        bold_check.grid(row=row, column=1, sticky="w", padx=5, pady=5)
        row += 1

        letter_spacing_label = tk.Label(settings_frame, text="Интервал между буквами:")
        letter_spacing_label.grid(row=row, column=0, sticky="w", padx=5, pady=5)
        letter_spacing_scale = tk.Scale(settings_frame, from_=-5, to=10, orient=tk.HORIZONTAL,
                                       variable=getattr(self, f"{text_position}_letter_spacing"))
        letter_spacing_scale.grid(row=row, column=1, padx=5, pady=5, sticky="ew")
        row += 1

        line_spacing_label = tk.Label(settings_frame, text="Интервал между строками:")
        line_spacing_label.grid(row=row, column=0, sticky="w", padx=5, pady=5)
        line_spacing_scale = tk.Scale(settings_frame, from_=0.5, to=2.0, resolution=0.1, orient=tk.HORIZONTAL,
                                     variable=getattr(self, f"{text_position}_line_spacing"))
        line_spacing_scale.grid(row=row, column=1, padx=5, pady=5, sticky="ew")
        row += 1

        stroke_color_label = tk.Label(settings_frame, text="Цвет обводки:")
        stroke_color_label.grid(row=row, column=0, sticky="w", padx=5, pady=5)
        stroke_color_button = tk.Button(settings_frame, text="Выбрать цвет обводки", command=lambda pos=text_position: self.choose_stroke_color(pos))
        stroke_color_button.grid(row=row, column=1, padx=5, pady=5, sticky="ew")
        row += 1

        stroke_width_label = tk.Label(settings_frame, text="Толщина обводки:")
        stroke_width_label.grid(row=row, column=0, sticky="w", padx=5, pady=5)
        stroke_width_scale = tk.Scale(settings_frame, from_=0, to=10, orient=tk.HORIZONTAL,
                                       variable=getattr(self, f"{text_position}_stroke_width"))
        stroke_width_scale.grid(row=row, column=1, padx=5, pady=5, sticky="ew")
        row += 1

        shadow_color_label = tk.Label(settings_frame, text="Цвет тени:")
        shadow_color_label.grid(row=row, column=0, sticky="w", padx=5, pady=5)
        shadow_color_button = tk.Button(settings_frame, text="Выбрать цвет тени", command=lambda pos=text_position: self.choose_shadow_color(pos))
        shadow_color_button.grid(row=row, column=1, padx=5, pady=5, sticky="ew")
        row += 1

        shadow_offset_x_label = tk.Label(settings_frame, text="Смещение тени X:")
        shadow_offset_x_label.grid(row=row, column=0, sticky="w", padx=5, pady=5)
        shadow_offset_x_scale = tk.Scale(settings_frame, from_=-10, to=10, orient=tk.HORIZONTAL,
                                          variable=getattr(self, f"{text_position}_shadow_offset_x"))
        shadow_offset_x_scale.grid(row=row, column=1, padx=5, pady=5, sticky="ew")
        row += 1

        shadow_offset_y_label = tk.Label(settings_frame, text="Смещение тени Y:")
        shadow_offset_y_label.grid(row=row, column=0, sticky="w", padx=5, pady=5)
        shadow_offset_y_scale = tk.Scale(settings_frame, from_=-10, to=10, orient=tk.HORIZONTAL,
                                          variable=getattr(self, f"{text_position}_shadow_offset_y"))
        shadow_offset_y_scale.grid(row=row, column=1, padx=5, pady=5, sticky="ew")
        row += 1

        position_label = tk.Label(settings_frame, text="Положение текста:")
        position_label.grid(row=row, column=0, sticky="w", padx=5, pady=5)

        position_options = {
            "Сверху слева": "сверху_слева",
            "Сверху по центру": "сверху_по_центру",
            "Сверху справа": "сверху_справа",
            "Посередине слева": "посередине_слева",
            "Посередине по центру": "посередине_по_центру",
            "Посередине справа": "посередине_справа",
            "Снизу слева": "снизу_слева",
            "Снизу по центру": "снизу_по_центру",
            "Снизу справа": "снизу_справа"
        }

        position_dropdown = tk.OptionMenu(settings_frame, getattr(self, f"{text_position}_text_position"), *position_options.values())
        position_dropdown.grid(row=row, column=1, padx=5, pady=5, sticky="ew")
        row += 1

        for i in range(2):
            settings_frame.columnconfigure(i, weight=1)

    def choose_color(self, text_position):
        color_code = colorchooser.askcolor(title=f"Выберите цвет для {text_position} текста")
        if color_code[1]:
            if text_position == "top":
                self.top_text_color = color_code[1]
            else:
                self.bottom_text_color = color_code[1]

    def choose_stroke_color(self, text_position):
        color_code = colorchooser.askcolor(title=f"Выберите цвет обводки для {text_position} текста")
        if color_code[1]:
            if text_position == "top":
                self.top_stroke_color = color_code[1]
            else:
                self.bottom_stroke_color = color_code[1]

    def choose_shadow_color(self, text_position):
        color_code = colorchooser.askcolor(title=f"Выберите цвет тени для {text_position} текста")
        if color_code[1]:
            if text_position == "top":
                self.top_shadow_color = color_code[1]
            else:
                self.bottom_shadow_color = color_code[1]

    def apply_settings(self):
        try:
            self.font_size = int(self.font_size_entry.get())
        except ValueError:
            messagebox.showerror("Ошибка", "Некорректный размер шрифта. Введите целое число.")
            return
        messagebox.showinfo("Успех", "Настройки применены!")
        self.update_preview()

    def select_image(self):
        self.image_path = filedialog.askopenfilename(
            initialdir=".",
            title="Выберите изображение",
            filetypes=(("JPEG files", "*.jpg"), ("PNG files", "*.png"), ("All files", "*.*"))
        )
        if self.image_path:
            self.original_image = Image.open(self.image_path)
            self.temp_image = self.original_image.copy()
            self.modified_image = self.original_image.copy()
            self.update_preview()

    def draw_shadow(self, draw, x, y, text, font, fill, stroke_width, stroke_fill, offset_x, offset_y):
        draw.text((x + offset_x, y + offset_y), text, font=font, fill=fill, stroke_width=stroke_width, stroke_fill=stroke_fill)

    def draw_outlined_text(self, draw, x, y, text, font, fill, stroke_width, stroke_fill):
        draw.text((x - stroke_width, y - stroke_width), text, font=font, fill=stroke_fill)
        draw.text((x + stroke_width, y - stroke_width), text, font=font, fill=stroke_fill)
        draw.text((x - stroke_width, y + stroke_width), text, font=font, fill=stroke_fill)
        draw.text((x + stroke_width, y + stroke_width), text, font=font, fill=stroke_fill)

        draw.text((x, y), text, font=font, fill=fill)


    def save_meme(self):
        if not self.image_path:
            messagebox.showerror("Ошибка", "Сначала выберите изображение!")
            return

        try:
            img = self.modified_image if self.modified_image else self.original_image

            draw = ImageDraw.Draw(img)

            font_style = ""
            if self.top_text_italic.get() or self.bottom_text_italic.get():
                font_style += "italic"
            if self.top_text_bold.get() or self.bottom_text_bold.get():
                font_style += "bold"

            try:
                font_path = "arial.ttf"
                font = ImageFont.truetype(font_path, self.font_size)
            except IOError:
                messagebox.showerror("Ошибка", "Не найден шрифт arial.ttf. Укажите путь к шрифту в коде.")
                return

            width, height = img.size

            def calculate_text_position(text, font, position, image_width, image_height, letter_spacing):
                bbox = draw.textbbox((0, 0), text, font=font)
                text_width = bbox[2] - bbox[0]
                text_height = bbox[3] - bbox[1]

                words = text.split()
                total_text_width = 0
                for word in words:
                    word_bbox = draw.textbbox((0, 0), word, font=font)
                    total_text_width += word_bbox[2] - word_bbox[0]
                    if word != words[-1]:
                        total_text_width += letter_spacing

                x, y = 0, 0

                if "сверху" in position:
                    y = 10
                elif "посередине" in position:
                    y = (image_height - text_height) / 2
                elif "снизу" in position:
                    y = image_height - text_height - 10

                if "слева" in position:
                    x = 10
                elif "по_центру" in position:
                    x = (image_width - total_text_width) / 2
                elif "справа" in position:
                    x = image_width - total_text_width - 10

                return x, y

            top_text = self.top_text.get().upper()
            top_letter_spacing = self.top_letter_spacing.get()
            top_x, top_y = calculate_text_position(top_text, font, self.top_text_position.get(), width, height, top_letter_spacing)

            x = top_x
            y = top_y
            for letter in list(top_text):
                bbox = draw.textbbox((0, 0), letter, font=font)
                text_width = bbox[2] - bbox[0]
                text_height = bbox[3] - bbox[1]

                self.draw_shadow(draw, x, y, letter, font, self.top_shadow_color, self.top_stroke_width, self.top_stroke_color, self.top_shadow_offset_x, self.top_shadow_offset_y)

                self.draw_outlined_text(draw, x, y, letter, font, self.top_text_color, self.top_stroke_width, self.top_stroke_color)

                x += text_width + top_letter_spacing

            bottom_text = self.bottom_text.get().upper()
            bottom_letter_spacing = self.bottom_letter_spacing.get()
            bottom_x, bottom_y = calculate_text_position(bottom_text, font, self.bottom_text_position.get(), width, height, bottom_letter_spacing)

            x = bottom_x
            y = bottom_y
            for letter in list(bottom_text):
                bbox = draw.textbbox((0, 0), letter, font=font)
                text_width = bbox[2] - bbox[0]
                text_height = bbox[3] - bbox[1]

                self.draw_shadow(draw, x, y, letter, font, self.bottom_shadow_color, self.bottom_stroke_width, self.bottom_stroke_color, self.bottom_shadow_offset_x, self.bottom_shadow_offset_y)

                self.draw_outlined_text(draw, x, y, letter, font, self.bottom_text_color, self.bottom_stroke_width, self.bottom_stroke_color)

                x += text_width + bottom_letter_spacing

            save_path = filedialog.asksaveasfilename(
                initialdir=".",
                title="Сохранить мем",
                defaultextension=".jpg",
                filetypes=(("JPEG files", "*.jpg"), ("All files", "*.*"))
            )

            if save_path:
                img.save(save_path)
                messagebox.showinfo("Успех", "Мем сохранен!")

        except Exception as e:
            messagebox.showerror("Ошибка", f"Произошла ошибка: {e}")

    def update_preview(self):
        if not self.image_path:
            return

        try:
            img = self.modified_image if self.modified_image else self.original_image

            draw = ImageDraw.Draw(img)

            font_style = ""
            if self.top_text_italic.get() or self.bottom_text_italic.get():
                font_style += "italic"
            if self.top_text_bold.get() or self.bottom_text_bold.get():
                font_style += "bold"

            try:
                font_path = "arial.ttf"
                font = ImageFont.truetype(font_path, self.font_size)
            except IOError:
                messagebox.showerror("Ошибка", "Не найден шрифт arial.ttf. Укажите путь к шрифту в коде.")
                return

            width, height = img.size

            def calculate_text_position(text, font, position, image_width, image_height, letter_spacing):
                bbox = draw.textbbox((0, 0), text, font=font)
                text_width = bbox[2] - bbox[0]
                text_height = bbox[3] - bbox[1]

                words = text.split()
                total_text_width = 0
                for word in words:
                    word_bbox = draw.textbbox((0, 0), word, font=font)
                    total_text_width += word_bbox[2] - word_bbox[0]
                    if word != words[-1]:
                        total_text_width += letter_spacing

                x, y = 0, 0

                if "сверху" in position:
                    y = 10
                elif "посередине" in position:
                    y = (image_height - text_height) / 2
                elif "снизу" in position:
                    y = image_height - text_height - 10

                if "слева" in position:
                    x = 10
                elif "по_центру" in position:
                    x = (image_width - total_text_width) / 2
                elif "справа" in position:
                    x = image_width - total_text_width - 10

                return x, y

            top_text = self.top_text.get().upper()
            top_letter_spacing = self.top_letter_spacing.get()
            top_x, top_y = calculate_text_position(top_text, font, self.top_text_position.get(), width, height, top_letter_spacing)

            x = top_x
            y = top_y
            for letter in list(top_text):
                bbox = draw.textbbox((0, 0), letter, font=font)
                text_width = bbox[2] - bbox[0]
                text_height = bbox[3] - bbox[1]

                self.draw_shadow(draw, x, y, letter, font, self.top_shadow_color, self.top_stroke_width, self.top_stroke_color, self.top_shadow_offset_x, self.top_shadow_offset_y)

                self.draw_outlined_text(draw, x, y, letter, font, self.top_text_color, self.top_stroke_width, self.top_stroke_color)

                x += text_width + top_letter_spacing

            bottom_text = self.bottom_text.get().upper()
            bottom_letter_spacing = self.bottom_letter_spacing.get()
            bottom_x, bottom_y = calculate_text_position(bottom_text, font, self.bottom_text_position.get(), width, height, bottom_letter_spacing)

            x = bottom_x
            y = bottom_y
            for letter in list(bottom_text):
                bbox = draw.textbbox((0, 0), letter, font=font)
                text_width = bbox[2] - bbox[0]
                text_height = bbox[3] - bbox[1]

                self.draw_shadow(draw, x, y, letter, font, self.bottom_shadow_color, self.bottom_stroke_width, self.bottom_stroke_color, self.bottom_shadow_offset_x, self.bottom_shadow_offset_y)

                self.draw_outlined_text(draw, x, y, letter, font, self.bottom_text_color, self.bottom_stroke_width, self.bottom_stroke_color)

                x += text_width + bottom_letter_spacing

            max_size = (500, 500)
            img.thumbnail(max_size)

            self.photo = ImageTk.PhotoImage(img)
            self.preview_image_label.config(image=self.photo)
            self.preview_image_label.image = self.photo

        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка предпросмотра: {e}")


root = tk.Tk()
app = MemeGeneratorApp(root)
root.mainloop()