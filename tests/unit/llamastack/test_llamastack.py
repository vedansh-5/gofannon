import pytest
from gofannon.base import BaseTool
from gofannon.base.llamastack import LlamaStackMixin

# Test fixture - a sample tool to test with
@pytest.fixture
def sample_gofannon_tool():
    class SampleTool(BaseTool):
        def __init__(self, **kwargs):
            self.name = "sample_tool"  # Set the name attribute explicitly
            super().__init__(**kwargs)
            
        @property
        def definition(self):
            return {
                "function": {
                    "name": "sample_tool",
                    "description": "Sample tool description",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "a": {"type": "number", "description": "First number"},
                            "b": {"type": "number", "description": "Second number"}
                        },
                        "required": ["a", "b"]
                    }
                }
            }
        
        def fn(self, a: float, b: float) -> float:
            """Sample tool description
            
            :param a: First number
            :param b: Second number
            :return: The sum of a and b
            """
            return a + b
    
    return SampleTool()

# Test fixture - a concrete implementation of BaseTool for testing importing
@pytest.fixture
def concrete_tool():
    class ConcreteTool(BaseTool):
        def __init__(self, **kwargs):
            self.name = "concrete_tool"
            self._definition = {
                "function": {
                    "name": "concrete_tool",
                    "description": "Empty tool for testing",
                    "parameters": {
                        "type": "object",
                        "properties": {},
                        "required": []
                    }
                }
            }
            super().__init__(**kwargs)
        
        @property
        def name(self):
            return self._name

        @name.setter
        def name(self, val):
            self._name = val

        @property
        def definition(self):
            return self._definition
            
        @definition.setter
        def definition(self, value):
            self._definition = value

        def fn(self, **kwargs):
            pass
    
    return ConcreteTool()

# Test fixture - a sample Llama Stack function
@pytest.fixture
def sample_llamastack_function():
    def add_numbers(a: float, b: float = 0):
        """Add two numbers together.
        
        :param a: First number
        :param b: Second number (optional)
        :return: The sum of a and b
        """
        return a + b
    
    return add_numbers

def test_export_to_llamastack(sample_gofannon_tool):
    # Export the Gofannon tool to a Llama Stack function
    llamastack_func = sample_gofannon_tool.export_to_llamastack()
    
    # Verify it's a callable function
    assert callable(llamastack_func)
    
    # Verify the function name matches the tool name
    assert llamastack_func.__name__ == "sample_tool"
    
    # Verify the docstring is properly formatted with parameters
    assert "Sample tool description" in llamastack_func.__doc__
    assert ":param a: First number" in llamastack_func.__doc__
    assert ":param b: Second number" in llamastack_func.__doc__
    
    # Test the function's behavior
    result = llamastack_func(2, 3)
    assert result == 5
    
    # Test with keyword arguments
    result = llamastack_func(a=4, b=5)
    assert result == 9

def test_import_from_llamastack(concrete_tool, sample_llamastack_function):
    # Import the Llama Stack function into our concrete tool
    concrete_tool.import_from_llamastack(sample_llamastack_function)
    
    # Verify the tool properties
    assert concrete_tool.name == "add_numbers"
    assert "Add two numbers together" in concrete_tool.description
    
    # Check the parameter definitions
    params = concrete_tool.definition["function"]["parameters"]
    assert "a" in params["properties"]
    assert params["properties"]["a"]["type"] == "number"
    assert "b" in params["properties"]
    
    # Check required parameters
    assert "a" in params["required"]
    assert "b" not in params["required"]
    
    # Test the tool's function
    result = concrete_tool.fn(a=2, b=3)
    assert result == 5