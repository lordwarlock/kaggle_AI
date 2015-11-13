# -*- coding: utf-8  -*-
from __future__ import unicode_literals
import codecs
from nltk import word_tokenize

class QuestionAnswer(object):
    def __init__(self,qid = None, question = 0,correct_answer = 0,answer_list = 0):
        self.qid = qid
        self.question = self.question_to_word_list(question)
        self.correct_answer = ord(correct_answer) - ord('A')
        self.answer_list = self.answers_to_word_list(answer_list)

    def question_to_word_list(self,line):
        return self.sentences_to_word_list(line)

    def answers_to_word_list(self,answers):
        answer_list = [self.answer_to_word_list(answer) for answer in answers]
        return answer_list

    def answer_to_word_list(self,answer):
        return self.sentences_to_word_list(answer)

    def sentences_to_word_list(self,line):
        word_list = word_tokenize(line)
        return word_list

    def get_candidates(self):
        return [self.question + words for words in self.answer_list]

class QuestionAnswerList(object):
    def __init__(self,path):
        self.qa_list = []
        self.import_qa_list(path)

    def import_qa_list(self,path):
        with codecs.open(path,mode='r',encoding='utf-8') as fin:
            fin.readline()
            for line in fin:
                parts = line[:-1].split('\t')
                qa = QuestionAnswer(parts[0], parts[1], parts[2], parts[3:])
                self.qa_list.append(qa)
                
if __name__ == '__main__':
    qa_list = QuestionAnswerList('training_set.tsv')
    print qa_list.qa_list[0].get_candidates()
