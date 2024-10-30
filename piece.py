from main import EPiece

class Piece:
    def getMoves(self, type: EPiece, x: int, y: int):
        if self.type == EPiece.DAME_P1 or self.type == EPiece.DAME_P2:
            return DamePiece.getMoves(self, type, x, y)
        if self.type == EPiece.DEFAULT_P1 or self.type == EPiece.DEFAULT_P2:
            return DefaultPiece.getMoves(self, type, x, y)
        return []

class DefaultPiece(Piece):
    def getMoves(self, type, x, y):
        # TODO: implement
        return []

class DamePiece(Piece):
    def getMoves(self, type, x, y):
        # TODO: implement
        return []