from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.models import User, db
from app.forms import LoginForm, RegistrationForm

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = RegistrationForm()
    
    print(f"🔍 Método: {request.method}")
    print(f"🔍 Form data: {request.form}")
    print(f"🔍 Form validate_on_submit: {form.validate_on_submit()}")
    print(f"🔍 Form errors: {form.errors}")
    
    if request.method == 'POST':
        print(f"📝 Username: {request.form.get('username')}")
        print(f"📝 Email: {request.form.get('email')}")
        print(f"📝 Password: {'***' if request.form.get('password') else 'None'}")
        print(f"📝 Password2: {'***' if request.form.get('password2') else 'None'}")
        print(f"📝 CSRF Token: {request.form.get('csrf_token')}")
    
    if form.validate_on_submit():
        print(f"✅ Formulario válido - creando usuario")
        
        # Verificar si el usuario ya existe
        if User.query.filter_by(username=form.username.data).first():
            flash('El nombre de usuario ya existe', 'error')
            return render_template('register.html', form=form)
        
        if User.query.filter_by(email=form.email.data).first():
            flash('El email ya está registrado', 'error')
            return render_template('register.html', form=form)
        
        # Crear nuevo usuario
        try:
            user = User(
                username=form.username.data,
                email=form.email.data
            )
            user.set_password(form.password.data)
            
            db.session.add(user)
            db.session.commit()
            
            print(f"✅ Usuario {user.username} creado exitosamente")
            flash('¡Registro exitoso! Ya puedes iniciar sesión', 'success')
            return redirect(url_for('auth.login'))
            
        except Exception as e:
            print(f"💥 Error al guardar usuario: {e}")
            db.session.rollback()
            flash(f'Error al registrar usuario: {str(e)}', 'error')
    else:
        if request.method == 'POST':
            print(f"❌ Formulario NO válido")
            for field, errors in form.errors.items():
                for error in errors:
                    print(f"   - {field}: {error}")
                    flash(f'{field}: {error}', 'error')
    
    return render_template('register.html', form=form)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        
        if user and user.check_password(form.password.data):
            login_user(user, remember=True)
            flash(f'¡Bienvenido {user.username}!', 'success')
            return redirect(url_for('main.index'))
        else:
            flash('Usuario o contraseña incorrectos', 'error')
    
    return render_template('login.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Has cerrado sesión correctamente', 'info')
    return redirect(url_for('main.index'))