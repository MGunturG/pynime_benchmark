from PIL import Image, ImageDraw, ImageFont

image_canvas = Image.new("RGBA", (820, 60))

def generate_image(asset_image, color, status, *, font="./assets/font.ttf"):
	canvas_copy = image_canvas.copy()
	draw_font = ImageFont.truetype(font, size=32)
	content = Image.open(asset_image).resize((50, 50))

	canvas_copy.paste(content, (15, 0))

	draw = ImageDraw.Draw(canvas_copy)
	draw.text((80, 5), status, color, draw_font, align='center')

	return canvas_copy