class tree:
    branching_list = []

    def __str__(self):
        return ([str(item.value) for item in self.branching_list])