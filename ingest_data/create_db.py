import duckdb

# Kết nối (sẽ tạo file nếu chưa có)
con = duckdb.connect(database="../ingest_data/tin_chi.duckdb", read_only=False)

# --- Giai đoạn 1: Tạo Schema cải tiến ---
# Thêm cột HocKy vào LopHocPhan
con.execute(
    """
    CREATE TABLE GiangVien (
        MaGV VARCHAR(10) PRIMARY KEY,
        TenGV VARCHAR(100) NOT NULL,
        Khoa VARCHAR(100)
    );
"""
)
con.execute(
    """
    CREATE TABLE MonHoc (
        MaMH VARCHAR(10) PRIMARY KEY,
        TenMH VARCHAR(150) NOT NULL,
        SoTinChi INT
    );
"""
)
con.execute(
    """
    CREATE TABLE LopHocPhan (
        MaLopHP VARCHAR(15) PRIMARY KEY,
        MaMH VARCHAR(10) NOT NULL,
        MaGV VARCHAR(10) NOT NULL,
        BuoiHoc VARCHAR(10), -- 'Sáng', 'Chiều', 'Tối'
        HocKy VARCHAR(20)
    );
"""
)

# --- Giai đoạn 2: Nạp dữ liệu mẫu đa dạng ---
# Giảng viên
con.execute(
    "INSERT INTO GiangVien VALUES ('GV001', 'Nguyễn Văn An', 'Công nghệ thông tin');"
)
con.execute(
    "INSERT INTO GiangVien VALUES ('GV002', 'Trần Thị Bích', 'Công nghệ thông tin');"
)
con.execute("INSERT INTO GiangVien VALUES ('GV003', 'Lê Minh Hải', 'Kinh tế');")
con.execute(
    "INSERT INTO GiangVien VALUES ('GV004', 'Phạm Thị Duyên', 'Công nghệ thông tin');"
)
con.execute("INSERT INTO GiangVien VALUES ('GV005', 'Hoàng Văn Tuấn', 'Ngoại ngữ');")


# Môn học
con.execute("INSERT INTO MonHoc VALUES ('MH001', 'Lập trình Python', 3);")
con.execute("INSERT INTO MonHoc VALUES ('MH002', 'Cơ sở dữ liệu', 3);")
con.execute("INSERT INTO MonHoc VALUES ('MH003', 'Kinh tế vĩ mô', 2);")
con.execute("INSERT INTO MonHoc VALUES ('MH004', 'Tiếng Anh giao tiếp', 4);")
con.execute("INSERT INTO MonHoc VALUES ('MH005', 'Nhập môn Trí tuệ nhân tạo', 3);")

# Lớp học phần
con.execute(
    "INSERT INTO LopHocPhan VALUES ('LHP001', 'MH001', 'GV001', 'Sáng', 'HK1_2025-2026');"
)
con.execute(
    "INSERT INTO LopHocPhan VALUES ('LHP002', 'MH001', 'GV002', 'Chiều', 'HK1_2025-2026');"
)
con.execute(
    "INSERT INTO LopHocPhan VALUES ('LHP003', 'MH002', 'GV001', 'Chiều', 'HK1_2025-2026');"
)
con.execute(
    "INSERT INTO LopHocPhan VALUES ('LHP004', 'MH003', 'GV003', 'Sáng', 'HK2_2025-2026');"
)
con.execute(
    "INSERT INTO LopHocPhan VALUES ('LHP005', 'MH004', 'GV005', 'Tối', 'HK1_2025-2026');"
)
con.execute(
    "INSERT INTO LopHocPhan VALUES ('LHP006', 'MH005', 'GV002', 'Sáng', 'HK2_2025-2026');"
)
con.execute(
    "INSERT INTO LopHocPhan VALUES ('LHP007', 'MH002', 'GV004', 'Chiều', 'HK2_2025-2026');"
)


print("✅ Database đã được tạo và nạp dữ liệu mẫu thành công!")
con.close()
