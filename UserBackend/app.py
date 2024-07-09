import jwt
import datetime
from flask import Flask, jsonify, request, url_for
from flask_cors import CORS
from functools import wraps
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
from itsdangerous import SignatureExpired, URLSafeTimedSerializer
from werkzeug.security import generate_password_hash, check_password_hash
from config import config
from sqlalchemy.exc import IntegrityError
import uuid
from sqlalchemy.dialects.postgresql import UUID

from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = 'your_secret_key'


if config.DB_CONNECTED:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///game.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db = SQLAlchemy(app)
    with app.app_context():
        db.create_all()

    # User table
    class User(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        username = db.Column(db.String(80), unique=True, nullable=False)
        display_name = db.Column(db.String(80), nullable=False, default="haha") # todo: remove default, fix frontend
        password = db.Column(db.String(200), nullable=False)
        email = db.Column(db.String(120), unique=True, nullable=False)
        elo = db.Column(db.Integer, default=1100)
        deck_id = db.Column(db.Integer, db.ForeignKey('deck.id'), default=None)
        email_confirm = db.Column(db.Boolean, nullable=False, default=False)

    # Deck table
    class Deck(db.Model):
        id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
        ability = db.Column(db.String(50), nullable=False)
        count = db.Column(db.Integer, nullable=False)
        secondary_id = db.Column(db.Integer, nullable=False)
        
        __table_args__ = (
            db.UniqueConstraint('secondary_id', 'ability', name='_deck_secondary_id_ability_uc'),
        )

    # Game table
    class Game(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        game_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
        user_ids = db.Column(db.JSON, nullable=False)  # Example: [1, 2, 3, 4]
        user_ranks = db.Column(db.JSON, nullable=False)  # Example: {"1": "1st", "2": "2nd", "3": "3rd", "4": "4th"}


    with app.app_context():
    # def create_tables():
        # Deck.__table__.drop(db.engine)
        db.create_all()

# for the email register
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'lavavaacc@gmail.com'
app.config['MAIL_PASSWORD'] = 'enwueidxiwivjvxn'  # Use the app password you generated
mail = Mail(app)

s = URLSafeTimedSerializer(app.config['SECRET_KEY']) # serializer

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]  # Assuming bearer token is used
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = data['user']
        except:
            return jsonify({'message': 'Token is invalid!'}), 401
        
        return f(current_user, *args, **kwargs)
    
    return decorated

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if config.DB_CONNECTED: 
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password) and user.email_confirm:
            token = jwt.encode({
                'user_id': user.id,
                'user': username,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=72)
            }, app.config['SECRET_KEY'], algorithm="HS256")
            return jsonify({"token": token}), 200

    elif username.lower() in ('default', 'other'):
        token = jwt.encode({
            'user': username,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=72)  # Token expires in 24 hours
        }, app.config['SECRET_KEY'], algorithm="HS256")
        return jsonify({"token": token}), 200
    
    if user.email_confirm == False:
        return jsonify({"message": "Email not confirmed"}), 401
    return jsonify({"message": "Invalid credentials"}), 401
    
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    email = data.get('email')  # Email is received and will be used to send welcome email
    password = data.get('password') # password received and used to check requirements before sending email
    display_name = ""

    if config.DB_CONNECTED:
        if User.query.filter_by(username=username).first():
            return jsonify({"success": False, "message": "Username already exists"}), 400
        if User.query.filter_by(email=email).first():
            return jsonify({"success": False, "message": "Account with this email already exists"}), 400
        if len(password) < 8: # checks for password requirements
            return jsonify({"success": False, "message": "Password must be at least 8 characters long"}), 400
        if not any(char.islower() for char in password):
            return jsonify({"success": False, "message": "Password must have at least one lowercase letter"}), 400
        if not any(char.isupper() for char in password):
            return jsonify({"success": False, "message": "Password must have at least one uppercase letter"}), 400
        token = s.dumps(email, salt='email-confirm')
        link = url_for('confirm_email', token=token, _external=True)
        send_confirmation_email(email, link)  # Send confirm email
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(username=username, display_name="haha", email=email, password=hashed_password) # type: ignore
        db.session.add(new_user)
        db.session.commit()

        return jsonify({"success": True, "message": "Registration successful"}), 200

    else:
        token = s.dumps(email, salt='email-confirm')
        link = url_for('confirm_email', token=token, _external=True)

        if len(password) < 8: # checks for password requirements
            return jsonify({"success": False, "message": "Password must be at least 8 characters long"}), 400
        if not any(char.islower() for char in password):
            return jsonify({"success": False, "message": "Password must have at least one lowercase letter"}), 400
        if not any(char.isupper() for char in password):
            return jsonify({"success": False, "message": "Password must have at least one uppercase letter"}), 400
        if username.lower() in ('default', 'other'):
            send_confirmation_email(email, link)  # Send confirm email
            return jsonify({"success": True, "message": "Registration successful. Please follow the confirmation email sent to: {}".format(email)}), 200
        else:
            return jsonify({"success": False, "message": "Registration failed, username must be 'default or other'"}), 400


