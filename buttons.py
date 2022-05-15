

class Button:
	def __init__(self, text, image, x, y, font, color):
		self.text_in = text
		self.font = font
		self.color = color
		self.text = self.font.render(self.text_in, True, self.color)
		self.image = image
		self.x = x
		self.y = y
		self.rect = self.image.get_rect(center=(self.x, self.y))
		self.text_rect = self.text.get_rect(center=(self.x, self.y))

	def buttonPosition(self, position):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			return True
		return False