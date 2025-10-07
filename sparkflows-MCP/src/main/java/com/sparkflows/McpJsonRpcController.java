package com.sparkflows;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.UUID;

@RestController
@RequestMapping("/mcp")
public class McpJsonRpcController {

    private final ObjectMapper objectMapper = new ObjectMapper();

    @Autowired
    private MySqlMcpService mySqlMcpService;

    @PostMapping(value = "/rpc", consumes = "application/json", produces = "application/json")
    public ResponseEntity<Map<String, Object>> handleJsonRpc(@RequestBody JsonNode request) {
        try {
            String method = request.get("method").asText();
            String id = request.has("id") ? request.get("id").asText() : "1";

            System.out.println("Received JSON-RPC request for method: " + method);

            Map<String, Object> response = new HashMap<>();
            response.put("jsonrpc", "2.0");
            response.put("id", id);

            switch (method) {
                case "tools/list":
                    Map<String, Object> toolsList = getToolsList();
                    System.out.println("Returning " + ((List<?>) toolsList.get("tools")).size() + " tools");
                    response.put("result", toolsList);
                    break;
                case "tools/call":
                    response.put("result", handleToolCall(request.get("params")));
                    break;
                case "initialize":
                    response.put("result", getInitializeResponse());
                    break;
                default:
                    Map<String, Object> error = new HashMap<>();
                    error.put("code", -32601);
                    error.put("message", "Method not found");
                    response.put("error", error);
                    break;
            }

            return ResponseEntity.ok(response);
        } catch (Exception e) {
            e.printStackTrace();
            Map<String, Object> errorResponse = new HashMap<>();
            errorResponse.put("jsonrpc", "2.0");
            errorResponse.put("id", "1");
            Map<String, Object> error = new HashMap<>();
            error.put("code", -32603);
            error.put("message", "Internal error: " + e.getMessage());
            errorResponse.put("error", error);
            return ResponseEntity.ok(errorResponse);
        }
    }

    private Map<String, Object> getToolsList() {
        Map<String, Object> result = new HashMap<>();
        List<Map<String, Object>> tools = new ArrayList<>();

        // Workflow Tools
        tools.add(createTool("createWorkflow", "Create workflow - returns the workflow JSON", Map.of(), List.of()));

        tools.add(createTool("LegoblockXMLParser", "Lego Block: Execute Generic XML Parser (a wrapper around Spark XML)", Map.of(), List.of()));

        tools.add(createTool("LegoblockXMLMapping", "Lego Block: Execute Mapping Language Pipeline (a wrapper around Mapping Language Engine)", Map.of(), List.of()));

        tools.add(createTool("createPipelineNode", "Create pipeline node - returns the pipeline node JSON", Map.of(), List.of()));

        tools.add(createTool("createWorkflowNode", "Create workflow node - returns the workflow node JSON", Map.of(), List.of()));

        // Extraction Lego Block Tool
        tools.add(createTool("CreateExtractionLegoBlock", "Create an Extraction Lego Block with specified configuration",
            Map.of("first_string", Map.of("type", "string", "description", "Source input string"),
                   "second_string", Map.of("type", "string", "description", "Target output string")),
            List.of("first_string", "second_string")));

        // Logo Block XML Parser Tool
        tools.add(createTool("logoblockXMl", "Parse XML for Logo Block with cluster and deployment configuration",
            Map.of("ClusterId", Map.of("type", "string", "description", "Cluster identifier for the logo block"),
                   "StepName", Map.of("type", "string", "description", "Name of the execution step"),
                   "deploy-mode", Map.of("type", "string", "description", "Deployment mode (e.g., cluster, client)")),
            List.of("ClusterId", "StepName", "deploy-mode")));

        // Read CSV Tool
        tools.add(createTool("ReadCSV", "Read CSV file from the specified path",
            Map.of("path", Map.of("type", "string", "description", "Path to the CSV file to read")),
            List.of("path")));

        result.put("tools", tools);
        return result;
    }

