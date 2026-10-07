from flask import Flask, render_template_string, request, url_for, jsonify, abort, redirect, make_response
import io
import csv

app = Flask(__name__)
# API trả về tiếng Việt có dấu
app.json.ensure_ascii = False

STUDENTS = {
    "23T1020001": {"name": "Nguyễn Văn An", "lop": "K47A",
        "scores": {"PMMNM": 8.5, "CSDL": 7.0, "MMT": 9.0}},
    "23T1020002": {"name": "Trần Thị Bình", "lop": "K47A",
        "scores": {"PMMNM": 6.0, "CSDL": 5.5, "MMT": 7.0}},
    "23T1020003": {"name": "Lê Hoàng Cường", "lop": "K47B",
        "scores": {"PMMNM": 9.5, "CSDL": 9.0}},
    "23T1020004": {"name": "Phạm Minh Dũng", "lop": "K47B",
        "scores": {"PMMNM": 4.0, "CSDL": 3.5, "MMT": 5.0}},
    "23T1020005": {"name": "Hoàng Thu Hà", "lop": "K47A", 
        "scores": {}},
    "23T1020006": {"name": "Võ Quốc Khánh", "lop": "K47C",
        "scores": {"PMMNM": 7.5, "MMT": 8.0}},
}

# Layout cơ sở Bootstrap 5
BASE_LAYOUT = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title if title else "Quản Lý Sinh Viên" }}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.1/font/bootstrap-icons.css">
</head>
<body class="bg-light">
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary mb-4 shadow-sm">
        <div class="container">
            <a class="navbar-brand fw-bold" href="/"><i class="bi bi-mortarboard-fill me-2"></i>QLSV System</a>
            <div class="collapse navbar-collapse">
                <ul class="navbar-nav ms-auto">
                    <li class="nav-item"><a class="nav-link" href="{{ url_for('home') }}">Trang chủ</a></li>
                    <li class="nav-item"><a class="nav-link" href="{{ url_for('student_list') }}">Danh sách SV</a></li>
                    <li class="nav-item"><a class="nav-link" href="{{ url_for('api_students') }}" target="_blank">API JSON</a></li>
                </ul>
            </div>
        </div>
    </nav>

    <div class="container mb-5">
        {% block content %}{% endblock %}
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
"""

# CÂU 1: Trang chủ
@app.route("/")
def home():
    total_students = len(STUDENTS)
    classes = sorted(list({s["lop"] for s in STUDENTS.values()}))
    
    html_content = BASE_LAYOUT.replace("{% block content %}{% endblock %}", """
    <div class="row justify-content-center">
        <div class="col-md-8">
            <div class="card shadow-sm border-0">
                <div class="card-body p-4">
                    <h1 class="h3 card-title text-primary mb-4"><i class="bi bi-house-door me-2"></i>Trang Chủ - Quản Lý Sinh Viên</h1>
                    
                    <div class="row g-3 mb-4">
                        <div class="col-md-6">
                            <div class="p-3 bg-primary bg-opacity-10 rounded-3 border border-primary border-opacity-25">
                                <div class="text-muted small">Tổng số sinh viên</div>
                                <div class="fs-2 fw-bold text-primary">{{ total_students }}</div>
                            </div>
                        </div>
                        <div class="col-md-6">
                            <div class="p-3 bg-success bg-opacity-10 rounded-3 border border-success border-opacity-25">
                                <div class="text-muted small">Danh sách lớp</div>
                                <div class="fs-4 fw-bold text-success">{{ classes | join(', ') }}</div>
                            </div>
                        </div>
                    </div>

                    <h5 class="text-secondary mb-3">Liên kết nhanh:</h5>
                    <div class="d-flex gap-2">
                        <a href="{{ url_for('student_list') }}" class="btn btn-primary">
                            <i class="bi bi-people me-1"></i> Xem danh sách sinh viên
                        </a>
                        <a href="{{ url_for('api_students') }}" target="_blank" class="btn btn-outline-secondary">
                            <i class="bi bi-code-slash me-1"></i> Xem API Sinh viên
                        </a>
                    </div>
                </div>
            </div>
        </div>
    </div>
    """)
    return render_template_string(html_content, total_students=total_students, classes=classes, title="Trang Chủ")

# CÂU 2: Danh sách sinh viên (Có thêm Form Tìm kiếm của Câu 6)
@app.route("/students")
def student_list():
    lop_filter = request.args.get("lop", "").strip()
    all_classes = sorted(list({s["lop"] for s in STUDENTS.values()}))
    
    filtered_students = {}
    for mssv, info in STUDENTS.items():
        if not lop_filter or info["lop"].lower() == lop_filter.lower():
            filtered_students[mssv] = info

    processed_students = []
    for mssv, info in filtered_students.items():
        scores = info["scores"].values()
        if scores:
            dtb = round(sum(scores) / len(scores), 2)
            if dtb >= 8.5: xep_loai, badge_class = "Giỏi", "bg-success"
            elif dtb >= 7.0: xep_loai, badge_class = "Khá", "bg-primary"
            elif dtb >= 5.0: xep_loai, badge_class = "Trung bình", "bg-warning text-dark"
            else: xep_loai, badge_class = "Yếu", "bg-danger"
            dtb_str = str(dtb)
        else:
            dtb_str, xep_loai, badge_class = "-", "-", "bg-secondary"

        processed_students.append({
            "mssv": mssv, "name": info["name"], "lop": info["lop"],
            "dtb": dtb_str, "xep_loai": xep_loai, "badge_class": badge_class
        })

    html_content = BASE_LAYOUT.replace("{% block content %}{% endblock %}", """
    <div class="card shadow-sm border-0">
        <div class="card-body p-4">
            <div class="d-flex justify-content-between align-items-center mb-4">
                <h2 class="h3 text-primary m-0"><i class="bi bi-list-task me-2"></i>Danh Sách Sinh Viên</h2>
                <a href="/" class="btn btn-outline-secondary btn-sm"><i class="bi bi-arrow-left me-1"></i>Trang chủ</a>
            </div>
            
            <!-- CÂU 6: Form tìm kiếm GET -->
            <form action="{{ url_for('search_students') }}" method="GET" class="mb-4">
                <div class="input-group">
                    <input type="text" name="q" class="form-control" placeholder="Tìm theo tên hoặc MSSV..." required>
                    <button class="btn btn-primary" type="submit"><i class="bi bi-search me-1"></i>Tìm kiếm</button>
                </div>
            </form>

            <div class="mb-4">
                <span class="me-2 fw-bold text-muted">Lọc theo lớp:</span>
                <div class="btn-group" role="group">
                    <a href="{{ url_for('student_list') }}" 
                       class="btn btn-sm {{ 'btn-primary' if not lop_filter else 'btn-outline-primary' }}">Tất cả</a>
                    {% for c in all_classes %}
                        <a href="{{ url_for('student_list', lop=c) }}" 
                           class="btn btn-sm {{ 'btn-primary' if lop_filter.lower() == c.lower() else 'btn-outline-primary' }}">{{ c }}</a>
                    {% endfor %}
                </div>
            </div>

            {% if processed_students %}
            <div class="table-responsive">
                <table class="table table-hover align-middle border">
                    <thead class="table-light">
                        <tr>
                            <th>MSSV</th>
                            <th>Họ tên</th>
                            <th>Lớp</th>
                            <th class="text-center">Điểm TB</th>
                            <th class="text-center">Xếp loại</th>
                            <th class="text-end">Hành động</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for s in processed_students %}
                        <tr>
                            <td class="fw-bold">{{ s.mssv }}</td>
                            <td>{{ s.name }}</td>
                            <td>
                                <a href="{{ url_for('student_list', lop=s.lop) }}" class="badge bg-light text-primary border text-decoration-none">
                                    {{ s.lop }}
                                </a>
                            </td>
                            <td class="text-center fw-semibold">{{ s.dtb }}</td>
                            <td class="text-center"><span class="badge {{ s.badge_class }}">{{ s.xep_loai }}</span></td>
                            <td class="text-end">
                                <a href="{{ url_for('student_detail', mssv=s.mssv) }}" class="btn btn-sm btn-info text-white me-1">
                                    <i class="bi bi-eye me-1"></i>Chi tiết
                                </a>
                                <a href="{{ url_for('export_student_csv', mssv=s.mssv) }}" class="btn btn-sm btn-outline-success">
                                    <i class="bi bi-download me-1"></i>CSV
                                </a>
                            </td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
            {% else %}
            <div class="alert alert-warning mb-0"><i class="bi bi-exclamation-triangle me-2"></i>Không có sinh viên phù hợp.</div>
            {% endif %}
        </div>
    </div>
    """)
    return render_template_string(html_content, processed_students=processed_students, all_classes=all_classes, lop_filter=lop_filter, title="Danh Sách Sinh Viên")

# CÂU 6: Tìm kiếm an toàn (/search?q=...)
@app.route("/search")
def search_students():
    q = request.args.get("q", "").strip()
    
    results = []
    if q:
        for mssv, info in STUDENTS.items():
            # Lọc theo MSSV hoặc Họ tên (không phân biệt hoa/thường)
            if q.lower() in mssv.lower() or q.lower() in info["name"].lower():
                scores = info["scores"].values()
                if scores:
                    dtb = round(sum(scores) / len(scores), 2)
                    if dtb >= 8.5: xep_loai, badge_class = "Giỏi", "bg-success"
                    elif dtb >= 7.0: xep_loai, badge_class = "Khá", "bg-primary"
                    elif dtb >= 5.0: xep_loai, badge_class = "Trung bình", "bg-warning text-dark"
                    else: xep_loai, badge_class = "Yếu", "bg-danger"
                    dtb_str = str(dtb)
                else:
                    dtb_str, xep_loai, badge_class = "-", "-", "bg-secondary"

                results.append({
                    "mssv": mssv, "name": info["name"], "lop": info["lop"],
                    "dtb": dtb_str, "xep_loai": xep_loai, "badge_class": badge_class
                })

    html_content = BASE_LAYOUT.replace("{% block content %}{% endblock %}", """
    <div class="card shadow-sm border-0">
        <div class="card-body p-4">
            <div class="d-flex justify-content-between align-items-center mb-4">
                <h2 class="h3 text-primary m-0"><i class="bi bi-search me-2"></i>Kết Quả Tìm Kiếm</h2>
                <a href="/students" class="btn btn-outline-secondary btn-sm"><i class="bi bi-arrow-left me-1"></i>Xem tất cả SV</a>
            </div>

            <!-- Form GET giữ lại từ khoá trong value -->
            <form action="{{ url_for('search_students') }}" method="GET" class="mb-4">
                <div class="input-group">
                    <input type="text" name="q" value="{{ q }}" class="form-control" placeholder="Tìm theo tên hoặc MSSV..." required>
                    <button class="btn btn-primary" type="submit"><i class="bi bi-search me-1"></i>Tìm kiếm</button>
                </div>
            </form>

            <!-- Thông báo số lượng kết quả (đã escape an toàn bởi Jinja2) -->
            <div class="alert alert-info mb-4">
                <i class="bi bi-info-circle me-2"></i>Tìm thấy <strong>{{ results|length }}</strong> kết quả cho "<strong>{{ q }}</strong>".
            </div>

            {% if results %}
            <div class="table-responsive">
                <table class="table table-hover align-middle border">
                    <thead class="table-light">
                        <tr>
                            <th>MSSV</th>
                            <th>Họ tên</th>
                            <th>Lớp</th>
                            <th class="text-center">Điểm TB</th>
                            <th class="text-center">Xếp loại</th>
                            <th class="text-end">Hành động</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for s in results %}
                        <tr>
                            <td class="fw-bold">{{ s.mssv }}</td>
                            <td>{{ s.name }}</td>
                            <td>
                                <a href="{{ url_for('student_list', lop=s.lop) }}" class="badge bg-light text-primary border text-decoration-none">
                                    {{ s.lop }}
                                </a>
                            </td>
                            <td class="text-center fw-semibold">{{ s.dtb }}</td>
                            <td class="text-center"><span class="badge {{ s.badge_class }}">{{ s.xep_loai }}</span></td>
                            <td class="text-end">
                                <a href="{{ url_for('student_detail', mssv=s.mssv) }}" class="btn btn-sm btn-info text-white me-1">
                                    <i class="bi bi-eye me-1"></i>Chi tiết
                                </a>
                                <a href="{{ url_for('export_student_csv', mssv=s.mssv) }}" class="btn btn-sm btn-outline-success">
                                    <i class="bi bi-download me-1"></i>CSV
                                </a>
                            </td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
            {% else %}
            <div class="alert alert-warning mb-0"><i class="bi bi-exclamation-triangle me-2"></i>Không tìm thấy sinh viên nào phù hợp với từ khoá.</div>
            {% endif %}
        </div>
    </div>
    """)
    return render_template_string(html_content, q=q, results=results, title="Kết Quả Tìm Kiếm")

# CÂU 3: Chi tiết sinh viên
@app.route("/students/<mssv>")
def student_detail(mssv):
    student = STUDENTS.get(mssv)
    if not student:
        abort(404, description=f"Không có sinh viên với MSSV = {mssv}.")

    scores = student["scores"]
    if scores:
        dtb = round(sum(scores.values()) / len(scores), 2)
        if dtb >= 8.5: xep_loai, badge_class = "Giỏi", "bg-success"
        elif dtb >= 7.0: xep_loai, badge_class = "Khá", "bg-primary"
        elif dtb >= 5.0: xep_loai, badge_class = "Trung bình", "bg-warning text-dark"
        else: xep_loai, badge_class = "Yếu", "bg-danger"
    else:
        dtb, xep_loai, badge_class = "-", "-", "bg-secondary"

    short_url = url_for('short_student_detail', mssv=mssv, _external=True)

    html_content = BASE_LAYOUT.replace("{% block content %}{% endblock %}", """
    <div class="row justify-content-center">
        <div class="col-md-8">
            <div class="card shadow-sm border-0">
                <div class="card-body p-4">
                    <div class="d-flex justify-content-between align-items-center mb-4">
                        <h2 class="h3 text-primary m-0"><i class="bi bi-person-badge me-2"></i>Chi Tiết Sinh Viên</h2>
                        <a href="/students" class="btn btn-outline-secondary btn-sm"><i class="bi bi-arrow-left me-1"></i>Quay lại</a>
                    </div>

                    <div class="row g-3 mb-4">
                        <div class="col-md-6">
                            <p class="mb-1 text-muted">MSSV</p>
                            <p class="fs-5 fw-bold text-dark">{{ mssv }}</p>
                        </div>
                        <div class="col-md-6">
                            <p class="mb-1 text-muted">Họ tên</p>
                            <p class="fs-5 fw-bold text-dark">{{ student.name }}</p>
                        </div>
                        <div class="col-md-4">
                            <p class="mb-1 text-muted">Lớp</p>
                            <p><a href="{{ url_for('student_list', lop=student.lop) }}" class="btn btn-sm btn-outline-primary fw-semibold">{{ student.lop }}</a></p>
                        </div>
                        <div class="col-md-4">
                            <p class="mb-1 text-muted">Điểm trung bình</p>
                            <p class="fw-semibold fs-5">{{ dtb }}</p>
                        </div>
                        <div class="col-md-4">
                            <p class="mb-1 text-muted">Xếp loại</p>
                            <p><span class="badge {{ badge_class }} fs-6">{{ xep_loai }}</span></p>
                        </div>
                    </div>

                    <div class="alert alert-light border mb-4 d-flex align-items-center justify-content-between">
                        <div>
                            <i class="bi bi-link-45deg me-2 text-primary fs-5"></i>
                            <span class="fw-semibold">Link rút gọn (Câu 4):</span>
                            <a href="{{ short_url }}" target="_blank" class="ms-2 text-decoration-none">{{ short_url }}</a>
                        </div>
                        <span class="badge bg-secondary">Redirect 301</span>
                    </div>

                    <div class="d-flex justify-content-between align-items-center border-bottom pb-2 mb-3">
                        <h4 class="h5 text-secondary m-0"><i class="bi bi-journal-bookmark me-2"></i>Bảng điểm chi tiết</h4>
                        <a href="{{ url_for('export_student_csv', mssv=mssv) }}" class="btn btn-success btn-sm">
                            <i class="bi bi-file-earmark-spreadsheet me-1"></i>Tải bảng điểm (CSV)
                        </a>
                    </div>

                    {% if student.scores %}
                    <div class="table-responsive">
                        <table class="table table-bordered table-striped align-middle">
                            <thead class="table-light">
                                <tr>
                                    <th>Môn học</th>
                                    <th class="text-center" style="width: 150px;">Điểm số</th>
                                </tr>
                            </thead>
                            <tbody>
                                {% for mon, diem in student.scores.items() %}
                                <tr>
                                    <td>{{ mon }}</td>
                                    <td class="text-center fw-bold">{{ diem }}</td>
                                </tr>
                                {% endfor %}
                            </tbody>
                        </table>
                    </div>
                    {% else %}
                    <div class="alert alert-info" role="alert"><i class="bi bi-info-circle me-2"></i>Chưa có điểm môn nào.</div>
                    {% endif %}
                </div>
            </div>
        </div>
    </div>
    """)
    return render_template_string(html_content, mssv=mssv, student=student, dtb=dtb, xep_loai=xep_loai, badge_class=badge_class, short_url=short_url, title=f"Chi Tiết - {student['name']}")

# CÂU 4: Chuyển hướng 301
@app.route("/sv/<mssv>")
def short_student_detail(mssv):
    return redirect(url_for("student_detail", mssv=mssv), code=301)

# CÂU 5: Xuất bảng điểm CSV
@app.route("/students/<mssv>/export")
def export_student_csv(mssv):
    student = STUDENTS.get(mssv)
    if not student:
        abort(404, description=f"Không có sinh viên với MSSV = {mssv}.")

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["hoc_phan", "diem"])
    for mon, diem in student["scores"].items():
        writer.writerow([mon, diem])

    response = make_response(output.getvalue().encode('utf-8-sig'))
    response.headers["Content-Type"] = "text/csv; charset=utf-8"
    response.headers["Content-Disposition"] = f"attachment; filename=diem_{mssv}.csv"
    return response

# API trả về JSON tiếng Việt
@app.route("/api/students")
def api_students():
    return jsonify(STUDENTS)

if __name__ == "__main__":
    app.run(debug=True, port=8000)