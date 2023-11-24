def make_new_edge(new_edge_id):
    def new_edge(data):
        return (new_edge_id(data[0].id), data[0].id, data[1].id)
    return new_edge