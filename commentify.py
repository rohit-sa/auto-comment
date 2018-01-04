# -*- coding: utf-8 -*-
"""
Created on Wed Jan  3 19:31:39 2018

@author: Rohit
"""
import os
import os.path
import sys
import re


"""
function: input_handling
input parameters: 
Notes: 
"""
def input_handling():
    
    user_def_filepaths = []
    target_filepaths = []
    
    if len(sys.argv) > 1:
        input_arg = sys.argv[1]
        if '.py' in input_arg:
            user_def_filepaths = [input_arg]
        else:
            for dirpath, dirnames, filenames in os.walk(input_arg):
                target_filepaths += [os.path.join(dirpath,files) for files in filenames if files.endswith('.py')]
            user_def_filepaths = [path for path in target_filepaths if input_arg in path]
            
    
    root_filepaths = []
    for dirpath, dirnames, filenames in os.walk('.'):
        root_filepaths += [os.path.join(dirpath,files) for files in filenames if files.endswith('.py')]
#    print(target_filepaths)
    
    self_name = os.path.basename(sys.argv[0])
    self_index = []
    for i in range(len(root_filepaths)):
        path = root_filepaths[i]
        if self_name in path:
            self_index.append(i)
    for i in self_index:
        del root_filepaths[i]
               
#    print(root_filepaths)
    if len(user_def_filepaths) == 0:
        return root_filepaths
    else:
        return user_def_filepaths

"""
function: commentify
input parameters: file_contents
Notes: 
"""
def commentify(file_contents):
    
    func_comment_count = 0
    func_def_regex = re.compile(r'def')
    func_name_regex = re.compile(r'\ (.*)\(')
    in_param_regex = re.compile(r'\((.*)\)')
    comment_regex = re.compile(r'"""')
    
    commented_file_contents = []
    comments = ['"""','function: ','input parameters: ','Notes: ','"""']
    comment_format = [None]*2*len(comments)
    comment_format[0::2] = comments
    comment_format[1::2] = ['\n']*len(comments)
                      
                      
    for i in range(len(file_contents)):
        line = file_contents[i]
        comment = list(comment_format)
        
        if re.match(func_def_regex, line):
            func_name = re.search(func_name_regex,line)
            comment[2] = comment[2] + func_name.group(1)
            
            in_param_name = re.search(in_param_regex,line)
            if len(in_param_name.group(1)) != 0 :
                comment[4] = comment[4] + in_param_name.group(1)
            else:
                comment[4] = comment[4] + 'None'
                 
            prev_line = file_contents[i-1]
            
            if re.match(comment_regex,prev_line):
                func_comment_count += 1
            else:
                commented_file_contents += comment
                
        commented_file_contents.append(line)
        

    return commented_file_contents

"""
function: file_handling
input parameters: filename 
Notes: 
"""
def file_handling(filename ):
    
    assert os.path.isfile(filename),'Invalid filepath'
    print(filename)
    file_contents = []
    with open(filename,'r+') as f_handle:
        for line in f_handle:
            file_contents.append(line)
#    print(file_contents)
#    print(len(file_contents))
    commented_file_contents = commentify(file_contents)
    
    with open(filename,'w') as f_handle:
        for line in commented_file_contents:
            f_handle.write(line)
        

"""
function: main
input parameters: 
Notes: 
"""
def main():
    print('Running')
    target_files = input_handling()
    for file in target_files:
        file_handling(file)
    return

if __name__ == '__main__':
    main()
    