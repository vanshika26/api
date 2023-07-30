##########################first code try with security code ###################################

from flask import Flask, request, jsonify
from bardapi import Bard
from flask_cors import CORS
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
CORS(app)

# Function to convert sets to lists in JSON data
def set_to_list(obj):
    if isinstance(obj, set):
        return list(obj)
    elif isinstance(obj, dict):
        return {key: set_to_list(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [set_to_list(item) for item in obj]
    else:
        return obj

# Function to get bard's answer
def bard_answer(query):
    try:
        # Sanitize the input query to prevent potential code injection
        sanitized_query = sanitize_query(query)
        answer = Bard().get_answer(sanitized_query)
        return set_to_list(answer)  # Convert sets to lists in the response
    except Exception as e:
        app.logger.error(f"Error while processing request: {e}")
        return {'error': 'An error occurred while processing your request. Please try again later.'}, 500

# Function to sanitize the input query
def sanitize_query(query):
    # Implement your own sanitization logic here based on your requirements
    # For example, you can use a library like bleach to strip HTML tags and
    # disallow certain characters or patterns to prevent code injection.
    return query.strip()

# API
@app.route('/get_answer', methods=['GET'])
def get_answer():
    query = request.args.get('query')

    # Input validation
    if query is None or not isinstance(query, str) or len(query.strip()) == 0:
        return jsonify({'error': 'Invalid request. Missing or invalid "query" parameter.'}), 400

    try:
        response = bard_answer(query)
        return jsonify(response)
    except Exception as e:
        app.logger.error(f"Error while processing request: {e}")
        return jsonify({'error': 'An unexpected error occurred. Please try again later.'}), 500

# Add CSP header to the response
@app.after_request
def add_security_headers(response):
    # Replace 'example.com' with your API's domain to limit script sources
    response.headers['Content-Security-Policy'] = "default-src 'self'; script-src 'self' 'unsafe-inline' 'unsafe-eval' https://example.com;"
    
    # Disable server header to reduce information disclosure
    response.headers['Server'] = ''
    
    # Set X-Content-Type-Options to prevent MIME sniffing
    response.headers['X-Content-Type-Options'] = 'nosniff'
    
    # Set X-Frame-Options to prevent clickjacking
    response.headers['X-Frame-Options'] = 'DENY'
    
    # Set X-XSS-Protection to prevent reflected XSS attacks
    response.headers['X-XSS-Protection'] = '1; mode=block'
    
    return response

if __name__ == '__main__':
    # Configure logging
    import logging
    logging.basicConfig(level=logging.INFO)

    # Run the Flask app with the following settings to enhance security
    app.run(debug=False, port=5000, host='0.0.0.0', ssl_context='adhoc')


################## second code which returns only bard's response data in json without security ################

# from flask import Flask, request, jsonify
# from bardapi import Bard
# from flask_cors import CORS
# from dotenv import load_dotenv
# import os

# load_dotenv()

# app = Flask(__name__)

# CORS(app)

# # Function to get bard's  answer 
# def bard_answer(query):
#     try:
#         answer = Bard().get_answer(query)
#         return answer['content']
#     except Exception as e:
#         return str(e)
    
# #api
# @app.route('/get_answer', methods=['GET'])
# def get_answer():
#     query = request.args.get('query') 

#     if query is not None:
#         response = bard_answer(query)
#         return jsonify({'response': response})
#     else:
#         return jsonify({'error': 'Invalid request. Missing "query" parameter.'}), 400

# if __name__ == '__main__':

# Configure logging
    # import logging
    # logging.basicConfig(level=logging.INFO)
#     app.run(debug=True)



###################### third code which returns all the bard data in json without secuirty################


# from flask import Flask, request, jsonify
# from bardapi import Bard
# from flask_cors import CORS
# from dotenv import load_dotenv
# import os

# load_dotenv()

# app = Flask(__name__)

# CORS(app)

# #Function to convert sets to lists in JSON data
# def set_to_list(obj):
#     if isinstance(obj, set):
#         return list(obj)
#     elif isinstance(obj, dict):
#         return {key: set_to_list(value) for key, value in obj.items()}
#     elif isinstance(obj, list):
#         return [set_to_list(item) for item in obj]
#     else:
#         return obj

# # Function to get bard's answer
# def bard_answer(query):
#     try:
#         answer = Bard().get_answer(query)
#         return set_to_list(answer)  # Convert sets to lists in the response
#     except Exception as e:
#         return {'error': str(e)}  # Return a JSON response with the error message
    
# # API
# @app.route('/get_answer', methods=['GET'])
# def get_answer():
#     query = request.args.get('query')

#     # Input validation
#     if query is None or query.strip() == '':
#         return jsonify({'error': 'Invalid request. Missing or empty "query" parameter.'}), 400

#     try:
#         response = bard_answer(query)
#         return jsonify(response)
#     except Exception as e:
#         app.logger.error(f"Error while processing request: {e}")
#         return jsonify({'error': 'An unexpected error occurred. Please try again later.'}), 500

# if __name__ == '__main__':
#     # Configure logging
#     import logging
#     logging.basicConfig(level=logging.INFO)

#     app.run(debug=False)
