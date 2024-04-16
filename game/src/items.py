class Item:
    def __init__(self, name, description, image, **kwargs):
        self.name = name
        self.description = description
        self.attributes = kwargs
        self.image = image
    
    def __str__(self):
        return f"{self.name}: {self.description}"
