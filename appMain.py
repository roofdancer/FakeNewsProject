from flask import Flask, request, jsonify
import bertClassifier

app = Flask(__name__)
classifier = bertClassifier.BertClassifier()


@app.route('/check', methods=['POST'])
def check_fake():
    json = request.json
    print(json)
    res = classifier.classify(json.get('headline'), json.get('article'))
    return jsonify(isError=False,
                   message="Success",
                   statusCode=200,
                   data=res), 200


if __name__ == '__main__':
    app.run("0.0.0.0")
