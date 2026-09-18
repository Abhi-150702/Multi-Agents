"""
Test script to verify the routing system works correctly with CamelCase format.
This tests the graph compilation and routing logic.
"""

from orchestrator.graph import get_workflow
from schemas.state import AgentState

def test_graph_compilation():
    """Test that the graph compiles without errors."""
    print("=" * 60)
    print("TEST 1: Graph Compilation")
    print("=" * 60)
    
    try:
        app = get_workflow()
        print("✅ Graph compiled successfully!")
        return True
    except Exception as e:
        print(f"❌ Graph compilation failed: {e}")
        return False

def test_mermaid_diagram():
    """Test that Mermaid diagram can be generated."""
    print("\n" + "=" * 60)
    print("TEST 2: Mermaid Diagram Generation")
    print("=" * 60)
    
    try:
        app = get_workflow()
        diagram = app.get_graph().draw_mermaid()
        print("✅ Mermaid diagram generated successfully!")
        print("\nDiagram:")
        print(diagram)
        return True
    except Exception as e:
        print(f"❌ Mermaid diagram generation failed: {e}")
        return False

def test_routing_values():
    """Test that routing values are in correct CamelCase format."""
    print("\n" + "=" * 60)
    print("TEST 3: Routing Values Format")
    print("=" * 60)
    
    from schemas.routing import RoutingDecision
    from orchestrator.routes import get_supervisor_routes
    
    # Check schema literal values
    valid_routes = ["Research", "Coding", "ResearchAndCoding"]
    print(f"Expected route values: {valid_routes}")
    
    # Check route mapping
    route_map = get_supervisor_routes()
    print(f"Route mapping: {route_map}")
    
    # Verify all expected routes are in the mapping
    for route in valid_routes:
        if route in route_map:
            print(f"✅ Route '{route}' → '{route_map[route]}' (OK)")
        else:
            print(f"❌ Route '{route}' not found in mapping")
            return False
    
    return True

def test_node_names():
    """Test that node names match expected CamelCase format."""
    print("\n" + "=" * 60)
    print("TEST 4: Node Names")
    print("=" * 60)
    
    try:
        app = get_workflow()
        graph = app.get_graph()
        nodes = list(graph.nodes.keys())
        
        expected_nodes = ["__start__", "Supervisor", "Researcher", "Coder"]
        print(f"Expected nodes: {expected_nodes}")
        print(f"Actual nodes: {nodes}")
        
        for node in expected_nodes:
            if node in nodes:
                print(f"✅ Node '{node}' exists (OK)")
            else:
                print(f"❌ Node '{node}' not found")
                return False
        
        return True
    except Exception as e:
        print(f"❌ Node name test failed: {e}")
        return False

def run_all_tests():
    """Run all tests and report results."""
    print("\n" + "🧪 " * 30)
    print("ROUTING SYSTEM TEST SUITE - CamelCase Verification")
    print("🧪 " * 30 + "\n")
    
    tests = [
        ("Graph Compilation", test_graph_compilation),
        ("Mermaid Diagram", test_mermaid_diagram),
        ("Routing Values", test_routing_values),
        ("Node Names", test_node_names)
    ]
    
    results = []
    for test_name, test_func in tests:
        result = test_func()
        results.append((test_name, result))
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{status} - {test_name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! The routing system is working correctly.")
        return True
    else:
        print(f"\n⚠️ {total - passed} test(s) failed. Please review the errors above.")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)
