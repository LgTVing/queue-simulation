"""
Script lam sach du lieu goi tong dai ngan hang Anonymous Bank (Technion SEE Center)
Quy ve dinh dang chuan cua du an hang doi cho Tuan 1.
"""

import os
import pandas as pd
import numpy as np

def clean_data():
    raw_path = os.path.join(r"d:\KHDV", "data", "raw", "September1999.txt")
    clean_path = os.path.join(r"d:\KHDV", "data", "clean", "data_clean.csv")

    print(f"Dang doc du lieu tho tu: {raw_path}")
    df = pd.read_csv(raw_path, sep="\t", encoding="latin1", low_memory=False)
    initial_count = len(df)
    print(f"Tong so ban ghi ban dau: {initial_count}")

    # 1. Loc ban ghi hop le ve outcome va priority
    df = df[df["outcome"].isin(["AGENT", "HANG"])].copy()
    df["priority"] = pd.to_numeric(df["priority"], errors="coerce").fillna(0).astype(int)
    df = df[df["priority"].isin([0, 1, 2])]

    # 2. Chi giu cac cuoc goi thuc su vao hang doi phuc vu (loai bo cuoc goi cup may truoc khi vao hang)
    in_queue = (df["outcome"] == "AGENT") | (
        (df["outcome"] == "HANG") & (~df["q_start"].astype(str).str.strip().isin(["0:00:00", "00:00:00", "nan", ""]))
    )
    df = df[in_queue].copy()

    # 3. Chon nghiep vu giao dich tieu chuan cua ngan hang (PS: Peilut Shotefet - Regular Activity)
    df = df[df["type"] == "PS"].copy()

    # 4. Tinh thoi diem khach vao hang (tinh bang giay trong ngay)
    def get_arrival_seconds(row):
        s = str(row["q_start"]).strip()
        if s not in ["0:00:00", "00:00:00", "nan", ""] and ":" in s:
            parts = s.split(":")
            return int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])
        v = str(row["vru_exit"]).strip()
        if ":" in v:
            parts = v.split(":")
            return int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])
        return None

    df["arr_sec"] = df.apply(get_arrival_seconds, axis=1)
    df = df.dropna(subset=["arr_sec"])

    # 5. Loc khung gio lam viec ban ngay: 8:00 - 17:00 (28800s den 61200s)
    df = df[(df["arr_sec"] >= 8 * 3600) & (df["arr_sec"] < 17 * 3600)].copy()

    # 6. Loc cac ngay lam viec tieu chuan (Chu nhat den Thu nam, loai ngay le va nua buoi)
    standard_workdays = [
        "990901", "990902", "990905", "990906", "990907", "990908", "990909",
        "990913", "990914", "990915", "990916", "990921", "990922", "990923"
    ]
    df = df[df["date"].astype(str).str.strip().isin(standard_workdays)].copy()

    # 7. Anh xa sang cac cot chuan cua du an
    day_mapping = {d: i for i, d in enumerate(sorted(standard_workdays))}
    df["day"] = df["date"].astype(str).str.strip().map(day_mapping)
    df["t"] = (df["arr_sec"] - 8 * 3600) / 60.0  # Phut ke tu 8h sang
    df["hour"] = (df["t"] // 60).astype(int)     # 0: 8h-9h, ..., 8: 16h-17h
    df["cls"] = ""                               # Nghiep vu chuan
    df["vip"] = (df["priority"] == 2).astype(int) # Priority 2 la khach hang uu tien
    
    # Thoi gian cho (wait) tinh bang phut
    df["q_time"] = pd.to_numeric(df["q_time"], errors="coerce").fillna(0)
    df["wait"] = df["q_time"] / 60.0
    
    # Trang thai phuc vu
    df["served"] = (df["outcome"] == "AGENT").astype(int)
    
    # Thoi gian phuc vu (svc) tinh bang phut
    df["ser_time"] = pd.to_numeric(df["ser_time"], errors="coerce")
    df["svc"] = np.where(df["served"] == 1, df["ser_time"] / 60.0, np.nan)

    # 8. Kiem tra tinh toan ven du lieu
    # - Khach duoc phuc vu phai co svc > 0
    # - wait phai >= 0
    # - Loai bo cac ngoai lai bat thuong (thoi gian phuc vu qua dai > 60 phut)
    df = df[df["wait"] >= 0]
    df = df[(df["served"] == 0) | ((df["svc"] > 0) & (df["svc"] <= 60))]

    # Sap xep theo thoi gian den
    df = df.sort_values(by=["day", "t"]).reset_index(drop=True)

    final_cols = ["day", "t", "hour", "cls", "vip", "wait", "served", "svc"]
    df_clean = df[final_cols]

    os.makedirs(os.path.dirname(clean_path), exist_ok=True)
    df_clean.to_csv(clean_path, index=False)
    print(f"Xuat du lieu sach thanh cong ra: {clean_path}")
    print(f"So ban ghi hop le: {len(df_clean)} / {initial_count} ({len(df_clean)/initial_count*100:.1f}%)")
    print(f"So ngay quan sat: {len(standard_workdays)} ngay")
    print(f"So luong phuc vu trung binh/ngay: {len(df_clean)/len(standard_workdays):.1f} khach")
    return df_clean

if __name__ == "__main__":
    clean_data()
