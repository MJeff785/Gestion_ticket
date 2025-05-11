from flask import Flask, render_template, request, redirect, url_for, session, flash, abort
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from flask_mail import Message
from connection import mail

def determiner_priorite(description):
    # Mots-clés pour chaque niveau de priorité
    mots_haute_priorite = ['urgent', 'critique', 'panne', 'bloqué', 'impossible', 'erreur grave', 
                          'ne fonctionne plus', 'immédiat', 'emergency']
    mots_moyenne_priorite = ['problème', 'bug', 'erreur', 'dysfonctionnement', 'lent', 
                            'ralentissement', 'mise à jour']
    
    description = description.lower()
    
    # Vérification de la priorité
    for mot in mots_haute_priorite:
        if mot in description:
            return 'Haute'
            
    for mot in mots_moyenne_priorite:
        if mot in description:
            return 'Moyenne'
    
    return 'Basse'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/ticket'
app.config['SQLALCHEMY_POOL_RECYCLE'] = 280
app.config['SQLALCHEMY_POOL_TIMEOUT'] = 20
app.config['SQLALCHEMY_POOL_SIZE'] = 30
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'votre_clé_secrète_ici'

# Add Flask-Mail configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'maizeroi.gerson@gmail.com'  # Replace with your email
app.config['MAIL_PASSWORD'] = 'lruk kial hpic ulfc'     # Replace with your app password
app.config['MAIL_DEFAULT_SENDER'] = 'maizeroi.gerson@gmail.com'

db = SQLAlchemy(app)
mail.init_app(app)  # Initialize Flask-Mail with your app

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

class ResolvedTicket(db.Model):
    __tablename__ = 'resolved_tickets'
    id = db.Column(db.Integer, primary_key=True)
    original_ticket_id = db.Column(db.Integer, nullable=False)
    titre = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    priorite = db.Column(db.String(20), nullable=False)
    date_creation = db.Column(db.DateTime, nullable=False)
    date_resolution = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    resolved_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

class Ticket(db.Model):
    __tablename__ = 'tickets'  # Specify the table name
    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    priorite = db.Column(db.String(20), nullable=False)
    statut = db.Column(db.String(20), default='En attente')
    date_creation = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    assignee_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', foreign_keys=[user_id], backref='created_tickets')
    assignee = db.relationship('User', foreign_keys=[assignee_id], backref='assigned_tickets')

# Add after the imports
def is_first_run():
    return User.query.count() == 0

@app.route('/setup', methods=['GET', 'POST'])
def setup():
    if not is_first_run():
        flash('Setup already completed')
        return redirect(url_for('login'))
        
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']  # Add email field
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            flash('Passwords do not match')
            return redirect(url_for('setup'))

        admin = User(
            username=username,
            email=email,  # Add email
            password=generate_password_hash(password),
            is_admin=True
        )
        db.session.add(admin)
        db.session.commit()

        flash('Admin account created successfully! Please login.')
        return redirect(url_for('login'))

    return render_template('setup.html')

