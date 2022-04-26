class LogicalOperator:
    def __init__(self, apply, notation):
        self._apply = apply
        self._notation = notation

    def __str__(self):
        return self._notation

    def apply(self, left, right = None):
        return self._apply(left, right)