@app.route('/confirm_email/<token>')
def confirm_email(token):
    try:
        email = s.loads(token, salt='email-confirm', max_age=3600) # token expires after 1 hour
    except SignatureExpired:
        return '<h1>Email confirmation link expired!</h1>' # token expired
    except:
        return '<h1>Error!</h1>' # other error like incorrect token
    if config.DB_CONNECTED:
        user = User.query.filter_by(email=email).first()
        user.email_confirm = True
        db.session.commit()
    return '<h1>Email Confirmed!</h1><p>Proceed to login page to login.</p>' 

#  sending email for registration
def send_confirmation_email(user_email, link):
    msg = Message("Email Confirmation!",
                  sender='lavavaacc@gmail.com',
                  recipients=[user_email])
    msg.body = 'Follow the link to confirm your account: {}'.format(link)
    try:
        mail.send(msg)
        return "Email sent successfully!"
    except Exception as e:
        print(f"Failed to send email: {e}")
        return "Error sending email."


@app.route('/user_abilities', methods=['GET'])
@token_required
def get_home(current_user):
    # NEEDS ACTUAL DB QUERIES
    if config.DB_CONNECTED:
        user = User.query.filter_by(username=current_user).first()
        if user and user.deck_id:
            deck = Deck.query.filter_by(id=user.deck_id).first()
            return jsonify({
                "abilities": user_decks(current_user)
            })
        else:
            return jsonify({"error": "User not found or no deck assigned"}), 404
    
    elif current_user in {"default", "other"}:
        return jsonify({
            "abilities": user_decks(current_user),
        })
    else:
        return jsonify({"error": "User not found"}), 404


@app.route('/profile', methods=['GET'])
@token_required
def get_profile(current_user):
    if config.DB_CONNECTED:
        user = User.query.filter_by(username=current_user).first()
        if user:
            games = Game.query.filter(Game.user_ids.contains(str(user.id))).order_by(Game.game_date.desc()).limit(3).all()
            past_games = [game.user_ranks.get(str(user.id), "N/A") for game in games]
            return jsonify({
                "userName": user.username,
                "displayName": user.display_name,
                "email": user.email,
                "abilities": user_decks(current_user),
                "elo": user.elo,
                "past_games": past_games
            })
        else:
            return jsonify({"error": "User not found"}), 404
    else:
        return jsonify({
            "userName": "Default-User",
            "displayName": "John Doe",
            "email": "john.doe@example.com",
            "abilities": user_decks(current_user),
            "elo": 1138,
            "past_games": ["1st", "4th", "2nd"]
        })
    

def user_decks(current_user):
    if config.DB_CONNECTED:
        user = User.query.filter_by(username=current_user).first()
        if user:
            decks = Deck.query.filter_by(secondary_id=user.id).all()
            abilities = [{"name": deck.ability, "count": deck.count} for deck in decks]
            return abilities
        return []
    else:
        return [{"name": "Capital", "count": 1}, {"name": "Cannon", "count": 1}, {"name": "Rage", "count": 2}, {"name": "Poison", "count": 1}]
    

@app.route('/save_deck', methods=['POST'])
@token_required
def save_deck(current_user):
    if config.DB_CONNECTED:
        data = request.json
        abilities = data.get('abilities')
        user = User.query.filter_by(username=current_user).first()

        if not abilities:
            delete_rows_with_secondary_id(user.id)
            return jsonify({"success": False, "message": "Missing abilities"}), 400

        if not user:
            return jsonify({"success": False, "message": "User not found"}), 404
        
        if user.deck_id is None:
            # Generate a new UUID for the deck.
            new_deck_id = uuid.uuid4() 
            # max_deck_id = db.session.query(db.func.max(Deck.id)).scalar()
            # new_deck_id = (max_deck_id or 0) + 1
            user.deck_id = new_deck_id
            db.session.commit()

        # Delete old deck entries for the user
        Deck.query.filter_by(id=user.deck_id).delete()
        db.session.commit()

        # deck_id=user.deck_id,
        for item in abilities:
            new_deck_entry = Deck(secondary_id=user.deck_id, ability=item['name'], count=item['count'])
            add_or_replace_deck(secondary_id=user.deck_id, ability=item['name'], count=item['count'])
        
        db.session.commit()

        # # Convert abilities list to a dictionary
        # items = {item['name']: item['count'] for item in abilities}
        # new_deck = Deck(items=items, count=count)
        # db.session.add(new_deck)
        # db.session.commit()

        # Update user's deck_id
        # user.deck_id = new_deck.id
        # db.session.commit()

        return jsonify({"success": True, "message": "Deck saved successfully"}), 200
    return jsonify({"success": False, "message": "Database not connected"}), 500

