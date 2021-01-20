import random
class board:
	
	def __init__(self, width, height):
		self.board=[[0 for i in range(height)]for j in range(width)]
		#self.board =  self.board=[[1 for i in range(height == 0 or height-1)] for j in range(width == 0 or width - 1)]
		for i in range(height):
			self.board[random.randrange(height)][random.randrange(height)] =-100
		self.board[0][0] = 0
		self.mouseposition = [0][0]
		self.board[5][5] = 100
	def __str__(self):
		h=len(self.board)
		w=len(self.board[0])
		bar="+"+"---+"*w+"\n"
		output=bar
		
		for j in range(h):
			
			for i in range(w):
				v=self.board[i][j]
				m = self.mouseposition
				output+="|"
				if v==0:
					output+=" . "
				elif v==-100:
					output+=" O "
				elif v==100:
					output+=" C "
				elif():
					output+=" M "
			output+="|\n"+bar
		
		return output

a = board(6,6)
out = a.__str__()
print(out)


