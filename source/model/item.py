class ItemSteam:

    def __init__(self, game_id, title, price, discount, review_score, number_reviews, released, platforms):
        self.game_id = game_id
        self.title = title
        self.price = price
        self.discount = discount
        self.review_score = review_score
        self.number_reviews = number_reviews
        self.released = released
        self.platforms = platforms

    def json(self):
        atr = self.__dict__.copy()
        return atr




