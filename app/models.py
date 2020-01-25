import app.db
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash
import sqlalchemy as sa
import app.config
import jwt
import datetime
Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    id = sa.Column(sa.Integer, primary_key=True)
    email = sa.Column(sa.String(120), index=True, unique=True)
    name = sa.Column(sa.String)
    password_hash = sa.Column(sa.String(128))
    created_at = sa.Column(sa.DateTime, server_default=sa.sql.expression.text('NOW()'), nullable=False)
    updated_at = sa.Column(sa.DateTime, server_default=sa.sql.expression.text('NOW()'), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def encode_auth_token(self):
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=180, seconds=0),
                'iat': datetime.datetime.utcnow(),
                'sub': self.id
            }
            return jwt.encode(
                payload,
                app.config.get('SECRET_KEY'),
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(request):
        auth_header = request.headers.get('Authorization')
        if auth_header:
            auth_token = auth_header.split(" ")[1]
        else:
            auth_token = ''
        try:
            payload = jwt.decode(auth_token, app.config.get('SECRET_KEY'))
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return None
            # return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return None
        except:
            return None
            # return 'Invalid token. Please log in again.'


class UserLog(Base):
    __tablename__ = 'user_log'
    id = sa.Column(sa.Integer, primary_key=True)
    user_id = sa.Column(sa.ForeignKey("user.id"))
    query = sa.Column(sa.Text)
    variables = sa.Column(sa.Text)
    user_agent = sa.Column(sa.Text)
    response = sa.Column(sa.JSON)

    created_at = sa.Column(sa.DateTime, server_default=sa.sql.expression.text('NOW()'), nullable=False)

    user = relationship("User")


class Joke(Base):
    __tablename__ = 'joke'

    id = sa.Column(sa.Integer, primary_key=True)
    text = sa.Column(sa.String())
    user_id = sa.Column(sa.Integer, index=True)
    created_at = sa.Column(sa.DateTime, server_default=sa.sql.expression.text('NOW()'), nullable=False)