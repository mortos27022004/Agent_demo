
try:
    import agentlightning as agl
    print("AgentLightning imported")
    
    p = agl.PromptTemplate(template="test prompt", engine="f-string")
    print(f"str(p): {str(p)}")
    print(f"hasattr(p, 'template'): {hasattr(p, 'template')}")
    if hasattr(p, 'template'):
        print(f"p.template: {p.template}")
        
except ImportError:
    print("AgentLightning not found")
except Exception as e:
    print(f"Error: {e}")
