
# Sistem de Gestionare a Angajaților

Aplicația este un sistem de gestionare a angajaților bazat pe Flask. Permite înregistrarea, autentificarea și administrarea informațiilor angajaților.

## Instrucțiuni de Instalare

1. **Clonare sau Descărcare**: 
   - Clonați acest repository folosind `git clone [URL_REPOSITORY]` sau descărcați-l direct din platforma.

2. **Crearea unui Mediu Virtual**:
   - Navigați în directorul proiectului: `cd EmployeeManagementSystem`
   - Creați un mediu virtual: `python -m venv venv`

3. **Activare Mediu Virtual**:
   - Windows: `venv\Scripts activate`
   - PowerShell: `.\venv\Scripts\Activate`
   - Linux/MacOS: `source venv/bin/activate`

4. **Setare environment variable a FLASK_APP
   - Setați variabila environment folosind: `$env:FLASK_APP="myapp:create_app"`

5. **Setare environment variable a FLASK_CONFIG
   - Setați variabila environment folosind: `$env:FLASK_CONFIG="development"` sau `$env:FLASK_CONFIG="production"` sau `$env:FLASK_CONFIG="testing"`

6. **Instalare Dependințe**:
   - Instalați toate pachetele necesare folosind: `pip install -r requirements.txt`

7. **Configurare Bază de Date**:
   - Inițializați baza de date: `flask db init`
   - Aplicați migrările: `flask db migrate`
   - Actualizați baza de date: `flask db upgrade`

8. **Rulare Aplicație**:
   - Rulați aplicația folosind: `flask run`
   - Accesați aplicația în browser la adresa: `http://127.0.0.1:5000/`

