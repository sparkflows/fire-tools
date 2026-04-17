package fire.output;

import java.io.Serializable;
import java.text.SimpleDateFormat;
import java.util.Date;

/**
 * Created by jayantshekhar
 */
public abstract class Output implements Serializable {

    private static final long serialVersionUID = 1L;

    public static final int RESULTTYPE_MODEL = 2;
    public static final int RESULTTYPE_DATA = 3;
    public static final int RESULTTYPE_NOTDEFINED = 99;

    public static final int ID_RANDOMNODE = 99999;


    public int id;  // it is generally the id of the node
    // 99999, 8, 6, 5, 99999 -> applicationId, 99999 -> uiWebUrl, 1 -> Executing node... , 2 -> ...table...

    public String name = ""; // applicationId, uiWebUrl, ReadCSV, VectorAssembler, "", ML Model Save

    public String type = ""; // header, executeWorkflow, text, table, model, modelevaluation, modelsave,
    // failure, success, forest, graph, metrics, geograph

    /*public Date time = new Date();
    DateFormat df = new SimpleDateFormat("yyyy/MM/dd HH:mm:SS");
    String time = df.format(new Date());*/

    String time = new SimpleDateFormat("yyyy MM dd HH:mm:SS").format(new Date());
    //public Date time = new Date();

    public int resultType = RESULTTYPE_NOTDEFINED; // type of result
    // it is used when displaying the RESULT page.
    // Both, model and data types are displayed in it
    // RESULTTYPE_NOTDEFINED is not displayed in the RESULT page

    public Visibility visibility = Visibility.EXPANDED;
    public String tabId = "";

    public Output() {

    }

    public Output(int id, String name, String type) {
        this.id = id;
        this.name = name;
        this.type = type;
    }
}
