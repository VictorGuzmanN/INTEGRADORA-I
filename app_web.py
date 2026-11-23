import os
from flask import Flask, render_template_string, request, redirect, url_for, session, flash, send_from_directory
from controller.auth_controller import AuthController
from controller.doctor_controller import DoctorController
from controller.paciente_controller import PacienteController
from controller.tratamiento_controller import TratamientoController

from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "clave_por_defecto")


@app.route("/logo.png")
def logo():
    return send_from_directory(os.path.join(app.root_path, "assets"), "logo.png")


# ==========================================================
# PLANTILLAS HTML RESPONSIVAS (MÓVIL + ESCRITORIO)
# ==========================================================
HTML_LOGIN = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SIRCRA - Iniciar sesión</title>
    <link rel="apple-touch-icon" href="/logo.png">
    <link rel="icon" type="image/png" href="/logo.png">
    <style>
        * { box-sizing: border-box; font-family: 'Segoe UI', system-ui, sans-serif; }
        body { margin: 0; background: #F4F6F8; display: flex; justify-content: center; align-items: center; min-height: 100vh; padding: 16px; }
        .card { background: #FFF; border: 1px solid #111827; border-radius: 10px; padding: 28px 24px; width: 100%; max-width: 400px; box-shadow: 0 4px 12px rgba(0,0,0,0.06); }
        .logo-box { text-align: center; margin-bottom: 12px; }
        .logo-box img { max-width: 170px; height: auto; }
        h2 { margin: 0 0 6px; color: #111827; font-size: 20px; }
        p.sub { margin: 0 0 18px; color: #6B7280; font-size: 13px; }
        label { display: block; font-size: 13px; font-weight: 600; color: #111827; margin-bottom: 5px; }
        input { width: 100%; padding: 11px; border: 1px solid #D1D5DB; border-radius: 6px; font-size: 15px; margin-bottom: 14px; }
        button { width: 100%; background: #009966; color: #FFF; border: none; padding: 12px; border-radius: 6px; font-size: 15px; font-weight: 700; cursor: pointer; }
        button:active { background: #007A52; }
        .alert { background: #FEE2E2; color: #991B1B; padding: 10px; border-radius: 6px; font-size: 13px; margin-bottom: 14px; }
        .link-olvido { display: block; text-align: center; margin-top: 14px; color: #111827; font-weight: 600; font-size: 13px; text-decoration: none; }
    </style>
</head>
<body>
    <div class="card">
        <div class="logo-box"><img src="/logo.png" alt="SIRCRA"></div>
        <h2>Iniciar sesión</h2>
        <p class="sub">Ingresa tus credenciales para acceder a tu cuenta.</p>
        {% with messages = get_flashed_messages() %}
            {% if messages %}
                {% for m in messages %}<div class="alert">{{ m }}</div>{% endfor %}
            {% endif %}
        {% endwith %}
        <form method="POST">
            <label>Usuario</label>
            <input type="text" name="usuario" placeholder="Ingresa tu usuario" required>
            <label>Contraseña</label>
            <input type="password" name="contrasena" placeholder="Ingresa tu contraseña" required>
            <button type="submit">Iniciar sesión</button>
        </form>
        <a href="{{ url_for('recuperar') }}" class="link-olvido">Olvidé mi contraseña</a>
    </div>
</body>
</html>
"""

HTML_RECUPERAR = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SIRCRA - Recuperar contraseña</title>
    <style>
        * { box-sizing: border-box; font-family: 'Segoe UI', system-ui, sans-serif; }
        body { margin: 0; background: #F4F6F8; display: flex; justify-content: center; align-items: center; min-height: 100vh; padding: 16px; }
        .card { background: #FFF; border: 1px solid #111827; border-radius: 10px; padding: 28px 24px; width: 100%; max-width: 400px; }
        h2 { margin: 0 0 6px; color: #111827; }
        p.sub { margin: 0 0 18px; color: #6B7280; font-size: 13px; }
        label { display: block; font-size: 13px; font-weight: 600; margin-bottom: 5px; }
        input { width: 100%; padding: 11px; border: 1px solid #D1D5DB; border-radius: 6px; font-size: 15px; margin-bottom: 14px; }
        button { width: 100%; background: #009966; color: #FFF; border: none; padding: 12px; border-radius: 6px; font-size: 15px; font-weight: 700; cursor: pointer; }
        .alert { background: #FEF3C7; color: #92400E; padding: 10px; border-radius: 6px; font-size: 13px; margin-bottom: 14px; }
        .volver { display: block; text-align: center; margin-top: 14px; color: #6B7280; font-size: 13px; text-decoration: none; }
    </style>
</head>
<body>
    <div class="card">
        <h2>Restablecer contraseña</h2>
        <p class="sub">Ingresa tu nombre de usuario y define una nueva contraseña.</p>
        {% with messages = get_flashed_messages() %}
            {% if messages %}{% for m in messages %}<div class="alert">{{ m }}</div>{% endfor %}{% endif %}
        {% endwith %}
        <form method="POST">
            <label>Nombre de usuario</label>
            <input type="text" name="usuario" placeholder="Tu usuario registrado" required>
            <label>Nueva contraseña</label>
            <input type="password" name="nueva_contrasena" placeholder="Nueva contraseña" required>
            <button type="submit">Guardar datos</button>
        </form>
        <a href="{{ url_for('login') }}" class="volver">Volver a iniciar sesión</a>
    </div>
</body>
</html>
"""

HTML_PANEL = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SIRCRA Móvil</title>
    <link rel="apple-touch-icon" href="/logo.png">
    <style>
        * { box-sizing: border-box; font-family: 'Segoe UI', system-ui, sans-serif; }
        body { margin: 0; background: #F4F6F8; color: #111827; padding-bottom: 40px; }
        header { background: #FFF; padding: 12px 16px; border-bottom: 1px solid #E5E7EB; display: flex; justify-content: space-between; align-items: center; position: sticky; top: 0; z-index: 10; }
        .brand { display: flex; align-items: center; gap: 10px; font-weight: 800; font-size: 18px; }
        .brand img { height: 34px; }
        .user-info { font-size: 12px; color: #4B5563; display: flex; align-items: center; gap: 10px; }
        .btn-salir { border: 1px solid #111827; background: #FFF; color: #111827; padding: 5px 10px; border-radius: 6px; text-decoration: none; font-weight: 600; font-size: 12px; }
        nav { display: flex; overflow-x: auto; background: #E5E7EB; padding: 8px; gap: 6px; }
        nav a { text-decoration: none; color: #1F2937; padding: 9px 14px; border-radius: 6px; font-size: 13px; font-weight: 700; white-space: nowrap; }
        nav a.activo { background: #A7F3D0; color: #065F46; }
        .container { max-width: 900px; margin: 16px auto; padding: 0 14px; }
        .card { background: #FFF; border-radius: 10px; padding: 18px; margin-bottom: 16px; box-shadow: 0 1px 4px rgba(0,0,0,0.05); }
        h3 { margin: 0 0 12px; font-size: 18px; }
        .grid-form { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 10px; }
        label { font-size: 12px; font-weight: 700; display: block; margin-bottom: 4px; }
        input, select { width: 100%; padding: 9px; border: 1px solid #D1D5DB; border-radius: 6px; font-size: 14px; }
        .btn-verde { background: #009966; color: #FFF; border: none; padding: 11px 16px; border-radius: 6px; font-weight: 700; font-size: 14px; cursor: pointer; margin-top: 12px; width: 100%; }
        .table-wrap { overflow-x: auto; }
        table { width: 100%; border-collapse: collapse; font-size: 13px; }
        th, td { text-align: left; padding: 10px 8px; border-bottom: 1px solid #E5E7EB; white-space: nowrap; }
        th { background: #F9FAFB; color: #374151; }
        .btn-del { background: #111827; color: #FFF; border: none; padding: 5px 10px; border-radius: 4px; font-size: 12px; text-decoration: none; }
        .flash { background: #D1FAE5; color: #065F46; padding: 10px 14px; border-radius: 6px; margin-bottom: 14px; font-size: 13px; font-weight: 600; }
    </style>
</head>
<body>
    <header>
        <div class="brand"><img src="/logo.png" alt="Logo"> SIRCRA</div>
        <div class="user-info">
            <span>{{ usuario }} ({{ rol }})</span>
            <a href="{{ url_for('logout') }}" class="btn-salir">Salir</a>
        </div>
    </header>

    <nav>
        <a href="{{ url_for('panel', tab='pacientes') }}" class="{{ 'activo' if tab == 'pacientes' else '' }}">Pacientes</a>
        {% if rol_norm == 'total' %}
            <a href="{{ url_for('panel', tab='doctores') }}" class="{{ 'activo' if tab == 'doctores' else '' }}">Doctores</a>
        {% endif %}
        <a href="{{ url_for('panel', tab='tratamientos') }}" class="{{ 'activo' if tab == 'tratamientos' else '' }}">Tratamientos</a>
        {% if rol_norm == 'total' %}
            <a href="{{ url_for('panel', tab='usuarios') }}" class="{{ 'activo' if tab == 'usuarios' else '' }}">Usuarios</a>
        {% endif %}
    </nav>

    <div class="container">
        {% with messages = get_flashed_messages() %}
            {% if messages %}{% for m in messages %}<div class="flash">{{ m }}</div>{% endfor %}{% endif %}
        {% endwith %}

        {% if tab == 'pacientes' %}
            {% if rol_norm in ('total', 'doctor') %}
            <div class="card">
                <h3>Registrar paciente</h3>
                <form method="POST" action="{{ url_for('guardar_paciente') }}">
                    <div class="grid-form">
                        <div><label>Nombre</label><input type="text" name="nombre" required></div>
                        <div><label>Primer Apellido</label><input type="text" name="apellido1" required></div>
                        <div><label>Segundo Apellido</label><input type="text" name="apellido2"></div>
                        <div><label>Teléfono</label><input type="text" name="telefono" required></div>
                        <div><label>Tipo de sangre</label><input type="text" name="tipo_sangre" placeholder="Ej. O+" required></div>
                        <div><label>Alergias</label><input type="text" name="alergias" placeholder="Ninguna"></div>
                    </div>
                    <button type="submit" class="btn-verde">Guardar paciente</button>
                </form>
            </div>
            {% endif %}
            <div class="card">
                <h3>Lista de pacientes</h3>
                <div class="table-wrap">
                    <table>
                        <tr><th>ID</th><th>Nombre</th><th>Teléfono</th><th>Sangre</th><th>Estado</th>{% if rol_norm in ('total', 'doctor') %}<th>Acción</th>{% endif %}</tr>
                        {% for p in pacientes %}
                        <tr>
                            <td>{{ p.id_paciente }}</td>
                            <td>{{ p.nombre }} {{ p.apellido1 }}</td>
                            <td>{{ p.telefono }}</td>
                            <td>{{ p.tipo_sangre }}</td>
                            <td>{{ p.estado_paciente }}</td>
                            {% if rol_norm in ('total', 'doctor') %}
                            <td><a href="{{ url_for('borrar_paciente', id_paciente=p.id_paciente) }}" class="btn-del" onclick="return confirm('¿Eliminar paciente?')">Eliminar</a></td>
                            {% endif %}
                        </tr>
                        {% endfor %}
                    </table>
                </div>
            </div>

        {% elif tab == 'doctores' and rol_norm == 'total' %}
            <div class="card">
                <h3>Registrar doctor</h3>
                <form method="POST" action="{{ url_for('guardar_doctor') }}">
                    <div class="grid-form">
                        <div><label>Nombre</label><input type="text" name="nombre" required></div>
                        <div><label>Primer Apellido</label><input type="text" name="apellido1" required></div>
                        <div><label>Especialidad</label><input type="text" name="especialidad" required></div>
                        <div><label>Cédula Profesional</label><input type="text" name="numero_cedula" required></div>
                        <div><label>Teléfono</label><input type="text" name="telefono"></div>
                    </div>
                    <button type="submit" class="btn-verde">Guardar doctor</button>
                </form>
            </div>
            <div class="card">
                <h3>Lista de doctores</h3>
                <div class="table-wrap">
                    <table>
                        <tr><th>ID</th><th>Nombre</th><th>Especialidad</th><th>Cédula</th><th>Acción</th></tr>
                        {% for d in doctores %}
                        <tr>
                            <td>{{ d.id_doctor }}</td>
                            <td>{{ d.nombre }} {{ d.apellido1 }}</td>
                            <td>{{ d.especialidad }}</td>
                            <td>{{ d.numero_cedula }}</td>
                            <td><a href="{{ url_for('borrar_doctor', id_doctor=d.id_doctor) }}" class="btn-del" onclick="return confirm('¿Eliminar doctor?')">Eliminar</a></td>
                        </tr>
                        {% endfor %}
                    </table>
                </div>
            </div>

        {% elif tab == 'tratamientos' %}
            {% if rol_norm in ('total', 'doctor') %}
            <div class="card">
                <h3>Asignar tratamiento</h3>
                <form method="POST" action="{{ url_for('guardar_tratamiento') }}">
                    <div class="grid-form">
                        <div>
                            <label>Doctor</label>
                            <select name="id_doctor" required>
                                {% for d in doctores %}
                                    <option value="{{ d.id_doctor }}">{{ d.id_doctor }} - {{ d.nombre }} {{ d.apellido1 }}</option>
                                {% endfor %}
                            </select>
                        </div>
                        <div>
                            <label>Paciente</label>
                            <select name="id_paciente" required>
                                {% for p in pacientes %}
                                    <option value="{{ p.id_paciente }}">{{ p.id_paciente }} - {{ p.nombre }} {{ p.apellido1 }}</option>
                                {% endfor %}
                            </select>
                        </div>
                        <div><label>Fecha</label><input type="date" name="fecha" required></div>
                        <div><label>Hora</label><input type="time" name="hora" value="10:00" required></div>
                        <div><label>Tratamiento</label><input type="text" name="tratamiento" required></div>
                        <div><label>Diagnóstico Inicial</label><input type="text" name="diagnostico_inicial" required></div>
                        <div><label>Fecha Entrada</label><input type="date" name="fecha_entrada" required></div>
                    </div>
                    <button type="submit" class="btn-verde">Guardar tratamiento</button>
                </form>
            </div>
            {% endif %}
            <div class="card">
                <h3>Tratamientos registrados</h3>
                <div class="table-wrap">
                    <table>
                        <tr><th>ID</th><th>Doctor</th><th>Paciente</th><th>Fecha</th><th>Tratamiento</th><th>Diagnóstico</th>{% if rol_norm in ('total', 'doctor') %}<th>Acción</th>{% endif %}</tr>
                        {% for t in tratamientos %}
                        <tr>
                            <td>{{ t.id_tratamiento }}</td>
                            <td>{{ t.doctor_nombre }}</td>
                            <td>{{ t.paciente_nombre }}</td>
                            <td>{{ t.fecha }}</td>
                            <td>{{ t.tratamiento }}</td>
                            <td>{{ t.diagnostico_inicial }}</td>
                            {% if rol_norm in ('total', 'doctor') %}
                            <td><a href="{{ url_for('borrar_tratamiento', id_tratamiento=t.id_tratamiento) }}" class="btn-del" onclick="return confirm('¿Eliminar tratamiento?')">Eliminar</a></td>
                            {% endif %}
                        </tr>
                        {% endfor %}
                    </table>
                </div>
            </div>

        {% elif tab == 'usuarios' and rol_norm == 'total' %}
            <div class="card">
                <h3>Registrar usuario</h3>
                <form method="POST" action="{{ url_for('guardar_usuario') }}">
                    <div class="grid-form">
                        <div><label>Nombre de Usuario</label><input type="text" name="usuario" required></div>
                        <div><label>Contraseña</label><input type="password" name="contrasena" required></div>
                        <div>
                            <label>Rol / Privilegios</label>
                            <select name="rol">
                                <option value="Doctor">Doctor</option>
                                <option value="Paciente">Paciente</option>
                                <option value="Total">Total (Admin)</option>
                            </select>
                        </div>
                    </div>
                    <button type="submit" class="btn-verde">Registrar usuario</button>
                </form>
            </div>
            <div class="card">
                <h3>Usuarios registrados</h3>
                <div class="table-wrap">
                    <table>
                        <tr><th>ID</th><th>Usuario</th><th>Rol</th><th>Acción</th></tr>
                        {% for u in usuarios %}
                        <tr>
                            <td>{{ u.id_admin }}</td>
                            <td>{{ u.usuario }}</td>
                            <td>{{ u.privilegios }}</td>
                            <td><a href="{{ url_for('borrar_usuario', id_admin=u.id_admin) }}" class="btn-del" onclick="return confirm('¿Eliminar usuario?')">Eliminar</a></td>
                        </tr>
                        {% endfor %}
                    </table>
                </div>
            </div>
        {% endif %}
    </div>
</body>
</html>
"""


# ==========================================================
# RUTAS DE NAVEGACIÓN Y CRUD
# ==========================================================
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario = request.form.get("usuario", "").strip()
        contrasena = request.form.get("contrasena", "").strip()
        admin = AuthController.iniciar_sesion(usuario, contrasena)
        if admin:
            session["usuario"] = admin.usuario
            session["rol"] = admin.privilegios
            return redirect(url_for("panel", tab="pacientes"))
        flash("Usuario o contraseña incorrectos.")
    return render_template_string(HTML_LOGIN)


@app.route("/recuperar", methods=["GET", "POST"])
def recuperar():
    if request.method == "POST":
        usuario = request.form.get("usuario", "").strip()
        nueva = request.form.get("nueva_contrasena", "").strip()
        ok, msg = AuthController.restablecer_contrasena(usuario, nueva)
        flash(msg)
        if ok:
            return redirect(url_for("login"))
    return render_template_string(HTML_RECUPERAR)


@app.route("/panel")
def panel():
    if "usuario" not in session:
        return redirect(url_for("login"))
    tab = request.args.get("tab", "pacientes")
    rol_norm = session["rol"].strip().lower()
    return render_template_string(
        HTML_PANEL,
        tab=tab,
        usuario=session["usuario"],
        rol=session["rol"],
        rol_norm=rol_norm,
        pacientes=PacienteController.obtener_pacientes(),
        doctores=DoctorController.obtener_doctores(),
        tratamientos=TratamientoController.obtener_tratamientos(),
        usuarios=AuthController.obtener_usuarios() if rol_norm == "total" else []
    )


@app.route("/paciente/guardar", methods=["POST"])
def guardar_paciente():
    ok, msg = PacienteController.crear_paciente(
        nombre=request.form.get("nombre", ""),
        apellido1=request.form.get("apellido1", ""),
        apellido2=request.form.get("apellido2", ""),
        telefono=request.form.get("telefono", ""),
        tipo_sangre=request.form.get("tipo_sangre", ""),
        alergias=request.form.get("alergias", "")
    )
    flash(msg)
    return redirect(url_for("panel", tab="pacientes"))


@app.route("/paciente/borrar/<int:id_paciente>")
def borrar_paciente(id_paciente):
    ok, msg = PacienteController.eliminar_paciente(id_paciente)
    flash(msg)
    return redirect(url_for("panel", tab="pacientes"))


@app.route("/doctor/guardar", methods=["POST"])
def guardar_doctor():
    ok, msg = DoctorController.crear_doctor(
        nombre=request.form.get("nombre", ""),
        apellido1=request.form.get("apellido1", ""),
        especialidad=request.form.get("especialidad", ""),
        numero_cedula=request.form.get("numero_cedula", ""),
        telefono=request.form.get("telefono", "")
    )
    flash(msg)
    return redirect(url_for("panel", tab="doctores"))


@app.route("/doctor/borrar/<int:id_doctor>")
def borrar_doctor(id_doctor):
    ok, msg = DoctorController.eliminar_doctor(id_doctor)
    flash(msg)
    return redirect(url_for("panel", tab="doctores"))


@app.route("/tratamiento/guardar", methods=["POST"])
def guardar_tratamiento():
    ok, msg = TratamientoController.crear_tratamiento(
        id_doctor=request.form.get("id_doctor"),
        id_paciente=request.form.get("id_paciente"),
        fecha=request.form.get("fecha"),
        hora=request.form.get("hora"),
        tratamiento=request.form.get("tratamiento"),
        diagnostico_inicial=request.form.get("diagnostico_inicial"),
        fecha_entrada=request.form.get("fecha_entrada")
    )
    flash(msg)
    return redirect(url_for("panel", tab="tratamientos"))


@app.route("/tratamiento/borrar/<int:id_tratamiento>")
def borrar_tratamiento(id_tratamiento):
    ok, msg = TratamientoController.eliminar_tratamiento(id_tratamiento)
    flash(msg)
    return redirect(url_for("panel", tab="tratamientos"))


@app.route("/usuario/guardar", methods=["POST"])
def guardar_usuario():
    ok, msg = AuthController.registrar_usuario(
        usuario=request.form.get("usuario", ""),
        contrasena=request.form.get("contrasena", ""),
        rol=request.form.get("rol", "Doctor")
    )
    flash(msg)
    return redirect(url_for("panel", tab="usuarios"))


@app.route("/usuario/borrar/<int:id_admin>")
def borrar_usuario(id_admin):
    ok, msg = AuthController.eliminar_usuario(id_admin)
    flash(msg)
    return redirect(url_for("panel", tab="usuarios"))


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


if __name__ == "__main__":
    # host="0.0.0.0" permite entrar desde tu celular en la misma red Wi-Fi
    app.run(host="0.0.0.0", port=5000, debug=True)