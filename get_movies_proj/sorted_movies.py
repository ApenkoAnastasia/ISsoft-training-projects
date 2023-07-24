class Movies:
    """Class Movies. 

       This class contains __init__ and show_all methods. 
       Each object have genre, title, year and rating fields.

       """
    def __init__(self,genre,title,year,rating):
        self.genre = genre
        self.title = title
        self.year = year
        self.rating = rating

    def show_all(self):
        print(self.genre,',',self.title,',',self.year,',',self.rating) 