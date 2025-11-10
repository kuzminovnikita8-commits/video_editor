import tkinter as tk
from tkinter import filedialog, messagebox
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip

class MiniEditor:
    def __init__(self, root):
        self.root = root
        root.title("Mini Video Editor")
        self.src = None
        self.clip = None

        tk.Button(root, text="Open Video", command=self.open_video).pack(fill='x')
        frame = tk.Frame(root); frame.pack(fill='x')
        tk.Label(frame, text="Start (s)").grid(row=0,column=0)
        tk.Label(frame, text="End (s)").grid(row=0,column=2)
        self.start_var = tk.StringVar(value="0")
        self.end_var = tk.StringVar(value="10")
        tk.Entry(frame, textvariable=self.start_var, width=8).grid(row=0,column=1)
        tk.Entry(frame, textvariable=self.end_var, width=8).grid(row=0,column=3)

        tk.Label(root, text="Overlay text:").pack(anchor='w')
        self.text_var = tk.StringVar()
        tk.Entry(root, textvariable=self.text_var).pack(fill='x')

        tk.Button(root, text="Preview (play external)", command=self.preview).pack(fill='x')
        tk.Button(root, text="Export", command=self.export).pack(fill='x')

    def open_video(self):
        path = filedialog.askopenfilename(filetypes=[("Video files","*.mp4;*.mov;*.mkv;*.avi")])
        if not path: return
        self.src = path
        try:
            self.clip = VideoFileClip(path)
            messagebox.showinfo("Loaded", f"Loaded: {path}\nDuration: {self.clip.duration:.2f}s")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load video: {e}")

    def preview(self):
        if not self.clip:
            messagebox.showwarning("No video", "Open a video first")
            return
        try:
            start = float(self.start_var.get())
            end = float(self.end_var.get())
        except:
            messagebox.showerror("Error", "Invalid start/end")
            return
        sub = self.clip.subclip(max(0,start), min(self.clip.duration, end))
        txt = self.text_var.get().strip()
        if txt:
            txtc = TextClip(txt, fontsize=48, color='white').set_pos(('center','bottom')).set_duration(sub.duration)
            comp = CompositeVideoClip([sub, txtc])
        else:
            comp = sub
        # preview by writing a temporary file and using default player
        tmp = "preview_temp.mp4"
        comp.write_videofile(tmp, codec='libx264', audio_codec='aac', threads=2, verbose=False, logger=None)
        import webbrowser, os
        webbrowser.open('file://' + os.path.abspath(tmp))

    def export(self):
        if not self.clip:
            messagebox.showwarning("No video", "Open a video first")
            return
        out = filedialog.asksaveasfilename(defaultextension=".mp4", filetypes=[("MP4","*.mp4")])
        if not out: return
        try:
            start = float(self.start_var.get())
            end = float(self.end_var.get())
        except:
            messagebox.showerror("Error", "Invalid start/end"); return
        sub = self.clip.subclip(max(0,start), min(self.clip.duration, end))
        txt = self.text_var.get().strip()
        if txt:
            txtc = TextClip(txt, fontsize=48, color='white', stroke_color='black', stroke_width=2).set_pos(('center','bottom')).set_duration(sub.duration)
            comp = CompositeVideoClip([sub, txtc])
        else:
            comp = sub
        comp.write_videofile(out, codec='libx264', audio_codec='aac')
        messagebox.showinfo("Done", f"Exported to {out}")

if __name__ == "__main__":
    root = tk.Tk()
    app = MiniEditor(root)
    root.mainloop()
