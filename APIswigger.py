
from flask import Flask, jsonify, request 
from flasgger import Swagger, LazyString, LazyJSONEncoder
from flasgger import swag_from

app = Flask(__name__) 


app.json_encoder = LazyJSONEncoder

swagger_template = dict(
    info = {
        'title': LazyString(lambda:'API Documentation for Data Processing and Modeling'),
        'version': LazyString(lambda:'1.0.0'),
        'description': LazyString(lambda:'Dokumentasi API untuk Data Processing dan Modeling')
        }, host = LazyString(lambda: request.host)
    )

swagger_config = {
        "headers":[],
        "specs":[
            {
            "endpoint":'docs',
            "route":'/docs.json'
            }
        ],
        "static_url_path":"/flasgger_static",
        "swagger_ui":True,
        "specs_route":"/docs/"
    }

swagger = Swagger(app, template=swagger_template, config=swagger_config)


languages = [{'name' : 'JavaScript'}, {'name' : 'Python'}, {'name' : 'Ruby'}]

######################################################################################
@swag_from("docs/Index.yml", methods=['GET'])
@app.route('/', methods=['GET'])
def test():
	return jsonify({'message' : 'It works!'})
######################################################################################

######################################################################################
@swag_from("docs/Lang1.yml", methods=['GET'])
@app.route('/lang', methods=['GET'])
def returnAll():
	return jsonify({'languages' : languages})
#######################################################################################

#######################################################################################
@swag_from("docs/Lang2.yml", methods=['GET'])
@app.route('/lang/<string:name>', methods=['GET'])
def returnOne(name):
    langs = [language for language in languages if language['name'] == name]
    return jsonify({'language' : langs[0]})
#######################################################################################

########################################################################################
@swag_from("docs/Lang3.yml", methods=['POST'])
@app.route('/lang', methods=['POST'])
def addOne():
	language = {'name' : request.json['name']}
	languages.append(language)
	return jsonify({'languages' : languages})
######################################################################################

########################################################################################
@swag_from("docs/Lang4.yml", methods=['PUT'])
@app.route('/lang/<string:name>', methods=['PUT'])
def editOne(name):
	langs = [language for language in languages if language['name'] == name]
	langs[0]['name'] = request.json['name']
	return jsonify({'language' : langs[0]})
######################################################################################

########################################################################################
@swag_from("docs/Lang5.yml", methods=['DELETE'])
@app.route('/lang/<string:name>', methods=['DELETE'])
def removeOne(name):
	lang = [language for language in languages if language['name'] == name]
	languages.remove(lang[0])
	return jsonify({'languages' : languages})
#########################################################################################

if __name__ == '__main__':
	app.run(debug=True, port=8080)