import json
import os
from app.db import db_session
from app.models import User, UserLog
from flask import Flask, request, g
from app import db
from flask_graphql import GraphQLView
from app.graphql.schema import schema
from flask_cors import CORS

app = Flask(__name__)
app.debug = os.environ.get('ENV') != 'production'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.secret_key = os.environ.get("SECRET_KEY")
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


class LoggingMiddleware(object):
    def resolve(self, next, root, info, **kwargs):
        if root is None:
            ignore = ['signUp','login','IntrospectionQuery']
            user_id = User.decode_auth_token(request)

            if not info.operation.name or info.operation.name.value not in ignore:
                with db.session() as session:
                    log = UserLog(
                        user_id=user_id,
                        query=json.dumps(request.json['query']),
                        variables=json.dumps(request.json['variables']),
                        user_agent=request.headers.environ.get('HTTP_USER_AGENT')+"---"+request.headers.environ.get('REMOTE_ADDR')
                    )
                    session.add(log)
                    session.commit()
                    g.log_id = log.id


        return next(root, info, **kwargs)


app.add_url_rule(
    "/graphql", view_func=GraphQLView.as_view(
        "graphql",
        schema=schema,
        graphiql=os.environ.get('ENV') != 'production',
        get_context=lambda:{'session': db_session},
        middleware=[LoggingMiddleware()]
    )
)


@app.after_request
def after_request(response):
    if g.get('log_id', False):
        if response.is_json:
            with db.session() as session:
                session.query(UserLog). \
                    filter(UserLog.id == g.log_id). \
                    update({"response": response.json})
    return response

@app.teardown_appcontext
def shutdown_session(context):
    db_session.remove()


if __name__ == "__main__":
    app.run(debug=True, port=os.environ.get("PORT"), host=os.environ.get("HOST"))