    private Map<String, Object> handleToolCall(JsonNode params) {
        try {
            String toolName = params.get("name").asText();
            JsonNode arguments = params.get("arguments");

            System.out.println("Calling tool: " + toolName + " with arguments: " + arguments);

            String result;
            switch (toolName) {
                // Workflow Tools
                case "createWorkflow":
                    result = mySqlMcpService.createWorkflow();
                    break;
                case "LegoblockXMLParser":
                    result = mySqlMcpService.createLegoblockXMLParser();
                    break;
                case "LegoblockXMLMapping":
                    result = mySqlMcpService.createLegoblockXMLMapping();
                    break;
                case "createPipelineNode":
                    result = mySqlMcpService.createPipelineNode();
                    break;
                case "createWorkflowNode":
                    result = mySqlMcpService.createWorkflowNode();
                    break;

                // Extraction Lego Block Tool
                case "CreateExtractionLegoBlock":
                    String firstString = arguments.get("first_string").asText();
                    String secondString = arguments.get("second_string").asText();
                    result = createExtractionLegoBlock(firstString, secondString);
                    break;

                // Logo Block XML Parser Tool
                case "logoblockXMl":
                    String clusterId = arguments.get("ClusterId").asText();
                    String stepName = arguments.get("StepName").asText();
                    String deployMode = arguments.get("deploy-mode").asText();
                    result = createLogoblockXMl(clusterId, stepName, deployMode);
                    break;

                // Read CSV Tool
                case "ReadCSV":
                    String path = arguments.get("path").asText();
                    result = createReadCSV(path);
                    break;

                default:
                    throw new IllegalArgumentException("Unknown tool: " + toolName);
            }

            Map<String, Object> response = new HashMap<>();
            response.put("content", List.of(Map.of("type", "text", "text", result)));
            response.put("isError", false);
            return response;

        } catch (Exception e) {
            Map<String, Object> errorResponse = new HashMap<>();
            errorResponse.put("content", List.of(Map.of("type", "text", "text", "Error: " + e.getMessage())));
            errorResponse.put("isError", true);
            return errorResponse;
        }
    }

    private Map<String, Object> createTool(String name, String description, Map<String, Object> properties, List<String> required) {
        Map<String, Object> tool = new HashMap<>();
        tool.put("name", name);
        tool.put("description", description);

        // Input schema
        Map<String, Object> inputSchema = new HashMap<>();
        inputSchema.put("type", "object");
        inputSchema.put("properties", properties);
        inputSchema.put("required", required);
        tool.put("input_schema", inputSchema);

        // Output schema
        Map<String, Object> outputSchema = new HashMap<>();
        outputSchema.put("type", "object");
        Map<String, Object> outputProperties = new HashMap<>();
        outputProperties.put("content", Map.of(
            "type", "array",
            "items", Map.of(
                "type", "object",
                "properties", Map.of(
                    "type", Map.of("type", "string"),
                    "text", Map.of("type", "string")
                )
            )
        ));
        outputProperties.put("isError", Map.of("type", "boolean"));
        outputSchema.put("properties", outputProperties);
        outputSchema.put("required", List.of("content", "isError"));
        tool.put("output_schema", outputSchema);

        // Next steps (empty for now, can be customized per tool)
        tool.put("next_steps", Map.of());

        return tool;
    }

    private Map<String, Object> getInitializeResponse() {
        Map<String, Object> result = new HashMap<>();
        result.put("protocolVersion", "2024-11-05");

        Map<String, Object> capabilities = new HashMap<>();
        Map<String, Object> tools = new HashMap<>();
        tools.put("listChanged", true);
        capabilities.put("tools", tools);
        result.put("capabilities", capabilities);

        Map<String, Object> serverInfo = new HashMap<>();
        serverInfo.put("name", "MCP Shopping List Server");
        serverInfo.put("version", "1.0.0");
        result.put("serverInfo", serverInfo);

        return result;
    }

