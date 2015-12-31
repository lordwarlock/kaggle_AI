from numpy import *

class WordVecFeature():
    def __init__(self,word_list,word_vec):
        self.fvector = self.extract(word_list,word_vec)
    def extract(self,word_list,word_vec):
        counter = 0
        result = None
        for word in word_list:
            if word_vec.get(word) is None: continue
            counter = counter + 1
            curr_array = array(word_vec.get(word))
            if result is None: result = curr_array
            else: result = result + curr_array
        if counter != 0:
            result = result/counter
        return result

class TrainingFeature():
    def __init__(self,q_fv,a_fv):
        self.fv = similarity(q_fv,a_fv)
    def similarity(self,q_fv,a_fv):
        return q_fv/norm(q_fv)-a_fv/norm(a_fv)
