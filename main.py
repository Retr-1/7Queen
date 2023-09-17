import tkinter as tk
from PIL import ImageTk, Image

class Queens_Problem:
    def __init__(self, size, queens) -> None:
        self.solutions = []
        self.size = size
        self.queens = queens

    def solve(self):
        def put(x,y,val):
            rows[y] = val
            columns[x] = val
            ldiagonal[x-y+self.size] = val
            rdiagonal[x+y] = val
        
        def is_occupied(x,y):
            return rows[y] or columns[x] or ldiagonal[x-y+self.size] or rdiagonal[x+y]
        
        def main(depth,current:list,sx):
            if depth == 0:
                self.solutions.append(current.copy())
                # print(current)
                return
            
            for x in range(sx, self.size):
                for y in range(self.size):
                    if not is_occupied(x,y):
                        put(x,y,True)
                        current.append((x,y))
                        main(depth-1,current,x+1)
                        current.pop()
                        put(x,y,False)


        rows = [False]*self.size
        columns = [False]*self.size
        ldiagonal = [False]*(self.size*2)
        rdiagonal = [False]*(self.size*2)
        main(self.queens, [], 0)
        # print(len(self.solutions), len(set(map(tuple,map(sorted, self.solutions)))))
        return self


class Graphics:
    def __init__(self) -> None:
        self.width = 777
        self.height = 777
        size = 7
        queens = 7
        self.index = 0

        self.problem = Queens_Problem(size,queens).solve()
        root = tk.Tk()
        root.title('Queen Problem')
        frame = tk.Frame(master=root)
        self.canvas = tk.Canvas(master=root, width=self.width, height=self.height, background='white')
        self.page_lablel = tk.Label(master=root,text='0/0')
        size_label = tk.Label(master=frame, text='size,queens:')
        self.size_input = tk.Entry(master=frame)
        self.size_input.insert(0, '7,7')
        size_button = tk.Button(master=frame, text='solve', command=self.__set_new_size)
        
        self.canvas.grid(row=0, column=0, columnspan=2)
        self.page_lablel.grid(row=1, column=0)
        frame.grid(row=1, column=1)
        size_label.pack(side=tk.LEFT)
        self.size_input.pack(side=tk.LEFT)
        size_button.pack(side=tk.LEFT)
        self.page_lablel.bind('<Left>',self.previous)
        self.page_lablel.bind('<Right>',self.next)
        self.canvas.bind('<Button-1>', lambda e: self.page_lablel.focus())
        
        self.__load_image()
        self.__draw_solution()

        tk.mainloop()

    def move(self, direction):
        if self.index+direction < 0 or self.index+direction >= len(self.problem.solutions):
            return
        self.index += direction
        self.__draw_solution()
        

    def previous(self,ev):
        self.move(-1)

    def next(self,ev):
        # print(ev)
        self.move(1)

    def __set_new_size(self):
        self.page_lablel.focus()
        size,queens = map(int, self.size_input.get().split(','))
        self.index = 0
        self.problem = Queens_Problem(size,queens).solve()
        self.__load_image()
        self.__draw_solution()

    def __load_image(self):
        s = 0.8
        self.image = ImageTk.PhotoImage(Image.open('queen.jpg').resize((int(self.width/self.problem.size*s), int(self.height/self.problem.size*s))))
        
    def __draw_image(self,x,y):
        d = self.width/self.problem.size
        h = d*.5
        self.canvas.create_image(x*d+h, y*d+h, image=self.image)

    def __draw_checkboard(self):
        d = self.width/self.problem.size
        for x in range(self.problem.size):
            for y in range(self.problem.size):
                color = 'white' if (x&1)^(y&1) else 'black'
                self.canvas.create_rectangle(x*d, y*d, x*d+d, y*d+d, fill=color)
    
    def __draw_solution(self):
        self.canvas.delete('all')
        self.__draw_checkboard()
        if len(self.problem.solutions) == 0:
            self.canvas.create_text(self.width/2, self.height/2, text='No Possible Solution', fill='red', font=('Impact', 50))
            self.page_lablel.configure(text='0/0')
            return
        for pos in self.problem.solutions[self.index]:
            self.__draw_image(pos[0], pos[1])
        self.page_lablel.configure(text=f'{self.index+1}/{len(self.problem.solutions)}')

        

Graphics()
# print(Queens_Problem(5).solve().solutions)