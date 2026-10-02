# Supplier Collector
1. `pip install -r requirements.txt`
2. `python app.py` -> terminal-e PC ar Phone-er link dekhabe.
3. Data: `data/responses.xlsx` (Suppliers, Interviews sheet). Safety copy: `data/backup.jsonl`

## Phone theke use
- Same WiFi: phone browser-e terminal-er "Phone" link kholen (Windows firewall allow korte hote pare).
- Bairer (mobile data) theke: PC chalu rekhe `cloudflared tunnel --url http://localhost:5000` (ba ngrok) chalan -> public link pabe.
  Public link dile age password din:  Windows: `set APP_PASSWORD=yourpass`  Mac/Linux: `export APP_PASSWORD=yourpass` (python app.py cholar age). Browser-e password chaibe, username kichu likhlei hobe.
- Permanent: kono server/VPS/Render-e deploy korun, data/ folder persistent rakhben.

Notun field: "Fields" tab theke add korun -> form + Excel column auto toiri.
Excel file open thakle save hobe na (backup.jsonl-e data safe thake).
