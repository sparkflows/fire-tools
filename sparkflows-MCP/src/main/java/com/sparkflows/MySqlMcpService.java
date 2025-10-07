package com.sparkflows;

import org.springframework.ai.tool.annotation.Tool;
import org.springframework.core.io.ClassPathResource;
import org.springframework.stereotype.Service;
import java.io.IOException;
import java.nio.charset.StandardCharsets;

@Service
public class MySqlMcpService {

    @Tool(name = "createWorkflow",
          description = "Create workflow - returns the  workflow JSON")
    public String createWorkflow() {
        try {
            ClassPathResource resource = new ClassPathResource("workflow/Read-And-Display-Data.json");
            return new String(resource.getInputStream().readAllBytes(), StandardCharsets.UTF_8);
        } catch (IOException e) {
            throw new RuntimeException("Unable to read workflow file: " + e.getMessage());
        }
    }

    @Tool(name = "LegoblockXMLParser",
          description = "Lego Block: Execute Generic XML Parser (a wrapper around Spark XML)")
    public String createLegoblockXMLParser() {
        try {
            ClassPathResource resource = new ClassPathResource("pipeline/xmlparser.json");
            return new String(resource.getInputStream().readAllBytes(), StandardCharsets.UTF_8);
        } catch (IOException e) {
            throw new RuntimeException("Unable to read LegoblockXMLParser file: " + e.getMessage());
        }
    }

    @Tool(name = "LegoblockXMLMapping",
          description = "Lego Block: Execute Mapping Language Pipeline (a wrapper around Mapping Language Engine)")
    public String createLegoblockXMLMapping() {
        try {
            ClassPathResource resource = new ClassPathResource("pipeline/xmlMapping.json");
            return new String(resource.getInputStream().readAllBytes(), StandardCharsets.UTF_8);
        } catch (IOException e) {
            throw new RuntimeException("Unable to read LegoblockXMLMapping file: " + e.getMessage());
        }
    }

    @Tool(name = "createPipelineNode",
          description = "Create pipeline node - returns the pipeline node JSON")
    public String createPipelineNode() {
        try {
            ClassPathResource resource = new ClassPathResource("pipeline_node/branchPythonOperator.json");
            return new String(resource.getInputStream().readAllBytes(), StandardCharsets.UTF_8);
        } catch (IOException e) {
            throw new RuntimeException("Unable to read pipeline node file: " + e.getMessage());
        }
    }

    @Tool(name = "createWorkflowNode",
          description = "Create workflow node - returns the workflow node JSON")
    public String createWorkflowNode() {
        try {
            ClassPathResource resource = new ClassPathResource("workflow_node/csv.json");
            return new String(resource.getInputStream().readAllBytes(), StandardCharsets.UTF_8);
        } catch (IOException e) {
            throw new RuntimeException("Unable to read workflow node file: " + e.getMessage());
        }
    }

}