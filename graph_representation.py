class GraphRepresentation:
    def __init__(self, filepath):
        self.filepath = filepath
        self.representation = None

    def convert_to_adj_matrix(self):
        raise NotImplementedError()

    def convert_to_inc_matrix(self):
        raise NotImplementedError()

    def convert_to_adj_list(self):
        raise NotImplementedError()

    