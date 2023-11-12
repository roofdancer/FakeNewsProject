# FakeNewsProject

This is a web service that accepts an article headline and body and classify the relation between the headline and the article body. The output can be 'agree' 'disagree' 'discuss' 'unrelated'.

This task is described in https://www.kaggle.com/datasets/abhinavkrjha/fake-news-challenge. The dataset is taken from there too.

The training is done in Jupyter notebook LSML_FP_Egorov.ipynb, the resulting model is saved in model folder. To keep track of the experiments MLFlow via Databrick community edition was used. Baseline experiment was conducted with Random forest model and word2vec tokenizer, and main experiment was with pre-trained BERT model, fine-tuned with different learning rate values. Experiments folder contains csv export from Databrick.

The classifier that uses the trained model is in bertClassifier.py. The flask service, providing a REST API to call the classifier, is in appMain.py. Using Dockerfile, a docker image antone/fake-news-container:latest is created. It can be run via the following command:

docker run -it -e MODEL_PATH='/opt/my_service/model/model/' -p 5000:5000 antone/fake-news-container:latest" command.

The body of a sample request is in resources/exampleRequest.json. To send it, a standard curl command can be used. In case of Windows PowerShell, the command is the following:

Invoke-RestMethod -uri "http://127.0.0.1:5000/check" -Method POST -ContentType 'application/json' -InFile exampleRequest.json

To check the timing, the following command can be used:

(Measure-Command -Expression { $site = Invoke-RestMethod -uri "http://127.0.0.1:5000/check" -Method POST -ContentType 'application/json' -InFile exampleRequest.json }).Milliseconds

In my experiments, using a quantized model reduced the response time roughly in two times (from 520 ms to 270 ms).
