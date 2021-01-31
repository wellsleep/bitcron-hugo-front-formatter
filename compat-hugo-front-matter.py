import os

def is_contains_chinese(strs):
    for _char in strs:
        if '\u4e00' <= _char <= '\u9fa5':
            return True
    return False

def findAllFile(base): # find files in same dir, return date in fname and full path
    for root, ds, fs in os.walk(base):
        for f in fs:
            if f.endswith(('.md','.markdown','.txt')): #endswith needs a tuple
                fdate = findFileDate(f)
                if fdate is not 'unmatch':
                    fullname = os.path.join(root, f)    
                    yield fdate, fullname

def findFileDate(filename):
    if filename.startswith('20') and filename[4] == '-': #find pattern
        return filename[:len('2020-01-01')] # '2020-01-01' 9 digits, cut them out
    else:
        return 'unmatch'

def frontmatterCleanUp(origin_file):
    """
    1. 如果开头是'---'， 则替换为空行；
    2. 如果前10行内有'---'，则替换为空行；
    3. 如果开头不是'---'，则插入空行；
    4. 如果前10行内，第一行无冒号 或 有冒号但字数大于6个字符且含中文字符，认为是正文第一行。在正文第一行之前插入空行。
    """
    with open(origin_file, 'r') as f1, open("%s.clean" % origin_file, 'w') as f2: #f1 is origin, f2 is cleaned file
        line_num = 1
        end_fm = False
        isDateAvail = False
        end_fm_lnum = 1
        newlines = ['\n']
        
        lines = f1.readlines()
        
        if lines[0].startswith('---') is False: # fit condition #3
            #lines.insert(0, '\n')
            newlines[0] = '\n'
            newlines.append(lines[0])
            #print('+++ found start of front matter 1 +++')
        else: # fit condition #1
            #lines[0] = '\n'
            newlines[0] = '\n'
            #print('+++ found start of front matter 2 +++')
            
        for line in lines[1:]:
            #print(len(line),line_num, line[:10])
            if line.find(':') != -1:
                #print('found :', line_num, len(line), end_fm)
                pass
            
            if line.startswith('---') and line_num < 10:   # fit condition #2        
                #line = '\n'
                end_fm = True
                #print('+++ found end of front matter +++')
                end_fm_lnum = line_num
                #f2.write(line)
                
                newlines.append('\n')
                continue
            
            if end_fm == False and line_num > 10: 
                #print('--- did not find end of fm ---')
                pass
            
            if line.startswith('date:'):
                isDateAvail = True
            
            if ( \
                (line.find(':') == -1) or \
                (len(line) > 6 and is_contains_chinese(line) and line.find(':')) \
                )  and end_fm == False: # fit condition #4
                #lines.insert(line_num, '\n')
                end_fm = True
                end_fm_lnum = line_num
                #print('end_fm_lnum:', end_fm_lnum)
                
                newlines.append('\n')
                newlines.append(line)
                #print(newlines)
                continue
                                
            line_num += 1
            newlines.append(line)
            
        contents = "".join(newlines)
        f2.write(contents)
       
    return isDateAvail, end_fm_lnum

def addFrontMatter(fdate, fullname):
    """
    #1. 如果开头是'---'， 则替换为空行；
    #2. 如果前10行内有'---'，则替换为空行；
    #3. 如果开头不是'---'，则插入空行；
    #4. 如果前10行内，第一行无冒号或有冒号但字数大于6个字符，认为是正文第一行。在正文第一行之前插入空行。
    5. 将头两个空行之间的内容按照yaml格式填充：
        a. 如果之前的front matter没有date，则写入'date:'信息
        b. 将头两个两个空行替换为'---'
    *6. 将 title: 中增加单引号
    """
    line_num = 0
    isDateAvail = False
    isDateWritten = False
    isEndFMWritten = False
    end_fm_lnum = 1
    newlines = ['\n']
    
    isDateAvail, end_fm_lnum = frontmatterCleanUp(fullname)
    
    with open('%s.clean' % fullname, 'r') as f1, open("%s.new" % fullname, 'w') as f2: #f1 is origin, f2 is new file
        
        lines = f1.readlines()
        newlines[0] = '---\n'        # fit #5b
        
        for line in lines[1:]:
            if line is '\n' and isDateAvail == False and isDateWritten == False: # fit #5a
                #lines.insert(end_fm_lnum, 'date: %s\n' % fdate)
                isDateWritten = True
                
                newlines.append('date: %s' % fdate)
                newlines.append(line)
                
                
                
            if line == '\n' and isEndFMWritten == False: # fit 5b
                newlines.append('---\n')
                isEndFMWritten = True
                
            if line.find('title:') != -1:
                offset = line.find(':')
                newlines.append("title: '" + line[offset+1:-1] + "'\n")
                continue
            
            newlines.append(line)
            
        contents = "".join(newlines)
        f2.write(contents)
      

def main():
    base = '.'
    for fdate,fullname in findAllFile(base):
        #print(fdate)

        addFrontMatter(fdate,fullname)
        print(fdate,fullname)
        
        os.rename(fullname, fullname+'.old')
        os.rename(fullname+'.new', fullname)
        


if __name__ == '__main__':
    main()
