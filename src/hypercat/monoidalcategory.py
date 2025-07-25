class MonoidalCategory(Category):
    """Represents a monoidal category."""
    
    def __init__(self, name: str):
        super().__init__(name)
        self.tensor_product: Optional[Callable[[Object, Object], Object]] = None
        self.unit_object: Optional[Object] = None
        self.associator: Dict = {}
        self.left_unitor: Dict = {}
        self.right_unitor: Dict = {}
    
    def set_tensor_product(self, tensor_func: Callable[[Object, Object], Object]) -> 'MonoidalCategory':
        """Set the tensor product operation."""
        self.tensor_product = tensor_func
        return self
    
    def set_unit_object(self, unit: Object) -> 'MonoidalCategory':
        """Set the unit object for the tensor product."""
        self.unit_object = unit
        return self
    
    def tensor_objects(self, obj1: Object, obj2: Object) -> Optional[Object]:
        """Compute tensor product of objects."""
        if self.tensor_product:
            return self.tensor_product(obj1, obj2)
        return None
