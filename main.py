class PrinterString:
    #Initialize
    def __init__(self,np,pages):
        #Total number of Pages
        self.np = np
        #Page String
        self.pages = pages
        #Creating a List from Page string
        self.pg = self.page_list()
        #A list for remaining pages
        self.pg_list = self.remaining_pgs()
    #Function to create page list
    def page_list(self):
        if "-" not in self.pages:
            p = self.pages.split(",")
            p = list(map(int,p))
        else:
            p = self.pages.split(",")
            p = self.rstrings(p)
        p.sort()
        return p
    #Function for remaining page list
    def remaining_pgs(self):
        nlist = set([i for i in range(1,self.np+1)])
        rem_pg = nlist.difference(set(self.pg))
        return list(rem_pg)
    #Function to create printer strings
    def pstrings(self,n:list):
        s = []
        for i in n:
            if len(i)>1:
                s.append(f"{i[0]}-{i[-1]}")
            else:
                s.append(f"{i[0]}")
        return s
    #Function to create lists from printer strings
    #For eg: 1,2-5,9
    def rstrings(self,n:list):
        s = []
        for i in n:
            if "-" in i:
                x = i.split("-")
                x = list(map(int,x))
                for j in range(x[0],x[1]+1):
                    s.append(j)
            else:
                s.append(int(i))
        s.sort()
        return s
    #Main function which creates a list of pages and prints string
    def printer_str(self):
        fs = []
        i = 0
        j = 0
        while (i<len(self.pg_list)):
            if j==len(self.pg_list)-1:
                fs.append([self.pg_list[s] for s in range(i,j+1)])
                break
            if self.pg_list[j+1]-self.pg_list[j]==1:
                j+=1
                continue
            
            else:
                fs.append([self.pg_list[s] for s in range(i,j+1)])
                i = j+1
                j = i
        #Final strings
        fs.sort()
        s = self.pstrings(fs)
        return ",".join(s) 

if __name__=="__main__":
    n = int(input("Enter Total number of Pages: "))

    bwc = input("Enter b/w or colored page numbers (comma separated): ")

    obj1 = PrinterString(n,bwc)
    print(obj1.printer_str())


