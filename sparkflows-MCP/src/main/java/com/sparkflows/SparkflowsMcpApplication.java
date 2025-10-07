package com.sparkflows;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import org.springframework.ai.support.ToolCallbacks;
import org.springframework.ai.tool.ToolCallback;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean; // Needed to expose the tools

@SpringBootApplication
public class SparkflowsMcpApplication {

	public static void main(String[] args) {
		SpringApplication.run(SparkflowsMcpApplication.class, args);
	}

	@Bean
	public List<ToolCallback> tools(MySqlMcpService mySqlMcpService) {
		var tools = new ArrayList<ToolCallback>();
		tools.addAll(Arrays.asList(ToolCallbacks.from(mySqlMcpService)));
		return tools;
	}

}
