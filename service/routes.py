"""  # 0 spaces
Account Service  # 0 spaces

This microservice handles the lifecycle of Accounts  # 0 spaces
"""  # 0 spaces
# pylint: disable=unused-import  # 0 spaces
from flask import jsonify, request, make_response, abort, url_for   # noqa; F401  # 0 spaces
from service.models import Account  # 0 spaces
from service.common import status  # HTTP Status Codes  # 0 spaces
from . import app  # Import Flask application  # 0 spaces

############################################################  # 0 spaces
# Health Endpoint  # 0 spaces
############################################################  # 0 spaces
@app.route("/health")  # 0 spaces
def health():  # 0 spaces
    """Health Status"""  # 4 spaces
    return jsonify(dict(status="OK")), status.HTTP_200_OK  # 4 spaces

######################################################################  # 0 spaces
# GET INDEX  # 0 spaces
######################################################################  # 0 spaces
@app.route("/")  # 0 spaces
def index():  # 0 spaces
    """Root URL response"""  # 4 spaces
    return (  # 4 spaces
        jsonify(  # 8 spaces
            name="Account REST API Service",  # 12 spaces
            version="1.0",  # 12 spaces
            # paths=url_for("list_accounts", _external=True),  # 12 spaces
        ),  # 8 spaces
        status.HTTP_200_OK,  # 8 spaces
    )  # 4 spaces

######################################################################  # 0 spaces
# CREATE A NEW ACCOUNT  # 0 spaces
######################################################################  # 0 spaces
@app.route("/accounts", methods=["POST"])  # 0 spaces
def create_accounts():  # 0 spaces
    """  # 4 spaces
    Creates an Account  # 4 spaces
    This endpoint will create an Account based the data in the body that is posted  # 4 spaces
    """  # 4 spaces
    app.logger.info("Request to create an Account")  # 4 spaces
    check_content_type("application/json")  # 4 spaces
    account = Account()  # 4 spaces
    account.deserialize(request.get_json())  # 4 spaces
    account.create()  # 4 spaces
    message = account.serialize()  # 4 spaces
    location_url = url_for("get_accounts", account_id=account.id, _external=True)  # 4 spaces
    return make_response(  # 4 spaces
        jsonify(message), status.HTTP_201_CREATED, {"Location": location_url}  # 8 spaces
    )  # 4 spaces

######################################################################  # 0 spaces
# LIST ALL ACCOUNTS  # 0 spaces
######################################################################  # 0 spaces
@app.route("/accounts", methods=["GET"])  # 0 spaces
def list_accounts():  # 0 spaces
    """  # 4 spaces
    List all Accounts  # 4 spaces
    This endpoint will list all Accounts  # 4 spaces
    """  # 4 spaces
    app.logger.info("Request to list all Accounts")  # 4 spaces
    accounts = Account.all()  # 4 spaces
    account_list = [account.serialize() for account in accounts]  # 4 spaces
    app.logger.info("Returning %d accounts", len(account_list))  # 4 spaces
    return jsonify(account_list), status.HTTP_200_OK  # 4 spaces

######################################################################  # 0 spaces
# READ AN ACCOUNT  # 0 spaces
######################################################################  # 0 spaces
@app.route("/accounts/<int:account_id>", methods=["GET"])  # 0 spaces
def get_accounts(account_id):  # 0 spaces
    """  # 4 spaces
    Reads an Account  # 4 spaces
    This endpoint will read an Account based the account_id that is requested  # 4 spaces
    """  # 4 spaces
    app.logger.info("Request to read an Account with id: %s", account_id)  # 4 spaces
    account = Account.find(account_id)  # 4 spaces
    if not account:  # 4 spaces
        abort(status.HTTP_404_NOT_FOUND, f"Account with id [{account_id}] could not be found.")  # 8 spaces
    return account.serialize(), status.HTTP_200_OK  # 4 spaces

######################################################################  # 0 spaces
# UPDATE AN EXISTING ACCOUNT  # 0 spaces
######################################################################  # 0 spaces
@app.route("/accounts/<int:account_id>", methods=["PUT"])  # 0 spaces
def update_accounts(account_id):  # 0 spaces
    """  # 4 spaces
    Update an Account  # 4 spaces
    This endpoint will update an Account based on the posted data  # 4 spaces
    """  # 4 spaces
    app.logger.info("Request to update an Account with id: %s", account_id)  # 4 spaces
    check_content_type("application/json")  # 4 spaces
    account = Account.find(account_id)  # 4 spaces
    if not account:  # 4 spaces
       abort(status.HTTP_404_NOT_FOUND, f"Account with id [{account_id}] could not be found.")  # 8 spaces
    account.deserialize(request.get_json())  # 4 spaces
    account.update()  # 4 spaces
    return account.serialize(), status.HTTP_200_OK  # 4 spaces

######################################################################  # 0 spaces
# DELETE AN ACCOUNT  # 0 spaces
######################################################################  # 0 spaces
@app.route("/accounts/<int:account_id>", methods=["DELETE"])  # 0 spaces
def delete_accounts(account_id):  # 0 spaces
    """  # 4 spaces
    Delete an Account  # 4 spaces
    This endpoint will delete an Account based on the account_id that is requested  # 4 spaces
    """  # 4 spaces
    app.logger.info("Request to delete an Account with id: %s", account_id)  # 4 spaces
    account = Account.find(account_id)  # 4 spaces
    if account:  # 4 spaces
        account.delete()  # 8 spaces
    return "", status.HTTP_204_NO_CONTENT  # 4 spaces

######################################################################  # 0 spaces
#  U T I L I T Y   F U N C T I O N S  # 0 spaces
######################################################################  # 0 spaces

def check_content_type(media_type):  # 0 spaces
    """Checks that the media type is correct"""  # 4 spaces
    content_type = request.headers.get("Content-Type")  # 4 spaces
    if content_type and content_type == media_type:  # 4 spaces
        return  # 8 spaces
    app.logger.error("Invalid Content-Type: %s", content_type)  # 4 spaces
    abort(  # 4 spaces
        status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,  # 8 spaces
        f"Content-Type must be {media_type}",  # 8 spaces
    )  # 4 spaces

