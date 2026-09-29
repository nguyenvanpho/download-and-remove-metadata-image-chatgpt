<p align="center"><img src="assets/logo.png" alt="PdzTools" height="64"></p>

# PDZ - Download or Remove Metadata Image ChatGPT

Tool desktop (Windows) chạy offline để:

- **Download ảnh hàng loạt từ URL** và xoá metadata ngay khi tải.
- **Xoá metadata ảnh có sẵn trên máy** (cả thư mục, kể cả thư mục con, hoặc từng file).
- **Chuyển đổi / nén ảnh**: JPG, WEBP, PNG hoặc giữ nguyên định dạng; chỉnh chất lượng, giới hạn kích thước.

Metadata bị xoá: EXIF, XMP, IPTC, C2PA / Content Credentials, text chunk PNG…
Ảnh được dựng lại chỉ từ dữ liệu pixel nên không còn sót metadata.

> **Lưu ý:** Watermark ẩn trong pixel (ví dụ SynthID) **không** bị xoá. Khi dùng ảnh AI trên
> các sàn TMĐT, hãy tuân thủ quy định khai báo nội dung AI của từng sàn.

## Tải bản dùng ngay

Vào [**Releases**](https://github.com/nguyenvanpho/download-and-remove-metadata-image-chatgpt/releases/latest) → tải file `PDZ-Download-Remove-Metadata_vX.Y.Z.zip` → giải nén →
chạy `PDZ-Download-Remove-Metadata.exe`. Không cần cài Python.
Hướng dẫn chi tiết: [HUONG-DAN-SU-DUNG.txt](HUONG-DAN-SU-DUNG.txt).

## Chạy từ mã nguồn

```bash
git clone https://github.com/nguyenvanpho/download-and-remove-metadata-image-chatgpt.git
cd download-and-remove-metadata-image-chatgpt
```


Yêu cầu Python 3.9+ (Windows: tick *Add python.exe to PATH* khi cài).

```bat
run.bat
```

hoặc:

```bash
pip install -r requirements.txt
python image_tool.py
```

## Build exe

**Trên máy Windows:**

```bat
build_exe.bat
```

Kết quả: `release\PDZ-Download-Remove-Metadata.zip` (gồm exe + hướng dẫn).

**Tự động bằng GitHub Actions:** push một tag dạng `v*`, GitHub sẽ build trên Windows và tạo Release kèm file zip.

```bash
git tag v1.0.2
git push origin v1.0.2
```

Có thể chạy tay ở tab **Actions → Build & Release → Run workflow** để build thử (file zip nằm ở mục *Artifacts*).

## Quy trình ra bản mới

1. Sửa code, cập nhật `CHANGELOG.md`.
2. Cập nhật số phiên bản trong `version.txt` (`filevers`, `prodvers`, `FileVersion`, `ProductVersion`).
3. Commit → `git tag vX.Y.Z` → `git push && git push --tags`.

## Cấu trúc

```
image_tool.py            # toàn bộ ứng dụng (Tkinter + Pillow)
assets/pdz.ico           # icon exe
assets/logo.png          # logo (bản gốc; logo trong app đã được nhúng base64)
version.txt              # thông tin phiên bản cho file exe (Properties > Details)
requirements*.txt        # thư viện chạy / build
run.bat, build_exe.bat   # chạy nhanh / build trên Windows
.github/workflows/       # build & release tự động
HUONG-DAN-SU-DUNG.txt    # hướng dẫn cho người dùng cuối (đóng kèm zip)
```
