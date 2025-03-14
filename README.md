# PTUD-GK-DE-2

## Thông tin cá nhân
- **Tên:** Phan Tôn Bá Sang
- **MSSV**:22677351
- **STT**: 53

## Mô tả dự án
Dự án này là một ứng dụng web quản lý công việc sử dụng Django. Hệ thống cho phép user và admin tạo, cập nhật, xóa công việc và theo dõi trạng thái hoàn thành. Ngoài ra, hệ thống hỗ trợ upload avatar cho user và hiển thị các công việc quá hạn.

## Hướng dẫn cài đặt
### Yêu cầu
- Python 3.x
- Django
- SQLite (hoặc PostgreSQL/MySQL)

### Các bước cài đặt
1. **Clone repository:**
   ```sh
   git clone https://github.com/[tên-tài-khoản]/ptud-gk-de-2.git
   cd ptud-gk-de-2
   ```

2. **Tạo và kích hoạt virtual environment:**
   ```sh
   python -m venv venv
   source venv/bin/activate  # Trên macOS/Linux
   venv\Scripts\activate  # Trên Windows
   ```

3. **Cài đặt các dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

4. **Chạy makemigrations và migration:**
   ```sh
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Tạo superuser (nếu cần):**
   ```sh
   python manage.py createsuperuser
   ```

6. **Chạy server:**
   ```sh
   python manage.py runserver
   ```

7. **Truy cập trang web:**
   Mở trình duyệt và truy cập `http://127.0.0.1:8000/`

## Tính năng chính
- Quản lý công việc (tạo, chỉnh sửa, xóa, xem danh sách)
- Phân quyền user và admin
- Upload avatar user
- Hiển thị số công việc quá hạn (gần avatar)
- Giao diện dạng Single Column/Card-Based

## Các layout frontend đã dùng
- **Single Column** (Một Cột)

## Chức năng bổ sung
- **Hiển thị các công việc quá hạn**: Hệ thống hiển thị số lượng công việc quá hạn của user dưới dạng cảnh báo.

## Liên hệ
- Nếu có bất kỳ vấn đề gì, vui lòng liên hệ qua email hoặc tạo issue trên Github.

