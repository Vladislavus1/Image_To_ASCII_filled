from imports import *


def run_app():
    root = ctk.CTk()
    root.title("Image to ASCII")
    root.iconbitmap("root_icon.ico")
    root.geometry("600x300")
    root.resizable(False, False)

    title_label = ctk.CTkLabel(master=root, text="Image to ASCII text format.", font=("System", 30))
    title_label.place(relx=0.5, rely=0.1, anchor=ctk.CENTER)

    def convert_file(master):
        nonlocal success_label
        if success_label:
            success_label.destroy()

        file_path = filedialog.askopenfilename(filetypes=[('JPG Files', '*.jpg'),
                                                          ('PNG Files', '*.png')])
        if file_path:
            photo_name = file_path.split("/")[-1]
            photo = cv2.imread(file_path)
            gray_photo = cv2.cvtColor(photo, cv2.COLOR_BGR2GRAY)
            cv2.imwrite("GRAY_" + photo_name, gray_photo)
            img = Image.open("GRAY_" + photo_name).convert('L')
            os.remove("GRAY_" + photo_name)
            WIDTH, HEIGHT = img.size

            data = list(img.getdata())
            data = [data[offset:offset + WIDTH] for offset in range(0, WIDTH * HEIGHT, WIDTH)]
            with open(photo_name + ".txt", "w", encoding="utf-8") as file:
                for binary_line in data:
                    file.write(''.join([
                        "█" if 0 <= pixel < 62 else "▓" if 62 < pixel < 124 else "▒" if 124 < pixel < 186 else "░" if 186 < pixel < 255 else " " if pixel == 255 else " "
                        for pixel in binary_line]) + "\n")

            success_label = ctk.CTkLabel(master=root, text_color='white', fg_color='dark green',
                                         text=f'ASCII content of your image\nis successfully loaded to\n"{photo_name}.txt"',
                                         font=("System", 1),
                                         corner_radius=15)

            success_label.place(relx=0.5, rely=0.9, anchor=ctk.CENTER)

            def hide_label(event):
                success_label.place_forget()

            success_label.bind("<Button-1>", hide_label)

    get_file_path_button = ctk.CTkButton(master=root,
                                         text="Convert Image",
                                         font=("System", 25),
                                         fg_color="green",
                                         hover_color="dark green",
                                         corner_radius=15,
                                         command=lambda: convert_file(root))
    get_file_path_button.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

    success_label = None

    root.mainloop()


if __name__ == "__main__":
    run_app()
