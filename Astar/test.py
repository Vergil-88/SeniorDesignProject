import Astar


x_path=[]
y_path=[]

x,y,dest_x,dest_y=0,0,-3,2

src =  [x, y]
dest = [dest_x, dest_y]

x_path,y_path=Astar.main(src, dest)

print(x_path)
print(y_path)


