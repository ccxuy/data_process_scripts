import datetime  # python datetime module
import json      # python json module
import os,sys    # python os module, used for creating folders
import re        # python rRegular expression

class TweetParser():

    def walk_dir(dir,fileinfo,topdown=True):  
        for root, dirs, files in os.walk(dir, topdown):  
            for name in files:  
                print(os.path.join(name))  
                fileinfo.write(os.path.join(root,name) + '/n')  
            for name in dirs:  
                print(os.path.join(name))  
                fileinfo.write('  ' + os.path.join(root,name) + '/n')
            

    def load_json_file(res_list, fname):
        json_file = open(fname)
        for line in json_file.readlines():
            res_list.append(json.loads(line))
                

    def load_json_folder0(dir, topdown=True):
        json_folder_dict = {}
        for root, dirs, files in os.walk(dir, topdown):
            for dir_name in dirs:
                json_folder_dict.setdefault(dir_name,{})
                json_folder_dict[dir_name].setdefault('json',[])
                for root, dirs, files in os.walk(dir_name, topdown):
                    for name in files:
                        print dir_name, (os.path.join(name))
                        load_json_file(json_folder_dict[dir_name]['json']\
                            , os.path.join(dir_name,name))
                            
                json_list = json_folder_dict[dir_name]['json']
                with open(dir_name+'.csv','w') as out_file:
                    for jdic in json_list:
                        try:
                            #print jdic.keys()
                            print>>out_file,\
                                '\t'.join([str(jdic['id']), str(jdic['created_at'])\
                                , str(jdic['user']['id']), jdic['text'].encode('utf-8')])
                        except UnicodeEncodeError:
                            print 'UnicodeEncodeError'
                            print jdic
                            print jdic['text'].encode('utf-8')
                
                ########## Release memory
                json_folder_dict = {}
                            
        return json_folder_dict
        

    def load_json_file1(fname, base_name):
        json_file = open(fname)
        l = json_file.readline()
        
        with open(base_name+'.csv','a') as out_file:
            while l:
                jdic = json.loads(l)
                print>>out_file,\
                    '\t'.join([str(jdic['id']), str(jdic['created_at'])\
                    , str(jdic['user']['id']), jdic['text'].encode('utf-8')])   
                l = json_file.readline()
        

    def load_json_file_individual(fname, base_name, save_folder = '../tweet_text_only/'):
        json_file = open(fname)
        l = json_file.readline()
        
        t_count = 0
        while l:
            jdic = json.loads(l)
            #print 'read lines: ', jdic.__len__()
            with open(save_folder+base_name+'-'+str(t_count)+'.txt','a') as out_file:
                print>>out_file, jdic['text'].encode('utf-8')   
                t_count+=1
            l = json_file.readline()
        

    def load_json_folder1(dir, topdown=True):
        json_folder_dict = {}
        for root, dirs, files in os.walk(dir, topdown):
            for dir_name in dirs:
                for root, dirs, files in os.walk(dir_name, topdown):
                    for name in files:
                        print dir_name, (os.path.join(name))
                        load_json_file_individual(os.path.join(dir_name,name), os.path.join(name))
                

    def process_json_in_folder(self, folder_name, topdown=True):

        for root, dirs, files in os.walk(folder_name, topdown):
            for name in files:
                print folder_name, (os.path.join(name))
                self.save_filtered_json(os.path.join(folder_name,name))

    def save_filtered_json(self, fname, save_fname = "./output"):

        data = {}
        
        with open(fname,'r') as json_file:
            l = json_file.readline()

            l_count = 0
            while l:
                try:
                    jdic = json.loads(l)
                    l_count += 1

                    if self.match_condition_json(jdic):
                        jdic = self.extract_dict_partial_field(jdic)
                        with open(save_fname+'.json','a') as out_file:
                            print>>out_file, json.dumps(jdic)
                except ValueError:
                    print fname
                    print l
                    exit()

                l = json_file.readline()
                
            print 'tweet count', l_count


    def extract_dict_partial_field(self, jdic):
        new_dic = {}
        for key in jdic:
            if key in ['text', 'id', 'urls', 'retweeted'
                       , 'entities', 'hashtags', 'retweet_count'
                       , 'favorited', 'retweeted_status']:
                new_dic[key] = jdic[key]
        return new_dic


    def match_condition_json(self, json_dic):
        try:
            if re.search('petition', json_dic['text']):
                return True
            else:
                for url in json_dic['entities']['urls']:
                    if url['expanded_url'] != None and re.search('petitions.whitehouse', url['expanded_url']):
                        return True
        except TypeError:
            print json_dic

        return False
            
        #return re.search(pattern, json_dic)

def main():
    tp = TweetParser()
    tp.process_json_in_folder(folder_name = "./obama_gun/")


if __name__ == '__main__':
    main()