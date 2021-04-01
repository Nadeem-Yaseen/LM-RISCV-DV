# //////////////////////////////////////////////////////////////////////
#    Copyright [2020] [Lampro Mellon]
# 
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
# 
#      http://www.apache.org/licenses/LICENSE-2.0
# 
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
# //////////////////////////////////////////////////////////////////////

from argparse import ArgumentParser


def nb_post_fix(rtl_log_f,rtl_log,nb_log):
    ''' Replaces non-blocking load results in rd of trace log.
    Sees time/CycleCnt at which non-block load is written back to gpr,
    checks from that time/CycleCnt backwards, where this gpr was written in trace log,
    replaces the result in rd (also load) at that instruction'''
    
    nb_file = open(nb_log,"r")
    load_lines = nb_file.readlines()
    #read whole file
    trace_file = open(rtl_log,"r")
    trace_lines = trace_file.readlines()
    list1 = []
    list2 = []
    list3 = ['lb', 'lh', 'lw', 'lbu', 'lhu', 'c.lw', 'c.lwsp', 'c.ld', 'c.ldsp', 'c.lq', 'c.lqsp']
    x = 1
    i = 1
    
    for i in range(len(load_lines)):
        l= load_lines[i].split()
        list1.append(l)
    for i in range(len(trace_lines)):
        l2 = trace_lines[i].split()
        list2.append(l2)
    #flow with trace log read as whole
    # find and replace the non-block load instruction reg
    i = 1
    while (x < len(load_lines)):
        try:
            t = list1[x][0]
        except IndexError:
            break
        if(int(list1[x][0])<=int(list2[i][0])):
            for a in range(i,i-20,-1):               
                try:
                    t = list2[a][5].split(',')
                except IndexError:
                    continue
                try:
                    t = list2[a][10].split(':')
                except IndexError:
                    continue
                if(list1[x][2]==list2[a][5].split(',')[0] and (list2[a][10].split(':')[0]=="load") and (list2[a][4] in list3)):
                    list2[a][7]=("%s=0x%s" %(list1[x][2],list1[x][3]))
                    list2[a][10]=("load:0x%s" %(list1[x][3]))
                    i=a+1    
                    break
            x+=1
        i+=1

    #update trace lines
    for i in range(len(trace_lines)):
        list2[i]='\t'.join(list2[i])
        trace_lines[i]=str(list2[i]+'\n')
    #writing back lines
    nb_file = open(rtl_log_f, "w")
    nb_file.writelines(trace_lines)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--rtl_log_f",
                        help="Output core simulation log post-fixed (default: stdout)",
                        type=argparse.FileType('w'),
                        default=sys.stdout)
    parser.add_argument("--nb_log",
                        help="Input core simulation log (default: stdin)",
                        type=argparse.FileType('r'),
                        default=sys.stdin)
    parser.add_argument("--rtl_log",
                        help="Input core simulation log (default: stdin)",
                        type=argparse.FileType('r'),
                        default=sys.stdin)

    args = parser.parse_args()

    print("Post-fix log for nonblock load values\n")
    nb_post_fix(args.rtl_log_f, args.rtl_log, args.nb_log)



if __name__ == "__main__":
    main()
    