# Modify the login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if is_first_run():
        return redirect(url_for('setup'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['is_admin'] = user.is_admin
            return redirect(url_for('index'))  # Vérifiez cette ligne
        flash('Invalid username or password')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# Decorators for route protection
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session or not session.get('is_admin'):
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
@login_required
def index():
    if session.get('is_admin'):
        tickets = Ticket.query.order_by(Ticket.date_creation.desc()).all()
    else:
        tickets = Ticket.query.filter_by(user_id=session['user_id']).order_by(Ticket.date_creation.desc()).all()
    return render_template('index.html', tickets=tickets)

@app.route('/ajouter_ticket', methods=['GET', 'POST'])
@login_required
def ajouter_ticket():
    if request.method == 'POST':
        titre = request.form['titre']
        description = request.form['description']
        priorite = determiner_priorite(description)
        
        nouveau_ticket = Ticket(
            titre=titre,
            description=description,
            priorite=priorite,
            user_id=session['user_id']
        )
        db.session.add(nouveau_ticket)
        db.session.commit()
        flash('Ticket créé avec succès!', 'success')
        return redirect(url_for('index'))
    return render_template('ajouter_ticket.html')

@app.route('/modifier_ticket/<int:ticket_id>', methods=['GET', 'POST'])
@login_required
def modifier_ticket(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)
    if not session.get('is_admin') and ticket.user_id != session['user_id']:  # Fixed: users_id to user_id
        abort(403)
    
    if request.method == 'POST':
        ticket.titre = request.form['titre']
        ticket.description = request.form['description']
        if session.get('is_admin'):
            ticket.priorite = request.form['priorite']
            ticket.statut = request.form['statut']
            assignee_id = request.form.get('assignee_id')
            ticket.assignee_id = int(assignee_id) if assignee_id else None
        
        db.session.commit()
        flash('Ticket modifié avec succès!', 'success')
        return redirect(url_for('index'))
    
    users = User.query.all() if session.get('is_admin') else None
    return render_template('modifier_ticket.html', ticket=ticket, users=users)

@app.route('/supprimer_ticket/<int:ticket_id>', methods=['POST'])
@login_required
def supprimer_ticket(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)
    if not session.get('is_admin') and ticket.user_id != session['user_id']:
        abort(403)
    
    db.session.delete(ticket)
    db.session.commit()
    flash('Ticket supprimé avec succès!', 'success')
    return redirect(url_for('index'))

@app.route('/changer_statut/<int:ticket_id>', methods=['POST'])
@login_required
def changer_statut(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)
    if not session.get('is_admin') and ticket.assignee_id != session['user_id']:
        abort(403)
    
    nouveau_statut = request.form.get('statut')
    if nouveau_statut in ['En attente', 'En cours', 'Résolu']:
        ticket.statut = nouveau_statut
        db.session.commit()
        flash('Statut du ticket mis à jour!', 'success')
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']  # Add email field
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # Check if user or email already exists
        user_exists = User.query.filter_by(username=username).first()
        email_exists = User.query.filter_by(email=email).first()
        
        if user_exists:
            flash('Username already exists')
            return redirect(url_for('register'))
        if email_exists:
            flash('Email already exists')
            return redirect(url_for('register'))

        if password != confirm_password:
            flash('Passwords do not match')
            return redirect(url_for('register'))

        # Create new user
        new_user = User(
            username=username,
            email=email,  # Add email
            password=generate_password_hash(password),
            is_admin=False
        )
        db.session.add(new_user)
        db.session.commit()

        flash('Account created successfully! Please login.')
        return redirect(url_for('login'))

    return render_template('register.html')
    # Remove the duplicate return statement below
    # return render_template('ajouter_ticket.html')

@app.route('/historique')
@admin_required
def historique():
    resolved_tickets = ResolvedTicket.query.order_by(ResolvedTicket.date_resolution.desc()).all()
    return render_template('historique.html', tickets=resolved_tickets)

def send_resolution_email(user_email, ticket_titre):
    msg = Message('Ticket Résolu',
                  sender='your-email@gmail.com',
                  recipients=[user_email])
    
    msg.body = f"""
    Bonjour,
    
    Votre ticket "{ticket_titre}" a été résolu.
    
    Cordialement,
    L'équipe support
    """
    
    mail.send(msg)

@app.route('/resoudre_ticket/<int:ticket_id>', methods=['POST'])
@admin_required
def resoudre_ticket(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)
    user = User.query.get(ticket.user_id)
    
    # Create historical record
    resolved_ticket = ResolvedTicket(
        original_ticket_id=ticket.id,
        titre=ticket.titre,
        description=ticket.description,
        priorite=ticket.priorite,
        date_creation=ticket.date_creation,
        user_id=ticket.user_id,
        resolved_by=session['user_id']
    )
    
    # Send email notification
    send_resolution_email(user.email, ticket.titre)
    
    # Save to history and delete original ticket
    db.session.add(resolved_ticket)
    db.session.delete(ticket)
    db.session.commit()
    
    flash('Ticket marqué comme résolu et déplacé dans l\'historique')
    return redirect(url_for('index'))

@app.route('/calendrier')
@admin_required
def calendrier():
    tickets = Ticket.query.all()
    # Format tickets for calendar
    calendar_events = []
    for ticket in tickets:
        calendar_events.append({
            'id': ticket.id,
            'title': ticket.titre,
            'start': ticket.date_creation.strftime('%Y-%m-%d %H:%M:%S'),
            'description': ticket.description,
            'priority': ticket.priorite,
            'status': ticket.statut
        })
    return render_template('calendrier.html', events=calendar_events)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)