def add_or_replace_deck(secondary_id, ability, count):
    try:
        new_deck_entry = Deck(
            secondary_id=secondary_id,
            ability=ability,
            count=count
        )
        db.session.add(new_deck_entry)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        existing_deck_entry = db.session.query(Deck).filter_by(
            secondary_id=secondary_id,
            ability=ability
        ).one()
        existing_deck_entry.count = count
        db.session.commit()

def delete_rows_with_secondary_id(secondary_id):
    try:
        db.session.query(Deck).filter_by(secondary_id=secondary_id).delete()
        db.session.commit()
        print(f"All rows with secondary_id = {secondary_id} have been deleted.")
    except Exception as e:
        db.session.rollback()
        print(f"An error occurred: {e}")

def update_elos(new_elos, usernames):
    if config.DB_CONNECTED:
        for username, new_elo in zip(usernames, new_elos):
            user = User.query.filter_by(username=username).first()
            if user:
                user.elo = new_elo
        db.session.commit()
    else:
        print("Database not connected. Elo updates not saved.")

def calculate_elos(elos, k_factor=32):
    n = len(elos)
    new_elos = elos.copy()
    
    for i in range(n):
        for j in range(i+1, n):
            expected_i = 1 / (1 + 10**((elos[j] - elos[i]) / 400))
            expected_j = 1 - expected_i
            
            score_i = 1  # Player i won against player j
            score_j = 0  # Player j lost against player i
            
            new_elos[i] += k_factor * (score_i - expected_i)
            new_elos[j] += k_factor * (score_j - expected_j)
    
    return [round(elo) for elo in new_elos]

def token_to_username(token: str):
    try:
        return jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])['user']
    except jwt.ExpiredSignatureError:
        return 'Expired token'
    except jwt.InvalidTokenError:
        return 'Invalid token'

def username_to_elo(name: str):
    if config.DB_CONNECTED:
        user = User.query.filter_by(username=name).first()
        return user.elo if user else 1100  # Default ELO if user not found
    else:
        dummy = {"other": 1200, "default": 1300}
        return dummy.get(name, 1100)  # Def
    
@app.route('/abilities', methods=['GET'])
def get_abilities():
    abilities = [
        {"name": "Freeze", "cost": 1},
        {"name": "Spawn", "cost": 1},
        {"name": "Zombie", "cost": 1},
        {"name": "Burn", "cost": 1},
        {"name": "Poison", "cost": 2},
        {"name": "Rage", "cost": 2},
        {"name": "D-Bridge", "cost": 2},
        {"name": "Bridge", "cost": 2},
        {"name": "Capital", "cost": 3},
        {"name": "Nuke", "cost": 3},
        {"name": "Cannon", "cost": 3},
        {"name": "Pump", "cost": 3},
    ]
    return jsonify({"abilities": abilities, "salary": 15})

@app.route('/elo', methods=['POST'])
def update_elo():
    # important that order is maintained throughout the process, as that preserves ranking in game
    # hence why lists are used
    # first two method calls are placeholders for actual db queries
    ordered_tokens = request.json.get("ordered_players")

    usernames = [token_to_username(token) for token in ordered_tokens]
    old_elos = [username_to_elo(user) for user in usernames]
    new_elos = calculate_elos(old_elos)

    update_elos(new_elos, usernames)

    elo_tuples = {ordered_tokens[i]: list(zip(old_elos, new_elos))[i] for i in range(len(ordered_tokens))}
    return jsonify({"new_elos": elo_tuples})


@app.route('/leaderboard', methods=['GET'])
def get_leaderboard():
    if config.DB_CONNECTED:
        # Query the database for all users, ordered by elo descending
        users = User.query.order_by(User.elo.desc()).all()
        leaderboard = [{"userName": user.username, "elo": user.elo} for user in users]
        return jsonify({"leaderboard": leaderboard})
    
    return jsonify({
        "leaderboard": [
            {"userName": "Default-User", "elo": 1138},
            {"userName": "Alice", "elo": 1500},
            {"userName": "Bob", "elo": 1400},
            {"userName": "Charlie", "elo": 1300},
            {"userName": "Alice", "elo": 1500},
            {"userName": "Bob", "elo": 1400},
            {"userName": "Charlie", "elo": 1300},
            {"userName": "Alice", "elo": 1500},
            {"userName": "Bob", "elo": 1400},
            {"userName": "Charlie", "elo": 1300},
            {"userName": "Bob", "elo": 1400},
            {"userName": "Charlie", "elo": 1300},
            {"userName": "Alice", "elo": 1500},
            {"userName": "Bob", "elo": 1400},
            {"userName": "Charlie", "elo": 1300},
            {"userName": "Alice", "elo": 1500},
            {"userName": "Bob", "elo": 1400},
            {"userName": "Charlie", "elo": 1300},
            {"userName": "David", "elo": 1200}
        ]
    })


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