    private String createExtractionLegoBlock(String firstString, String secondString) {
        try {
            if (firstString == null || firstString.trim().isEmpty() ||
                secondString == null || secondString.trim().isEmpty()) {
                throw new IllegalArgumentException("Both first_string and second_string are required");
            }

            // Generate unique block ID
            String blockId = UUID.randomUUID().toString().substring(0, 8);
            String timestamp = LocalDateTime.now().format(DateTimeFormatter.ISO_LOCAL_DATE_TIME);

            // Create configuration based on inputs
            Map<String, Object> inputProcessing = Map.of(
                "source", firstString,
                "validation", true,
                "encoding", "utf-8"
            );

            Map<String, Object> outputProcessing = Map.of(
                "target", secondString,
                "format", "structured",
                "compression", "none"
            );

            List<Map<String, Object>> extractionRules = List.of(
                Map.of("type", "data_validation", "enabled", true),
                Map.of("type", "schema_inference", "enabled", true),
                Map.of("type", "null_handling", "enabled", true)
            );

            Map<String, Object> settings = Map.of(
                "inputProcessing", inputProcessing,
                "outputProcessing", outputProcessing,
                "extractionRules", extractionRules
            );

            Map<String, Object> configuration = Map.of(
                "blockId", blockId,
                "extractionType", "data_extraction",
                "sourceInput", firstString,
                "targetOutput", secondString,
                "timestamp", timestamp,
                "settings", settings
            );

            // Create location parameters
            Map<String, Object> location = Map.of(
                "x", 100,
                "y", 150,
                "width", 200,
                "height", 100,
                "zIndex", 1,
                "gridAlign", true
            );

            // Create parameters for next_steps
            List<Map<String, Object>> parameters = List.of(
                Map.of(
                    "configuration", objectMapper.writeValueAsString(configuration),
                    "type", "string",
                    "description", "Configuration Parameter"
                ),
                Map.of(
                    "location", objectMapper.writeValueAsString(location),
                    "type", "string",
                    "description", "Location Parameter"
                )
            );

            // Create next_steps as an array containing the step object
            List<Map<String, Object>> nextSteps = List.of(
                Map.of(
                    "action", "create_node",
                    "node_name", "ExtractionLegoBlock",
                    "parameters", parameters,
                    "required", List.of("message", "next_steps")
                )
            );

            // Create the response in the exact format from the document
            Map<String, Object> response = Map.of(
                "tool_name", "CreateExtractionLegoBlock",
                "status", "success",
                "result", Map.of("message", "Create an Extraction Lego Block"),
                "next_steps", nextSteps
            );

            System.out.println("Successfully created extraction lego block: " + blockId);
            return objectMapper.writeValueAsString(response);

        } catch (Exception e) {
            System.err.println("Error creating extraction lego block: " + e.getMessage());

            Map<String, Object> errorResponse = Map.of(
                "tool_name", "CreateExtractionLegoBlock",
                "status", "error",
                "result", Map.of("message", "Failed to create extraction lego block: " + e.getMessage()),
                "next_steps", Map.of()
            );

            try {
                return objectMapper.writeValueAsString(errorResponse);
            } catch (Exception jsonException) {
                return "{\"error\": \"Failed to serialize error response\"}";
            }
        }
    }

    private String createLogoblockXMl(String clusterId, String stepName, String deployMode) {
        try {
            if (clusterId == null || clusterId.trim().isEmpty() ||
                stepName == null || stepName.trim().isEmpty() ||
                deployMode == null || deployMode.trim().isEmpty()) {
                throw new IllegalArgumentException("ClusterId, StepName, and deploy-mode are all required");
            }

            // Generate unique block ID
            String blockId = UUID.randomUUID().toString().substring(0, 8);
            String timestamp = LocalDateTime.now().format(DateTimeFormatter.ISO_LOCAL_DATE_TIME);

            // Create cluster configuration
            Map<String, Object> clusterConfig = Map.of(
                "clusterId", clusterId,
                "region", "us-east-1",
                "instanceType", "m5.xlarge",
                "autoScaling", true
            );

            // Create step configuration
            Map<String, Object> stepConfig = Map.of(
                "stepName", stepName,
                "actionOnFailure", "CONTINUE",
                "hadoopJarStep", Map.of(
                    "jar", "command-runner.jar",
                    "args", List.of("spark-submit", "--deploy-mode", deployMode)
                )
            );

            // Create deployment configuration
            Map<String, Object> deploymentConfig = Map.of(
                "deployMode", deployMode,
                "driverMemory", "2g",
                "executorMemory", "4g",
                "executorCores", 2,
                "numExecutors", 3
            );

            List<Map<String, Object>> processingRules = List.of(
                Map.of("type", "xml_validation", "enabled", true),
                Map.of("type", "schema_validation", "enabled", true),
                Map.of("type", "transformation", "enabled", true)
            );

            Map<String, Object> settings = Map.of(
                "clusterConfig", clusterConfig,
                "stepConfig", stepConfig,
                "deploymentConfig", deploymentConfig,
                "processingRules", processingRules
            );

            Map<String, Object> xmlParserConfig = Map.of(
                "blockId", blockId,
                "parserType", "xml_logoblock_parser",
                "clusterId", clusterId,
                "stepName", stepName,
                "deployMode", deployMode,
                "timestamp", timestamp,
                "settings", settings
            );

            // Create position parameters (similar to location but with different naming)
            Map<String, Object> position = Map.of(
                "x", 150,
                "y", 200,
                "width", 250,
                "height", 120,
                "zIndex", 1,
                "gridAlign", true
            );

            // Create parameters for next_steps
            List<Map<String, Object>> parameters = List.of(
                Map.of(
                    "ClusterId", clusterId,
                    "type", "string",
                    "description", "Cluster identifier for the logo block"
                ),
                Map.of(
                    "StepName", stepName,
                    "type", "string",
                    "description", "Name of the execution step"
                ),
                Map.of(
                    "deployMode", deployMode,
                    "type", "string",
                    "description", "Deployment mode (e.g., cluster, client)"
                ),
                Map.of(
                    "xmlParserConfig", objectMapper.writeValueAsString(xmlParserConfig),
                    "type", "string",
                    "description", "XML Parser Configuration Parameter"
                ),
                Map.of(
                    "position", objectMapper.writeValueAsString(position),
                    "type", "string",
                    "description", "Position Parameter"
                )
            );

            // Create next_steps as an array containing the step object
            List<Map<String, Object>> nextSteps = List.of(
                Map.of(
                    "action", "create_node",
                    "node_name", "XMLMapping",
                    "parameters", parameters,
                    "required", List.of("message", "next_steps")
                )
            );

            // Create the response
            Map<String, Object> response = Map.of(
                "tool_name", "logoblockXMl",
                "status", "success",
                "result", Map.of("message", "Parse XML for Logo Block with cluster configuration"),
                "next_steps", nextSteps
            );

            System.out.println("Successfully created logoblock XML parser: " + blockId);
            return objectMapper.writeValueAsString(response);

        } catch (Exception e) {
            System.err.println("Error creating logoblock XML parser: " + e.getMessage());

            Map<String, Object> errorResponse = Map.of(
                "tool_name", "logoblockXMl",
                "status", "error",
                "result", Map.of("message", "Failed to create logoblock XML parser: " + e.getMessage()),
                "next_steps", Map.of()
            );

            try {
                return objectMapper.writeValueAsString(errorResponse);
            } catch (Exception jsonException) {
                return "{\"error\": \"Failed to serialize error response\"}";
            }
        }
    }

