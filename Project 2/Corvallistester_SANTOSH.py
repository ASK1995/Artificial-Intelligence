from Tower import *
import time
 
from Corvallis import *
 
if __name__ == "__main__":
    #testStr = listStr(list(range(10)))
    testStr=["5462031",
"2364150",
"0623541",
"4061532",
"6342105",
"1625043",
"2365014",
"6013254",
"4031265",
"3206154",
"1306425",
"0354216",
"4106235",
"3105246",
"5213406",
"4623051",
"2463150",
"5603421",
"1256304",
"2104356"
]

    cntr=[]
    dntr=[]
    for i in testStr:
        cVal = Corvallis(i, 1, admissible = True)
        print(cVal)
    
	
        cnt = 0
        goal = 0
        t = time.time()
        while not isinstance(goal, list) and cnt < 1000000000:
            goal = cVal.takeTurn()
            cnt += 1
            if not cnt % 200:
                print(cnt, tupler(cVal.tower), cVal.depth)
             
    dt = time.time()-t
    print(cnt)
    cntr.append(cnt)
    print(cVal)
    dntr.append(dt)    	
    print(dt)
 
    print(cntr)
    print(dntr)
    
 
 
 
 
         
            

