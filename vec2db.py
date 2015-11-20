import sqlite3
import codecs

class Vec2DB():
    def __init__(self,vec_path,db_path):
        self.conn = sqlite3.connect(db_path)
        self.c = self.conn.cursor()
        self.insert_query = self.make_insert_query()
        self.create_table()
        self.process_vec_file(vec_path)
        self.conn.close()

    def create_table(self,table_name = 'word_vector',\
                          key_name = 'word', key_type = 'text',\
                          dimension = 300, vec_type = 'real'):
        create_query = "CREATE TABLE " + table_name + '( ' + key_name + ' '\
                       + key_type + 'primary key'
        for i in range(dimension):
            create_query += ', dim'+str(i)+' '+vec_type
        create_query += ')'
        print create_query
        self.c.execute(create_query)

    def process_vec_file(self,vec_path):
        with codecs.open(vec_path,mode='r') as fin:
            fin.readline()
            for line in fin:
                parts = line.split()
                if len(parts) < 300:
                    #print line
                    continue
                else:
                    try:
                        self.insert_table(self.get_tuple(parts))
                    except:
                        print line
        self.conn.commit()

    def get_tuple(self,parts):
        #parts = line.split()
        word = parts[0]
        vec = [float(x) for x in parts[1:301]]
        return tuple([word]+vec)

    def insert_table(self,insert_tuple, commit = 0):
        self.c.execute(self.insert_query,insert_tuple)
        if commit: self.conn.commit()

    def make_insert_query(self,table_name = 'word_vector',dimension = 300):
        insert_query = 'INSERT INTO '+table_name+' VALUES (?'
        for i in range(dimension):
            insert_query += ',?'
        insert_query += ')'
        print insert_query
        return insert_query

if __name__ == '__main__':
    v2d = Vec2DB('google_news_vectors.txt','google_vec.db')
