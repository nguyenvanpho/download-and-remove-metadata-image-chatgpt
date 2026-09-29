"""
PDZ - Download or Remove Metadata Image ChatGPT
- Tab 1: Download ảnh hàng loạt từ URL + xoá metadata
- Tab 2: Xoá metadata ảnh có sẵn trên máy
Yêu cầu: Python 3.9+, Pillow (pip install pillow)
"""
import os
import re
import sys
import threading
import urllib.request
import urllib.parse
import multiprocessing as mp
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor, as_completed

import tkinter as tk
from tkinter import ttk, filedialog, messagebox

from PIL import Image

APP_NAME = "PDZ - Download or Remove Metadata Image ChatGPT"
APP_SUB = "Download or Remove Metadata Image ChatGPT"
LOGO_PNG_B64 = "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"
ICON_PNG_B64 = "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"
EXTS = {".png", ".jpg", ".jpeg", ".webp", ".bmp", ".tif", ".tiff", ".gif"}
URL_RE = re.compile(
    r"https://[^\s\"'<>,]+?\.(?:png|jpe?g|webp|bmp|tiff?|gif)(?:\?[^\s\"'<>,]*)?(?=$|[\s\"'<>,])",
    re.IGNORECASE,
)
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0 Safari/537.36")


# ============================================================ xử lý ảnh
def unique_path(folder: Path, stem: str, ext: str) -> Path:
    p = folder / f"{stem}{ext}"
    n = 1
    while p.exists():
        p = folder / f"{stem}_{n}{ext}"
        n += 1
    return p


def clean_image(src, out_dir, stem, opts):
    """Mở ảnh -> dựng lại chỉ từ pixel -> lưu (không còn EXIF/XMP/IPTC/C2PA...)."""
    fmt, quality, max_size, keep_icc, bg_hex = opts
    src = Path(src)
    with Image.open(src) as im:
        im.load()
        src_fmt = (im.format or "").upper()
        if fmt == "GIỮ NGUYÊN":
            fmt = {"JPEG": "JPG", "WEBP": "WEBP"}.get(src_fmt, "PNG")
        ext = {"JPG": ".jpg", "WEBP": ".webp", "PNG": ".png"}[fmt]

        icc = im.info.get("icc_profile") if keep_icc else None
        has_alpha = "A" in im.getbands() or (im.mode == "P" and "transparency" in im.info)
        if fmt == "JPG":
            if has_alpha:
                rgba = im.convert("RGBA")
                bg = Image.new("RGB", rgba.size, tuple(int(bg_hex[i:i + 2], 16) for i in (1, 3, 5)))
                bg.paste(rgba, mask=rgba.split()[3])
                im = bg
            else:
                im = im.convert("RGB")
        elif im.mode not in ("RGB", "RGBA", "L", "LA"):
            im = im.convert("RGBA" if has_alpha else "RGB")

        if max_size and max(im.size) > max_size:
            im = im.copy()
            im.thumbnail((max_size, max_size), Image.LANCZOS)

        clean = Image.frombytes(im.mode, im.size, im.tobytes())

    dst = unique_path(Path(out_dir), stem, ext)
    kw = {"icc_profile": icc} if icc else {}
    if fmt == "JPG":
        clean.save(dst, "JPEG", quality=quality, optimize=True, progressive=True,
                   subsampling=0 if quality >= 90 else 2, **kw)
    elif fmt == "WEBP":
        clean.save(dst, "WEBP", quality=quality, method=6, **kw)
    else:
        clean.save(dst, "PNG", optimize=True, **kw)
    return dst


def job_local(src, out_dir, opts):
    """Chạy trong process riêng."""
    src = Path(src)
    try:
        dst = clean_image(src, out_dir, src.stem, opts)
        return True, src.name, src.stat().st_size, dst.stat().st_size, dst.name
    except Exception as e:
        return False, str(src), f"Lỗi xoá metadata: {e}", 0, ""


def job_url(url, out_dir, opts, tmp_dir):
    """Chạy trong thread: tải -> xoá metadata -> xoá file tạm."""
    name = Path(urllib.parse.unquote(urllib.parse.urlparse(url).path)).stem or "image"
    name = re.sub(r'[\\/:*?"<>|]+', "_", name)[:120]
    tmp = unique_path(Path(tmp_dir), name, ".part")
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "image/*,*/*"})
        with urllib.request.urlopen(req, timeout=60) as r, open(tmp, "wb") as f:
            while True:
                chunk = r.read(1 << 16)
                if not chunk:
                    break
                f.write(chunk)
    except Exception as e:
        tmp.unlink(missing_ok=True)
        return False, url, f"Lỗi download: {e}", 0, ""
    try:
        size = tmp.stat().st_size
        dst = clean_image(tmp, out_dir, name, opts)
        return True, url, size, dst.stat().st_size, dst.name
    except Exception as e:
        return False, url, f"Lỗi xoá metadata (file tải về có thể không phải ảnh): {e}", 0, ""
    finally:
        tmp.unlink(missing_ok=True)


