# Prompt Hub

A library server for all your favorite prompt templates, resources, and tools. Ready for use with Claude, Cursor, and any MCP client.

---

## 📦 How to Add to Your MCP Client

Add this to your MCP client configuration:

```json
{
  "mcpServers": {
    "Prompt Hub": {        
      "command": "npx",
      "args": ["-y", "mcp-remote", "https://prompt-hub.ai/mcp"]    
    }
  }
}
```

## 🚀 How to Use

Once added to your MCP client, you'll have access to:

- **Prompts**: Pre-built prompt templates with customizable parameters
- **Resources**: Helpful resources and documentation 
- **Tools**: Utility functions and tools

Simply browse the available prompts, resources, and tools in your MCP client and use them directly in your conversations.

### Example: SEO Optimized Caption Prompt
- **Name**: `seo_optimized_caption`
- **Parameters**: 
  - `platform` (e.g., "Instagram", "Twitter", "LinkedIn")
  - `description` (brief description of your content)
- **Usage**: The prompt will generate SEO-optimized captions tailored for your specified platform

## 🤝 Request New Templates

Want to add a new prompt, resource, or tool to the hub? Contact me with your template request using the structures below:

### Prompt Template Structure
```json
{
    "name": "your_prompt_name",
    "title": "Your Prompt Title",
    "description": "What your prompt does and when to use it",
    "args": [
        {
            "name": "parameter_name",
            "type": "str"
        }
    ],
    "content": "Your prompt content with {parameter_name} placeholders",
    "role": "user"
}
```

### Resource Template Structure
```json
{
    "name": "your_resource_name",
    "title": "Your Resource Title",
    "description": "What this resource provides",
    "args": [
        {
            "name": "parameter_name",
            "type": "str"
        }
    ],
    "uri": "Your resource uri this will be called via GET request passing all the args as query parameter",
    "mime_type": "application/json"
}
```

### Tool Template Structure
```json
{
    "name": "your_tool_name",
    "title": "Your Tool Title",
    "description": "What this tool does",
    "args": [
        {
            "name": "parameter_name",
            "type": "str"
        }
    ],
    "uri": "This uri will be called via POST request passing all the args along with the userInfo in the request's body",
    "mime_type": "application/json"
}
```

**Contact**: Send your template requests and I'll review and add them to the hub for everyone to use!
