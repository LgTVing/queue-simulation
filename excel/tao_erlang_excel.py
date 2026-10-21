"""
Script tao file Excel Erlang C: excel/erlang.xlsx
Dap ung day du tat ca cac yeu cau trong Muc 5 cua TUAN_1_HUONG_DAN.md:
- Sheet Input: tham so dau vao
- Sheet ErlangC: tinh toan c, rho, C(c, a), Wq, Lq, P(Wq<=t), danh gia DAT/KHONG
- Sheet Tra_c: bang tra so quay toi thieu theo lambda va E[S]
- Sheet Allen_Cunneen: tinh Wq cho phan phoi tong quat M/G/c
- Sheet Quyet_dinh: bang quyet dinh so quay theo 9 khung gio thuc te
"""

import os
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

def build_erlang_excel():
    excel_path = os.path.join(r"d:\KHDV", "excel", "erlang.xlsx")
    os.makedirs(os.path.dirname(excel_path), exist_ok=True)
    
    wb = openpyxl.Workbook()
    # Xoa sheet mac dinh
    wb.remove(wb.active)

    # Dinh dang chung
    font_title = Font(name='Segoe UI', size=14, bold=True, color='1F4E78')
    font_header = Font(name='Segoe UI', size=11, bold=True, color='FFFFFF')
    font_bold = Font(name='Segoe UI', size=11, bold=True)
    font_normal = Font(name='Segoe UI', size=11)
    font_highlight = Font(name='Segoe UI', size=12, bold=True, color='9C0006')

    fill_header_dark = PatternFill(start_color='1F4E78', end_color='1F4E78', fill_type='solid')
    fill_header_blue = PatternFill(start_color='2E75B6', end_color='2E75B6', fill_type='solid')
    fill_input = PatternFill(start_color='D9E1F2', end_color='D9E1F2', fill_type='solid')
    fill_pass = PatternFill(start_color='C6EFCE', end_color='C6EFCE', fill_type='solid')
    fill_fail = PatternFill(start_color='FFC7CE', end_color='FFC7CE', fill_type='solid')

    border_thin = Border(
        left=Side(style='thin', color='D9D9D9'),
        right=Side(style='thin', color='D9D9D9'),
        top=Side(style='thin', color='D9D9D9'),
        bottom=Side(style='thin', color='D9D9D9')
    )

    # =========================================================================
    # 1. SHEET Input
    # =========================================================================
    ws_input = wb.create_sheet('Input')
    ws_input.views.sheetView[0].showGridLines = True

    ws_input['A1'] = "BẢNG THAM SỐ ĐẦU VÀO M/M/c (Erlang C)"
    ws_input['A1'].font = font_title

    input_data = [
        ("A3", "Tham số", "B3", "Giá trị", "C3", "Đơn vị", "D3", "Ý nghĩa"),
        ("A4", "Tốc độ đến (λ)", "B4", 1.5, "C4", "khách/phút", "D4", "Số khách trung bình đến hệ thống trong 1 phút"),
        ("A5", "Thời gian phục vụ TB (E[S])", "B5", 3.0, "C5", "phút", "D5", "Thời gian xử lý trung bình của 1 quầy"),
        ("A6", "Tốc độ phục vụ mỗi quầy (μ)", "B6", "=1/B5", "C6", "khách/phút", "D6", "Năng suất phục vụ của 1 quầy (μ = 1/E[S])"),
        ("A7", "Cường độ tải giao thông (a)", "B7", "=B4*B5", "C7", "Erlang", "D7", "Tải lượng công việc (a = λ / μ = λ * E[S])"),
        ("A8", "Ngưỡng thời gian chờ cam kết (t)", "B8", 5.0, "C8", "phút", "D8", "Ngưỡng thời gian chờ mục tiêu của SLA"),
        ("A9", "Mục tiêu cam kết dịch vụ (SLA)", "B9", 0.90, "C9", "tỉ lệ (90%)", "D9", "Tối thiểu 90% khách chờ <= t phút")
    ]

    for r in input_data:
        ws_input[r[0]] = r[1]
        ws_input[r[2]] = r[3]
        ws_input[r[4]] = r[5]
        ws_input[r[6]] = r[7]

    # Format header Input
    for col in ['A3', 'B3', 'C3', 'D3']:
        ws_input[col].font = font_header
        ws_input[col].fill = fill_header_dark
        ws_input[col].alignment = Alignment(horizontal='center', vertical='center')

    for row in range(4, 10):
        ws_input[f'A{row}'].font = font_bold
        ws_input[f'B{row}'].font = font_normal
        ws_input[f'B{row}'].fill = fill_input
        ws_input[f'B{row}'].alignment = Alignment(horizontal='center')
        ws_input[f'C{row}'].font = font_normal
        ws_input[f'C{row}'].alignment = Alignment(horizontal='center')
        ws_input[f'D{row}'].font = font_normal
        for col in ['A', 'B', 'C', 'D']:
            ws_input[f'{col}{row}'].border = border_thin

    ws_input['B4'].number_format = '0.00'
    ws_input['B5'].number_format = '0.00'
    ws_input['B6'].number_format = '0.0000'
    ws_input['B7'].number_format = '0.00'
    ws_input['B8'].number_format = '0.0'
    ws_input['B9'].number_format = '0.0%'

    # =========================================================================
    # 2. SHEET ErlangC
    # =========================================================================
    ws_erlang = wb.create_sheet('ErlangC')
    ws_erlang.views.sheetView[0].showGridLines = True

    ws_erlang['A1'] = "TÍNH TOÁN CÔNG THỨC ERLANG C VÀ XÁC ĐỊNH SỐ QUẦY TỐI THIỂU"
    ws_erlang['A1'].font = font_title

    # Box ket qua chinh
    ws_erlang['A3'] = "KẾT QUẢ TỐI ƯU:"
    ws_erlang['A3'].font = font_bold
    ws_erlang['A4'] = "Số quầy nhỏ nhất đạt SLA:"
    ws_erlang['A4'].font = font_bold
    ws_erlang['B4'] = '=INDEX(A10:A24, MATCH("ĐẠT", G10:G24, 0))'
    ws_erlang['B4'].font = Font(name='Segoe UI', size=16, bold=True, color='006100')
    ws_erlang['B4'].fill = fill_pass
    ws_erlang['B4'].alignment = Alignment(horizontal='center', vertical='center')

    ws_erlang['A5'] = "Hiệu suất sử dụng tương ứng (ρ):"
    ws_erlang['A5'].font = font_bold
    ws_erlang['B5'] = '=VLOOKUP(B4, A10:G24, 2, FALSE)'
    ws_erlang['B5'].font = font_bold
    ws_erlang['B5'].number_format = '0.0%'
    ws_erlang['B5'].alignment = Alignment(horizontal='center', vertical='center')

    ws_erlang['A6'] = "Thời gian chờ trung bình (Wq):"
    ws_erlang['A6'].font = font_bold
    ws_erlang['B6'] = '=VLOOKUP(B4, A10:G24, 4, FALSE)'
    ws_erlang['B6'].font = font_bold
    ws_erlang['B6'].number_format = '0.00 "phút"'
    ws_erlang['B6'].alignment = Alignment(horizontal='center', vertical='center')

    ws_erlang['A7'] = "Tỉ lệ đạt SLA (P(Wq <= 5 phút)):"
    ws_erlang['A7'].font = font_bold
    ws_erlang['B7'] = '=VLOOKUP(B4, A10:G24, 6, FALSE)'
    ws_erlang['B7'].font = Font(name='Segoe UI', size=12, bold=True, color='006100')
    ws_erlang['B7'].number_format = '0.0%'
    ws_erlang['B7'].alignment = Alignment(horizontal='center', vertical='center')

    # Bang chi tiet Erlang C
    headers_erlang = [
        "Số quầy (c)", "Hiệu suất (ρ)", "Xác suất chờ C(c, a)", 
        "TG chờ TB Wq (phút)", "Độ dài hàng Lq", "P(Wq <= 5 phút)", "Đạt SLA?"
    ]
    for col_idx, h_text in enumerate(headers_erlang, start=1):
        cell = ws_erlang.cell(row=9, column=col_idx, value=h_text)
        cell.font = font_header
        cell.fill = fill_header_dark
        cell.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)

    # Cong thuc dong 10 (c = INT(a) + 1)
    # Dong 10 ung voi c = 5 (khi a = 4.5)
    for i in range(15):
        r = 10 + i
        if i == 0:
            ws_erlang[f'A{r}'] = '=INT(Input!$B$7)+1'
        else:
            ws_erlang[f'A{r}'] = f'=A{r-1}+1'
        
        ws_erlang[f'B{r}'] = f'=Input!$B$7/A{r}'
        # Cong thuc Erlang C dung POISSON.DIST
        ws_erlang[f'C{r}'] = f'=(POISSON.DIST(A{r},Input!$B$7,FALSE)/(1-B{r}))/((POISSON.DIST(A{r},Input!$B$7,FALSE)/(1-B{r}))+POISSON.DIST(A{r}-1,Input!$B$7,TRUE))'
        # Wq = C / (c*mu - lambda)
        ws_erlang[f'D{r}'] = f'=C{r}/(A{r}*Input!$B$6-Input!$B$4)'
        # Lq = lambda * Wq
        ws_erlang[f'E{r}'] = f'=Input!$B$4*D{r}'
        # P(Wq <= t) = 1 - C * exp(-(c*mu - lambda)*t)
        ws_erlang[f'F{r}'] = f'=1-C{r}*EXP(-(A{r}*Input!$B$6-Input!$B$4)*Input!$B$8)'
        # Dat muc tieu?
        ws_erlang[f'G{r}'] = f'=IF(F{r}>=Input!$B$9,"ĐẠT","KHÔNG")'

        # Formatting
        ws_erlang[f'A{r}'].alignment = Alignment(horizontal='center')
        ws_erlang[f'A{r}'].font = font_bold
        ws_erlang[f'B{r}'].number_format = '0.0%'
        ws_erlang[f'B{r}'].alignment = Alignment(horizontal='center')
        ws_erlang[f'C{r}'].number_format = '0.0000'
        ws_erlang[f'C{r}'].alignment = Alignment(horizontal='center')
        ws_erlang[f'D{r}'].number_format = '0.00'
        ws_erlang[f'D{r}'].alignment = Alignment(horizontal='center')
        ws_erlang[f'E{r}'].number_format = '0.00'
        ws_erlang[f'E{r}'].alignment = Alignment(horizontal='center')
        ws_erlang[f'F{r}'].number_format = '0.0%'
        ws_erlang[f'F{r}'].alignment = Alignment(horizontal='center')
        ws_erlang[f'G{r}'].alignment = Alignment(horizontal='center')
        ws_erlang[f'G{r}'].font = font_bold

        for col_l in ['A', 'B', 'C', 'D', 'E', 'F', 'G']:
            ws_erlang[f'{col_l}{r}'].border = border_thin

    # =========================================================================
    # 3. SHEET Tra_c (Bảng tra số quầy theo λ và E[S])
    # =========================================================================
    ws_trac = wb.create_sheet('Tra_c')
    ws_trac.views.sheetView[0].showGridLines = True

    ws_trac['A1'] = "BẢNG TRA SỐ QUẦY TỐI THIỂU ĐẠT SLA 90% (t <= 5 phút)"
    ws_trac['A1'].font = font_title

    # Headers Tra_c
    es_values = [2.0, 3.0, 4.0, 5.0]
    ws_trac['A3'] = "λ (khách/phút)"
    ws_trac['A3'].font = font_header
    ws_trac['A3'].fill = fill_header_dark
    ws_trac['A3'].alignment = Alignment(horizontal='center', vertical='center')

    for idx, es in enumerate(es_values, start=2):
        col_l = get_column_letter(idx)
        cell = ws_trac[f'{col_l}3']
        cell.value = f"E[S] = {es:.1f} phút (μ = {1/es:.2f})"
        cell.font = font_header
        cell.fill = fill_header_blue
        cell.alignment = Alignment(horizontal='center', vertical='center')

    # Tinh toan c toi thieu theo cong thuc Erlang C bang Python de dien san gia tri chuan
    import math
    def erlang_c_prob(c, a):
        if c <= a:
            return 1.0
        rho = a / c
        # Poisson terms: p(k) = e^-a * a^k / k!
        sum_k = sum((a**k)/math.factorial(k) for k in range(c))
        term_c = (a**c)/(math.factorial(c) * (1 - rho))
        return term_c / (sum_k + term_c)

    def find_min_c(lam, es, t=5.0, target=0.90):
        mu = 1.0 / es
        a = lam * es
        for c in range(int(a) + 1, int(a) + 50):
            C = erlang_c_prob(c, a)
            sl = 1.0 - C * math.exp(-(c * mu - lam) * t)
            if sl >= target:
                return c
        return int(a) + 1

    lambdas = [0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0, 2.25, 2.5, 2.75, 3.0]
    for r_idx, lam in enumerate(lambdas, start=4):
        ws_trac[f'A{r_idx}'] = lam
        ws_trac[f'A{r_idx}'].number_format = '0.00'
        ws_trac[f'A{r_idx}'].font = font_bold
        ws_trac[f'A{r_idx}'].alignment = Alignment(horizontal='center')
        ws_trac[f'A{r_idx}'].border = border_thin

        for c_idx, es in enumerate(es_values, start=2):
            col_l = get_column_letter(c_idx)
            c_min = find_min_c(lam, es)
            cell = ws_trac[f'{col_l}{r_idx}']
            cell.value = c_min
            cell.font = font_normal
            cell.alignment = Alignment(horizontal='center')
            cell.border = border_thin
            if es == 3.0 and lam == 1.5:
                cell.fill = fill_pass
                cell.font = font_bold

    # =========================================================================
    # 4. SHEET Allen_Cunneen (M/G/c)
    # =========================================================================
    ws_ac = wb.create_sheet('Allen_Cunneen')
    ws_ac.views.sheetView[0].showGridLines = True

    ws_ac['A1'] = "XẤP XỈ ALLEN - CUNNEEN CHO HÀNG ĐỢI M/G/c"
    ws_ac['A1'].font = font_title
    ws_ac['A2'] = "Công thức: Wq(M/G/c) ≈ (1 + cs²) / 2 * Wq(M/M/c)"
    ws_ac['A2'].font = font_bold

    headers_ac = ["Số quầy c", "Wq M/M/c (cs²=1.0)", "Wq (cs²=0.5)", "Wq (cs²=1.2 - Thực tế)", "Wq (cs²=1.5)", "Tăng thời gian chờ do cs²>1"]
    for idx, h_text in enumerate(headers_ac, start=1):
        cell = ws_ac.cell(row=4, column=idx, value=h_text)
        cell.font = font_header
        cell.fill = fill_header_dark
        cell.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)

    for i in range(10):
        r = 5 + i
        c_val = 5 + i
        ws_ac[f'A{r}'] = c_val
        ws_ac[f'A{r}'].alignment = Alignment(horizontal='center')
        ws_ac[f'A{r}'].font = font_bold
        
        # Link tu sheet ErlangC
        ws_ac[f'B{r}'] = f'=ErlangC!D{10+i}'
        ws_ac[f'C{r}'] = f'=(1 + 0.5)/2 * B{r}'
        ws_ac[f'D{r}'] = f'=(1 + 1.20)/2 * B{r}'
        ws_ac[f'E{r}'] = f'=(1 + 1.5)/2 * B{r}'
        ws_ac[f'F{r}'] = f'=(D{r} - B{r})/B{r}'

        ws_ac[f'B{r}'].number_format = '0.00'
        ws_ac[f'C{r}'].number_format = '0.00'
        ws_ac[f'D{r}'].number_format = '0.00'
        ws_ac[f'E{r}'].number_format = '0.00'
        ws_ac[f'F{r}'].number_format = '+0.0%'

        for col_l in ['A', 'B', 'C', 'D', 'E', 'F']:
            ws_ac[f'{col_l}{r}'].border = border_thin
            ws_ac[f'{col_l}{r}'].alignment = Alignment(horizontal='center')

    # =========================================================================
    # 5. SHEET Quyet_dinh (Bảng quyết định số quầy theo 9 khung giờ thực tế)
    # =========================================================================
    ws_qd = wb.create_sheet('Quyet_dinh')
    ws_qd.views.sheetView[0].showGridLines = True

    ws_qd['A1'] = "BẢNG QUYẾT ĐỊNH SỐ QUẦY THEO KHUNG GIỜ (SIPP LÝ THUYẾT)"
    ws_qd['A1'].font = font_title
    ws_qd['A2'] = "Dữ liệu tham số thực tế: E[S] = 2.88 phút, cs² = 1.20, SLA: P(Wq <= 5 phút) >= 90%"
    ws_qd['A2'].font = font_bold

    headers_qd = [
        "Khung giờ", "λ (khách/phút)", "E[S] (phút)", "cs²", 
        "Tải a (Erlang)", "Số quầy c (Erlang C)", "Hiệu suất ρ", "P(Wq <= 5) dự kiến", "Đạt SLA?"
    ]
    for idx, h_text in enumerate(headers_qd, start=1):
        cell = ws_qd.cell(row=4, column=idx, value=h_text)
        cell.font = font_header
        cell.fill = fill_header_dark
        cell.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)

    # 9 khung gio thuc te tu data_clean
    real_lambdas = [1.0190, 1.4333, 1.6440, 1.4393, 1.2393, 1.2429, 1.3214, 1.3048, 1.0655]
    es_real = 2.8784
    mu_real = 1.0 / es_real

    for idx, lam in enumerate(real_lambdas, start=5):
        h_label = f"{idx+3}h - {idx+4}h"
        ws_qd[f'A{idx}'] = h_label
        ws_qd[f'B{idx}'] = lam
        ws_qd[f'C{idx}'] = round(es_real, 2)
        ws_qd[f'D{idx}'] = 1.20
        ws_qd[f'E{idx}'] = f'=B{idx}*C{idx}'
        
        # Tim c_min cho gio nay
        c_opt = find_min_c(lam, es_real)
        ws_qd[f'F{idx}'] = c_opt
        ws_qd[f'G{idx}'] = f'=E{idx}/F{idx}'
        
        # Tinh SL
        C_val = erlang_c_prob(c_opt, lam * es_real)
        sl_val = 1.0 - C_val * math.exp(-(c_opt * mu_real - lam) * 5.0)
        ws_qd[f'H{idx}'] = round(sl_val, 4)
        ws_qd[f'I{idx}'] = "ĐẠT"

        ws_qd[f'A{idx}'].font = font_bold
        ws_qd[f'A{idx}'].alignment = Alignment(horizontal='center')
        ws_qd[f'B{idx}'].number_format = '0.0000'
        ws_qd[f'B{idx}'].alignment = Alignment(horizontal='center')
        ws_qd[f'C{idx}'].number_format = '0.00'
        ws_qd[f'C{idx}'].alignment = Alignment(horizontal='center')
        ws_qd[f'D{idx}'].number_format = '0.00'
        ws_qd[f'D{idx}'].alignment = Alignment(horizontal='center')
        ws_qd[f'E{idx}'].number_format = '0.00'
        ws_qd[f'E{idx}'].alignment = Alignment(horizontal='center')
        ws_qd[f'F{idx}'].font = Font(name='Segoe UI', size=11, bold=True, color='006100')
        ws_qd[f'F{idx}'].fill = fill_pass
        ws_qd[f'F{idx}'].alignment = Alignment(horizontal='center')
        ws_qd[f'G{idx}'].number_format = '0.0%'
        ws_qd[f'G{idx}'].alignment = Alignment(horizontal='center')
        ws_qd[f'H{idx}'].number_format = '0.0%'
        ws_qd[f'H{idx}'].alignment = Alignment(horizontal='center')
        ws_qd[f'I{idx}'].font = font_bold
        ws_qd[f'I{idx}'].alignment = Alignment(horizontal='center')

        for col_l in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']:
            ws_qd[f'{col_l}{idx}'].border = border_thin

    # Dong tong ket
    ws_qd['A14'] = "TỔNG CỘNG / TRUNG BÌNH"
    ws_qd['A14'].font = font_bold
    ws_qd['A14'].alignment = Alignment(horizontal='center')
    ws_qd['F14'] = "=SUM(F5:F13)"
    ws_qd['F14'].font = Font(name='Segoe UI', size=12, bold=True, color='1F4E78')
    ws_qd['F14'].alignment = Alignment(horizontal='center')
    ws_qd['G14'] = "=AVERAGE(G5:G13)"
    ws_qd['G14'].number_format = '0.0%'
    ws_qd['G14'].font = font_bold
    ws_qd['G14'].alignment = Alignment(horizontal='center')
    ws_qd['H14'] = "=AVERAGE(H5:H13)"
    ws_qd['H14'].number_format = '0.0%'
    ws_qd['H14'].font = font_bold
    ws_qd['H14'].alignment = Alignment(horizontal='center')

    # Chinh do rong tat ca cac sheet
    for sheet in wb.sheetnames:
        ws = wb[sheet]
        for col in ws.columns:
            max_len = max(len(str(cell.value or '')) for cell in col)
            col_letter = get_column_letter(col[0].column)
            ws.column_dimensions[col_letter].width = max(max_len + 4, 12)

    wb.save(excel_path)
    print(f"Xuat file Excel Erlang thanh cong ra: {excel_path}")

if __name__ == '__main__':
    build_erlang_excel()
