from transformers import AutoTokenizer, BertForSequenceClassification
import torch
import numpy as np
import os
from sklearn.preprocessing import LabelEncoder

model_path = os.environ['MODEL_PATH']
max_length = 150


class BertClassifier:
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        self.model = BertForSequenceClassification.from_pretrained(model_path)
        self.model.eval()
        self.labelEncoder = LabelEncoder()
        self.labelEncoder.classes_ = np.load(model_path + 'classes.npy', allow_pickle=True)

    def classify(self, headline, article):
        print('Checking headline', headline)
        encoded = self.tokenizer([headline], text_pair=[article], padding='max_length',
                                 max_length=max_length, truncation='only_second', return_tensors='pt')
        input_id = torch.cat([encoded['input_ids']], dim=0)
        attention_mask = torch.cat([encoded['attention_mask']], dim=0)
        with torch.no_grad():
            outputs = self.model(input_id, token_type_ids=None, attention_mask=attention_mask)
        label = np.argmax(outputs[0], axis=1).flatten()
        text_label = self.labelEncoder.inverse_transform(label)
        return text_label[0]