def hsize(n):
    return f"{n/1e6:.1f} MB" if n >= 1e6 else f"{n/1024:.0f} KB"


# ============================================================ giao diện
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(APP_NAME)
        self.geometry("820x740")
        self.minsize(720, 600)
        self.files = []
        self.running = False
        pad = {"padx": 8, "pady": 4}

        # ---------- Header: logo PdzTools
        try:
            self._icon = tk.PhotoImage(data=ICON_PNG_B64)
            self.iconphoto(True, self._icon)
        except tk.TclError:
            pass
        hdr = ttk.Frame(self)
        hdr.pack(fill="x", padx=10, pady=(10, 2))
        try:
            self._logo = tk.PhotoImage(data=LOGO_PNG_B64)
            ttk.Label(hdr, image=self._logo).pack(side="left")
        except tk.TclError:
            ttk.Label(hdr, text="PdzTools", font=("Segoe UI", 18, "bold"), foreground="#e8641e").pack(side="left")
        ttk.Label(hdr, text=APP_SUB, font=("Segoe UI", 11, "bold"), foreground="#555")            .pack(side="left", padx=12, pady=(10, 0))
        ttk.Separator(self).pack(fill="x", padx=10, pady=(6, 0))

        self.nb = ttk.Notebook(self)
        self.nb.pack(fill="both", expand=False, **pad)

        # ---------- Tab 1: URL
        t1 = ttk.Frame(self.nb)
        self.nb.add(t1, text="  Download từ URL  ")
        ttk.Label(t1, text="Dán URL ảnh (https://…png/jpg/webp…), một hoặc nhiều dòng, cách nhau bởi dấu cách/dấu phẩy đều được:")\
            .pack(anchor="w", **pad)
        box = ttk.Frame(t1)
        box.pack(fill="both", expand=True, **pad)
        self.url_txt = tk.Text(box, height=9, wrap="word", font=("Consolas", 9))
        sb = ttk.Scrollbar(box, command=self.url_txt.yview)
        self.url_txt.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")
        self.url_txt.pack(fill="both", expand=True)
        self.url_txt.bind("<KeyRelease>", lambda e: self.count_urls())
        self.url_txt.bind("<<Paste>>", lambda e: self.after(50, self.count_urls))
        r = ttk.Frame(t1)
        r.pack(fill="x", **pad)
        self.url_count = ttk.Label(r, text="0 URL hợp lệ")
        self.url_count.pack(side="left")
        ttk.Button(r, text="Xoá nội dung", command=lambda: (self.url_txt.delete("1.0", "end"), self.count_urls()))\
            .pack(side="right")
        f = ttk.Frame(t1)
        f.pack(fill="x", **pad)
        ttk.Label(f, text="Lưu vào:").pack(side="left")
        self.url_out = tk.StringVar()
        ttk.Entry(f, textvariable=self.url_out).pack(side="left", fill="x", expand=True, padx=6)
        ttk.Button(f, text="Chọn folder…", command=lambda: self.pick_dir(self.url_out)).pack(side="left")

        # ---------- Tab 2: Local
        t2 = ttk.Frame(self.nb)
        self.nb.add(t2, text="  Xoá metadata ảnh trên máy  ")
        self.src_dir = ""
        f = ttk.Frame(t2)
        f.pack(fill="x", **pad)
        ttk.Label(f, text="Nguồn ảnh:", font=("Segoe UI", 9, "bold")).pack(side="left")
        self.src_mode = tk.StringVar(value="folder")
        ttk.Radiobutton(f, text="Cả thư mục", value="folder", variable=self.src_mode,
                        command=self.on_mode).pack(side="left", padx=(10, 4))
        ttk.Radiobutton(f, text="Chọn từng file", value="files", variable=self.src_mode,
                        command=self.on_mode).pack(side="left", padx=4)
        f = ttk.Frame(t2)
        f.pack(fill="x", **pad)
        self.src_disp = tk.StringVar()
        ttk.Entry(f, textvariable=self.src_disp, state="readonly").pack(side="left", fill="x", expand=True)
        self.src_btn = ttk.Button(f, text="Chọn thư mục…", command=self.pick_source, width=16)
        self.src_btn.pack(side="left", padx=(6, 0))
        f = ttk.Frame(t2)
        f.pack(fill="x", **pad)
        self.sub_var = tk.BooleanVar(value=True)
        self.sub_chk = ttk.Checkbutton(f, text="Gồm cả ảnh trong thư mục con", variable=self.sub_var,
                                       command=self.rescan)
        self.sub_chk.pack(side="left")
        self.src_lbl = ttk.Label(f, text="Chưa chọn ảnh", foreground="#666")
        self.src_lbl.pack(side="right")
        ttk.Separator(t2).pack(fill="x", padx=8, pady=4)
        f = ttk.Frame(t2)
        f.pack(fill="x", **pad)
        ttk.Label(f, text="Lưu vào:").pack(side="left")
        self.loc_out = tk.StringVar()
        ttk.Entry(f, textvariable=self.loc_out).pack(side="left", fill="x", expand=True, padx=6)
        ttk.Button(f, text="Chọn folder…", command=lambda: self.pick_dir(self.loc_out)).pack(side="left")

        # ---------- Tuỳ chọn chung
        f3 = ttk.LabelFrame(self, text="Tuỳ chọn xuất (metadata luôn được xoá)")
        f3.pack(fill="x", **pad)
        ttk.Label(f3, text="Định dạng:").grid(row=0, column=0, sticky="w", **pad)
        self.fmt_var = tk.StringVar(value="JPG")
        cb = ttk.Combobox(f3, textvariable=self.fmt_var, values=["JPG", "WEBP", "PNG", "GIỮ NGUYÊN"],
                          state="readonly", width=12)
        cb.grid(row=0, column=1, sticky="w", **pad)
        ttk.Label(f3, text="Chất lượng:").grid(row=0, column=2, sticky="e", **pad)
        self.q_var = tk.IntVar(value=85)
        ttk.Scale(f3, from_=40, to=100, variable=self.q_var, length=150,
                  command=lambda v: self.q_lbl.config(text=str(int(float(v))))).grid(row=0, column=3, sticky="w", **pad)
        self.q_lbl = ttk.Label(f3, text="85", width=4)
        self.q_lbl.grid(row=0, column=4, sticky="w")

        ttk.Label(f3, text="Cạnh dài tối đa (px, 0 = giữ):").grid(row=1, column=0, sticky="w", **pad)
        self.max_var = tk.IntVar(value=0)
        ttk.Spinbox(f3, from_=0, to=10000, increment=100, textvariable=self.max_var, width=10)\
            .grid(row=1, column=1, sticky="w", **pad)
        ttk.Label(f3, text="Nền ảnh trong suốt (JPG):").grid(row=1, column=2, sticky="e", **pad)
        self.bg_var = tk.StringVar(value="#FFFFFF")
        ttk.Entry(f3, textvariable=self.bg_var, width=10).grid(row=1, column=3, sticky="w", **pad)
        self.icc_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(f3, text="Giữ ICC profile (màu chuẩn)", variable=self.icc_var)\
            .grid(row=2, column=0, columnspan=2, sticky="w", **pad)
        ttk.Label(f3, text="Gợi ý: JPG 80–85 cho ảnh sản phẩm · WebP nhẹ nhất",
                  foreground="#666").grid(row=2, column=2, columnspan=3, sticky="w", **pad)

        # ---------- Chạy
        f4 = ttk.Frame(self)
        f4.pack(fill="x", **pad)
        self.run_btn = ttk.Button(f4, text="▶  Bắt đầu", command=self.start)
        self.run_btn.pack(side="left")
        ttk.Button(f4, text="Mở folder lưu", command=self.open_out).pack(side="left", padx=6)
        self.prog = ttk.Progressbar(f4, mode="determinate")
        self.prog.pack(side="left", fill="x", expand=True, padx=6)
        self.stat_lbl = ttk.Label(f4, text="")
        self.stat_lbl.pack(side="left")

        f5 = ttk.LabelFrame(self, text="Nhật ký")
        f5.pack(fill="both", expand=True, **pad)
        self.log = tk.Text(f5, height=10, wrap="none", font=("Consolas", 9))
        sb = ttk.Scrollbar(f5, command=self.log.yview)
        self.log.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")
        self.log.pack(fill="both", expand=True)
        self.log.tag_config("err", foreground="#c0392b")

    # ---------------- helpers
    def parse_urls(self):
        text = self.url_txt.get("1.0", "end")
        seen, out = set(), []
        for m in URL_RE.finditer(text):
            u = m.group(0)
            if u not in seen:
                seen.add(u)
                out.append(u)
        return out

    def count_urls(self):
        self.url_count.config(text=f"{len(self.parse_urls())} URL hợp lệ")

    def pick_dir(self, var):
        d = filedialog.askdirectory()
        if d:
            var.set(d)

    def set_files(self, files):
        self.files = sorted(set(files))
        if self.files:
            self.src_lbl.config(text=f"Tìm thấy {len(self.files)} ảnh", foreground="#1e7e34")
        else:
            self.src_lbl.config(text="Không có ảnh nào" if self.src_disp.get() else "Chưa chọn ảnh",
                                foreground="#c0392b" if self.src_disp.get() else "#666")

    def on_mode(self):
        """Đổi chế độ nguồn -> reset lựa chọn cũ để tránh nhầm."""
        folder = self.src_mode.get() == "folder"
        self.src_btn.config(text="Chọn thư mục…" if folder else "Chọn file ảnh…")
        self.sub_chk.state(["!disabled"] if folder else ["disabled"])
        self.src_dir = ""
        self.src_disp.set("")
        self.set_files([])

    def pick_source(self):
        if self.src_mode.get() == "folder":
            d = filedialog.askdirectory(title="Chọn thư mục chứa ảnh")
            if d:
                self.src_dir = d
                self.src_disp.set(d)
                self.rescan()
        else:
            fs = filedialog.askopenfilenames(title="Chọn file ảnh (giữ Ctrl để chọn nhiều)",
                                             filetypes=[("Ảnh", " ".join("*" + e for e in sorted(EXTS)))])
            if fs:
                self.src_disp.set(fs[0] if len(fs) == 1 else f"{len(fs)} file trong {Path(fs[0]).parent}")
                self.set_files(fs)

    def scan_folder(self):
        if not self.src_dir:
            return []
        it = Path(self.src_dir).rglob("*") if self.sub_var.get() else Path(self.src_dir).glob("*")
        out = Path(self.loc_out.get()).resolve() if self.loc_out.get() else None
        return [str(p) for p in it if p.is_file() and p.suffix.lower() in EXTS
                and not (out and (out == p.parent.resolve() or out in p.resolve().parents))]

    def rescan(self):
        if self.src_mode.get() == "folder" and self.src_dir:
            self.set_files(self.scan_folder())

    def current_out(self):
        return self.url_out.get() if self.nb.index("current") == 0 else self.loc_out.get()

    def open_out(self):
        d = self.current_out()
        if d and Path(d).exists():
            if sys.platform == "win32":
                os.startfile(d)
            else:
                os.system(f'{"open" if sys.platform == "darwin" else "xdg-open"} "{d}"')

    def write(self, s, err=False):
        self.log.insert("end", s + "\n", ("err",) if err else ())
        self.log.see("end")

    # ---------------- chạy
    def start(self):
        if self.running:
            return
        mode = self.nb.index("current")
        out = self.current_out().strip()
        if not out:
            messagebox.showwarning(APP_NAME, "Hãy chọn folder lưu trước khi chạy.")
            return
        bg = self.bg_var.get().strip()
        if not re.fullmatch(r"#[0-9A-Fa-f]{6}", bg):
            messagebox.showwarning(APP_NAME, "Màu nền dạng #RRGGBB, ví dụ #FFFFFF.")
            return
        if mode == 0:
            items = self.parse_urls()
            if not items:
                messagebox.showwarning(APP_NAME, "Không tìm thấy URL ảnh hợp lệ (https://… có đuôi .png/.jpg/.webp…).")
                return
        else:
            self.rescan()  # quét lại thư mục lúc bắt đầu (bỏ qua folder lưu nếu nằm bên trong)
            items = list(self.files)
            if not items:
                messagebox.showwarning(APP_NAME, "Chưa có ảnh nào. Hãy chọn thư mục hoặc file ảnh."
                                       if not self.src_disp.get() else "Không tìm thấy ảnh nào trong nguồn đã chọn.")
                return
        Path(out).mkdir(parents=True, exist_ok=True)
        opts = (self.fmt_var.get(), int(self.q_var.get()), int(self.max_var.get() or 0),
                self.icc_var.get(), bg)
        self.running = True
        self.run_btn.state(["disabled"])
        self.log.delete("1.0", "end")
        self.prog.config(maximum=len(items), value=0)
        self.write(f"Bắt đầu {'download' if mode == 0 else 'xử lý'} {len(items)} mục → {out}")
        threading.Thread(target=self.worker, args=(mode, items, out, opts), daemon=True).start()

    def worker(self, mode, items, out, opts):
        tin = tout = 0
        errors = []
        if mode == 0:
            tmp_dir = Path(out) / ".pdz_tmp"
            tmp_dir.mkdir(exist_ok=True)
            ex = ThreadPoolExecutor(max_workers=8)
            futs = [ex.submit(job_url, u, out, opts, str(tmp_dir)) for u in items]
        else:
            ex = ProcessPoolExecutor(max_workers=max(1, (os.cpu_count() or 2) - 1))
            futs = [ex.submit(job_local, f, out, opts) for f in items]
        with ex:
            for i, fu in enumerate(as_completed(futs), 1):
                try:
                    ok, name, a, b, dn = fu.result()
                except Exception as e:
                    ok, name, a, b, dn = False, "?", f"Lỗi: {e}", 0, ""
                if ok:
                    tin += a
                    tout += b
                    short = name if len(name) < 70 else "…" + name[-68:]
                    msg, err = f"✓ {short}  {a/1024:,.0f} KB → {b/1024:,.0f} KB  ({dn})", False
                else:
                    errors.append((name, a))
                    msg, err = f"✗ {name}\n    {a}", True
                self.after(0, self.update_ui, i, len(items), msg, err)
        if mode == 0:
            try:
                tmp_dir.rmdir()
            except OSError:
                pass
        ok_n = len(items) - len(errors)
        summary = f"\nHoàn tất: {ok_n}/{len(items)} thành công, {len(errors)} lỗi."
        if tin:
            summary += f"  Dung lượng: {hsize(tin)} → {hsize(tout)} ({100*tout/tin:.0f}%)"
        if errors:
            try:
                with open(Path(out) / "pdz_errors.txt", "w", encoding="utf-8") as f:
                    for n, reason in errors:
                        f.write(f"{n}\t{reason}\n")
                summary += f"\nDanh sách lỗi đã lưu: {Path(out) / 'pdz_errors.txt'}"
            except OSError:
                pass
        self.after(0, self.done, summary, errors, mode, len(items))

    def update_ui(self, i, total, msg, err):
        self.prog.config(value=i)
        self.stat_lbl.config(text=f"{i}/{total}")
        self.write(msg, err)

    def done(self, summary, errors, mode, total):
        self.write(summary)
        self.running = False
        self.run_btn.state(["!disabled"])
        if errors:
            self.show_errors(errors, mode, total)
        else:
            messagebox.showinfo(APP_NAME, f"Hoàn tất! {total}/{total} ảnh thành công, không có lỗi.")

    def show_errors(self, errors, mode, total):
        w = tk.Toplevel(self)
        w.title(f"{len(errors)}/{total} mục bị lỗi")
        w.geometry("760x380")
        w.transient(self)
        ttk.Label(w, text=f"⚠ {len(errors)} trên {total} mục bị lỗi:", font=("Segoe UI", 10, "bold"),
                  foreground="#c0392b").pack(anchor="w", padx=10, pady=(10, 4))
        fr = ttk.Frame(w)
        fr.pack(fill="both", expand=True, padx=10)
        tv = ttk.Treeview(fr, columns=("item", "reason"), show="headings")
        tv.heading("item", text="URL / File")
        tv.heading("reason", text="Lý do")
        tv.column("item", width=380)
        tv.column("reason", width=340)
        for n, reason in errors:
            tv.insert("", "end", values=(n, reason))
        sb = ttk.Scrollbar(fr, command=tv.yview)
        tv.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")
        tv.pack(fill="both", expand=True)
        bf = ttk.Frame(w)
        bf.pack(fill="x", padx=10, pady=8)

        def copy_items():
            self.clipboard_clear()
            self.clipboard_append("\n".join(n for n, _ in errors))
        ttk.Button(bf, text="Copy danh sách lỗi", command=copy_items).pack(side="left")
        if mode == 0:
            def retry():
                self.url_txt.delete("1.0", "end")
                self.url_txt.insert("1.0", "\n".join(n for n, _ in errors))
                self.count_urls()
                w.destroy()
            ttk.Button(bf, text="Đưa URL lỗi vào ô để chạy lại", command=retry).pack(side="left", padx=6)
        ttk.Button(bf, text="Đóng", command=w.destroy).pack(side="right")


if __name__ == "__main__":
    mp.freeze_support()  # bắt buộc khi đóng gói .exe trên Windows
    App().mainloop()
