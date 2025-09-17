# TikTok Reup Video Generator: 
Con tool tôi viết cho ae nào re up mà cứ bị tiktok quét bản quyền
1. Background (BG):
- Load file nền cố định ocean.mp4, mute audio.
- Resize để chiều rộng / cao là số chẵn (tránh lỗi encoder).
- Sau đó loop lại để dài bằng video overlay.
  
2. Overlay (video gốc):
- Load video gốc từ videos_reup, mute audio.
- Resize chiếm khoảng 75% chiều cao của background, giữ tỷ lệ.
- 50% xác suất flip ngang (mirror).
- Random speedup nhẹ từ 1.03 → 1.07.
- Thêm hiệu ứng fade in/out 1 giây.
- Set độ mờ 85% để thấy background.
- Tăng brightness ~10% (làm sáng hơn).
- Đặt overlay vào giữa background.
  
3. Logo:
- Thêm logo.png làm watermark.
- Resize logo = ~10% chiều cao overlay.
- Đặt ở góc trên bên phải overlay, cách lề 10px.

4. Background & sync:
- Nối (loop) background để đủ dài bằng overlay.
- Crop/truncate background đúng bằng duration của overlay.
  
5. Composite:
- Ghép 3 lớp: background + overlay + logo.

6. Xuất video:
- Codec libx264, fps = 30.
- Xuất ra output/final_{tên gốc}.mp4.
- Không có audio.

## Yêu cầu hệ thống

- Python 3.8 trở lên
- Windows (khuyến nghị)

## Hướng dẫn cài đặt & sử dụng

### 1. Tải và cài đặt Python

- Tải Python tại [python.org/downloads](https://www.python.org/downloads/)
- Khi cài đặt, nhớ chọn **Add Python to PATH**.

### 2. Tải mã nguồn về máy

```sh
git clone https://github.com/phantrang2002/tiktokreup-tools.git
cd tiktokreup-tools
```

### 3. Tạo môi trường ảo (venv)

```sh
python -m venv venv
```

### 4. Cài đặt các thư viện cần thiết

```sh
venv\Scripts\activate
pip install -r requirements.txt
```

### 5. Chuẩn bị dữ liệu

- Tạo thư mục `videos_reup` và đặt các video nguồn vào đó.
- Đặt file background (`ocean.mp4`) và logo (`logo.png`) vào thư mục gốc dự án.

### 6. Cho phép chạy script PowerShell (chỉ cần làm 1 lần)

Mở PowerShell và chạy:
```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

### 7. Chạy tool bằng PowerShell

```powershell
.\run_main.ps1
```

## Kết quả

- Video đã xử lý sẽ nằm trong thư mục `output`.
