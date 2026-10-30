# CLAUDE.md

Ứng dụng desktop Windows dùng Python 3.9+, Tkinter và Pillow. Mã chính: `image_tool.py`. Đọc README.md để chạy/build và CHANGELOG.md để xem phiên bản.

## Decision Log

### Giữ cấu trúc thư mục con khi xử lý ảnh local (2026-10-30)

- User yêu cầu checkbox tùy chọn giữ tên/cấu trúc thư mục con bên đích để dễ đối chiếu ảnh nguồn.
- Mặc định tắt; chỉ áp dụng cho nguồn Cả thư mục và có bật Gồm cả ảnh trong thư mục con. Chọn từng file và tải URL giữ nguyên.
- Dùng đường dẫn tương đối từ thư mục nguồn, giữ mọi cấp con. Ảnh ở gốc nguồn lưu ngay gốc đích; không bọc thêm tên thư mục nguồn.
- Chốt source root lúc Bắt đầu rồi truyền cho worker để đổi UI giữa chừng không làm thay đổi đường dẫn batch đang chạy.
- Giữ logic chuyển định dạng/xóa metadata/hậu tố tên trùng; nhật ký hiện đường dẫn tương đối của ảnh đã lưu.
- Cập nhật source và tài liệu cho v1.0.2; chưa build exe/phát hành.
- QA: đạt 12 kiểm tra xử lý ảnh/đường dẫn (Unicode, nhiều cấp, root, suffix, flat, xóa metadata, giữ pixel/ảnh gốc, từ chối nguồn ngoài root) và 9 kiểm tra giao diện Tk/batch (default, disabled/enabled, bỏ qua thư mục đích, chốt source root, flat và URL). Python syntax và git diff --check đạt. Chưa commit/push khi chưa có yêu cầu riêng.

### Build và commit/push v1.0.2 — user đã duyệt (2026-10-30)

- User yêu cầu rõ: "build exe rồi commit push đi"; ghi chú chưa build/chưa commit ở trên là trạng thái trước yêu cầu này.
- Đã pull --ff-only thành công trên main. Build bằng môi trường .venv riêng: Python 3.12.14, Pillow 13.0.0, PyInstaller 6.22.3; tùy chọn onefile/windowed, icon và version.txt theo build_exe.bat. Khi dùng runtime Python đóng gói của Codex, đặt TCL_LIBRARY/TK_LIBRARY trỏ tcl/tcl8.6 và tcl/tk8.6 trong runtime để hook Tk tìm đủ tài nguyên; không cần đổi mã app.
- Build thành công dist/PDZ-Download-Remove-Metadata.exe, Windows FileVersion 1.0.2. Đã mở thử exe, cửa sổ chính khởi tạo đúng và đóng với exit code 0.
- Gói release/PDZ-Download-Remove-Metadata_v1.0.2.zip chứa đúng exe và HUONG-DAN-SU-DUNG.txt. Build artifacts/.venv được .gitignore loại trừ, không đưa binary vào Git.
- QA bổ sung với chính thư viện build: ProcessPoolExecutor trên Windows giữ nhiều cấp thư mục và ảnh trùng tên ở các nhánh, xóa metadata PNG, chuyển JPG/resize và chế độ flat đều đạt. Diff check đạt.
- Commit/push mã nguồn, version, changelog, hướng dẫn và tài liệu trên main theo yêu cầu. Không tạo tag/GitHub Release trong lượt này; ZIP/exe nằm local.

### Phát hành GitHub Release v1.0.2 — user đã duyệt (2026-10-30)

- User yêu cầu phát hành Release ngay sau khi đã build, QA, commit/push tính năng.
- Dùng quy trình sẵn có .github/workflows/release.yml: tạo/push tag v1.0.2 để GitHub Actions build trên Windows (Python 3.11), đóng ZIP kèm hướng dẫn và tự tạo GitHub Release với ZIP đính kèm. Bản ZIP phát hành do CI build từ source của tag; bản build local trước đó vẫn giữ làm bản đã smoke-test.
- Đã pull main và kiểm tra v1.0.2 chưa tồn tại trên local/remote trước khi tạo tag; không thay/di chuyển tag đã có.