    private String createReadCSV(String path) {
        try {
            if (path == null || path.trim().isEmpty()) {
                throw new IllegalArgumentException("path is required");
            }

            // Generate unique block ID
            String blockId = UUID.randomUUID().toString().substring(0, 8);
            String timestamp = LocalDateTime.now().format(DateTimeFormatter.ISO_LOCAL_DATE_TIME);

            // Create CSV configuration
            Map<String, Object> csvConfig = Map.of(
                "blockId", blockId,
                "path", path,
                "delimiter", ",",
                "header", true,
                "encoding", "utf-8",
                "timestamp", timestamp
            );

            // Create position parameters
            Map<String, Object> position = Map.of(
                "x", 150,
                "y", 200,
                "width", 250,
                "height", 120,
                "zIndex", 1,
                "gridAlign", true
            );

            // Create parameters for next_steps
            List<Map<String, Object>> parameters = List.of(
                Map.of(
                    "path", path,
                    "type", "string",
                    "description", "Path to the CSV file"
                ),
                Map.of(
                    "csvConfig", objectMapper.writeValueAsString(csvConfig),
                    "type", "string",
                    "description", "CSV Configuration Parameter"
                ),
                Map.of(
                    "position", objectMapper.writeValueAsString(position),
                    "type", "string",
                    "description", "Position Parameter"
                )
            );

            // Create next_steps as an array containing the step object
            List<Map<String, Object>> nextSteps = List.of(
                Map.of(
                    "action", "create_node",
                    "node_name", "Read CSV",
                    "parameters", parameters,
                    "required", List.of("message", "next_steps")
                )
            );

            // Create the response
            Map<String, Object> response = Map.of(
                "tool_name", "ReadCSV",
                "status", "success",
                "result", Map.of("message", "Read CSV file from path"),
                "next_steps", nextSteps
            );

            System.out.println("Successfully created ReadCSV: " + blockId);
            return objectMapper.writeValueAsString(response);

        } catch (Exception e) {
            System.err.println("Error creating ReadCSV: " + e.getMessage());

            Map<String, Object> errorResponse = Map.of(
                "tool_name", "ReadCSV",
                "status", "error",
                "result", Map.of("message", "Failed to create ReadCSV: " + e.getMessage()),
                "next_steps", Map.of()
            );

            try {
                return objectMapper.writeValueAsString(errorResponse);
            } catch (Exception jsonException) {
                return "{\"error\": \"Failed to serialize error response\"}";
            }
        }
    }

}