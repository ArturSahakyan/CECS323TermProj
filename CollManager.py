class CollManager:

    s_collections = {}

    @staticmethod
    def AddCollection(coll_name, collection):
       CollManager.s_collections[coll_name] = collection

    @staticmethod
    def GetCollection(coll_name):
        return CollManager.s_collections[coll_name]

    @staticmethod
    @property
    def collections():
        print("HEY, BAD, STOP, no touchy touchy")
        return None
