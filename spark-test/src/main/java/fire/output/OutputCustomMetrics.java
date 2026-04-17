package fire.output;

import com.google.gson.Gson;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.Serializable;
import java.util.LinkedHashMap;
import java.util.Map;

public class OutputCustomMetrics extends Output implements Serializable {

    private static final Logger logger = LoggerFactory.getLogger(OutputCustomMetrics.class);
    private static final long serialVersionUID = 1L;

    // Dynamic user-defined fields
    public Map<String, Object> customFields = new LinkedHashMap<>();

    public OutputCustomMetrics() {
        type = "custom-metrics";
    }

    public String toJSON() {

        Gson gson = new Gson();
        String json = gson.toJson(this);
        return json;
    }

    public static OutputCustomMetrics fromGSON(String json) {
        Gson gson= new Gson();

        OutputCustomMetrics outputMetrics = gson.fromJson(json, OutputCustomMetrics.class);

        return outputMetrics;
    }

    public static void main(String[] args) {
        OutputCustomMetrics outputMetrics = new OutputCustomMetrics();

        outputMetrics.customFields.put("region", "us-east-1");// String
        outputMetrics.customFields.put("retryCount", 3);// Integer
        outputMetrics.customFields.put("isSpilled", true);// Boolean
        outputMetrics.customFields.put("latencyP99", 245.7);//Double
        outputMetrics.customFields.put("throughput", 9800L);// Long, type-validated
        logger.info(outputMetrics.toJSON());

        String string = outputMetrics.toJSON();
        logger.info(string);
    }
}
