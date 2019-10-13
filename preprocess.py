import pandas as pd
import re

class text_preprocessor:
    def __init__(self, dataframe):
        self.pre_df = dataframe
        self.post_df = self.clean_df()

    def clean_df(self):
        temp_df = self.pre_df.copy()
        temp_df.iloc[:,1] = temp_df.iloc[:,1].apply(self.clean_text)
        return temp_df
                
    def clean_text(self,text):

        temp_list = re.findall('\[([\w \-,]+)\]|(\w+)',text)
        word_list = list([i[0].lower() if len(i[0])>len(i[1]) else i[1].lower() for i in temp_list])
        return word_list