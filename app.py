import json, os, re, socket, threading, uuid
from datetime import datetime
from pathlib import Path
from flask import Flask, Response, jsonify, request, send_file
from openpyxl import Workbook, load_workbook
from openpyxl.styles import Font, PatternFill, Alignment

BASE = Path(__file__).parent
SCHEMA = BASE / "schema.json"
XLSX = BASE / "data" / "responses.xlsx"
BACKUP = BASE / "data" / "backup.jsonl"   # safety copy of every submission
XLSX.parent.mkdir(exist_ok=True)
lock = threading.Lock()
app = Flask(__name__, static_folder="static", static_url_path="")


def load_schema():
    return json.loads(SCHEMA.read_text("utf-8"))

def save_schema(s):
    SCHEMA.write_text(json.dumps(s, ensure_ascii=False, indent=1), "utf-8")

def all_fields(form):
    return [f for sec in form["sections"] for f in sec["fields"]]

def sync_sheet(wb, form):
    """Row1 = labels, row2 (hidden) = field keys. Missing keys become new columns."""
    name = form["sheet"]
    if name in wb.sheetnames:
        ws = wb[name]
    else:
        ws = wb.create_sheet(name)
        ws.cell(1, 1, "Submitted At"); ws.cell(2, 1, "_ts")
        ws.row_dimensions[2].hidden = True
        ws.freeze_panes = "B3"
    cols = {ws.cell(2, c).value: c for c in range(1, ws.max_column + 1) if ws.cell(2, c).value}
    for f in all_fields(form):
        if f["key"] not in cols:
            c = ws.max_column + 1
            ws.cell(2, c, f["key"]); cols[f["key"]] = c
        ws.cell(1, cols[f["key"]], f["label"])
    for c in range(1, ws.max_column + 1):
        h = ws.cell(1, c)
        h.font = Font(bold=True, color="FFFFFF")
        h.fill = PatternFill("solid", fgColor="1F2D3D")
        h.alignment = Alignment(wrap_text=True, vertical="center")
        ws.column_dimensions[h.column_letter].width = 24
    return ws, cols

def open_wb():
    if XLSX.exists():
        return load_workbook(XLSX)
    wb = Workbook(); wb.remove(wb.active)
    return wb

def save_wb(wb):
    try:
        wb.save(XLSX)
    except PermissionError:
        raise RuntimeError("Excel file open ache — bondho kore abar submit korun (data backup.jsonl-e safe ache).")


PASSWORD = os.environ.get("APP_PASSWORD")   # optional: set to protect the app (username: any)

@app.before_request
def guard():
    if PASSWORD and (not request.authorization or request.authorization.password != PASSWORD):
        return Response("Password dorkar", 401, {"WWW-Authenticate": 'Basic realm="Supplier Collector"'})

@app.get("/")
def index():
    return app.send_static_file("index.html")

@app.get("/api/schema")
def get_schema():
    # Ensure all form columns exist in Excel
    schema = load_schema()
    try:
        with lock:
            wb = open_wb()
            for form_id, form in schema["forms"].items():
                if form.get("sheet"):  # Only for forms that save to Excel
                    sync_sheet(wb, form)
            save_wb(wb)
    except Exception as e:
        print(f"[WARNING] Could not sync all form columns: {e}")
    return jsonify(schema)

@app.post("/api/submit/<fid>")
def submit(fid):
    schema = load_schema()
    form = schema["forms"].get(fid)
    if not form:
        return jsonify(error="unknown form"), 404
    data = request.get_json(force=True)
    
    # Get company name for row matching
    company_name = data.get("company", "").strip()
    print(f"[DEBUG] Form: {fid}, Company: '{company_name}'")  # Debug log
    
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with lock:
        with BACKUP.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps({"form": fid, "ts": ts, "data": data}, ensure_ascii=False) + "\n")
        try:
            wb = open_wb()
            ws, cols = sync_sheet(wb, form)
            
            # Find existing row for this company or create new
            existing_row = None
            if company_name:
                # First ensure company column exists
                if "company" not in cols:
                    c = ws.max_column + 1
                    ws.cell(2, c, "company")
                    ws.cell(1, c, "Company Name / কোম্পানির নাম")
                    cols["company"] = c
                
                company_col = cols["company"]
                print(f"[DEBUG] Searching in column {company_col} for '{company_name}'")
                
                # Search for existing company
                for row_num in range(3, ws.max_row + 1):
                    cell_value = ws.cell(row_num, company_col).value
                    if cell_value:
                        cell_str = str(cell_value).strip().lower()
                        company_str = company_name.strip().lower()
                        print(f"[DEBUG] Row {row_num}: '{cell_str}' vs '{company_str}'")
                        if cell_str == company_str:
                            existing_row = row_num
                            print(f"[DEBUG] ✓ Match found at row: {row_num}")
                            break
                
                if not existing_row:
                    print(f"[DEBUG] No match found, creating new row")
            
            # Use existing row or create new
            r = existing_row if existing_row else max(ws.max_row + 1, 3)
            
            # Update timestamp only if new row
            if not existing_row:
                ws.cell(r, 1, ts)
            
            # Write data to cells
            for k, v in data.items():
                if k in cols:
                    cell_value = ", ".join(v) if isinstance(v, list) else v
                    ws.cell(r, cols[k], cell_value)
            
            save_wb(wb)
        except RuntimeError as e:
            return jsonify(error=str(e)), 500
    return jsonify(ok=True, row=r, updated=bool(existing_row))

@app.post("/api/field")
def add_field():
    p = request.get_json(force=True)
    label = (p.get("label") or "").strip()
    if not label:
        return jsonify(error="Label dorkar"), 400
    with lock:
        schema = load_schema()
        form = schema["forms"][p["form"]]
        keys = {f["key"] for f in all_fields(form)}
        key = re.sub(r"[^a-z0-9]+", "_", label.lower()).strip("_")[:30] or "f"
        if key in keys or not re.match(r"^[a-z]", key):
            key = "f_" + uuid.uuid4().hex[:6]
        field = {"key": key, "label": label, "type": p.get("type", "text"),
                 "required": bool(p.get("required")), "star": bool(p.get("star"))}
        if field["type"] in ("radio", "checkbox", "select"):
            field["options"] = [o.strip() for o in (p.get("options") or "").split(",") if o.strip()]
        form["sections"][int(p.get("section", 0))]["fields"].append(field)
        save_schema(schema)
        try:  # column appears in Excel immediately
            wb = open_wb(); sync_sheet(wb, form); save_wb(wb)
        except RuntimeError as e:
            return jsonify(ok=True, warning=str(e))
    return jsonify(ok=True, key=key)

@app.delete("/api/field/<fid>/<key>")
def remove_field(fid, key):
    with lock:   # removed from the form only; old Excel column and data are kept
        schema = load_schema()
        for sec in schema["forms"][fid]["sections"]:
            sec["fields"] = [f for f in sec["fields"] if f["key"] != key]
        save_schema(schema)
    return jsonify(ok=True)

@app.get("/api/download")
def download():
    with lock:
        wb = open_wb()
        for form in load_schema()["forms"].values():
            sync_sheet(wb, form)
        save_wb(wb)
    return send_file(XLSX, as_attachment=True, download_name="responses.xlsx")


if __name__ == "__main__":
    try:
        ip = socket.gethostbyname(socket.gethostname())
    except Exception:
        ip = "<PC-IP>"
    print(f"\nPC: http://localhost:5000\nPhone (same WiFi): http://{ip}:5000\n")
    app.run(host="0.0.0.0", port=5000, debug=False)
